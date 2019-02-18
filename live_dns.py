import os
import json
import requests
import ipaddress

class liveDNS(object):
    def __init__(self, config, logger, domain):
        self.__logger = logger
        self.__config = config
        self.__domain = domain

        self.__header = {"Content-Type": "application/json",
                         "X-Api-Key": self.__config.gandi_api_key}


    def __record_query(self, url):
        req = requests.get(url,headers=self.__header)
        if req.status_code == 200:
            return json.loads(req.text)
        if req.status_code == 404:
            return False

    def __record_update(self, url, data):
        req = requests.put(url, headers=self.__header, json=data)
        if req.status_code != 201:
            self.__logger.warning("Cannot update record")
            self.__logger.debug("response status code is %s" % req.status_code)
            self.__logger.debug(req.text)
            return False
        return True


    def A_record_update(self, ipv4, record, ttl):
        url = "%sdomains/%s/records/%s/A" % (self.__config.gandi_api, self.__domain, record)
        req = self.__record_query(url)
        data = {"rrset_ttl": ttl,
                "rrset_values": [ipv4]}
        if not req:
            self.__record_update(url,data)
        else:
            if req['rrset_values'][0] == ipv4 and req['rrset_ttl'] == ttl:
                self.__logger.info("A record: %s does not need to change IP or TTL" % record)
                return False
            else:
                self.__record_update(url,data)

    def AAAA_record_update(self, ipv6, record, ttl):
        url = "%sdomains/%s/records/%s/AAAA" % (self.__config.gandi_api, self.__domain, record)
        req = self.__record_query(url)
        data = {"rrset_ttl": ttl,
                "rrset_values": [ipv6]}
        if not req:
            self.__record_update(url,data)
        else:
            if req['rrset_values'][0] == ipv6 and req['rrset_ttl'] == ttl:
                self.__logger.info("AAAA record: %s does not need to change IP or TTL" % record)
                return False
            else:
                self.__record_update(url,data)

    def records_update(self, update_ip):
        try:
            type = ipaddress.ip_address(update_ip).version
        except ValueError:
            return False

        if type == 4:
            reocrds = json.loads(self.__config.get_domain_A(self.__domain).replace("'", "\"")).items()
            for record,ttl in reocrds:
                self.A_record_update(update_ip, record, ttl)
        elif type == 6:
            records = reocrds = json.loads(self.__config.get_domain_AAAA(self.__domain).replace("'", "\"")).items()
            for record,ttl in records:
                self.AAAA_record_update(update_ip, record, ttl)

        return False
