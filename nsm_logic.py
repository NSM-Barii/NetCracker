# WIFI SCANNER  // THIS WILL BE A READ TEAM PROGRAM 


# UI IMPORTS
import pywifi.iface
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff


# ETC IMPORTS 
import threading, os, random, time



# NSM IMPORTS
from nsm_utilities import Utilities




class WifiScanner():
    """This class will be responsible for finding wifi networks within your area"""


    def __init__(self):

        # USE THE SAME CONSOLE OBJECT FOR EVERYTHING TO NOT FUCK UP THE LIVE FEATURE LOL
        self.networks = []
        
    

    def scanner(self, table):
        """Scanner"""
        

        # CREATE OBJECTS / GET CURRENT USER WIRELESS LAN INTERFACE
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        
        # TELL THE USER THE INTERFACE CURRENTLY BEING USED
        if len(self.networks) == 0:
            console.print(f"[bold green]Current WLAN:[/bold green] {iface.name}")
        
        
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
        table.add_column("Signal")
        table.add_column("SSID")
        table.add_column("Frequency")
        table.add_column("Authentication")
        table.add_column("Encryption")  # AKA AKM // AUTHENCTION AND KEY MANAGEMENT
        table.add_column("BSSID")
        

        # PANEL FOR DATA
        panel = Panel(renderable=f"Networks Found: {len(self.networks)}", style='bold red', border_style='bold yellow', expand=False)

        # USE THIS TO LOOP THROUGH THE WIFI SCANNER METHOD AND APPEND NEW RESULTS TO THE LIST
        interval = 3

        # LOOP THROUGH SCAN 3 TIMES JUST TO MAKE SURE WE DONT MISS ANYTHING
        loop = 3


        with Live(table, console=console, refresh_per_second=10):
            while loop > 0:

                self.scanner(table=table)

                # WAIT FOR THIS THEN REPEAT THE PROCESS 
                time.sleep(interval)
                loop -= 1
                

        # CURRENT NETWORKS FOUND
        console.print(f"\n[bold green]Total Networks Found: [/bold green]{len(self.networks)}")
        Utilities.tts(say=f"I have found a total of: {len(self.networks)} networks, sir")





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

for char in art:
    print(char, end='', flush=True)
    time.sleep(.04)
os.system('cls')

console.print(Panel(title="Malicious Practitionar", renderable=f"{art}", expand=False, style="bold purple"))
print('\n\n')

    
WifiScanner().loop_controller()


