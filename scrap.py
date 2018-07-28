
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
    dateNextCap = []
    status = None
    csrf_token = None
    delay = 0.3 #Delay between requests

    def __init__(self, b):
        # -1 -> Wrong credentials
        # -2 -> Error code 40X
        # -3 -> Status code 429: 'Too Many requests'
        if b:
            self.getCredentials()
        else:
            self.updateCredentials()

        self.status = self.loginMAL()
        while (self.status == -1 or self.status == -3):
            self.updateCredentials()
            if (self.status == -1):
                self.session = requests.Session()
            else: 
                time.sleep(self.delay)
                self.delay = self.delay+0.2
            self.status = self.loginMAL()
        if self.status == -2:
            time.sleep(5)
            exit(1)  

        self.getAnimesMAL()
        self.getLastEpFLV()

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
        if '429' in str(loginPage.status_code):
            errlog.write('Failed to open page. The server is refusing the connection. RETRYING...\n\n')
            return -3
        
        errlog.write('Parsing CSRF token...\n')
        tree = html.fromstring(loginPage.text)
        self.csrf_token = list(set(tree.xpath("//meta[@name='csrf_token']/@content")))[0]
        payload['csrf_token'] = self.csrf_token
        errlog.write(' - token :' + payload['csrf_token'] + '\n')
        del tree
        del loginPage
        time.sleep(self.delay)

        errlog.write('HTTP POST -> MAL loggin...\n')
        page = self.session.post('https://myanimelist.net/login.php', data = payload, headers = dict(referer='https://myanimelist.net/login.php'))
        errlog.write(" - status code: " + str(page.status_code) + '\n')
        errlog.write(" - url: " + page.url + '\n')
        if page.url != 'https://myanimelist.net/' and page.url != 'http://myanimelist.net/' :
            if '40' in str(page.status_code):
                print('Failed to login. The server is refusing the connection.\nTry it again in 1 min.')
                errlog.write('Failed to login. The server is refusing the connection.\n\n')
                return -2
            elif '429' in str(page.status_code):
                errlog.write('Failed to login. The server is refusing the connection. RETRYING...\n\n')
                return -3
            else:
                print('Failed to login. Your credentials may be wrong.')
                errlog.write('Failed to login. Your credentials may be wrong.\n\n')
                return -1

        print('Logged in.')
        errlog.write('Logged in.\n\n')
        time.sleep(self.delay)
        return 0

    def getAnimesMAL(self):
        errlog.write('HTTP GET -> MAL watching list...\n')
        page = self.session.get('https://myanimelist.net/animelist/{}?status=1'.format(self.user))
        errlog.write(" - status code: " + str(page.status_code) + '\n\n')

        items = page.text.split('data-items="[')[1].split(']">')[0].replace('&quot;', '"').split('},{')
        if len(items) >= 2:
            items[0] = items[0] + '}'
            items[len(items)-1] = '{' + items[len(items)-1]
        if len(items) >= 3:
            for i in range(1,len(items)-1):
                items[i] = '{' + items[i] + '}'
        for item in items:
            self.animesMAL.append(json.loads(item))
        
    def updateAnimeMAL(self, num, cap):
        payload = '{\"num_watched_episodes\":' + str(cap) + ',\"anime_id\":' + str(self.animesMAL[num]['anime_id']) + ',\"status\":1,\"csrf_token\":\"' + self.csrf_token + '\"}'

        headersObj = {
        'referer': 'https://myanimelist.net/animelist/{}?status=1'.format(self.user), 
        'user-agent': 'Mozilla/5.0', 
        'origin': 'https://myanimelist.net',
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*'
        }

        errlog.write('HTTP POST -> Update anime cap...\n')
        page = self.session.post('https://myanimelist.net/ownlist/anime/edit.json', data = payload, headers = headersObj)
        errlog.write(" - status code: " + str(page.status_code) + '\n\n')

        if '4' in str(page.status_code):
            print('An error occurred while trying to update MAL list...')
        else:
            print('Anime updated.')
            self.animesMAL[num]['num_watched_episodes'] = cap



















    def getLastEpFLV(self):
        for anime in self.animesMAL:

            if str(anime['anime_airing_status']) == '2': #FINISHED ANIME
                self.lastEpisodes.append(anime['anime_num_episodes'])
                self.dateNextCap.append('Finished')
            else: #AIRING ANIME

                rawName = anime['anime_title']
                formatedName = ''
                charFilter = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
                aux = ''
                for c in rawName:
                    if c in charFilter:
                        if c != ' ':
                            formatedName = formatedName + c
                            aux = c
                        elif aux != '+':
                            formatedName = formatedName + '+'
                            aux = '+'
                    else:
                        if aux != '+':
                            formatedName = formatedName + '+'
                            aux = '+'
                FLVurl = 'https://animeflv.net/browse?q={}'.format(formatedName)



























    def listAnimes(self):
        pass


### -------------- EXECUTION -------------- ###

errlog = open("debuglog.txt", 'w+')
ScriptTX = AnimeTX(True)

#time.sleep(0.5)
#ScriptTX.updateAnimeMAL(1, 25)

#while(1):
#    pass

errlog.close()
