# WIFI SCANNER  // UTILITIES MODULE

# UI IMPORTS
import pywifi.iface
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff


# ETC IMPORTS 
import threading, os, random, time, pyttsx3, platform, os



class Utilities():
    """This class will hold secondary methods that will provide info for main program logic"""


    def __init__(self):
        pass

    
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