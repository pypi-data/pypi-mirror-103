# dnsblock-update
Blocklist Updater for DNSmasq

## Usage

### Installation

Run the following command:
```pip3 install dnsblock_update```

### Configuration

Create a configuration file with the following content:
```yaml
dnsmasq: 
  path: "result.conf"   # Generated DNSMasq configuration
repository:
  path: "./repo/"       # Path to the cache repository used by the updater
blocklists:
  - name: "notracking"                      # name of the blocklist
    url: https://example.com/blacklist.txt  # url of the blocklist
```

### Execution

Create a cronjob:
```
0 2 * * * /usr/bin/python3 -m dnsblock_update /etc/dnsblock_update/config.yml
```
