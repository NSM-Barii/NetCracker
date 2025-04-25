# WIFI SCANNER  // THIS WILL BE WHERE FILE HANDLING WILL HAPPEN

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


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
      
        
        # LOOP THROUGH IN CASE OF ELSE OR EXCEPTION
        while True:

            try:
                
                if path_network.exists():

                    #console.print(self.data)

                    path = path_network / "networks.json"

                    with open(path, "w") as file:
                        json.dump(self.data, file, indent=4)
                        

                        break
                
                else:
                    path_network.mkdir(exist_ok=True, parents=True)


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


        console.print(f"\n[bold blue]Total Networks Saved: [/bold blue] {self.indent}")
    



# FOR MODULAR TESTING
if __name__ == "__main__":
    
    Network_Mapper().network_logging("aa", "ass", "as", "dd", "ff", "1111")