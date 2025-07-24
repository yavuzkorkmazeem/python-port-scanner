#!/bin/python
import ipaddress
import socket
from datetime import datetime as dt
import sys
from concurrent.futures import ThreadPoolExecutor


ip_list = []
a = 1

banner = """
Welcome to the port scanner!
This tool scans the provided IP addresses for open ports.
"""
print(banner+"\n")
print("the ip's that you will enter will be scanned for open ports press enter to stop entering ip's")

while True:
    if a%100 >= 10 and a%100 <= 20:
        th = "th"
    elif a%10 == 1:
        th = "st"
    elif a%10 == 2:
        th = "nd"
    elif a%10 == 3:
        th = "rd"
    else:
        th = "th"
    ip = input("Enter your {a}{th} IP address:".format(a=a,th=th)).strip()
    if ip == "":
        break
    ip_list.append(ip)
    a += 1

def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"port {port} is open on {ip}")
            s.close()
    except socket.gaierror:
        print(f"DNS resolution error for IP: {ip}")
    except socket.timeout:
         print(f"Connection to {ip} timed out.")
    except OSError:
        print(f"OS error occurred while scanning {ip}.")

with ThreadPoolExecutor(max_workers=50) as executor:
    for ip in ip_list:
        if not is_valid_ip(ip):
            print(f"Invalid IP address: {ip}")
            continue
        port_start = int(input("first port to scan (default is 1): ").strip())
        port_end = int(input("last port to scan (default is 150): ").strip())
        if port_start < 1 or port_end > 150:
            port_start = 1
            port_end = 150
        print(f"Scanning ports {port_start} to {port_end} on {ip} time : {dt.now()}")
        print("-" * 50)
        for port in range(port_start, port_end + 1):
            executor.submit(scan_port, ip, port)
