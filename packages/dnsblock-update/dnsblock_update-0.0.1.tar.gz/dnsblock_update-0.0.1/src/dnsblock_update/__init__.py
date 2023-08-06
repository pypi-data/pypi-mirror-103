import sys
from .blocklist import merge
from .config import Configuration

class DnsblockUpdateApp:

    def __init__(self):
        if len(sys.argv) < 2:
            print("Error: Path to configuration file is missing")
            exit(1)
        if len(sys.argv) > 2:
            print("Error: Too many arguments")
            exit(1)
        config_location = sys.argv[1]
        self.config = Configuration(config_location)
    
    def run(self):
        for blocklist in self.config.blocklists:
            blocklist.load(self.config.repo_path)
        result = merge(self.config.blocklists)
        with open(self.config.dnsmasq_path, "w") as file:
            file.writelines(result)