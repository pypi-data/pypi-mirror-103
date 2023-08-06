from yaml import safe_load
from .blocklist import Blocklist

class Configuration:

    def __init__(self, location):
        self.__location = location
        with open(location) as file:
            data = safe_load(file)
        self.repo_path = data["repository"]["path"]
        self.dnsmasq_path = data["dnsmasq"]["path"]
        self.blocklists = []
        for blocklist in data["blocklists"]:
            self.blocklists.append(Blocklist(blocklist["name"], blocklist["url"]))
        # TODO handle the configuration here