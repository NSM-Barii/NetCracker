# WIFI SCANNER  // UTILITIES MODULE

# UI IMPORTS
import pywifi.iface
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress, requests, manuf
from scapy.all import sniff, RadioTap
from scapy.layers.dot11 import Dot11Elt
from mac_vendor_lookup import MacLookup

# DOWNLOAD THE WHOLE DATABASE
#MacLookup().update_vendors(data_store_path="mac-vendors.json")
vendors = MacLookup()
vendors.load_vendors()




# ETC IMPORTS 
import threading, os, random, time, pyttsx3, platform, os, subprocess



class Utilities():
    """This class will hold secondary methods that will provide info for main program logic"""


    def __init__(self):
        pass
    
    

    @staticmethod
    def get_vendor(mac:str):
        """This class will be responsible for getting the vendor"""

        
        # FOR DEBUGIGNG
        verbose = False


        # TRY API FIRST
        url = f"https://api.macvendors.com/{mac}"
        

        try:
            response = requests.get(url=url, timeout=3)

            if response.status_code == 200:

                if verbose:
                    console.print(f"Successfully retrieved API Key: {response.text}")

                
                return response.text

        
        
        # DESTROY ERRORS
        except Exception as e:

            if verbose:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

            
            
            #response = vendors.lookup(mac=mac) if vendors.lookup(mac=mac) else None

            response = manuf.MacParser("manuf.txt").get_manuf_long(mac=mac)

            return response
    
    
    @staticmethod
    def tts(say, lock = False, voice_rate = 20, voice_sound=False) -> str:
        """This method will be used to speak to the user through voice engines, use a thread locker if using threads to prevent race conditions"""


        
        # CHECK FOR OS FIRST // TRANSITION TO LINUX FROM WINDOWS
        if Utilities.get_os(windows=True):
        

            # CREATE OBJECT
            engine = pyttsx3.init()


            # SET VARIABLES
            try:
            
                rate = engine.getProperty('rate')
                voices = engine.getProperty('voices')


                # SET RATE
                engine.setProperty('rate', rate - voice_rate)
            
                
                # NOW TO CHOOSE THE VOICE WE WANT TO USE
                if voice_sound != False:
                    voice_sound = int(voice_sound)
                    engine.setProperty('voice', voices[voice_sound])
                    T = "1"

                elif len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                    T = "2"

                else:
                    engine.setProperty('voice', voices[0].id)
                    T = "3"
                
                # FOR DEBUGGING
                #console.print(T)
                
                # NOW TO SPEAK TTS
                if not lock:
                        
                    engine.say(say)
                    engine.runAndWait()
                    
                else:

                    with lock:
                        engine.say(say)
                        engine.runAndWait()
                

            except Exception as e:
                console.print(e)


    
    @staticmethod
    def clear_screen():
        """This will be used to clear the os screen"""

        # WINDOWS
        if os.name.strip() == "nt":
            os.system('cls')

        # LINUX
        elif os.name.strip() == "posix":
            os.system('clear')
        
        else:
            console.print("[bold red]Utilities Module Error:[/bold red] [yellow]failed to clear screen, platform not supported[yellow]")


    
    @classmethod
    def get_os(cls, windows=False, linux=False):
        """THis method will be used to get the os that the user is operating this program off of"""


        try:
            
            # CAPTURE OS
            OS = platform.system()
            

            # BOOLEAN MAKING IT EASIER
            if linux: 
                if OS.lower() == "linux":
                    return True
            
                else:
                    return False

            
            
            if windows:
                if OS.lower() == "windows":
                    return True
            
                else:
                    return False
            

            # IF BOTH ARE FALSE
            if OS.lower() in ["windows","linx"]:
                return OS
            
            else:
                return "mac"

        

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

    


