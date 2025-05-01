# WIFI SCANNER  // THIS WILL BE WHERE THE SCAN LOGIC IS PERFORMED


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff


# ETC IMPORTS 
import threading, os, random, time, pyfiglet, random



# NSM IMPORTS
from nsm_utilities import Utilities
from nsm_files import Network_Mapper




class WifiScanner():
    """This class will be responsible for finding wifi networks within your area"""


    def __init__(self):

        # USE THE SAME CONSOLE OBJECT FOR EVERYTHING TO NOT FUCK UP THE LIVE FEATURE LOL
        self.networks = []

        # CREATE A INSTANCE FOR MAPPING
        self.map = Network_Mapper()
        
    

    def scanner(self, table):
        """Scanner"""
        

        # CREATE OBJECTS / GET CURRENT USER WIRELESS LAN INTERFACE
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        
        # TELL THE USER THE INTERFACE CURRENTLY BEING USED
        if len(self.networks) == 0:
            console.print(f"[bold green]Current WLAN:[/bold green] {iface.name()}")
        
        
        # NOW TO SCAN AND INTERATE THROUGH THE LIST
        console.print("Scanning for wireless networks...", style="yellow")
        iface.scan()
        results = iface.scan_results()

        for net in results:

            if not results:
                console.print(f"[bold red]No Wireless networks found[/bold red]") 
            
            else:
                
                use = False

                # GET FREQ AND AKM TYPE
                frequency = self.get_frequency(frequency=net.freq)
                encryption = self.get_encryption(akm=net.akm[0])

                # CATCH EMPTY SSID
                if net.ssid.strip().lower() == "" or net.ssid.strip().lower() == "5ghz" or net.ssid.strip().lower() == "2ghz":
                    net.ssid = "N/A"
               

                # THESE PRINT STATEMENTS WILL NO LONGER BE USED BUT WILL BE KEPT FOR DEBUGGING REASONS FOR THE TIME BEING 
                if use:
                    console.print(f"[bold blue]SSID: [/bold blue]{net.ssid}  |  [yellow]Signal: [/yellow]{net.signal}  |  BSSID: {net.bssid}  |  Encryption: {encryption}")
                
                # USE TABLES INSTEAD
                else:
                    
                    # MAKE SURE WE HAVENT ALREADY LOGGED THE NETWORK
                    if net.bssid not in self.networks:

                        # APPEND NETWORK TO LIST
                        self.networks.append(net.bssid)
                        
                        # ADD DATA TO TABLE
                        table.add_row(f"{len(self.networks)}",f"{net.signal}", f"{net.ssid}", f"{frequency}", f"{net.auth}", f"{encryption}", f"{net.bssid}")
                        
                        # ADD NETWORK TO FILE
                        self.map.network_logging(ssid=net.ssid, bssid=net.bssid, signal=net.signal, auth=net.auth, frequency=frequency, encryption=encryption)


    
    def get_encryption(self, akm):
        """This method will be used to get the get_encryption type that the network is using"""


        # CREATE A LIST FULL OF THE AUTHENTICATION TYPES
        encryptions = {
            0: "Open",
            1: "WPA",
            2: "WPA-PSK",
            3: "WPA2",
            4: "WPA2-PSK",
            5: "Unkown",
            6: "WPA3",
            7: "WPA3-SAE"

        }
        
        encryption = encryptions.get(akm)
        
        return encryption
    
    def get_frequency(self, frequency):
        """Get the frequency being used by the wifi"""


        # 2.4GHZ OR 5GHZ
        if  frequency in range(2400000, 2500000):
            return "2.4 GHz"
        
        elif frequency in range(5000000, 5800000):
            return "5 GHz"
        
        elif frequency in range(5900000, 7200000):
            return "6 GHz"


        else:
            return frequency
        
    
    def loop_controller(self):
        """This will be responsible for looping through wifi scanning and appending data to the table"""
        

        # TABLE FOR WIFI NETWORKS
        table = Table(title="Wireless Network's", title_style='bold red',header_style='red', style='bold purple')
        table.add_column("#")
        table.add_column("Signal", style='yellow')
        table.add_column("SSID", style='bold green')
        table.add_column("Frequency")
        table.add_column("Authentication")
        table.add_column("Encryption")  # AKA AKM // AUTHENCTION AND KEY MANAGEMENT
        table.add_column("BSSID", style='cyan')
        

        # PANEL FOR DATA
        panel = Panel(renderable=f"Networks Found: {len(self.networks)}", style='bold red', border_style='bold yellow', expand=False)

        # USE THIS TO LOOP THROUGH THE WIFI SCANNER METHOD AND APPEND NEW RESULTS TO THE LIST
        interval = 3

        # LOOP THROUGH SCAN 3 TIMES JUST TO MAKE SURE WE DONT MISS ANYTHING
        loop = 3


        # TELL USER SCAN HAS STARTED
        threading.Thread(target=Utilities.tts, args=("Beginning network wide scanning", ), daemon=True).start()


        with Live(table, console=console, refresh_per_second=1):
            while loop > 0:

                self.scanner(table=table)

                # WAIT FOR THIS THEN REPEAT THE PROCESS 
                time.sleep(interval)
                loop -= 1
                

        # CURRENT NETWORKS FOUND
        self.map.network_saver()
        self.map.done()
        Utilities.tts(say=f"I have found a total of: {len(self.networks)} networks sir. ")
        Utilities.tts(say="I WILL NOW BEGIN TO HACK TARGETED NETWORKS" , voice_sound="1")



