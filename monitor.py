# Joshua Solo, 5/11/2022, 1:02 AM
# :
import requests
import secrets
import threading
import discord
import time
import os
import random
from colorama import Fore
from discord import Webhook, RequestsWebhookAdapter
from threading import Lock
from user_agent import generate_user_agent
from queue import Queue

class Clear:
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{Fore.BLUE}
                                                          
                                                          
  .--.--.    ,--,                    ____                 
 /  /    '.,--.'|    ,--,          ,'  , `.               
|  :  /`. /|  | :  ,--.'|       ,-+-,.' _ |               
;  |  |--` :  : '  |  |,     ,-+-. ;   , ||               
|  :  ;_   |  ' |  `--'_    ,--.'|'   |  ||,---.          
 \  \    `.'  | |  ,' ,'|  |   |  ,', |  |/     \         
  `----.   |  | :  '  | |  |   | /  | |--/    /  |        
  __ \  \  '  : |__|  | :  |   : |  | , .    ' / |        
 /  /`--'  |  | '.''  : |__|   : |  |/  '   ;   /|        
'--'.     /;  :    |  | '.'|   | |`-'   '   |  / |        
  `--'---' |  ,   /;  :    |   ;/       |   :    |        
            ---`-' |  ,   /'---'         \   \  /         
                    ---`-'                `----'   

        ~~ ig monitor
                  by joshua 
                        (@ulzi) ~~       
                                                          
    {Fore.RESET}\n""")


class Counter:
    def __init__(self):
        self.attempts = 0
    def start(self):
        self.rs = 1
        while self.attempts==0:
            time.sleep(1)
        while True:
            time.sleep(1)
            self.rs+=1

class Threader:
    def __init__(self,num):
        self.num = num
    
    def start(self):
        while len(sessions) > 0 and len(targets) > 0:
            for target in targets:userq.put(target)
            for i in range(self.num):
                t = threading.Thread(target=self.check)
                t.daemon = True
                threads.append(t)
                t.start()
            for i in threads:i.join()
            Log().update()
    
    def check(self):
        while userq.qsize() >0:
            usr = str(userq.get())
            Monitor(usr).check()


class Log:
    def __init__(self):
        pass 

    def update(self):
        global pr,sessions,targets
        with open('proxies.txt','r') as f:pr = f.read().splitlines();f.close()
        with open('sessions.txt','r') as f:sessions = f.read().splitlines();f.close()
        with open('targets.txt','r') as f:targets = f.read().splitlines();f.close()

    def claim(self,target,email,idd):
        with open('claimed.txt','a') as f:
            f.write(f'{target}:{email}:{idd}\n')
        self.delete(idd=idd)
        
    def delete(self,idd=None, target=None):
        with open('sessions.txt','r') as f:sessions = f.read().splitlines();f.close()
        with open('sessions.txt','w') as f:
            for i in sessions:
                if i != idd:
                    f.write(f'{i}\n')
        if target:
            with open('targets.txt','r') as f:targets = f.read().splitlines();f.close()
            with open('targets.txt','w') as f:
                for i in targets:
                    if i != target:
                        f.write(f'{i}\n')
        self.update()


class Monitor:
    def __init__(self, usr):
        self.r = requests.session()
        self.username = usr.lower()
        self.url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
        self.green = Fore.LIGHTGREEN_EX
        self.yellow = Fore.YELLOW
        self.reset = Fore.RESET
        self.webhook = "" # Webhook here :)
        
    def sprint(self,*a, **b):
        with lock:
            print(*a, **b)

    def check(self):
        head = {"method": "POST", "X-CSRFToken":"missing", "Referer": "https://www.instagram.com/accounts/web_create_ajax/", "X-Requested-With":"XMLHttpRequest","path":"/accounts/web_create_ajax/", "accept": "*/*", "ContentType": "application/x-www-form-urlencoded", "mid":secrets.token_hex(8)*2,"csrftoken":"missing","rur":"FTW","user-agent":generate_user_agent()}
        data = { 'email': "", 'password': "", "username": self.username, "first_name": "Slatt", "opt_into_one_tap": "false" }
        prox = random.choice(pr)
        self.r.proxies = {'http': 'http://' + prox, 'https': 'http://' + prox}  
        while True:
            try:response = self.r.post(self.url, headers=head,data=data);break
            except:pass
        if not response.text.__contains__("username_is_taken") and not response.text.__contains__("username_held_by_others") and response.status_code==200:self.claim()
        else:counter.attempts+=1;self.sprint(f'\r[{self.yellow}-{self.reset}] Attempts : {counter.attempts}{self.reset} | R/s : {round(counter.attempts/counter.rs)} | User : {self.username} ', end='',flush=True)

    def claim(self):
        self.sprint(f'\r[{self.yellow}-{self.reset}] Trying to claim == > {self.username}\n');
        for session in sessions:
            if self.apipost(session) and self.save(session):return
        self.disFail(self.username)
        Log().delete(target=self.username)
        

    def save(self,idd):
        headers = {'user-agent': 'Instagram 85.0.0.21.100 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)', 'content-type': 'application/x-www-form-urlencoded', 'cookie': f'sessionid={idd.rstrip()}' }
        x = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true",headers=headers)
        if not x.status_code == 200 :return False
        self.sprint(f'\n[{self.green}+{self.reset}] Successfully Claimed >> @{self.username} | Attempt #{counter.attempts}');
        self.email = x.json()["user"]["email"]
        Log().claim(self.username,self.email,idd)
        return True

    def disClaim(self, page):
        try:
            webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
            e = discord.Embed(title=f"Slatt! Slatt! New Claim: {page}",  url=f"https://instagram.com/{page}", color=discord.Color.random())
            e.add_field(name=f"**Attempts**: **{counter.attempts}**", value="-")
            e.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Edit_4x_rifle_scope.jpg/1200px-Edit_4x_rifle_scope.jpg')
            webhook.send(username="Slimy Sniper",avatar_url='https://i5.tagstat.com/p1/p/YZamH7Dm8hVTyN-tD-HkY3PfBe0G9BXQ3AbEal36pKKY6WbTwgoWlSf5lV4xN7Ua.png',embed=e)
        except Exception as e:
            print(e)

    def disFail(self, page):
        try:
            webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
            e = discord.Embed(title=f"Failed to Claim: {page}",  url=f"https://instagram.com/{page}", color=discord.Color.random())
            e.add_field(name=f"**Attempts**: **{counter.attempts}**", value="-")
            e.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Edit_4x_rifle_scope.jpg/1200px-Edit_4x_rifle_scope.jpg')
            webhook.send(username="Slimy Sniper",avatar_url='https://i5.tagstat.com/p1/p/YZamH7Dm8hVTyN-tD-HkY3PfBe0G9BXQ3AbEal36pKKY6WbTwgoWlSf5lV4xN7Ua.png',embed=e)
        except Exception as e:
            print(e)

    def apipost(self,idd):
        while True:
            r = requests.session()
            headers = { 'user-agent': 'Instagram 85.0.0.21.100 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)', 'content-type': 'application/x-www-form-urlencoded', 'cookie': f'sessionid={idd.rstrip()}' }
            data = {'username':self.username,}
            try:return r.post('https://i.instagram.com/api/v1/accounts/set_username/',headers=headers,data=data).status_code==200
            except Exception as e:self.sprint(e)
    



if __name__ == "__main__":
    threads = []
    counter = Counter()
    userq = Queue()
    lock = Lock()
    Clear().clear()
    Log().update()
    count = int(input(f"{Fore.MAGENTA}[+]{Fore.RESET} Enter Amount of Threads: "))
    t=threading.Thread(target=counter.start)
    t.daemon = True
    t.start()
    Threader(count).start()
    if len(sessions) == 0:input(f'\n[{Fore.RED}!{Fore.RESET}] You are out of sessions!')
    if len(targets) == 0:input(f'\n[{Fore.RED}!{Fore.RESET}] You are out of targets!')

# Joshua Solo 5/11/2022 3:00 AM