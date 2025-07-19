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

USER_HOME = Path(os.getenv("SUDO_USER") and f"/home/{os.getenv('SUDO_USER')}") or Path.home()
BASE_DIR = USER_HOME / "Documents" / "nsm_tools" / ".data" / "netcracker"
BASE_DIR.mkdir(exist_ok=True, parents=True)


# ALT PATH WAYS
path_network = BASE_DIR / "Networks" 




class Network_Mapper():
    """This class will be used to store and save found networks along with extra info about them"""
    

    def __init__(self):
        self.indent = 0
        self.data = {}
        pass



    def network_logging(self, ssid, bssid, signal, frequency, channel, auth, akm, cipher):
        """This will be used to store networks and there info"""

        
        # 1 FOR EACH NETWORK
        self.indent += 1
      

        # CREATE VARIABLES
        self.data[self.indent] = {

            "ssid": ssid,
            "bssid": bssid,
            "signal": signal,
            "frequency": frequency,
            "channel": channel,
            "auth": auth,
            "encryption": akm,  # ENCRYPTION  
            "cipher": cipher
            
        } 



        # FOR DEBUGGING
        verbose = False

        if verbose:
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
                break


            except Exception as e:
                console.print(f"[bold red]Exception Error:[/bold red] [yellow]{e}[/yellow]")
                break
            
    
    
    def done(self, go):
        """Call upon this method once you are done with previous method to confirm files have been saved"""

        if go:
            console.print(f"\n\n[bold green]Total Networks Found & Saved:[/bold green] {self.indent}")


    @staticmethod    
    def network_puller() -> str:
        """This will be used to pull all the save networks"""


        # SET TABLE CONSTANTS
        table_use = False


        # LOOP FOR ERROS
        while True:

            try:
                
                # MAKE SURE NETWORK DIR EXIST
                if path_network.exists() and path_network.is_dir():
                    
                    # USE THIS TO ITERATE THROUGH A DIR
                    for file in path_network.iterdir():
                        

                        # TO CHECK IF THERE ARE ANY FILES
                        if file:

                            with open(file, "r") as file:
                                content = json.load(file)
                                

                                # RAW OUTPUT EXAMPLE 
                                ('05-01-2025', '_', '01_18_16')

                                
                                # TO PREVENT FILE NAMING ERRORS // STILL IN TESTING STAGES
                                if os.name == "nt":
                                    # GET TIMESTAMP, DATE AND TIME
                                    timestamp = file.name.split("\\")[8].split('.')[0]
                                    date = timestamp.partition('_')[0]
                                    timee = ':'.join(timestamp.partition('_')[2].split("_"))
                                
                                else:
                                    timestamp = "N/A"
                                    date = "Still testing"
                                    timee = "for linux"

                                
                    
                                line = "-" * 80
                                

                                # FOR TEXT PRINT
                                if table_use == False:
                                    console.print("\n\n",line)                            
                                    console.print(f"Date: {date}  Time: {timee}\n")
                                

                                # TABLE OBJECT
                                table = Table(title=f"Date: {date}  Time: {timee}", title_style="bold green", header_style="bold red", style="bold purple")
                                table.add_column("signal")
                                table.add_column("ssid")
                                table.add_column("bssid")
                                table.add_column("auth")
                                table.add_column("frequency")
                                table.add_column("encryption")



                                # PRINT VALUES IN JSON
                                for key, value in content.items():

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

                        
                        # IF THERE ARE NO SAVED JSON FILES
                        else:
                            console.print("\n\n[bold red]No Files found")
                            

                    
 
                    # THIS WILL BE WERE THE USER CAN CHOOSE TO CHANGE OUTPUT STYLE OR CLEAR JSON FILES
                    panel = Panel(

                                renderable=
                                "[blue]\nJson View == [red]1 \n"
                                "[purple]Table View == [red]2 \n"
                                "[green]Clear log == [red]Coming soon\n",
                                
                                style="bold red",
                                title="Output Style",
                                border_style="bold red",
                                expand=False

                                )
                    

                    console.print("\n\n[bold green]All networks Successfully printed\n")
                    console.print(panel)


                    # MAKE A CHOICE
                    choice = console.input(f"\n[bold red]Press enter to exit: ")

                    
                    # TEXT VIEW
                    if choice.strip().lower() == "1" or choice.strip().lower() == "text" or choice.strip().lower() == "json":
                        table_use = False
                        Utilities.clear_screen()

                    # TABLE VIEW
                    elif choice.strip().lower() == "2" or choice.strip().lower() == "table":
                        table_use = True
                        Utilities.clear_screen()
                    
                    # DELETE FILES // NOT DONE // MIGHT NOT EVER BE DONE // LOLOLO
                    elif choice.strip().lower() == "clear" or choice.strip().lower() == "3" or choice.strip().lower() == "cls":
                        Network_Mapper.network_deleter()

                        time.sleep(2)
                        
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
        
    
    @staticmethod
    def network_deleter() -> None:
        """This will be responsible for deleting any and all json files within the network Dir"""
        
        global path_network

        try:

            if path_network.exists() and path_network.is_dir():
                
                # REDEFINE THE NETWORK DIR // I DONT THINK ITS NEEDED BUT FUCK IT LOL
                path_network = BASE_DIR / "Networks"

                # NOW TO OVERWRITE CURRENT DIR
                os.remove(path_network)
                path_network.mkdir(exist_ok=True, parents=False)
              
                console.print("\n[bold red]Network Directory sucessfully cleared!!!")
            
            else:
                console.print("[bold red]NSM_Files Error: [yellow]Check line 300 for debugging")
        
        except Exception as e:
            console.print(e)

                    
 

