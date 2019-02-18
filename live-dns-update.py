import sys
import json
import configparser
import ipaddress
import requests
from update_log import updateLog
from config_loader import configLoader
from ip_finder import IPFinder
from live_dns import liveDNS

if __name__ == "__main__":
    logger = updateLog()
    config = configLoader(logger, filename = "nuko.moe.conf")

    ip_finder = IPFinder(config, logger)
    try:
        ipv4 = ip_finder.get_ipv4()
    except:
        ipv4 = False

    try:
        ipv6 = ip_finder.get_ipv6()
    except:
        ipv6 = False

    domains = config.domain_list()

    for domain in domains:
        domain = liveDNS(config, logger, domain)
        if not ipv4:
            continue
        domain.records_update(ipv4)
        if not ipv6:
            continue
        domain.records_update(ipv6)
