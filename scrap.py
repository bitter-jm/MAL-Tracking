
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
    status = None

    def __init__(self, b):
        if b:
            self.getCredentials()
        else:
            self.updateCredentials()

        self.status = self.loginMAL()
        while (self.status == -1):
            self.updateCredentials()
            self.session = requests.Session()
            self.status = self.loginMAL()
        if self.status == -2:
            time.sleep(5)
            exit(1)  

        self.getAnimesMAL()

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

        errlog.write('HTTP GET -> MAL loggin page...\n')
        loginPage = self.session.get('https://myanimelist.net/login.php')
        errlog.write(" - status code: " + str(loginPage.status_code) + '\n')
        
        errlog.write('Parsing CSRF token...\n')
        tree = html.fromstring(loginPage.text)
        payload['csrf_token'] = list(set(tree.xpath("//meta[@name='csrf_token']/@content")))[0]
        errlog.write(' - token :' + payload['csrf_token'] + '\n')
        del tree
        del loginPage
        time.sleep(0.5)

        errlog.write('HTTP POST -> MAL loggin...\n')
        page = self.session.post('https://myanimelist.net/login.php', data = payload, headers = dict(referer='https://myanimelist.net/login.php'))
        errlog.write(" - status code: " + str(page.status_code) + '\n')
        errlog.write(" - url: " + page.url + '\n')
        if page.url != 'https://myanimelist.net/' and page.url != 'http://myanimelist.net/' :
            if '40' in str(page.status_code):
                print('Failed to login. The server is refusing the connection.\nTry it again in 1 min.')
                errlog.write('Failed to login. The server is refusing the connection.\n\n')
                return -2
            else:
                print('Failed to login. Your credentials may be wrong.')
                errlog.write('Failed to login. Your credentials may be wrong.\n\n')
                return -1

        print('Logged in.')
        errlog.write('Logged in.\n\n')
        time.sleep(0.5)
        return 0

    def getAnimesMAL(self):
        errlog.write('HTTP GET -> MAL watching list...\n')
        page = self.session.get('https://myanimelist.net/animelist/{}?status=1'.format(self.user))
        errlog.write(" - status code: " + str(page.status_code) + '\n')

        items = page.text.split('data-items="[')[1].split(']">')[0].replace('&quot;', '"').split('},{')
        if len(items) >= 2:
            items[0] = items[0] + '}'
            items[len(items)-1] = '{' + items[len(items)-1]
        if len(items) >= 3:
            for i in range(1,len(items)-1):
                items[i] = '{' + items[i] + '}'
        for item in items:
            self.animesMAL.append(json.loads(item))




































    def getLastEpFLV(self):
        pass

    def updateAnimeMAL(self):
        pass

    def listAnimes(self):
        pass


### -------------- EXECUTION -------------- ###

errlog = open("debuglog.txt", 'w+')
ScriptTX = AnimeTX(True)

#while(1):
#    pass

errlog.close()