

# 🛠️ NetCracker

NetCracker is a lightweight but powerful network tool designed to monitor, analyze, and take action in real-time during security assessments.


## ⚙️ Features

### 📡 Monitor Mode Attacks
- **Wardriving** -  WiFi network discovery and mapping
- **Wardriving Stationary Mode** - Discover wireless clients and non-AP devices
- **Deauth Attacks** - Disconnect all clients from target SSID
- **Targeted Deauth** - Disconnect specific clients
- **Client Sniffer** - Monitor and spy on network client traffic
- **Beacon Flood** - Spam fake access points
- **Packet Analysis** - Live metrics and deep packet inspection
- **Device Discovery** - Identify devices and manufacturers

### 🎭 Managed Mode Attacks
- **Evil Twin Attack** - Rogue AP with captive portal for credential harvesting

## 🧪 Tested On
- Kali Linux
- Arch Linux

## 📋 Prerequisites

### System Dependencies
Install required system packages before running NetCracker:

**Arch Linux:**
```bash
sudo pacman -S hostapd dnsmasq
```

**Kali Linux:**
```bash
sudo apt update
sudo apt install hostapd dnsmasq
```

Disable auto-start for these services:
```bash
sudo systemctl stop hostapd dnsmasq
sudo systemctl disable hostapd dnsmasq
```

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/nsm-barii/netcracker.git
   cd netcracker/nsm_modules
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Run NetCracker**
   ```bash
   sudo venv/bin/python nsm_main.py
   ```

## 🔮 Coming Soon
- Router crash frames
- WiFi password cracking (hashcat integration)

---

<img width="1215" height="911" alt="image" src="https://github.com/user-attachments/assets/2ce86603-1fa2-43c7-af7f-7a5213458646" />

> 📸 *Image above shows NetCracker running on a dual-laptop setup using ALFA adapters for extended wireless penetration testing.*