class NetTilities():
    """This class will house reusuable methods for scanning"""

    def __init__(self):
        pass



    @staticmethod
    def get_iface(get_name=False, verbose=False):
        """This method will be used to get an iface"""


        try:
            
            # GET THE IFACE AND RETURN IT
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[1]

            
            

            if get_name:
                return iface.name()
            
            return iface


        

        except Exception as e:
            if verbose:
                console.print(f"[bold red]NetTilities Error:[yellow] {e}")
            

            return False
    

    @staticmethod
    def get_cipher(cipher):
        """This method will be used to get cipher"""
        
       # console.print(cipher)
        ciphers = {
            0: "None",
            1: "WEP",
            2: "TKIP",
            3: "AES",
            4: "UNKOWN"
        }
        
        cipher = int(cipher)
        result = ciphers.get(cipher)


        return result


    @staticmethod
    def get_encryption(akm):
        """This method will be used to get the get_encryption type that the network is using"""


        # CREATE A LIST FULL OF THE AUTHENTICATION TYPES

        encryptions = {
            0: "Open",
            1: "WPA",
            2: "WPA-PSK",
            3: "WPA2",
            4: "WPA2-PSK",
            5: "Unkown",
            6: "WPA3",
            7: "WPA3-SAE"

        }
        
        encryption = encryptions.get(akm)
        
        return encryption
     

    @staticmethod
    def get_frequency(frequency):
        """Get the frequency being used by the wifi"""


        # 2.4GHZ OR 5GHZ
        if  frequency in range(2400000, 2500000):
            return "2.4 GHz"
        
        elif frequency in range(5000000, 5800000):
            return "5 GHz"
        
        elif frequency in range(5900000, 7200000):
            return "6 GHz"


        else:
            return frequency
        

    @staticmethod
    def get_channel(freq):
        """This method will be responsible for getting the channel"""

        
        if 2412 <= freq <= 2472:
            return (freq - 2407) // 5
        elif freq == 2484:
            return 14
        elif 5180 <= freq <= 5825:
            return (freq - 5000) // 5
        return None

 
    @staticmethod
    def get_ies(pkt, sort=False, client=False, ap=False):
        """This method will be responsible for pulling ie info"""


        # IE == INFORMATION ELEMENTS


        # FAIL SAFE
        if not pkt.haslayer(Dot11Elt):
            return False
        

        # COMMON IE NAMES
        IE_NAMES = { 
            0:  "SSID",
            1:  "Supported Rates",
            3:  "Channel",
            5:  "TIM",
            7:  "Country Info",
            45: "HT Capabilities",
            48: "RSN Info",
            50: "Extended Rates",
            61: "HT Information",
            191: "VHT Capabilities",
            192: "VHT Operation",
            221: "Vendor Specific"
        }
        
        
        # STORE IES
        elements = {}

        # GET IES
        elt = pkt[Dot11Elt]


        # LOOP THROUGH AND STORE IE's
        while elt:
            
            try:
            

                # GET ID & NAME
                ie_id = elt.ID
                ie_name = IE_NAMES.get(ie_id, f"UNKOWN({ie_id})")
                ie_data = elt.info.decode(errors="ignore") if elt.info.decode(errors="ignore") else 'False'


                # NOW TO ADD INFO
                elements[ie_id] = ie_data

                # NOW TO GO TO THE NEXT IE
                elt = elt.payload.getlayer(Dot11Elt)
            
            except Exception as e:
                console.print(f"[bold red]IE Error:[bold yellow] {e}")
        

        # FIX LATER
        if not elements[3]: elements[3] = False 
        

        # RETURN INFO

        # FOR AP
        if sort and ap:  # SSID, CHANNEL, RSN INFO, VENDOR
            return elements[0], elements[3], elements[48], elements[221]
        

        # FOR CLIENT
        elif sort and client:  # SSID, 
            return elements[0]

        # ELSE RETURN RAW DICT
        else:
            return elements
    

    @staticmethod
    def get_rssi(pkt, format=False):
        """This method will be responsible for pulling signal strength"""

        signal = ""; signal = f"[bold red]Signal:[/bold red] {signal}"  

        
        # CHECK FOR RADIO HEADER
        if pkt.haslayer(RadioTap):
            

            # PULL RSSI
            rssi = getattr(pkt, "dBm_AntSignal", False)
            
            # NOW RETURN
            if rssi:

                if format:
                    return f"{rssi} dBm"
                
                return rssi




class Background_Threads():
    """This module will house background permanent running threads"""
    

    # CLASS VARIABLES
    hop = True
    channel = 0




    @classmethod
    def get_channel(cls, pkt):
        """This will be used to get the ssid channel"""


        elt = pkt[Dot11Elt]
        channel = 0


        while isinstance(elt, Dot11Elt):

            if elt.ID == 3:
                channel = elt.info[0]
                return channel
            
            elt = elt.payload




    @classmethod
    def channel_hopper(cls, set_channel=False, verbose=False):
        """This method will be responsible for automatically hopping channels"""


        # NSM IMPORTS
        from nsm_files import Settings
        

        def hopper():

            delay = 0.25
            all_hops = [1, 6, 11, 36, 40, 44, 48, 149, 153, 157, 161]

            iface = Settings.get_json()['iface']


            # TUNE HOP
            if set_channel:


                cls.hop = False


                try:

                    subprocess.Popen(
                    ["sudo", "iw", "dev", iface, "set", "channel", str(set_channel)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[bold yellow] {e}")
   

            # AUTO HOPPING
            while cls.hop:

                for channel in all_hops:


                    try:
                    

                        # HOP CHANNEL
                        subprocess.Popen(
                            ["sudo", "iw", "dev", iface, "set", "channel", str(channel)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            stdin=subprocess.DEVNULL,
                            start_new_session=True
                        )
                        cls.channel = channel
                        if verbose:
                            console.print(f"[bold green]Hopping on Channel:[bold yellow] {channel}")

                        # DELAY
                        time.sleep(delay)
                    
                    except Exception as e:
                        console.print(f"[bold red]Exception Error:[bold yellow] {e}")



        threading.Thread(target=hopper, args=(), daemon=True).start()
        cls.hop = True












# FOR MODULE TESTING
if __name__ == "__main__":



    tests = {
        0: "ass",
        1: "toes",
        2: "booty",
        3: "but"
    }


    toe = 3

    console.print(tests.get(toe))


    console.print(os.name)



    Background_Threads.channel_hopper()



    while True:
        pass