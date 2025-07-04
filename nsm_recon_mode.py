# WIFI SCANNER  // THIS MODULE WILL BE RESPONSIBLE FOR INDEFINITE RECON


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
from nsm_utilities import Utilities, NetTilities
from nsm_files import Network_Mapper



class ReconScanner():

    # CLASS METHODS
    networks = []
    network_saver = Network_Mapper()



    def __init__(self):
        pass


    
    @classmethod
    def network_scanner(cls, table):
        """This method will be responsible for scanning and finding networks"""

        
        console.print(NetTilities.get_iface(get_name=True))


        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        if iface == False:
            console.print(f"[bold red]Error:[yellow] Failed to get network adapter")

            return False


        
        try:
            
            # PERFORM NETWORK SCAN
            iface.scan()
            networks = iface.scan_results()

    
            
            # IN CASE ITS EMPTY
            if not networks:
                raise KeyboardInterrupt

           
           # ITERATE THROUGH GIVEN LIST
            for net in networks:
                

                # GET ENCRYPTION AND FREQUENCY
                frequency = NetTilities.get_frequency(frequency=net.freq)
                encryption = NetTilities.get_encryption(akm=net.akm[0])
                console.print(f"Cipher: {net.cipher}")
                print(int(net.cipher))
                console.print(f"Cipher: {net.cipher}")
                cipher = NetTilities.get_cipher(cipher=net.cipher)
                channel = NetTilities.get_channel(freq=net.freq)


                # CATCH FUC UPS
                mess = ["", "5ghz", "2ghz"]

                if net.ssid.strip().lower() in mess:
                    net.ssid = "N/A"
               
                

                # NOW TO ITER THROUGH OBJECT
                if net.bssid not in cls.networks:
                    cls.networks.append(net.bssid)
                    

                    #ADD THE TABLE
                    table.add_row(f"{len(cls.networks)}", f"{net.signal}", f"{net.ssid}", f"{frequency}", f"{net.auth}", f"{cipher}", f"{encryption}",  f"{channel}", f"{net.bssid}")


                    # NOW TO SAVE DATA
                    cls.network_saver.network_logging(ssid=net.ssid, bssid=net.bssid, signal=net.signal, frequency=frequency, channel=1, auth=net.auth,  akm=encryption, cipher=cipher)

        

        #except 


        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

            return False


    
    @classmethod
    def loop_controller(cls, interval=3):
        """This method will be responsible for looping through network_scanner <-- until user kills it"""

        
        # MAKE SURE THEY HAVE A IFACE
        if NetTilities.get_iface(verbose=True):


            # CREATE TABLE FOR RESULTS
            table_results = Table(title='Recon Mode', style='bold purple', header_style='bold red')
            table_results.add_column("#")
            table_results.add_column("Signal", style='yellow')
            table_results.add_column("SSID", style='bold green')
            table_results.add_column("Frequency")
            table_results.add_column("Cipher")
            table_results.add_column("Authentication")
            table_results.add_column("Encryption")  # AKA AKM // AUTHENCTION AND KEY MANAGEMENT
            table_results.add_column("Channel")
            table_results.add_column("BSSID", style='cyan')

                
            # INDEFINITE UNTIL - CTRL + C
            with Live(table_results, console=console, refresh_per_second=.5):
                while True:

                    try:
                            
                        ReconScanner.network_scanner(table=table_results)

                        #console.print(table_results)

                        time.sleep(interval)


                    except KeyboardInterrupt as e:
                        console.print("\n\nKilling Recon mode...", style='bold red')
                        
                        break
                    

                    except Exception as e:
                        console.print(f"[bold red]Exception Error:[yellow] {e}")
            


            # SAVE RESULTS




        # IF FALSE
        else:
            text = pyfiglet.figlet_format(text='NO IFACE FOUND', font='bloody')
            console.print(text)

    


    @classmethod
    def main(cls):
        """This method will run module wide logic"""


        ReconScanner.loop_controller()



# FOR MODULER TESTING
if __name__ == "__main__":
    
    use = 1

    if use == 1:
        ReconScanner.main()
    

