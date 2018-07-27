
### -------------- LIBRARIES -------------- ###

import json
import requests
from lxml import html
import time
import os
import sys
from colorama import init, Fore, Back, Style

### --------------- OBJECT ---------------- ###

class AnimeTX:
    user = None
    password = None
    session = requests.Session()
    animesMAL = []
    lastEpisodes = []

    def getCredentials(self):
        pass


    def __init__(self):
        self.getCredentials()

    def help(self):
        pass

    def updateCredentials(self):
        pass

    def loginMAL(self):
        payload = {
            "user_name": "",
            "password": "",
            "csrf_token": "",
            "submit": 1,
            "Sublogin": "Login"
        }

    def getAnimesMAL(self):
        pass

    def getLastEpFLV(self):
        pass

    def updateAnimeMAL(self):
        pass

    def listAnimes(self):
        pass


### -------------- EXECUTION -------------- ###

ScriptTX = AnimeTX()

while(1):
    time.sleep(5)

