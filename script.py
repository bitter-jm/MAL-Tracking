
### -------------- LIBRARIES -------------- ###

import json
import difflib
import requests
from lxml import html
from bs4 import BeautifulSoup
import time
import os
import sys
from colorama import init, Fore, Back, Style

### --------------- CLASS ----------------- ###

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
    def help():
        print('\n' + Style.BRIGHT +'**COMMANDS**' + Style.RESET_ALL)
        print(' - help/h -> Prints all commands')
        print(' - changeuser/cu -> Changes the user of MyAnimeList.net')
        print(' - list/l -> Lists all watching animes')
        print(' - increase/i <num> -> Increases by one your current cap of anime<num>')
        print(' - update/u <num> <ep> -> Updates the current episode of anime<num> to <ep>')
        print(' - quit/q -> Ends the process')
        

    def getCredentials(self):
        if (not os.path.exists('credentials')):
            fp = open('credentials', 'w+', encoding="utf-8")
            self.updateCredentials()
            fp.close()
        else:
            with open('credentials', 'r', encoding="utf-8") as fp:
                self.user = fp.readline().replace('\n','')
                self.password = fp.readline().replace('\n','')

    def updateCredentials(self):
        self.user = input("Enter 'MyAnimeList.net' username: ")
        self.password = input("Enter password: ")
        with open('credentials', 'w+', encoding="utf-8") as fp:
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
        if '4' in str(loginPage.status_code):
            errlog.write('Failed to open page. The server is refusing the connection. RETRYING...\n\n')
            time.sleep(self.delay)
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
        page = None
        status = ''
        while status != '200':
            errlog.write('HTTP GET -> MAL watching list...\n')
            page = self.session.get('https://myanimelist.net/animelist/{}?status=1'.format(self.user))
            status = str(page.status_code)
            errlog.write(" - status code: " + status + '\n\n')

        items = page.text.split('data-items="[')[1].split(']">')[0].replace('&quot;', '"').split('},{')
        if len(items) >= 2:
            items[0] = items[0] + '}'
            items[len(items)-1] = '{' + items[len(items)-1]
        if len(items) >= 3:
            for i in range(1,len(items)-1):
                items[i] = '{' + items[i] + '}'
        for item in items:
            self.animesMAL.append(json.loads(item))
        
    def updateAnimeMAL(self, num, cap = 0, inc = False):
        payload = ''
        if (inc == False):
            payload = '{\"num_watched_episodes\":' + str(cap) + ',\"anime_id\":' + str(self.animesMAL[num]['anime_id']) + ',\"status\":1,\"csrf_token\":\"' + self.csrf_token + '\"}'
        else:
            payload = '{\"num_watched_episodes\":' + str(int(self.animesMAL['num_watched_episodes'])+1) + ',\"anime_id\":' + str(self.animesMAL[num]['anime_id']) + ',\"status\":1,\"csrf_token\":\"' + self.csrf_token + '\"}'

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
                
                status = ''
                page = None
                while status != '200':
                    errlog.write("HTTP GET -> {} FLV list\n".format(rawName))
                    page = self.session.get('https://animeflv.net/browse?q={}'.format(formatedName))
                    status = str(page.status_code)
                    errlog.write(" - status code: " + status + '\n\n')

                soup = BeautifulSoup(page.text, 'lxml')
                entries = soup.find_all('article', {'class': 'Anime'})

                ratio = 0
                url = ''
                for entry in entries:
                    tempUrl = entry.a['href']
                    tempName = entry.a.h3.text
                    if ratio < difflib.SequenceMatcher(None, rawName, tempName).ratio():
                        ratio = difflib.SequenceMatcher(None, rawName, tempName).ratio()
                        url = tempUrl
                url = 'https://animeflv.net' + url
                
                page = self.session.get(url)
                content = page.text
                try:
                    episodes = content.split('var episodes = [[')
                    self.lastEpisodes.append(episodes[1].split(',')[0])
                    animeInfo = content.split('var anime_info = [')[1].split(']')[0].split(',')
                    animeDate = 'Finished'
                    if len(animeInfo) == 4:
                        animeDate = animeInfo[3].replace('"','')
                    self.dateNextCap.append(animeDate)
                except:
                    self.lastEpisodes.append('Error')
                    self.dateNextCap.append('Error')

    def listAnimes(self):
        print('\n' + Style.BRIGHT +'**ANIME LIST**' + Style.RESET_ALL)
        print(Style.BRIGHT + 'NUM: ' + Fore.GREEN + 'TITLE' + Fore.WHITE + ' --> ' + Fore.CYAN + 'NEXT EPISODE ' + Fore.WHITE + '--> ' + Fore.MAGENTA + 'WATCHED:LAST' + Fore.RESET + Style.RESET_ALL)
        for i in range(0,len(self.animesMAL)):
            newEps = ''
            if int(self.animesMAL[i]['num_watched_episodes']) < int(self.lastEpisodes[i]) and self.dateNextCap[i] != 'Finished':
                newEps = 'New Episodes!'
            print("  " + str(i) + ": " + Fore.GREEN + str(self.animesMAL[i]['anime_title']) + Fore.WHITE + "  -->  " + Fore.CYAN + str(self.dateNextCap[i]) + Fore.WHITE 
            + "  -->  " + Fore.MAGENTA + str(self.animesMAL[i]['num_watched_episodes']) + ":" + str(self.lastEpisodes[i]) + Fore.RED + "  " + newEps + Fore.WHITE)
        print()

### -------------- EXECUTION -------------- ###

if __name__ == '__main__':

    errlog = open("debuglog.txt", 'w+', encoding="utf-8")
    init(convert=True) #Initialize colorama
    ScriptTX = AnimeTX(True)
    AnimeTX.help()
    ScriptTX.listAnimes()

    while(1):
        op = input()
        lop = op.split()
        if len(lop) > 0:
            if (lop[0] == 'exit' or lop[0] == 'quit' or lop[0] == 'q' or lop[0] == 'e'):
                errlog.close()
                exit()
            elif (lop[0] == 'update' or lop[0] == 'u'):
                ScriptTX.updateAnimeMAL(int(lop[1]), int(lop[2]))
            elif (lop[0] == 'increase' or lop[0] == 'i'):
                ScriptTX.updateAnimeMAL(int(lop[1]), inc = True)
            elif (lop[0] == 'list' or lop[0] == 'l'):
                ScriptTX.listAnimes()
            elif (lop[0] == 'help' or lop[0] == 'h'):
                AnimeTX.help()
            elif (lop[0] == 'changeuser' or lop[0] == 'cu'):
                ScriptTX = AnimeTX(False)
                AnimeTX.help()
                ScriptTX.listAnimes()
            else:
                print("instrucción no encontrada.")

