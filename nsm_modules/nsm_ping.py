# WIFI SCANNER  // PING MODULE // THIS CLASS IS STRICTLY TO BE USED AS A VICTIM NODE
import pyfiglet
from rich.console import Console
from scapy.all import IP, ICMP, sr1
import socket
import random
import time

console = Console()


# THIS CLASS IS STRICTLY TO BE USED AS A VICTIM NODE TO TEST IF THIS MODULE IS FUNCTIONAL
class You_Cant_DOS_ME:
    """This is testing ground for weather or not i can withstand a ddos attack"""

    def __init__(self):
        pass

    @classmethod
    def ping(cls, host="google.com", timeout=4, verbose=False):
        """Create the ping packet and send it out"""

        # PRINT WELCOME
        text = pyfiglet.figlet_format(text="DOS\n ME", font="bloody")
        console.print(text, style="bold red")

        console.input("\n[bold red]ARE U READY ?: ")

        online = True
        pings = 0

        # TALK SHII FOR FUN
        talks = [
            "You can't hit me offline — I host the cloud.",
            "Yawn... I'm still online.",
            "Your net too slow to even scan me.",
            "My packets run laps around yours.",
            "Bro I deauth for fun.",
            "Your IP is giving home router energy.",
            "My Wi-Fi's got better uptime than your excuses.",
            "I don't lag — I throttle reality.",
            "My ping is lower than your standards.",
            "Try harder... I'm behind 3 VPNs and your girl's Wi-Fi.",
            "You scan ports, I open wormholes.",
            "Your whole setup runs on hope and Starbucks Wi-Fi.",
            "Deauth me? I deauth back with feelings.",
            "Nice packet — shame it never reached me.",
            "You can't trace me — I lost myself years ago.",
        ]

        while True:
            try:
                # CREATE PACKET AND GET HOST
                ip = socket.gethostbyname(str(host))
                console.print(ip)
                ping = IP(dst=ip) / ICMP()

                # ERROR CHECK
                console.print(ping)
                time.sleep(3)

                break

            # CTRL + C
            except KeyboardInterrupt as e:
                console.print(e)

                return

            except Exception as e:
                console.print(f"[bold red]Socket Exception Error: {e}")
                time.sleep(3)
                return

        # LOOP THAT BITCH
        while online:
            try:
                # TRACK PING TIME
                time_start = time.time()
                response = sr1(ping, timeout=timeout, verbose=verbose)

                time_took = time.time() - time_start

                if response:
                    console.print(
                        f"[bold blue]Connection Status: [bold green]Online  -  Latency: {time_took:.2f}"
                    )

                else:
                    console.print(
                        "[bold blue]Connection Status: [bold red]Offline  -  I HATE YOU"
                    )

                pings += 1
                if time_took < 1.0:
                    time.sleep(1.5)

                ran = random.randint(0, 10)

                if ran == 4:
                    console.print(talks[random.randint(0, 14)])

            # CTRL + C
            except KeyboardInterrupt as e:
                console.print("\n", e)

                console.input("[bold yellow]Press Enter to leave: ")
                console.print("\nReturning to Main Menu", style="bold green")
                time.sleep(2)

                break

            except Exception as e:
                # SET ONLINE TO FALSE
                console.print(f"[bold red]Exception Error: {e}")
