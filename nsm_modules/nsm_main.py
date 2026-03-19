# WIFI SCANNER  // THIS WILL BE A RED TEAM PROGRAM


class import_handler:
    """This class and module is responsible for running before the official logic of the program is executed, this will therefore make sure each import is on the system to prevent any errors"""

    def __init__(self):

        # UNIVERSAL DEPENDANCIES
        self.libaries = {
            1: "rich",
            2: "scapy",
            3: "socket",
            4: "threading",
            5: "pyfiglet",
            6: "json",
            7: "pathlib",
            8: "pyttsx3",
            9: "random",
            10: "time",
            11: "datetime",
            12: "pywifi",
        }

    def import_installer(self):
        """This will be where we put all our imports used across all program modules"""

        try:
            # UI IMPORTS
            from rich.panel import Panel  # noqa: F401
            from rich.table import Table  # noqa: F401
            from rich.live import Live  # noqa: F401
            from rich.console import Console

            console = Console()

            # NETWORK IMPORTS
            import pywifi  # noqa: F401
            import socket  # noqa: F401
            import ipaddress  # noqa: F401
            from scapy.all import sniff  # noqa: F401

            # ETC IMPORTS
            import threading  # noqa: F401
            import os  # noqa: F401
            import random  # noqa: F401
            import time  # noqa: F401
            import pyttsx3  # noqa: F401
            import pyfiglet  # noqa: F401
            from datetime import datetime  # noqa: F401

            # FILE HANDLING
            import json  # noqa: F401
            import pathlib  # noqa: F401

            # NSM MODULES
            from nsm_logic import WifiUI  # noqa: F401

            # NOW TO BEGIN
            console.print("Module check complete", style="bold green")
            import_handler.main()

        except ImportError as e:
            print(f"Import Error: {e}")

            choice = (
                input("If you want to automatically install libaries type yes: ")
                .strip()
                .lower()
            )

            if choice == "yes" or choice == "y" or choice == "1":
                print("Bet now downloading Dependencies")
                # time.sleep(1)

                # LOOP FOR EXCEPTIONS
                while True:
                    try:
                        # IMPORT SUBPROCESS SO WE CAN INSTALL LIBARIES
                        import subprocess

                        for key, value in self.libaries.items():
                            print(f"Now trying to install: {value}   #{key}/12")
                            subprocess.run(["pip", "install", value])

                        # NOW IMPORT LIBARIES
                        from rich.console import Console
                        import time

                        console = Console()

                        # NOW PRINT SOME CODE
                        console.print("Dependencies now installed.", style="bold blue")
                        console.print("Now Restarting cmd instance", style="bold green")
                        time.sleep(3)

                        # NOW TO BRING BACK TO MAIN MENU
                        from nsm_ui import MainUI

                        MainUI.main()

                    except Exception as e:
                        print(f"Got a Exception error will, continue: {e}")

        except Exception as e:
            print(f"Main Module Error: {e}")

            while True:
                cmd = input("Enter command: ")

                if cmd == "exit":
                    print("later")
                    break

                else:
                    # os.system(cmd) was basically a free shell for anyone lol
                    print(f"Unknown command: {cmd}. Type 'exit' to leave.")

    def import_uninstaller(self):

        print(
            "This is where u come to unistall import\n"
            "Usually for testing the main modules program logic"
        )

        choice = (
            input("Are u sure u want to procceed if so type yes or be returned: ")
            .lower()
            .strip()
        )

        if choice == "y" or choice == "1" or choice == "yes":
            #
            import os

            while True:
                try:
                    for key, value in self.libaries.items():
                        print(f"Now Unistalling: {value}  #{key}")
                        os.system(f"pip uninstall {value}")

                    print("Libaries successfully unistalled")
                    break

                except Exception as e:
                    print(f"Got a Exception error will, continue: {e}")

    @staticmethod
    def main():
        """Multi-module logic will be called from here"""

        from nsm_ui import MainUI

        MainUI.main()


# BEGIN MULTI-MODULE LOGIC
if __name__ == "__main__":
    import_handler().import_installer()
