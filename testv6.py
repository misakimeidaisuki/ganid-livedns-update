import ipaddress
import requests
import sys
import os


def main():
    r = requests.get("https://api.ipify.org")
    print(r.text)

    pass



main()
