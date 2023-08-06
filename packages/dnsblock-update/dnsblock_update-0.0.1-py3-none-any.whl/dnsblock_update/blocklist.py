import requests
import re
import os
import json

from typing import List

BLOCKLIST_ENTRY_PATTERN=re.compile(r"address=/[A-z0-9-_.]*/#")

class Blocklist:

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.etag = None
        self.header = ""
        self.entries = []

    def load(self, repository):
        repo_path = os.path.join(repository, self.name+".json")
        if os.path.exists(repo_path):
            self.__load_from_repo(repo_path)
            response=requests.head(self.url)
            etag = response.headers["etag"].replace("\"", "")
            if self.etag != etag:
                print(f"E-Tag mismatch, stored {self.etag}, current {etag}")
                self.header = ""
                self.entries = []
                self.__download(repository)
        else:
            print(f"No existing cache entry was found for {self.name}")
            self.__download(repository)
    
    def __load_from_repo(self, repo_path):
        with open(repo_path) as file:
            data = json.load(file)
        self.etag = data["etag"]
        self.header = data["header"]
        self.entries = data["entries"]

    def __download(self, repository):
        response=requests.get(self.url)
        self.etag = response.headers["etag"].replace("\"", "")
        lines = response.text.splitlines()
        for line in lines:
            if self.__is_ignored(line):
                continue
            if self.__is_header(line):
                self.header += f"{line}\n"
                continue
            if self.__is_entry(line):
                self.__add_entry(line)
                continue
            print(f"Unknown Line Type: {line}\n")
        self.__reinvalidate_cache(repository)

    def __reinvalidate_cache(self, repository):
        repo_path = os.path.join(repository, self.name+".json")
        data = {
            "name": self.name,
            "url": self.url,
            "etag": self.etag,
            "header": self.header,
            "entries": self.entries
        }
        with open(repo_path, "w") as file:
            json.dump(data, file, indent=4)

    def __is_ignored(self, line):
        return line.strip() == ""
    
    def __is_header(self, line):
        return line.startswith("#")

    def __is_entry(self, line):
        return BLOCKLIST_ENTRY_PATTERN.match(line) is not None

    def __add_entry(self, line):
        self.entries.append(line.strip())


def merge(blocklists: List[Blocklist])->List[str]:
    entries = []
    for item in blocklists:
        entries.extend(item.entries)
    lines = []
    for entry in entries:
        lines.append(f"{entry}\n")
    return lines