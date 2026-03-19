# USE THIS MODULE TO CHANGE WIFI MODE


# IMPORTS
import argparse, os, subprocess




class Mode():
    """This class will be used to change iface with ease"""



    @staticmethod
    def get_args():
        """Get arguments"""


 
        parser = argparse.ArgumentParser(description="quicky way to change type mode")
        parser.add_argument("-i", required=True, help="enter iface")
        parser.add_argument("-r", required=False, action="store_true", help="choose mode")

        args = parser.parse_args()

        iface = args.i
        mode = "managed" if args.r else "monitor"
        
        return iface, mode
    

    @staticmethod
    def change_mode(iface, mode):
        """Change mode"""

        # No shell=True here, that's how you get command injection'd lol
        subprocess.run(["sudo", "ip", "link", "set", iface, "down"])
        subprocess.run(["sudo", "iw", "dev", iface, "set", "type", mode])
        subprocess.run(["sudo", "ip", "link", "set", iface, "up"])
        subprocess.run(["iwconfig"])
    


    @staticmethod
    def main():
        "run shit"


        iface, mode = Mode.get_args()
        Mode.change_mode(iface=iface, mode=mode)
    



if __name__ == "__main__":
    Mode.main()