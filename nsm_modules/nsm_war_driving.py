# WIFI SCANNER  // WAR DRIVING MODULE

import threading
import time

from rich.panel import Panel
from rich.live import Live
from rich.console import Console

from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeReq
from scapy.all import sniff

from nsm_utilities import Utilities, NetTilities, Background_Threads
from nsm_files import Recon_Pusher
from nsm_deauth import Frame_Snatcher, LOCK

console = Console()


class War_Driving:
    """This class will be responsible for allowing the user to war drive"""

    mode = 0

    def __init__(self):
        pass

    @classmethod
    def data_assist(cls, iface):
        """This method will be responsible for updating panel values"""

        # COLORS
        c1 = "bold red"
        _c2 = "bold green"
        _c3 = "bold blue"
        _c4 = "bold purple"

        # VARS
        d = 1

        # DEFINE PANEL
        panel = Panel(
            renderable="AP's Found: 0   -   Clients Found: 0   -   [bold green]Developed by NSM Barii",
            style="bold yellow",
            border_style="bold red",
            expand=False,
        )

        from rich.align import Align

        _panel_allign = Align(panel, align="left", vertical="bottom")

        # CREATE LIVE ENV
        with Live(panel, console=console, refresh_per_second=1, screen=False):
            while cls.LIVE:
                try:
                    if cls.LIVE:
                        # UPDATE RENDERABLE
                        panel.renderable = f"[{c1}]Channel:[/{c1}] {Background_Threads.channel}   -   [{c1}]AP's Found:[/{c1}] {len(cls.beacons)}   -   [{c1}]Clients Found:[/{c1}] {len(cls.macs)}   -   [bold green]Developed by NSM Barii"

                        # SMALL DELAY BECAUSE OF LOOP
                        time.sleep(1)

                        # USE THIS TO REMOVE APS FROM CLIENT LIST
                        for ap in cls.beacons:
                            if ap in cls.macs:
                                cls.macs.remove(ap)

                                # TELL USER
                                console.print(
                                    f"[bold yellow][-][/bold yellow] Removed AP from Client list --> {ap}",
                                    style="bold yellow",
                                )

                        # USE THIS TO UPDATE JSON
                        if d == 5:
                            Recon_Pusher.push_war(save_data=cls.aps, CONSOLE=console)
                            d = 0

                        d += 1

                except KeyboardInterrupt:
                    # console.print("Now escaping the MATRIX", style="bold red")

                    # KILL BACKGROUND THREAD
                    cls.LIVE = False

                    break

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[bold yellow] {e}")

                    # KILL BACKGROUND THREAD
                    cls.LIVE = False

                    break

    @classmethod
    def war_drive(cls, iface="wlan0", verbose=0):
        """This will begin the sniffing function"""

        # SET VARS
        attempts = 0

        # START BACKGROUND THREAD
        threading.Thread(
            target=War_Driving.data_assist, args=(iface,), daemon=True
        ).start()

        # LOOP FOF ERRORS
        while cls.LIVE:
            try:
                # APPEND
                attempts += 1

                console.print(f"Sniff Attempt #{attempts}", style="bold yellow")

                # SNIFF
                sniff(iface=iface, prn=War_Driving.packet_parser, store=0)

                # DELAY
                time.sleep(1)

            except KeyboardInterrupt as e:
                console.print(e)

                # KILL BACKGROUND THREAD
                cls.LIVE = False

                break

            # DESTROY ERRORS
            except Exception as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")

                # KILL BACKGROUND THREAD
                cls.LIVE = False

                # IN CASE OF LOOP ERRORS
                time.sleep(1)

    @classmethod
    def packet_parser(cls, pkt, verbose=True):
        """This method will parse packets"""

        def parser(pkt):

            # FOR AP's
            if pkt.haslayer(Dot11Beacon) and cls.mode == 1:
                # GET SSID
                ssid = (
                    pkt[Dot11Elt].info.decode(errors="ignore")
                    if pkt[Dot11Elt].info.decode(errors="ignore")
                    else "Missing SSID"
                )

                # GET ADDR
                addr1 = (
                    pkt[Dot11].addr1
                    if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff"
                    else False
                )
                addr2 = (
                    pkt[Dot11].addr2
                    if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff"
                    else False
                )

                # NONE AP //  ADDR1 == DST, ADDR2 == SRC
                if addr1 and addr1 not in cls.macs:
                    # APPEND TO LIST
                    cls.macs.append(addr1)

                    # GET SIGNAL
                    signal = NetTilities.get_rssi(pkt=pkt, format=True)

                    # GET VENDOR
                    vendor = Utilities.get_vendor(mac=addr2)

                    # REVISE SSID

                    signal = f"[bold red]Signal:[/bold red] {signal}"

                    # SET USE
                    if ssid:
                        use = f"{signal}  [bold red]Vendor:[bold yellow] {vendor}  [bold red]SSID:[/bold red] {ssid}"

                    elif vendor:
                        use = f"signal{signal}  [bold red]Vendor:[bold yellow] {vendor}"

                    else:
                        use = f"{signal}"

                    # OUTPUT
                    if verbose:
                        console.print(
                            f"[bold cyan][+] Found AP?:[/bold cyan] {addr1}   {use}",
                            style="bold yellow",
                        )

                # AP's ONLY
                if addr2 and addr2 not in cls.beacons:
                    # APPEND TO LIST
                    cls.beacons.append(addr2)

                    # GET IE's
                    # ssidd, channel, rsn, vendorr = NetTilities.get_ies(pkt=pkt, sort=True, ap=True)

                    # GET SIGNAL
                    signall = NetTilities.get_rssi(pkt=pkt, format=True)

                    # GET VENDOR
                    vendor = Utilities.get_vendor(mac=addr2)

                    # REVISE SSID

                    signal = f"[bold red]Signal:[/bold red] {signall}"

                    # SET USE
                    if ssid:
                        use = f"{signal}  [bold red]Vendor:[bold yellow] {vendor}  [bold red]SSID:[/bold red] {ssid}"

                    elif vendor:
                        use = f" {signal}  [bold red]Vendor:[bold yellow] {vendor}"

                    else:
                        use = f"{signal}"

                    # OUTPUT
                    if verbose:
                        console.print(
                            f"[bold cyan][+] Found AP:[/bold cyan] {addr2}   {use}",
                            style="bold yellow",
                        )

                        cls.aps[len(cls.aps)] = {
                            "ssid": ssid,
                            "bssid": addr2,
                            "vendor": vendor,
                            "encryption": "WPA2",
                            "signal": signall,
                            "lat": 21,
                            "long": 34,
                        }

            # FOR CLIENTS AND NON BEACON FRAMES
            elif pkt.haslayer(Dot11) and cls.mode == 2:
                # GET ADDR
                addr1 = (
                    pkt[Dot11].addr1
                    if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff"
                    else False
                )
                addr2 = (
                    pkt[Dot11].addr2
                    if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff"
                    else False
                )

                # NONE AP //  ADDR1 == DST, ADDR2 == SRC
                if addr1 and addr1 not in cls.macs and addr1 not in cls.beacons:
                    # APPEND TO LIST
                    cls.macs.append(addr1)

                    # GET SIGNAL
                    signal = NetTilities.get_rssi(pkt=pkt, format=True)

                    # GET VENDOR
                    vendor = Utilities.get_vendor(mac=addr2)

                    signal = f"[bold red]Signal:[/bold red] {signal}"

                    # SET USE
                    if vendor:
                        use = f"[bold red]Vendor:[bold yellow] {vendor}  {signal}"

                    else:
                        use = f"{signal}"

                    # OUTPUT
                    if verbose:
                        console.print(
                            f"[bold red][+] Found Mac Addr:[bold yellow] {addr1}   {use}",
                            style="bold yellow",
                        )

                # NONE AP //  ADDR1 == DST, ADDR2 == SRC
                if addr2 and addr2 not in cls.macs and addr2 not in cls.beacons:
                    # APPEND TO LIST
                    cls.macs.append(addr2)

                    # GET SIGNAL
                    signal = NetTilities.get_rssi(pkt=pkt, format=True)

                    # GET VENDOR
                    vendor = Utilities.get_vendor(mac=addr2)

                    # REVISE SSID
                    signal = f"[bold red]Signal:[/bold red] {signal}"

                    # SET USE
                    if vendor:
                        use = f"[bold red]Vendor:[bold yellow] {vendor}  {signal}"

                    else:
                        use = f"{signal}"

                    # OUTPUT
                    if verbose:
                        console.print(
                            f"[bold red][+] Found Mac Addr:[bold yellow] {addr2}   {use}",
                            style="bold yellow",
                        )

            # FOR CLIENT TRACKING
            War_Driving.track_clients(pkt)

        # THREAD IT SO THAT WAY MAIN THREAD CAN GET BACK TO WORK
        threading.Thread(target=parser, args=(pkt,), daemon=True).start()

    @classmethod
    def track_clients(cls, pkt):
        """This method will be responsible for tracking clinets that are in the client list"""

        # COLORS
        c1 = "bold red"
        c2 = "bold green"
        c3 = "bold purple"
        c4 = "bold yellow"
        _c5 = "bold cyan"

        # INFO
        # ADDR1 == DST, ADDR2 == SRC

        if pkt.haslayer(Dot11ProbeReq):
            # SET ADDR1
            _addr1 = (
                pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else False
            )
            addr2 = (
                pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else False
            )

            # SNAG SSID
            ssid = (
                pkt[Dot11Elt].info.decode(errors="ignore")
                if pkt[Dot11Elt].info.decode(errors="ignore")
                else False
            )

            # IF NOT SNAGGED ALREADY
            if addr2 and ssid:
                # MAKE
                if addr2 not in cls.probes:
                    cls.probes[addr2] = []
                    console.print(f"make --> {addr2}")

                # GET VENDOR
                vendor = Utilities.get_vendor(mac=addr2)

                # FOR SOURCE DESTINATION
                sd = f"[{c4}]{addr2}   [{c1}]Vendor:[/{c1}] {vendor}[/{c4}]  -->  [{c3}]{ssid}"

                # CHECK IF WE ALREADY SNAGGED THE SSID
                if ssid not in cls.probes[addr2]:
                    # PREVENT RACE ERRORS
                    with LOCK:
                        # OUTPUT RESULTS TO UI
                        console.print(f"[{c2}][+] Probe Detected:[/{c2}] {sd}")

                        # APPEND TO LIST
                        cls.probes[addr2].append(ssid)

            # FOR CLIENTS PROBING OR TALKING TO AP
            use = False
            if use:
                if addr2 and addr2 in cls.macs:
                    # MAKE
                    if addr2 not in cls.probes:
                        cls.probes[addr2] = []
                        console.print(f"make --> {addr2}")

                    # GET VENDOR
                    vendor = Utilities.get_vendor(mac=addr2)

                    # GET SSID IF AVAILABLE
                    try:
                        ssid = (
                            pkt[Dot11Elt].info.decode(errors="ignore")
                            if pkt[Dot11Elt].info.decode(errors="ignore")
                            else False
                        )
                    except Exception:
                        ssid = False

                    sd = f"[{c4}]{addr2}   [{c1}]Vendor:[/{c1}] {vendor}  -->  {ssid}"

                    # FILTER NON PROBES
                    if ssid:
                        # MAKE KEY
                        if addr2 not in cls.probes:
                            cls.probes[addr2] = []
                            console.print(f"make --> {addr2}")

                        # CHECK
                        if ssid not in cls.probes[addr2]:
                            # APPEND VALUE
                            cls.probes[addr2].append(ssid)

                            # OUTPUT RESULTS TO UI
                            console.print(f"[{c2}][+] Probe Detected:[/{c2}] {sd}")

        # TEST
        if len(cls.macs) == 40:
            console.print(cls.probes)

    @classmethod
    def main(cls, mode=1):
        """This will be in charge of running class wide logic"""

        # SET VARS
        cls.probes = {}
        cls.macs = []
        cls.beacons = []
        cls.LIVE = True
        cls.mode = mode

        # WAR DRIVER
        cls.aps = {}

        try:
            # GET IFACE
            iface = Frame_Snatcher.get_interface()

            # WELCOME UI
            Frame_Snatcher.welcome_ui(
                iface=iface, text="    War \nDriving", c2="bold blue"
            )
            Background_Threads.change_iface_mode(iface=iface, mode="monitor")

            # INIT WAR
            Recon_Pusher.main()

            # START CHANNEL HOPPER
            Background_Threads.channel_hopper(verbose=False)

            # START WAR DRIVING
            War_Driving.war_drive(iface=iface)
            # threading.Thread(target=War_Driving.war_drive, args=(iface, ), daemon=True).start()
            # War_Driving.data_assist(iface=iface)

            # NOW FOR THE EXIT
            time.sleep(0.2)
            console.input("\n\n[bold red]Press enter to return: ")

        except KeyboardInterrupt as e:
            console.print(e)

        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")
