"""Utility functions for NetCracker.

Provides helper functions for vendor lookup, text-to-speech, OS detection,
network utilities, and background threading operations.
"""

import os
import time
import platform
import subprocess
import threading
from typing import Optional, Tuple

import manuf
import pyttsx3
from rich.console import Console
from scapy.all import RadioTap
from scapy.layers.dot11 import Dot11Elt

# Initialize vendor lookup database
try:
    _vendor_parser = manuf.MacParser("manuf.txt")
except FileNotFoundError:
    _vendor_parser = None



class Utilities:
    """General utility functions for the application."""

    @staticmethod
    def get_vendor(mac: str) -> Optional[str]:
        """Get vendor name from MAC address.

        Args:
            mac: MAC address string (e.g., "00:11:22:33:44:55")

        Returns:
            Vendor name if found, None otherwise
        """
        if not _vendor_parser:
            return None

        try:
            return _vendor_parser.get_manuf_long(mac=mac)
        except Exception:
            return None

    @staticmethod
    def tts(text: str, lock: Optional[threading.Lock] = None,
            voice_rate: int = 20, voice_index: Optional[int] = None) -> None:
        """Text-to-speech output using system TTS engine.

        Args:
            text: Text to speak
            lock: Optional threading lock for thread-safe operation
            voice_rate: Speed reduction from default rate
            voice_index: Optional voice index to use
        """
        if not Utilities.get_os(windows=True):
            return

        try:
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            voices = engine.getProperty('voices')

            engine.setProperty('rate', rate - voice_rate)

            if voice_index is not None and 0 <= voice_index < len(voices):
                engine.setProperty('voice', voices[voice_index].id)
            elif len(voices) > 1:
                engine.setProperty('voice', voices[1].id)

            if lock:
                with lock:
                    engine.say(text)
                    engine.runAndWait()
            else:
                engine.say(text)
                engine.runAndWait()

        except Exception:
            pass

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_os(windows: bool = False, linux: bool = False) -> bool:
        """Check the operating system.

        Args:
            windows: Return True if Windows
            linux: Return True if Linux

        Returns:
            Boolean result based on requested OS check
        """
        system = platform.system().lower()

        if windows:
            return system == "windows"
        if linux:
            return system == "linux"

        return system

    


class NetworkUtilities:
    """Network-related utility functions for WiFi operations."""

    CIPHER_TYPES = {
        0: "None",
        1: "WEP",
        2: "TKIP",
        3: "AES",
        4: "Unknown"
    }

    ENCRYPTION_TYPES = {
        0: "Open",
        1: "WPA",
        2: "WPA-PSK",
        3: "WPA2",
        4: "WPA2-PSK",
        5: "Unknown",
        6: "WPA3",
        7: "WPA3-SAE"
    }

    @staticmethod
    def get_cipher(cipher: int) -> str:
        """Get cipher type name from cipher code."""
        return NetworkUtilities.CIPHER_TYPES.get(cipher, "Unknown")

    @staticmethod
    def get_encryption(akm: int) -> str:
        """Get encryption type name from AKM code."""
        return NetworkUtilities.ENCRYPTION_TYPES.get(akm, "Unknown")

    @staticmethod
    def get_frequency(frequency: int) -> str:
        """Get frequency band from frequency value."""
        if 2400000 <= frequency < 2500000:
            return "2.4 GHz"
        elif 5000000 <= frequency < 5800000:
            return "5 GHz"
        elif 5900000 <= frequency < 7200000:
            return "6 GHz"
        return f"{frequency} Hz"

    @staticmethod
    def get_channel(freq: int) -> Optional[int]:
        """Get WiFi channel number from frequency."""
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
    def get_rssi(pkt, format: bool = False) -> Optional[str]:
        """Extract RSSI (signal strength) from packet.

        Args:
            pkt: Scapy packet with RadioTap layer
            format: If True, return formatted string with units

        Returns:
            RSSI value as string if found, None otherwise
        """
        if not pkt.haslayer(RadioTap):
            return None

        rssi = getattr(pkt, "dBm_AntSignal", None)

        if rssi is None:
            return None

        return f"{rssi} dBm" if format else rssi




class BackgroundThreads:
    """Manages background thread operations for channel hopping."""

    hop = True
    channel = 0
    

    @staticmethod
    def _freq_to_channel(freq):
        # 2.4 GHz band
        if 2412 <= freq <= 2484:
            return (freq - 2407) // 5
        # 5 GHz band (partial support)
        elif 5180 <= freq <= 5825:
            return (freq - 5000) // 5
        # 6 GHz and others can be added as needed
        return None

        
    @staticmethod
    def _get_channel_from_radiotap(pkt):
        if pkt.haslayer(RadioTap):
            try:
                freq = pkt[RadioTap].ChannelFrequency
                if freq:
                    return Background_Threads._freq_to_channel(freq)
            except:
                pass
        return None




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


            channel = Background_Threads._get_channel_from_radiotap(pkt=pkt)
            #console.print(channel); return channel

        return channel

    

    @classmethod
    def get_freq(cls, freq):
        """This will return frequency"""


        if freq in range(2412, 2472): return "2.4 GHz"
        elif freq in range(5180, 5825): return "5 GHz"
        else: return "6 GHz"



    @classmethod
    def get_encryption(cls, pkt):
        """Get this encryption"""







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


                cls.hop = False; time.sleep(2)


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












# Backward compatibility aliases
NetTilities = NetworkUtilities
Background_Threads = BackgroundThreads


if __name__ == "__main__":
    print("NetCracker Utilities Module")
    print("Use 'from nsm_utilities import Utilities, NetworkUtilities' to import")