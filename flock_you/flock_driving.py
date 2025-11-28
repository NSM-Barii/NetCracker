# THIS MODULE WILL BE USED FOR FLOCK DRIVING


# UI IMPORTS
from rich.table import Table
from rich.live import Live 
from rich.panel import Panel
from rich.console import Console
console = Console()



# BT IMPORTS
from bleak import BleakScanner


# WIFI IMPORTS
from scapy.all import sniff, Ether, RadioTap
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth, Dot11ProbeReq


# ETC IMPORTS
import time, asyncio, threading


# NSM IMPORTS
from signatures import FLOCK_SIGNATURES
from nsm_modules.nsm_utilities import Background_Threads, NetTilities
from nsm_modules.nsm_utilities import Utilities as nsm_utilities
from nsm_modules.nsm_deauth import Frame_Snatcher







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
    def matches(cls, ssid=False, mac=False, ble_name=False, uuid=False, vendor=False):
        """This will output to the user what matches lead to a potential AI Camera being found"""

        space = "    "


        if ssid: console.print(f"{space}[bold green][+] Match SSID:[bold yellow] {ssid}") or console.print(f"{space}[bold red][-] Match SSID:[bold yellow] False")
        if mac: console.print(f"{space}[bold green][+] Match MAC:[bold yellow] {mac}") or console.print(f"{space}[bold red][-] Match MAC:[bold yellow] False")
        if vendor: console.print(f"{space}[bold green][+] Match Vendor:[bold yellow] {vendor}") or console.print(f"{space}[bold red][-] Match Vendor:[bold yellow] False")
        if ble_name: console.print(f"{space}[bold green][+] Match BLE_name:[bold yellow] {ble_name}") or console.print(f"{space}[bold red][-] Match BLE_name:[bold yellow] False")
        if uuid: console.print(f"{space}[bold green][+] Match UUID(s):[bold yellow] {uuid}") or console.print(f"{space}[bold red][-] Match UUID(s): [bold yellow] False")





    
    @classmethod
    def controller(cls, ssid=False, mac=False, ble_name=False, uuid=False):
        """This method will be the ultimate controller of all sub methods"""

        
        # BOOL CHECK DATA
        check_ssid = Utilities._check_ssid(ssid=ssid)            if ssid else False
        check_mac = Utilities._check_mac(mac=mac)                     if mac else False
        check_ble_name = Utilities._check_ble_name(ble_name=ble_name) if ble_name else False
        check_uuid = Utilities._check_uuid(uuid=uuid)                 if uuid else False



        return check_ssid, check_mac, check_ble_name, check_uuid
    








class BLE_Sniffer():
    """This class will be responsible for findning ble devices"""



    @staticmethod
    async def _discover(timeout):
        """internal scanner"""
        
        try:
            return await BleakScanner.discover(timeout=timeout, return_adv=True)
        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold red] {e}")


    @classmethod
    def ble_scan(cls, timeout=5):
        """This will sniff for ble advertisements traversing our surroundings"""

        
        devices = asyncio.run(BLE_Sniffer._discover(timeout=timeout))

        
        # PARSE DATA
        for mac, (device, adv) in devices.items():

            try:

                if mac not in cls.ble_devices: 

                    cls.ble_devices.append(mac)
                    

                    # STORE VARS
                    local_name = adv.local_name
                    rssi = adv.rssi
                    manufacturer = adv.manufacturer_data
                    services = adv.service_uuids
                    vendor = nsm_utilities.get_vendor(mac=mac)


                    data = {
                        "mac": mac,
                        "vendor": vendor,
                        "rssi": rssi,
                        "local_name": local_name,
                        "manufacturer": manufacturer,
                        "services": services
                    }


                    # ARE YOU FLOCK or AI ???
                    check_ssid, check_mac, check_ble_name, check_uuid = Utilities.controller(ssid=False, mac=mac, ble_name=local_name, uuid=services)
                                        

                    # REALISTICALLY THIS WOULD BE THE BEST ONE TO USE
                    if check_mac or check_ble_name or check_uuid: 

                        console.print(f"[bold green][+] Found AI Camera (BLE):[bold yellow] {data}")
                        Utilities.matches(ssid=False, mac=mac, vendor=vendor, ble_name=local_name, uuid=services)
                        cls.ai_cameras.append(data)
                    

                    if cls.verbose:
                        console.print(f"[bold red][-] Non AI Camera (BLE):[bold yellow] {data}")     
                
                            
            except KeyboardInterrupt as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
    
        
         
    @classmethod
    def main(cls, scan_duration=5, timeout=2, verbose=True):
        """This method will be resposnible for looping through ble_scan <-- scan"""


        # VARS
        cls.verbose = False
        scans = 1
        cls.ble_devices = []
        cls.ai_cameras = []



        console.print("[bold green][+] Starting BLE_Sniffer")


        while Main_Thread.BACKGROUND:


            BLE_Sniffer.ble_scan(timeout=scan_duration); scans += 1

            time.sleep(timeout)
        
        console.print(f"[bold red][-] Killed -->[bold yellow] BLE Sniffer")


