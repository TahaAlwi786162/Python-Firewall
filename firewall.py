from scapy.all import sniff, IP
import subprocess
from datetime import datetime

# example ips - swap these for your own network's ips when testing
# use ipconfig to find your own laptop ip and router ip
blocked_ips = {
    "192.168.1.100": "block",
}

# ips that should NEVER get blocked, even if added to blocked_ips by mistake
# main use case: your own router, so you dont accidentally lock yourself off your network
safe_list = {
    "192.168.1.1",  # replace with your actual router ip
}

already_blocked = set()  # keeps track so we dont keep re-adding the same firewall rule

LOG_FILE = "firewall_log.txt"


def log_event(message):
    # writes every important event to a file with a timestamp
    # this is what turns "some prints in a terminal" into actual evidence for a writeup
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def block_ip(ip):
    if ip in safe_list:
        # extra safety net - never actually block something on the safe list
        print(f"skipped blocking {ip}, its on the safe list")
        log_event(f"SKIPPED blocking {ip} (protected by safe_list)")
        return

    if ip in already_blocked:
        return  # already added this rule this run, dont spam netsh

    print(f"blocking {ip} for real now...")

    result = subprocess.run([
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name=Block_{ip}",
        "dir=in",
        "action=block",
        f"remoteip={ip}"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        log_event(f"BLOCKED {ip} (rule added successfully)")
    else:
        log_event(f"FAILED to block {ip} - stderr: {result.stderr.strip()}")

    print("Return code:", result.returncode)

    already_blocked.add(ip)


def check_ip(ip):
    for bad_ip in blocked_ips:
        if ip == bad_ip:
            return "block"
    return "allow"


def handle_packet(packet):
    if packet.haslayer(IP):
        source = packet[IP].src
        destination = packet[IP].dst

        result = check_ip(source)
        print("from:", source, "to:", destination, "-->", result)

        if result == "block":
            log_event(f"DETECTED blocked ip {source} -> {destination}")
            block_ip(source)


print("starting sniffer, ctrl+c to stop")
log_event("sniffer started")
sniff(filter="ip", prn=handle_packet, store=False)
