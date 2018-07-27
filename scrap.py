
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

    def __init__(self, b):
        if b:
            self.getCredentials()
        else:
            self.updateCredentials()

    def help(self):
        print('***COMANDOS:***')
        print(' - changeuser/cu -> Changes the user of MyAnimeList.net')
        print(' - increase/inc <num> -> Increases by one your current cap of that anime')

    def getCredentials(self):
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

ScriptTX = AnimeTX(True)

while(1):
    time.sleep(5)

