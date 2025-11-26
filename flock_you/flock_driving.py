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


# NSM IMPORTS
from signatures import FLOCK_SIGNATURES





class Utilities():
    """This class will be responsible for called upon methods"""


    # TESTING ONLY
    verbose = False

    
    # DATA
    wifi_ssid_patterns = FLOCK_SIGNATURES["wifi_ssid_patterns"]
    mac_prefixes = FLOCK_SIGNATURES["mac_prefixes"]
    ble_name_patterns = FLOCK_SIGNATURES["ble_name_patterns"]
    raven_service_uuids = FLOCK_SIGNATURES["raven_service_uuids"]



    @classmethod
    def _check_ssid(cls, ssid):
        """This method will be responsible for matching prefixes == ssid"""


        for camera_ssid in cls.wifi_ssid_patterns:

            if camera_ssid == ssid:

                if cls.verbose: console.print(f"[bold red][+] Found SSID Name:[bold yellow] {ssid}")

                return True
        
        return False


    @classmethod
    def _check_mac(cls, mac:str):
        """This method will be resposnible for matching prefixes == mac"""


        for flock_mac in cls.mac_prefixes:

            if flock_mac == mac:

                if cls.verboose: console.print(f"[bold red][+] Found Flock MAC:[bold yellow] {mac}")
                 
                return True
            
        return False
    
    
    @classmethod
    def _check_ble_name(cls, ble_name):
        """This method will be responsible for matching prefixes == ble_name"""



        for camera_name in cls.ble_name_patterns:

            if camera_name == ble_name:

                if cls.verbose: console.print(f"[bold red][+] Found BLE Name:[bold yellow] {ble_name}")


                return True
            
        
        return False


    @classmethod
    def _check_uuid(cls, uuid):
        """This metod will be responsible for matching prefixes == uuid(s)"""


        if len(uuid) > 1:


            for id in uuid:

                for raven_uuid in cls.raven_service_uuids:

                    if raven_uuid == id:
                        
                        if cls.verbose: console.print(f"[bold red][+] Found Raven UUID:[bold yellow] {uuid}")
                    
                        
                        return True
                
            return False
        

        else:

            for raven_uuid in cls.raven_service_uuids:

                if raven_uuid == uuid:
                    
                    if cls.verbose: console.print(f"[bold red][+] Found Raven UUID:[bold yellow] {uuid}")
                
                    
                    return True
            
            return False


    
    @classmethod
    def controller(cls, ssid=False, mac=False, ble_name=False, uuid=False):
        """This method will be the ultimate controller of all sub methods"""

        
        # BOOL CHECK DATA
        check_ssid = Utilities._check_ssid(wifi_ssid=ssid)            if ssid else False
        check_mac = Utilities._check_mac(mac=mac)                     if mac else False
        check_ble_name = Utilities._check_ble_name(ble_name=ble_name) if ble_name else False
        check_uuid = Utilities._check_uuid(uuid=uuid)                 if uuid else False


        return check_ssid, check_mac, check_ble_name, check_uuid




    



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

        
        # PARSE DATA
        for mac, (device, adv) in devices.items():

            if mac not in cls.ble_devices: 

                cls.ble_devices.append(mac)
                

                # STORE VARS
                local_name = adv.local_name
                rssi = adv.rssi
                manufacturer = adv.manufacturer_data
                services = adv.service_uuids


                data = {
                    "mac": mac,
                    "local_name": local_name,
                    "manufacturer": manufacturer,
                    "services": services,
                    "rssi": rssi
                }


                # ARE YOU FLOCK or AI ???
                check_ssid, check_mac, check_ble_name, check_uuid = Utilities.controller(ssid=False, mac=mac, ble_name=local_name, uuid=services)

                if check_mac:      console.print(f"[bold red][+] Found AI Camera:[bold yellow] {check_mac}")
                if check_ble_name: console.print(f"[bold red][+] Found AI Camera:[bold yellow] {check_ble_name}")
                if check_uuid:     console.print(f"[bold red][+] Found AI Camera:[bold yellow] {check_uuid}")
                

                # REALISTICALLY THIS WOULD BE THE BEST ONE TO USE
                if check_mac or check_ble_name or check_uuid: 

                    console.print(f"[bold red][+] Found AI Camera:[bold yellow] {data}")

                    cls.ai_cameras.append(data)
                

                
                console.print(data)

                
            
        
        #console.print(devices)
        #input("\n\n Done: ")


    
    @classmethod
    def main(cls, scan_duration=5, timeout=2, verbose=True):
        """This method will be resposnible for looping through ble_scan <-- scan"""


        # VARS
        scans = 1
        cls.ble_devices = []
        cls.ai_cameras = []



        console.print("[bold green][+] Starting BLE_Sniffer")


        while True:

            if verbose:
                console.print(f"[*] Starting scan #{scans}")

            BLE_Sniffer.ble_scan(timeout=scan_duration); scans += 1

            time.sleep(timeout)






if __name__ == "__main__":
    BLE_Sniffer.main()