class WiFi_Sniffer():
    """This class will be responsible for finding wifi devices"""


    @classmethod
    def _packet_parser(cls, pkt):
        """This will be responsible for parsing packets"""

        
        def _parser():

            if pkt.haslayer(Dot11Beacon):

                addr1 = pkt[Dot11].addr1 if pkt[Dot11].addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt[Dot11].addr2 if pkt[Dot11].addr2 != "ff:ff:ff:ff:ff:ff" else False


                ssid = pkt[Dot11Elt].info.decode(errors="ignore") or False


                channel = Background_Threads.get_channel(pkt=pkt)
                vendor = nsm_utilities.get_vendor(mac=addr2)
                rssi = NetTilities.get_rssi(pkt=pkt)
                encryption = Background_Threads.get_encryption(pkt=pkt)
                freq = Background_Threads.get_freq(freq=pkt[RadioTap].ChannelFrequency)

                data = {
                    "ssid": ssid,
                    "vendor": vendor,
                    "frequency": freq,
                    "encryption": encryption,
                    "channel": channel,
                    "rssi": rssi
                }

                if not ssid or not channel:
                    return

                if ssid and ssid not in cls.beacons: 

                    check_ssid, check_mac, check_ble_name, check_uuid = Utilities.controller(ssid=ssid, mac=addr2, ble_name=False, uuid=False)


                    if check_ssid or check_mac:
                        
                        console.print(f"[bold green][+] Found AI Camera (WiFi):[bold yellow] {data}")
                        Utilities.matches(ssid=ssid, mac=addr2, vendor=vendor, ble_name=False, uuid=False)

                        cls.ai_cameras.append(data)
                        cls.beacons.append(ssid)

                        return
                    
                if cls.verbose and ssid not in cls.beacons:
                    console.print(f"[bold red][-] Non AI Camera (WiFi):[bold yellow] {data}")
                    cls.beacons.append(ssid)
        
        
        if  Main_Thread.BACKGROUND: threading.Thread(target=_parser, args=(), daemon=True).start()
        else: raise KeyboardInterrupt
        


    @classmethod
    def _wifi_scan(cls, iface):
        """This will perform a wifi scan"""

        attempts = 0

        
        while True:

            try:

                attempts += 1

                if cls.verbose:
                    console.print(f"Attempt #{attempts}")

                sniff(iface=iface, store=0, prn=WiFi_Sniffer._packet_parser)

            
            except KeyboardInterrupt as e:
                console.print(f"[bold red][-] Killed -->[bold yellow] WiFi Sniffer")
                break
            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
                break
    

    @classmethod
    def main(cls, iface):
        """This method will be responsible for running wifi_scan <-- """


        console.print("[bold green][+]Starting WiFi_Sniffer")


        # VARS
        cls.verbose = True
        cls.beacons = []
        cls.ai_cameras = []

        
        Background_Threads.channel_hopper()

        WiFi_Sniffer._wifi_scan(iface=iface)

        console.print(f"[bold red][-] Killed -->[bold yellow] WiFi Sniffer")



class Main_Thread():
    """This class will be the main class in charge of sub classess"""


    @classmethod
    def main(cls):
        """Get shit done"""

        cls.BACKGROUND = True

        iface = Frame_Snatcher.get_interface()


        # WIFI SNIFFER
        threading.Thread(target=WiFi_Sniffer.main, args=(iface,), daemon=True).start()
        

        # BLE SNIFFER
        threading.Thread(target=BLE_Sniffer.main, args=(), daemon=True).start()

        
        time.sleep(.5); console.print(f"[bold green][+] ALL Background Threads Started")

        try:
            while True: time.sleep(0.1)

        except KeyboardInterrupt as e:

            cls.BACKGROUND = False
            time.sleep(0.5); console.print(f"Killing Background Threads")






if __name__ == "__main__":
    Main_Thread.main()