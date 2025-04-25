# WIFI SCANNER  // THIS WILL BE A RED TEAM PROGRAM 




class import_handler():
    """This class and module is responsible for running before the official logic of the program is executed, this will therefore make sure each import is on the system to prevent any errors"""


    def __init__(self):
        pass

    
    @staticmethod
    def imports():
        """This will be where we put all our imports used across all program modules"""

        try:

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
            import threading, os, random, time, pyttsx3, pyfiglet


            # FILE HANDLING
            import json, pathlib


            # NSM MODULES
            from nsm_logic import WifiUI

            

            # NOW TO BEGIN 
            console.print("Module check complete", style="bold green")
            import_handler.main()
        

        except Exception as e:

            print(f"Main Module Error: {e}")


            while True:
                cmd = input("Enter command: ")
                
                if cmd == "exit":
                    print("later")
                    break

                else:
                    os.system(cmd)
        
    
    @staticmethod
    def main():
        """Multi-module logic will be called from here"""

        from nsm_ui import MainUI
        MainUI.main()



# BEGIN MULTI-MODULE LOGIC
if __name__ == "__main__":
    import_handler.imports()
    
    