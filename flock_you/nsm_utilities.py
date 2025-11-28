# THIS WILL HOUSE SIDE UTILITIES FOR NON RADIO CODE


# UI IMPORTS
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Console
import pyfiglet
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress, requests, manuf
from scapy.all import sniff, RadioTap
from scapy.layers.dot11 import Dot11Elt
from mac_vendor_lookup import MacLookup

# ETC IMPORTS 
import threading, os, random, time, pyttsx3, platform, os, subprocess






class Utilities():
    """Utilities"""


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




class Background_Threads():
    """This module will house background permanent running threads"""
    

    # CLASS VARIABLES
    hop = True
    channel = 0




    @classmethod
    def get_channel(cls, pkt):
        """This will be used to get the ssid channel"""


        elt = pkt[Dot11Elt]
        channel = 0


        while isinstance(elt, Dot11Elt):

            if elt.ID == 3:
                channel = elt.info[0]
                return channel
            
            elt = elt.payload
        
        return False

    

    @classmethod
    def get_freq(cls, freq):
        """This will return frequency"""


        if freq in range(2412, 2472): return "2.4 GHz"
        elif freq in range(5180, 5825): return "5 GHz"
        else: return "6 GHz"


    @staticmethod
    def get_rssi(pkt, format=False):
        """This method will be responsible for pulling signal strength"""

        signal = ""; signal = f"[bold red]Signal:[/bold red] {signal}"  

        
        # CHECK FOR RADIO HEADER
        if pkt.haslayer(RadioTap):
            

            # PULL RSSI
            rssi = getattr(pkt, "dBm_AntSignal", False)
            
            # NOW RETURN
            if rssi:

                if format:
                    return f"{rssi} dBm"
                
                return rssi





    @classmethod
    def get_encryption(cls, pkt):
        """Get this encryption"""







    @classmethod
    def channel_hopper(cls, set_channel=False, verbose=False):
        """This method will be responsible for automatically hopping channels"""


        # NSM IMPORTS
        from nsm_modules.nsm_files import Settings
        

        def hopper():

            delay = 0.25
            all_hops = [1, 6, 11, 36, 40, 44, 48, 149, 153, 157, 161]

            iface = Settings.get_json()['iface']


            # TUNE HOP
            if set_channel:


                cls.hop = False; time.sleep(2)


                try:

                    subprocess.Popen(
                    ["sudo", "iw", "dev", iface, "set", "channel", str(set_channel)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[bold yellow] {e}")
   

            # AUTO HOPPING
            while cls.hop:

                for channel in all_hops:


                    try:
                    

                        # HOP CHANNEL
                        subprocess.Popen(
                            ["sudo", "iw", "dev", iface, "set", "channel", str(channel)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            stdin=subprocess.DEVNULL,
                            start_new_session=True
                        )
                        cls.channel = channel
                        if verbose:
                            console.print(f"[bold green]Hopping on Channel:[bold yellow] {channel}")

                        # DELAY
                        time.sleep(delay)
                    
                    except Exception as e:
                        console.print(f"[bold red]Exception Error:[bold yellow] {e}")



        threading.Thread(target=hopper, args=(), daemon=True).start()
        cls.hop = True
