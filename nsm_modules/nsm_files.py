"""File handling and data storage for NetCracker.

Manages network scan results, settings, and war driving data persistence.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize console for this module
_console = Console()


def get_base_dir() -> Path:
    """Get the base data directory, accounting for sudo usage.

    Returns:
        Path to base data directory
    """
    try:
        sudo_user = os.getenv("SUDO_USER")
        if sudo_user:
            user_home = Path(f"/home/{sudo_user}")
        else:
            user_home = Path.home()

        base_dir = user_home / "Documents" / "nsm_tools" / ".data" / "netcracker"
    except Exception:
        base_dir = Path.home() / "Documents" / "nsm_tools" / ".data" / "netcracker"

    base_dir.mkdir(exist_ok=True, parents=True)
    return base_dir


BASE_DIR = get_base_dir()
NETWORKS_DIR = BASE_DIR / "Networks"
WAR_DRIVES_DIR = BASE_DIR / "war_drives"
SETTINGS_FILE = BASE_DIR / "settings.json"

# Ensure directories exist
NETWORKS_DIR.mkdir(exist_ok=True, parents=True)
WAR_DRIVES_DIR.mkdir(exist_ok=True, parents=True) 




class NetworkMapper:
    """Stores and persists network scan results."""

    def __init__(self):
        self.network_count = 0
        self.data: Dict[int, Dict[str, Any]] = {}

    def add_network(self, ssid: str, bssid: str, signal: int,
                    frequency: str, channel: int, auth: str,
                    encryption: str, cipher: str) -> None:
        """Log a discovered network.

        Args:
            ssid: Network SSID
            bssid: Network BSSID (MAC address)
            signal: Signal strength
            frequency: Frequency band
            channel: WiFi channel
            auth: Authentication method
            encryption: Encryption type
            cipher: Cipher suite
        """
        self.network_count += 1

        self.data[self.network_count] = {
            "ssid": ssid,
            "bssid": bssid,
            "signal": signal,
            "frequency": frequency,
            "channel": channel,
            "auth": auth,
            "encryption": encryption,
            "cipher": cipher
        }

    def save_networks(self) -> bool:
        """Save discovered networks to JSON file.

        Returns:
            True if successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%m-%d-%Y_%H_%M_%S")
            filepath = NETWORKS_DIR / f"{timestamp}.json"

            with open(filepath, "w") as f:
                json.dump(self.data, f, indent=4)

            return True

        except Exception as e:
            _console.print(f"[bold red]Save error:[/bold red] {e}")
            return False

    def print_summary(self, success: bool = True) -> None:
        """Print scan summary.

        Args:
            success: Whether scan completed successfully
        """
        if success:
            _console.print(
                f"\n[bold green]Networks found & saved:[/bold green] {self.network_count}"
            )


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

                    
 

class Settings:
    """Manages application settings persistence."""

    DEFAULT_SETTINGS = {
        "iface": "",
        "captures": ""
    }

    @classmethod
    def load(cls, verbose: bool = False) -> Dict[str, Any]:
        """Load settings from JSON file.

        Args:
            verbose: Print status messages

        Returns:
            Settings dictionary
        """
        try:
            if not SETTINGS_FILE.exists():
                cls._create_default_settings()

            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)

            if verbose:
                _console.print(f"✓ Settings loaded from {SETTINGS_FILE}", style="green")

            return settings

        except json.JSONDecodeError as e:
            _console.print(f"[red]Invalid JSON in settings:[/red] {e}")
            cls._create_default_settings()
            return cls.DEFAULT_SETTINGS
        except Exception as e:
            _console.print(f"[red]Error loading settings:[/red] {e}")
            return cls.DEFAULT_SETTINGS

    @classmethod
    def save(cls, data: Dict[str, Any], verbose: bool = False) -> bool:
        """Save settings to JSON file.

        Args:
            data: Settings dictionary to save
            verbose: Print status messages

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)

            if verbose:
                _console.print("✓ Settings saved", style="green")

            return True

        except Exception as e:
            _console.print(f"[red]Error saving settings:[/red] {e}")
            return False

    @classmethod
    def _create_default_settings(cls) -> None:
        """Create default settings file."""
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(cls.DEFAULT_SETTINGS, f, indent=4)
            _console.print("✓ Created default settings", style="green")
        except Exception as e:
            _console.print(f"[red]Error creating settings:[/red] {e}")

    # Backward compatibility
    @classmethod
    def get_json(cls):
        """Deprecated: Use Settings.load() instead."""
        return cls.load(verbose=True)

    @classmethod
    def push_json(cls, data):
        """Deprecated: Use Settings.save() instead."""
        return cls.save(data, verbose=True)

    
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

                    
                    break

                


                else:


                    BASE_DIR.mkdir()
            



            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

                break



class Recon_Pusher():
    """This class will be used to push data from recon mode"""

    
    def __init__(self):
        pass


    @classmethod
    def get_path(cls):
        """This will be responsible for creating path"""

        
        # VARS
        count = 1

        paths = BASE_DIR / "war_drives"
        paths.mkdir(exist_ok=True, parents=True)

        if BASE_DIR.exists():


            # GET A VALID FILE NAME
            while True:
                
                # CREATE PATH
                p = paths / f"drive_{count}.json"
                 
                # IF ITS FALSE WE KEEP THAT PATH
                if not p.exists():
                    break
                
                
                # += 
                count += 1
            

            # VERBOSE SHII
            #console.print(f"File: drive_{count}")
         

            # NOW RETURN PATH
            return p, count
    

    @classmethod
    def push_war(cls, save_data, CONSOLE, verbose=False):
        """This method will be used to push results from war driving"""

        path = cls.path


        # PUSH
        try:
            with open(path, "w") as file:
                json.dump(save_data, file, indent=4)

                
                if verbose:
                    CONSOLE.print(f"[+] War Results Succesfully pushed", style="bold green")
            
        
        # DESTROY ERRORS
        except Exception as e:
            CONSOLE.print(f"[bold red]Exception Error:[bold yellow] {e}")
    

    @classmethod
    def main(cls):
        """This will be called upon to init class vars"""

        # SET PATH
        cls.path, c = Recon_Pusher.get_path()


        # VERBOSE
        console.print(f"Recon init --> {c}", style="bold green")






# Backward compatibility aliases
Network_Mapper = NetworkMapper
Recon_Pusher = ReconPusher


if __name__ == "__main__":
    print("NetCracker File Management Module")
    print(f"Base directory: {BASE_DIR}")
    print(f"Networks directory: {NETWORKS_DIR}")
    print(f"War drives directory: {WAR_DRIVES_DIR}")