class WifiUI():
    """This class will house basic UI logic"""

    def __init__(self):
        pass
    
    @staticmethod
    def welcome_message(sleep=.01):
        """This will hold and print the ascii text and a nice sexy looking manner"""

        art = """
        _____                                                     _____ 
        ( ___ )---------------------------------------------------( ___ )
        |   |                                                     |   | 
        |   |  _   _      _    ____                _              |   | 
        |   | | \ | | ___| |_ / ___|_ __ __ _  ___| | _____ _ __  |   | 
        |   | |  \| |/ _ \ __| |   | '__/ _` |/ __| |/ / _ \ '__| |   | 
        |   | | |\  |  __/ |_| |___| | | (_| | (__|   <  __/ |    |   | 
        |   | |_| \_|\___|\__|\____|_|  \__,_|\___|_|\_\___|_|    |   | 
        |___|                                                     |___| 
        (_____)---------------------------------------------------(_____)
        """
        from pathlib import Path
        path = Path.home() / "Documents" / "nsm tools" / "network tools" / "wifi scanner" / "art.txt"
        with open(path, "r") as file:
            console.print(file.read())
            
 
           
        say = "Initiating scan for all nearby networks. If I connect, it's legally a penetration test. If I get caught, it was a prank. FUCK YOU"

        threading.Thread(target=Utilities.tts, args=(say, False, 10)).start()

        for char in art:
            print(char, end='', flush=True)
            time.sleep(sleep)

        Utilities.clear_screen()


        fonts = pyfiglet.FigletFont.getFonts()
        console.print(fonts)
        
        use = False
        if use:
            for f in fonts:
                time.sleep(2)
            
                art_static = pyfiglet.figlet_format(text="Net\nCracker", font=f)
                console.print(f"Using: {f}\n{art_static}", style='bold red')
    

        art_static = pyfiglet.figlet_format(text="          Net", font="bloody")
        console.print(art_static)        
        art_static = pyfiglet.figlet_format(text="    Cracker", font="bloody")
        console.print(art_static, style="bold red")
       # console.print(Panel(title="Malicious Practitionar", renderable=f"{art_static}", expand=False, style="bold red", border_style="red"))
        print('\n\n')



    @staticmethod
    def main():
        """Call upon this method to start module logic"""


       # WifiUI.welcome_message()
        WifiScanner().loop_controller()
       
        console.input("\n\n[bold red]Press enter to exit: ")
        time.sleep(.3)



# CURRENTLY USED FOR PROGRAM TESTING
if __name__ == "__main__":
    WifiUI.main()