
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
        self.loginMAL()

    @staticmethod
    def help(self):
        print('***COMANDOS:***')
        print(' - changeuser/cu -> Changes the user of MyAnimeList.net')
        print(' - increase/inc <num> -> Increases by one your current cap of that anime')

    def getCredentials(self):
        if (not os.path.exists('credentials')):
            fp = open('credentials', 'w+')
            self.updateCredentials()
            fp.close()
        else:
            with open('credentials', 'r') as fp:
                self.user = fp.readline().replace('\n','')
                self.password = fp.readline().replace('\n','')

    def updateCredentials(self):
        self.user = input("Enter 'MyAnimeList.net' username: ")
        self.password = input("Enter password: ")
        with open('credentials', 'w+') as fp:
                fp.write(self.user + '\n')
                fp.write(self.password + '\n')
        


































    def loginMAL(self):
        payload = {
            'user_name': self.user,
            'password': self.password,
            #'cookie': 1,
            'sublogin': 'Login',
            'submit': 1,
            'csrf_token': ''
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

#while(1):
#    time.sleep(5)

