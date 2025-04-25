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


# OTHER MODULE IMPORTS
from nsm_logic import WifiUI 



class MainUI():
    """This will house main menu ui logic"""


    def __init__(self):
        pass

    
    @staticmethod
    def welcome_message():
        """This will be the welcome message that is displayed within the main menu"""

        art_static = pyfiglet.figlet_format(text="          Net", font="bloody")
        console.print(art_static)        
        art_static = pyfiglet.figlet_format(text="    Cracker", font="bloody")
        console.print(art_static, style="bold red")

    
    @staticmethod
    def main_menu():
        """This will house the main menu logic"""

        choices = Panel(

            renderable="\n[1] Scan for Networks\n[2] Crack Networks\n[4] View saved networks\n[5] EXIT", 
            title="Malicious Practioner",
            style="purple",
            border_style='bold purple',
            width=min(130, console_width - 2)
            
        
        )

       # console.print(choices)
        
        color = "red"
        color2 = "white"

        choicess = (

            f"\n[{color}][1][/{color}] [{color2}]Scan for Networks\n"
            f"[{color}][2][/{color}] [{color2}]Crack Networks\n"
            f"[{color}][3][/{color}] [{color2}]Deauth Attack\n"
            f"[{color}][4][/{color}] [{color2}]View saved networks\n"
            f"[{color}][5][/{color}] [{color2}]EXIT "
            
            )
        
        console.print("\n", choicess)

        try:

            choice = console.input("\n\n[bold red]Enter choice here: [/bold red]")


            # NOW FOR CHOICES 
            if choice == "1":
                WifiUI.main()
            
            elif choice == "2":
                pass

            elif choice == "3":
                pass

            elif choice == "4":
                pass
            
            elif choice == "5":
                console.print("\nLater..............", style="bold red")
                time.sleep(1)
                exit()


        
        except Exception as e:
            console.print(e)

    

    @staticmethod
    def main():
        """Call modular logic from this method"""

        
        # ANDDDD START
        MainUI.welcome_message()
        MainUI.main_menu()




# FOR MODULAR TESTING
if __name__ == "__main__":
    MainUI.main()