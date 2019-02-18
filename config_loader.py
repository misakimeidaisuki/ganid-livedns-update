import os
import sys
import json
import configparser

class configLoader(object):

    def __init__(self, logger, filename = "setting.conf"):

        self.__logger = logger

        self.__config = configparser.ConfigParser()
        self.__config.optionxform = str

        self.__path = os.path.dirname(os.path.realpath(__file__))
        self.__config_fullpath = os.path.join(self.__path, filename)
        self.__config_filename = filename

        self.config_load()

    def config_load(self):
        try:
            if not self.__config.read(self.__config_fullpath):
                self.__logger.info("Configure file \"%s\" is not exist! Creating default file." % self.__config_filename)
                self.__config__init()
                self.config_save()
                self.__logger.info("Configure file \"%s\" has been create, please modify and restart" % self.__config_filename)

                sys.exit(0)
        except configparser.Error:
            self.__logger.warning("Configure file parser error.")
            sys.exit(2)
        #do some config checks,now only return true
        return True

    def config_save(self):
        with open(self.__config_fullpath, 'w') as config_file:
            self.__config.write(config_file)

    @property
    def gandi_api(self):
        url = "https://dns.api.gandi.net/api/v5/"
        try:
            return self.__config['setting'].get("API_url", url)
        except KeyError:
            return url

    @property
    def gandi_api_key(self):
        key = "your_api_key"
        try:
            return self.__config['setting'].get("API_Key", key)
        except KeyError:
            return key

    @property
    def IPv4_address_api(self):
        url =  "https://api.ipify.org"
        try:
            return self.__config['setting'].get("IPv4_address_api", url)
        except KeyError:
            return url

    @property
    def IPv6_address_api(self):
        url = "http://v6.ipv6-test.com/api/myip.php"
        try:
            return self.__config['setting'].get("IPv6_address_api", url)
        except KeyError:
            return url

    def domain_list(self):
        list = self.__config.sections()
        try:
            list.remove("setting")
            return list
        except ValueError:
            self.__logger.warning("domain_list occur ValueError, myabe config cannot load correctly.")
            return list

    def get_domain_A(self, domain):
        if domain in self.__config:
            return self.__config[domain].get("A")

    def get_domain_AAAA(self, domain):
        if domain in self.__config:
            return self.__config[domain].get("AAAA")

    def __config__init(self):
        self.__config['setting'] = {
            'API_url': self.gandi_api,
            'API_Key': self.gandi_api_key,
            'IPv4_address_api': self.IPv4_address_api,
            'IPv6_address_api': self.IPv6_address_api
            }
        self.__config['example.com'] = {
            'A': json.dumps({"@": 300,
                  "www": 300}),
            'AAAA': json.dumps({"@": 300,
                  "www": 300})
            }
