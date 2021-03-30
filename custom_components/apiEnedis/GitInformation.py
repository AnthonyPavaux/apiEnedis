import logging

import urllib, json

_LOGGER = logging.getLogger(__name__)

class gitInformation:
    def __init__(self, repo):
        self._serverName = "https://api.github.com/repos/%s/releases/latest" %(repo)
        self._gitData = None

    def getInformation(self):
        from urllib.request import urlopen
        myURL = urlopen(self._serverName)
        s = myURL.read()
        dataAnswer = json.loads(s)
        self._gitData = dataAnswer

    def getVersion(self):
        return self._gitData.get("tag_name", "")