# WIFI SCANNER  // DEAUTH MODULE // THIS WILL HOLD MALICIOUS LOGIC MEANT FOR ETHICAL REASONS


# UI IMPORTS
import pywifi.iface
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff, Dot11



# ETC IMPORTS 
import threading, os, random, time, pyttsx3

    
# THINGS TO STUDY FOR MATH ASVAB 
MATH = ["percentage", "algebra", "PEMDAS", "Area & Distance", "regular to fraction", "factor equations", "angle of triangle", "area and volume"]


for m in MATH:
    console.print(m)

class Deauth_You():
    """This module will be responsible for crafting and sending deauth packets"""

    def __init__(self):
        pass

    
    @classmethod
    def packet(cls, target_ap, target_mac):
        "This method is responsible for crafting the actual deauth packets"

        
        # YOUR MONITOR MODE INTERFACE
        iface = 'wlan1mon'
        

        # BSSID
        target_ap   # AP'S MAC ADDRESS
        target_mac   # VICTIM / TARGET MAC ADDRESS 


        # CRAFT DEAUTH PACKETS
       # deauth = Radiotap()/\
            #     Dot11()

        







import pyttsx3, socket, pyfiglet
from scapy.all import IP, ICMP, sr1



class You_Cant_DOS_ME():
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
            "Try harder... I'm behind 3 VPNs and your girl’s Wi-Fi.",
            "You scan ports, I open wormholes.",
            "Your whole setup runs on hope and Starbucks Wi-Fi.",
            "Deauth me? I deauth back with feelings.",
            "Nice packet — shame it never reached me.",
            "You can’t trace me — I lost myself years ago."
        ]


        try:
            
            # CREATE PACKET AND GET HOST
            ip = socket.gethostbyname(str(host))
            console.print(IP)
            ping = IP(dst=ip) / ICMP()

            
            # ERROR CHECK
            console.print(ping)
            time.sleep(3)
        
        except Exception as e:
            console.print(f"[bold red]Socket Exception Error: {e}")
            
            
        # LOOP THAT BITCH
        while online:

            try:
            
                # TRACK PING TIME
                time_start = time.time()
                response = sr1(ping, timeout=timeout, verbose=verbose)

                time_took = time.time() - time_start

                
                if response:
                    console.print(f"[bold blue]Connection Status: [bold green]Online  -  Ping Latency: {time_took:.2f}")
                

                else:
                    console.print(f"[bold blue]Connection Status: [bold red]Offline  -  I HATE YOU")



                    

                
                pings += 1 
                if time_took < 1.0:
                    time.sleep(1.5)


                ran = random.randint(0,10)

                if ran == 4:

                    console.print(talks[random.randint(0,14)])


                
        

            except Exception as e:

                # SET ONLINE TO FALSE
                console.print(f"[bold red]Exception Error: {e}")




# FOR MODULE TESTING
if __name__ == "__main__":
    You_Cant_DOS_ME.ping()


