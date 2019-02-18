import os
import time
import ipaddress
import requests

class IPFinderError(Exception):
    pass

class IPv6FinderError(IPFinderError):
    pass

class IPv4FinderError(IPFinderError):
    pass

class IPFinder(object):

    def __init__(self, config, logger):
        self.__config = config
        self.__logger = logger

    def get_ipv6(self):
        for times in range(3):
            try:
                return self.__get_ip(self.__config.IPv6_address_api)
            except requests.exceptions.ConnectionError:
                self.__logger.warning("Cannot get IPv6 from API.")
                self.__logger.warning("Please check the API URL or IPv6 connectivity.")
                raise IPv6FinderError("Get IPv6 Error")
            except (requests.exceptions.RequestException, IPFinderError) as e:
                self.__logger.warning("Cannot get IPv6 from API, waiting for 30s to retry.")
                self.__logger.debug("Error type: %s" % e.args[-1])
                time.sleep(30)

        self.__logger.warning("Get IPv6 retry timeout!")
        raise IPv6FinderError("Get IPv6 retry timeout!")

    def get_ipv4(self):
        for times in range(3):
            try:
                return self.__get_ip(self.__config.IPv4_address_api)
            except requests.exceptions.ConnectionError:
                self.__logger.warning("Cannot get IPv4 from API.")
                self.__logger.warning("Please check the API URL or IPv4 connectivity.")
                raise IPv4FinderError("Get get_ipv4 Error")
            except (requests.exceptions.RequestException, IPFinderError) as e:
                self.__logger.warning("Cannot get IPv4 from API, waiting for 30s to retry.")
                self.__logger.debug("Error type: %s" % e.args[-1])
                time.sleep(30)

        self.__logger.warning("Get IPv4 retry timeout!")
        raise IPv4FinderError("Get IPv4 retry timeout!")

    def __get_ip(self, api_url):
        req = requests.get(api_url)

        if req.status_code != 200:
            __self.__logger.debug("The http status code is %s" % req.status_code)
            raise IPFinderError("Cannot get IP from the API")

        try:
            ipaddress.ip_address(req.text)
        except ValueError:
            __self.__logger.debug("The ip value is %s" % req.text)
            raise IPFinder("Cannot get the legitimate IP address")

        return req.text
