# WIFI SCANNER  // DEAUTH MODULE // THIS WILL HOLD MALICIOUS LOGIC MEANT FOR ETHICAL REASONS


# UI IMPORTS
import pywifi.iface
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()

# NETWORK IMPORTS
import pywifi, socket, ipaddress
from scapy.all import sniff, Dot11



# ETC IMPORTS 
import threading, os, random, time, pyttsx3

    
# THINGS TO STUDY FOR MATH ASVAB 
MATH = ["percentage", "algebra", "PEMDAS", "Area & Distance", "regular to fraction", "factor equations", "angle of triangle", "area and volume"]


for m in MATH:
    console.print(m)

class Deauth_You():
    """This module will be responsible for crafting and sending deauth packets"""

    def __init__(self):
        pass

    
    @classmethod
    def packet(cls, target_ap, target_mac):
        "This method is responsible for crafting the actual deauth packets"

        
        # YOUR MONITOR MODE INTERFACE
        iface = 'wlan1mon'
        

        # BSSID
        target_ap   # AP'S MAC ADDRESS
        target_mac   # VICTIM / TARGET MAC ADDRESS 


        # CRAFT DEAUTH PACKETS
       # deauth = Radiotap()/\
            #     Dot11()

        



#help(scapy.all)
