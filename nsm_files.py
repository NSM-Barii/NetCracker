# WIFI SCANNER  // THIS WILL BE WHERE FILE HANDLING WILL HAPPEN

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


# ETC IMPORTS
from datetime import datetime
import time

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
                console.print("Current Timestamp: ",timestamp)
                
                if path_network.exists():

                    #console.print(self.data)

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


        console.print(f"\n[bold green]Total Networks Found & Saved: [/bold green] {self.indent}")


    @staticmethod    
    def network_puller() -> str:
        """This will be used to pull all the save networks"""

        while True:

            try:
                
                # MAKE SURE NETWORK DIR EXIST
                if path_network.exists() and path_network.is_dir():
                    
                    # USE THIS TO ITERATE THROUGH A DIR
                    for file in path_network.iterdir():

                        with open(file, "r") as file:
                            content = json.load(file)

                            
                            # TIMESTAMP
                            timestamp = file.name.split("\\")[8].split('.')[0]
                            line = "-" * 80
 
                            console.print("\n\n",line)                            
                            console.print(f"TimeStamp: {timestamp}\n")


                            # PRINT VALUES IN JSON
                            for key, value in content.items():

                                console.print(f"[cyan]Network #{key}[/cyan]: {value}")

                            console.print("\n",line)   
                            

                            


                    console.print("\n\n[bold green]All networks printed successfully")
                    console.input(f"\n[bold red]Press enter to exit: ")

                    break

                
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