#!/bin/bash
# Evil Twin DHCP Debug Script

echo "=== Checking if dnsmasq is running ==="
ps aux | grep dnsmasq | grep -v grep

echo -e "\n=== Checking interface configuration ==="
ip addr show wlan0

echo -e "\n=== Checking IP forwarding ==="
sysctl net.ipv4.ip_forward

echo -e "\n=== Checking iptables rules ==="
sudo iptables -L -v -n | grep -E "67|68|DHCP"

echo -e "\n=== Checking if port 67 is listening ==="
sudo netstat -ulnp | grep :67

echo -e "\n=== Watching for DHCP traffic (press Ctrl+C after 10 seconds) ==="
sudo tcpdump -i wlan0 -vv port 67 or port 68