class Settings():
    """This method will be responsible for controlling json info"""


    def __init__(self):
        pass


    
    @classmethod
    def get_json(cls):
        """This will pull and return json info"""


        # DEBUG
        verbose = True

        
        # DESTROY ERRORS
        while True:
            try:

                # IF EXISTS
                if BASE_DIR.exists():


                    # MAKE SETTINGS
                    path = BASE_DIR / "settings.json"


                    with open(path, "r") as file:

                        settings = json.load(file)


                        if verbose:
                            console.print(f"Successfully Pulled settings.json from {path}", style="bold green")


                    return settings
                

                

                # MAKE PATHS
                else:

                    BASE_DIR.mkdir(exist_ok=True, parents=True)
            


            # MAKE JSON
            except FileNotFoundError as e:

                if verbose:
                    console.print(f"[bold red]FileNotFound Error:[yellow] {e}")

                
                # CREATE VARS
                path = BASE_DIR / "settings.json"
                data = {
                        "iface": "",
                        "captures": ""
                    }


                # PUSH IT 
                with open(path, "w") as file:

                    json.dump(data, file, indent=4)
                

                # PERFECT
                console.print("Successfully created json file", style="bold green")


        
            
            # ERRORS
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

                break



    @classmethod
    def push_json(cls, data):
        """This method will be used to push info to settings.json"""


        # VARS
        verbsoe = True
        time_stamp = datetime.now().strftime("%m/%d/%Y - %I:%M:%S")


        # DESTROY ERRORS
        while True:
            try:

                # 
                if BASE_DIR.exists():
                    

                    # VARS
                    path = BASE_DIR / "settings.json"

                    with open(path, "w") as file:

                        json.dump(data, file, indent=4)


                        if verbsoe:
                            console.print("Successfully pushed settings.json", style="bold green")
                    

                    return



                
                # MAKE DIR
                else:

                    BASE_DIR.mkdir(exist_ok=True, parents=True)


                    if verbsoe:
                        console.print(f"Successfully created dir", style="bold green")
                
            


            except FileNotFoundError as e:

                if verbsoe:
                    console.print(f"[bold red]FileNotFound Error:[yellow] {e}")

                
                # CREATE VARS
                path = BASE_DIR / "settings.json"
                data = {
                        "iface": "",
                        "captures": ""
                    }


                # PUSH IT 
                with open(path, "w") as file:

                    json.dump(data, file, indent=4)
                

                # PERFECT
                console.print("Successfully created json file", style="bold green")

                
            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
                
                break


    

    @classmethod
    def push_txt(cls, data):
        """This method is just to make a new txt file with info"""

        
        # VAR
        verbose = True


        
        # LOOP FOR ERRORS
        while True:

            try:

                if BASE_DIR.exists():

                    path = BASE_DIR / ""


                    with open(path, "a") as file:
                        file.write(data)


                    if verbose:
                        console.print(f"Successfully appended info", style="bold green")

                


                else:


                    BASE_DIR.mkdir()
            



            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")





# FOR MODULAR TESTING
if __name__ == "__main__":
    
    Network_Mapper().network_logging("aa", "ass", "as", "dd", "ff", "1111")