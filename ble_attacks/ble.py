#!/usr/bin/env python3
import asyncio
import argparse
from bleak import BleakScanner, BleakClient

# Known vulnerable BLE UUIDs (example set)
KNOWN_VULN_UUIDS = {
    "0000fff1-0000-1000-8000-00805f9b34fb": "Tuya Smart Plug – Writable",
    "0000fff2-0000-1000-8000-00805f9b34fb": "Generic BLE Light – RGB Control",
    "0000ffe1-0000-1000-8000-00805f9b34fb": "HM‑10 UART Module – Full Write Access",
}

async def scan_and_check_vuln(timeout: float = 5.0):
    print(f"[*] Scanning for BLE devices for {timeout} seconds...")
    devices = await BleakScanner.discover(timeout=timeout)

    for d in devices:
        rssi = getattr(d, "rssi", "N/A")
        print(f"[+] Device: {d.name or 'Unknown'} | {d.address} | RSSI: {rssi}")

        try:
            async with BleakClient(d) as client:
                if client.is_connected:
                    try:
                        #services = client.services                        
                        await client.get_services()
                        #services = client.services
                    except Exception as svc_err:
                        print(f"    [!] Failed to get services: {svc_err}")
                        continue

                    for service in services:
                        for char in service.characteristics:
                            props = char.properties
                            if "write" in props or "write-without-response" in props:
                                uuid = str(char.uuid).lower()
                                vuln_note = KNOWN_VULN_UUIDS.get(uuid, "")
                                print(f"  [WRITE] {uuid} | props: {props} {'-- VULN: ' + vuln_note if vuln_note else ''}")
                                try:
                                    await client.write_gatt_char(char.uuid, bytearray([0x01]), response=True)
                                    print("    -> Write succeeded.")
                                except Exception as write_err:
                                    print(f"    [!] Write failed: {write_err}")
                else:
                    print(f"[-] Could not stay connected to {d.address}")
        except Exception as conn_err:
            print(f"[-] Could not connect to {d.address}: {conn_err}")

def main():
    parser = argparse.ArgumentParser(description="BLE Recon & Write‑Test Scanner")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="Scan duration in seconds")
    args = parser.parse_args()

    asyncio.run(scan_and_check_vuln(timeout=args.timeout))

if __name__ == "__main__":
    main()

