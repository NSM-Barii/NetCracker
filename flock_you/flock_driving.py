# THIS MODULE WILL BE USED FOR FLOCK DRIVING


# UI IMPORTS
from rich.table import Table
from rich.live import Live 
from rich.panel import Panel
from rich.console import Console
console = Console()



# BT IMPORTS
from bleak import BleakScanner


# ETC IMPORTS
import time, asyncio





class BLE_Sniffer():
    """This class will be responsible for findning ble devices"""



    @staticmethod
    async def _discover(timeout):
        """internal scanner"""

        return await BleakScanner.discover(timeout=timeout, return_adv=True)

     
    @classmethod
    def ble_scan(cls, timeout=5):
        """This will sniff for ble advertisements traversing our surroundings"""

        
        devices = asyncio.run(BLE_Sniffer._discover(timeout=timeout))


        for dev in devices:
            #console.print(dev)
            pass
        

        console.print(devices)
        input("\n\n Done: ")


    
    @classmethod
    def main(cls, scan_duration=5, timeout=2, verbose=True):
        """This method will be resposnible for looping through ble_scan <-- scan"""


        # VARS
        scans = 0



        console.print("[bold green][+] Launching BLE_Sniffer")


        while True:

            BLE_Sniffer.ble_scan(timeout=scan_duration); scans += 1

            time.sleep(timeout)


            if verbose:
                console.print(f"[*] Starting scan #{scans}")




if __name__ == "__main__":
    BLE_Sniffer.main()