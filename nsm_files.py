# WIFI SCANNER  // THIS WILL BE WHERE FILE HANDLING WILL HAPPEN

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


# ETC IMPORTS
from datetime import datetime
import time, os


# NSM IMPORTS
from nsm_utilities import Utilities

# FILE HANDLING
from pathlib import Path
import json

# CREATE DEFAULT FILE PATH LOCATION
base_dir = Path.home() / "Documents" / "nsm tools" / ".data" / "NetCracker" 
base_dir.mkdir(exist_ok=True, parents=True)


# ALT PATH WAYS
path_network = base_dir / "Networks" 




class Network_Mapper():
    """This class will be used to store and save found networks along with extra info about them"""
    

    def __init__(self):
        self.indent = 0
        self.data = {}
        pass



    def network_logging(self, ssid, bssid, signal, auth, frequency, encryption):
        """This will be used to store networks and there info"""

        
        # 1 FOR EACH NETWORK
        self.indent += 1
      

        # CREATE VARIABLES
        self.data[self.indent] = {

            "ssid": ssid,
            "bssid": bssid,
            "signal": signal,
            "auth": auth,
            "frequency": frequency,
            "encryption": encryption
            
        } 



        # FOR DEBUGGING
        use = False

        if use:
            console.print(self.indent)


    
    def network_saver(self):
        """This will save the networks"""
      
        
        # LOOP THROUGH IN CASE OF ELSE OR EXCEPTION
        while True:

            try:

                timestamp = datetime.now().strftime("%m-%d-%Y_%H_%M_%S")
                
                # REDUNDENCY CHECK
                if path_network.exists():

                    path = path_network / f"{timestamp}.json"

                    with open(path, "w") as file:
                        json.dump(self.data, file, indent=4)
                        

                        break
                
                else:
                    path_network.mkdir(exist_ok=True, parents=True)

            
            except json.JSONDecodeError as e:
                console.print(f"JSON Error: {e}")
                break

            except FileNotFoundError as e:

                # CREATE FILE PATH
                with open(path_network, "w") as file:
                    json.dump(file)

                console.print(f"[bold red]File not found Error:[/bold red] [yellow]{e}[/yellow]")


            except Exception as e:
                console.print(f"[bold red]Exception Error:[/bold red] [yellow]{e}[/yellow]")
                break
    
    
    def done(self):
        """Call upon this method once you are done with previous method to confirm files have been saved"""


        console.print(f"\n[bold green]Total Networks Found & Saved:[/bold green] {self.indent}")


    @staticmethod    
    def network_puller() -> str:
        """This will be used to pull all the save networks"""


        # SET TABLE CONSTANTS
        table_use = False



        while True:

            try:
                
                # MAKE SURE NETWORK DIR EXIST
                if path_network.exists() and path_network.is_dir():
                    
                    # USE THIS TO ITERATE THROUGH A DIR
                    for file in path_network.iterdir():

                        if file.exists() == False:
                            console.print("False")

                        with open(file, "r") as file:
                            content = json.load(file)
                            

                            # RAW OUTPUT EXAMPLE 
                            ('05-01-2025', '_', '01_18_16')

                            
                            # TO PREVENT FILE NAMING ERRORS // STILL IN TESTING STAGES
                            if os.name == "nt":
                                # GET TIMESTAMP, DATE AND TIME
                                timestamp = file.name.split("\\")[8].split('.')[0]
                                date = timestamp.partition('_')[0]
                                time = ':'.join(timestamp.partition('_')[2].split("_"))
                            
                            else:
                                timestamp = "N/A"
                                date = "Still testing for linux"
                                time = "Still testing for linux"

                            
                   
                            line = "-" * 80
                            

                            # FOR TEXT PRINT
                            if table_use == False:
                                console.print("\n\n",line)                            
                                console.print(f"Date: {date}  Time: {time}\n")
                            

                            # TABLE OBJECT
                            table = Table(title=f"Date: {date}  Time: {time}", title_style="bold green", header_style="bold red", style="bold purple")
                            table.add_column("signal")
                            table.add_column("ssid")
                            table.add_column("bssid")
                            table.add_column("auth")
                            table.add_column("frequency")
                            table.add_column("encryption")



                            # PRINT VALUES IN JSON
                            for key, value in content.items():

                                if value == None or value == "" or value == False:
                                    go = False

                                # FOR SEXY ASS TABLE PRINT // LOL NOOB
                                if table_use:
                                    
                                    
                                    # APPEND DATA TO TABLE
                                    table.add_row(
                                                  f"{value["signal"]}",
                                                  f"{value["ssid"]}",
                                                  f"{value["bssid"]}",
                                                  f"{value["auth"]}",
                                                  f"{value["frequency"]}",
                                                  f"{value["encryption"]}",
                                                  
                                                  )

                                    
                                    
                                # FOR PLAIN JSON PRINT
                                else:

                                    console.print(f"[cyan]Network #{key}[/cyan]: {value}")
            
                            
                            if table_use:
                                console.print("\n\n",table)

                            else:
                                console.print("\n",line)   
                            

                    
 
                    # THIS WILL BE WERE THE USER CAN CHOOSE TO CHANGE OUTPUT STYLE OR CLEAR JSON FILES
                    panel = Panel(
                                renderable=
                                "[blue]Json View == [red]1 \n"
                                "[purple]Table View == [red]2 \n"
                                "[green]Clear log == [red]Coming soon",
                                
                                style="bold red",
                                title="Output Style",
                                border_style="bold red",

                                expand=False

                                )
                    

                    console.print("\n\n[bold green]All networks Successfully printed\n")
                    console.print(panel)


                    # MAKE A CHOICE
                    choice = console.input(f"\n[bold red]Press enter to exit: ")

                
                    if choice.strip().lower() == "1" or choice.strip().lower() == "text" or choice.strip().lower() == "json":
                        table_use = False
                        Utilities.clear_screen()


                    elif choice.strip().lower() == "2" or choice.strip().lower() == "table":
                        table_use = True
                        Utilities.clear_screen()
                    
                    elif choice.strip().lower() == "clear" or choice.strip().lower() == "101" or choice.strip().lower() == "cls":
                        
                        pass

                    
                    # EXIT
                    else:
                      
                      break

                
                # MAKE DEFAULT DIR
                else:
                    path_network.mkdir(exist_ok=True, parents=True)


            except Exception as e:

                console.print(e)
                time.sleep(4)

                break
        





class Network_Puller():
    """This will pull any and all saved networks"""
    pass



# FOR MODULAR TESTING
if __name__ == "__main__":
    
    Network_Mapper().network_logging("aa", "ass", "as", "dd", "ff", "1111")