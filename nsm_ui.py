# WIFI SCANNER  // THIS HOUSE MAIN UI LOGIC


# UI IMPORTS
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.console import Console
console = Console()
console_width = console.size.width
import pyfiglet


# ETC IMPORTS
import time


# NSM MODULE IMPORTS
from nsm_scanner_mode import WifiUI 
from nsm_utilities import Utilities
from nsm_files import Network_Mapper
from nsm_deauth import Frame_Snatcher, You_Cant_DOS_ME


class MainUI():
    """This will house main menu ui logic"""


    def __init__(self):
        pass

    
    @staticmethod
    def welcome_message(font="dos_rebel"):
        """This will be the welcome message that is displayed within the main menu"""
        
        # FOR SPACE FROM TOP OF TERMINAL
        print("\n\n")

        # CREATE
        art1 = pyfiglet.figlet_format(text="        Net", font=font)    
        art2 = pyfiglet.figlet_format(text="  Cracker", font=font)


        # PRINT
        console.print(art1, style="bold yellow")  
        console.print(art2, style="bold blue")
        
        

        console.print("        ========================================================================", style="bold yellow")
        console.print(
        
           "            ===================  Developed by NSM Barii  ===================",
           style="bold blue"

        )
        console.print("        ========================================================================", style="bold yellow")
     
    

    @staticmethod
    def main_menu():
        """This will house the main menu logic"""
        

        # WILL NO LONGER BE USING PANELS FOR MENU SELECTION AS I WANT BETTER LOOKING UI'S
        choices = Panel(

            renderable="\n[1] Scan for Networks\n[2] Crack Networks\n[4] View saved networks\n[5] EXIT", 
            title="Malicious Practioner",
            style="purple",
            border_style='bold purple',
            width=min(130, console_width - 2)
            
        
        )

        
        color = "bold blue"
        color2 = "bold yellow"

        choicess = (

            f"\n       [{color}][1][/{color}] [{color2}]Deauth One Client\n"
            f"       [{color}][2][/{color}] [{color2}]Deauth All Clients\n\n"
            f"       [{color}][3][/{color}] [{color2}]Capture n Crack Handshake\n\n"
            f"       [{color}][4][/{color}] [{color2}]Ping Me\n\n"
            f"       [{color}][5][/{color}] [{color2}]Scan for Networks\n"
            f"       [{color}][6][/{color}] [{color2}]View Saved Networks\n\n"
            f"       [{color}][7][/{color}] [{color2}]EXIT "
            
            )
        
        console.print("\n\n\n", choicess, "\n\n")
  
        try:

            
            # LOOP FOR ERRORS
            while True:

                choice = console.input("     [bold red]Enter choice here: [/bold red]")

                # ALL VALID OPTIONS EXCEPT EXIT
                cc = ["2", "4", "5", "6"]

                if choice in cc:
                    Utilities.clear_screen()



                # DEAUTH ATTACK - ONE CLIENT
                if choice == "1":
                    console.print("[bold yellow]     This option is still under Construction")
                

                # DEAUTH ATTACK - ALL CLIENTS
                elif choice == "2":
                    Frame_Snatcher.main()

                    break
                    

                # CAPTURE AND CRACK HANDSHAKES
                elif choice == "3":
                    console.print("[bold yellow]     This option is still under Construction")

                

                # PING ME 
                elif choice == "4":
                    You_Cant_DOS_ME.ping()

                    break
                

                # SCAN FOR NETWORKS
                elif choice == "5":
                    WifiUI.main()

                    break


                # VIEW SAVED NETWORKS
                elif choice == "6":
                    Network_Mapper.network_puller()

                    break
                
                

                # EXIT
                elif choice == "7":
                    console.print("\nLater..............", style="bold red")
                    time.sleep(.1)
                    exit()

                
                

                # THIS IS STRICTLY FOR TESTING // ITS ALSO DEAPPRECIATED
                elif choice == "101":
                    from nsm_main import import_handler

                    Utilities.clear_screen()
                    import_handler().import_uninstaller()

                    break
                
                else:
                    console.print("\n     Please choose a valid option")
                

        
        except Exception as e:
            console.print(e)

    

    @staticmethod
    def main():
        """Call modular logic from this method"""

        
        # ANDDDD START
        while True:
            Utilities.clear_screen()
            MainUI.welcome_message()
            MainUI.main_menu()





# FOR MODULAR TESTING
if __name__ == "__main__":
    MainUI.main()