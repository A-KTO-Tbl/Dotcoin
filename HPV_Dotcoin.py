from requests import post, get
from threading import Thread, Lock
from os import system as sys
from platform import system as s_name
from time import sleep
from random import randint
from colorama import Fore
from typing import Literal
from datetime import datetime, timedelta
from urllib.parse import unquote
from json import loads
from itertools import cycle

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker
from Core.Tools.HPV_User_Agent import HPV_User_Agent

from Core.Config.HPV_Config import *







class HPV_Dotcoin:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Получение бонуса`
    
    [2] - `Улучшение бустов`
        [2.1] - `Попытка улучшить буст 'Multitap' (урон за один тап)`
        
        [2.2] - `Попытка улучшить буст 'Daily Attempts' (максимальная ёмкость энергии)`
    
    [3] - `Улучшение майнинга DTC`
    
    [4] - `Получение кол-ва доступных игр и запуск их прохождения`
    
    [5] - `Просмотр рекламы и отыгрыш полученных игр`
    
    [6] - `Ожидание от 8 до 9 часов`
    
    [7] - `Повторение действий через 8-9 часов`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict) -> None:
        HPV = self.URL_Clean(URL)
        self.Name = Name                      # Ник аккаунта
        self.URL = HPV['URL']                 # Уникальная ссылка для авторизации в mini app
        self.USER_ID = HPV['UID']             # Telegram ID аккаунта
        self.Proxy = Proxy                    # Прокси (при наличии)
        self.UA = HPV_User_Agent()            # Генерация уникального User Agent
        self.Token = self.Authentication()    # Уникальный токен для взаимодействия с mini app



    def URL_Clean(self, _URL: str) -> dict:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            UID = str(loads(unquote(unquote(unquote(_URL))).split('&')[1].split('=')[1])['id'])
            URL = unquote(_URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            return {'UID': UID, 'URL': URL}
        except:
            return {'UID': None, 'URL': None}



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Name: str, Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()     # Текущее время
            Name = Fore.MAGENTA + Name     # Ник аккаунта
            Smile = COLOR + str(Smile)     # Смайлик
            Text = COLOR + Text            # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Authentication(self) -> str:
        '''Аутентификация аккаунта'''

        URL = 'https://jjvnmoyncmcewnuykyid.supabase.co/functions/v1/getToken'
        Headers = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'content-type': 'application/json', 'sec-ch-ua-mobile': '?1', 'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'user-agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'accept': '*/*', 'origin': 'https://dot.dapplab.xyz', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://dot.dapplab.xyz/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
        Json = {'initData': self.URL}

        try:
            Token = post(URL, headers=Headers, json=Json, proxies=self.Proxy).json()['token']
            self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
            return Token
        except:
            self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
            return ''



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        self.Token = self.Authentication()



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и наличии доступных игр'''

        URL = 'https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/get_user_info'
        Headers = {'x-client-info': 'postgrest-js/1.9.2', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'sec-ch-ua-mobile': '?1', 'authorization': f'Bearer {self.Token}', 'user-agent': self.UA, 'content-type': 'application/json', 'content-profile': 'public', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'x-telegram-user-id': self.USER_ID, 'sec-ch-ua-platform': '"Android"', 'accept': '*/*', 'origin': 'https://dot.dapplab.xyz', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://dot.dapplab.xyz/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = post(URL, headers=Headers, json={}, proxies=self.Proxy).json()

            Balance = HPV['balance'] # Текущий баланс
            Plays = HPV['daily_attempts'] # Доступное кол-во игр
            Click_LVL = str(HPV['multiple_clicks']) # Уровень силы клика
            Limit_LVL = str(HPV['limit_attempts'] - 9) # Уровень лимита энергии
            DTC_LVL = HPV['dtc_level'] # Уровень фарма DTC

            return {'Balance': f'{Balance:,}', 'Plays': Plays, 'Click_LVL': Click_LVL, 'Limit_LVL': Limit_LVL, 'DTC_LVL': DTC_LVL}
        except:
            return None



    def Get_DTC_Balance(self) -> int:
        '''Баланс DTC'''

        URL = 'https://api.dotcoin.bot/rest/v1/rpc/get_assets'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'accept-profile': 'public', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://dot.dapplab.xyz', 'priority': 'u=1, i', 'referer': 'https://dot.dapplab.xyz/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': self.UA, 'x-client-info': 'postgrest-js/0.0.0-automated', 'x-telegram-user-id': self.USER_ID}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()

            for TOKEN in HPV:
                if TOKEN['symbol'] == 'DTC':
                    return TOKEN['amount']
        except:
            return 0



    def Play(self) -> None:
        '''Запуск игры'''

        URL = 'https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/save_coins'
        Headers = {'x-client-info': 'postgrest-js/1.9.2', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'sec-ch-ua-mobile': '?1', 'authorization': f'Bearer {self.Token}', 'user-agent': self.UA, 'content-type': 'application/json', 'content-profile': 'public', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'x-telegram-user-id': self.USER_ID, 'sec-ch-ua-platform': '"Android"', 'accept': '*/*', 'origin': 'https://dot.dapplab.xyz', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://dot.dapplab.xyz/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'}
        _COINS = randint(COINS[0], COINS[1]) # Желаемое кол-во получения монет

        try:
            HPV = post(URL, headers=Headers, json={'coins': _COINS}, proxies=self.Proxy).json()['success']

            if HPV:
                self.Logging('Success', self.Name, '🟢', f'Игра сыграна! +{_COINS:,}!')
            else:
                self.Logging('Error', self.Name, '🔴', 'Игра не сыграна!')
        except:
            self.Logging('Error', self.Name, '🔴', 'Игра не сыграна!')



    def DTC_Update(self) -> bool:
        '''Апгрейд DTC майнинга'''

        URL = 'https://api.dotcoin.bot/functions/v1/upgradeDTCMiner'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://dot.dapplab.xyz', 'priority': 'u=1, i', 'referer': 'https://dot.dapplab.xyz/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': self.UA, 'x-telegram-user-id': self.USER_ID}

        try:
            return True if post(URL, headers=Headers, proxies=self.Proxy).json()['success'] == True else False
        except:
            return False



    def Update_Boosts(self, UP_Type: Literal['Click_LVL', 'Limit_LVL']) -> bool:
        '''Обновление бустов'''

        Boosts_LVL = self.Get_Info()
        if UP_Type == 'Click_LVL':
            URL = 'https://api.dotcoin.bot/rest/v1/rpc/add_multitap'
            Data = '{"lvl":' + Boosts_LVL['Click_LVL'] + '}'
        else:
            URL = 'https://api.dotcoin.bot/rest/v1/rpc/add_attempts'
            Data = '{"lvl":' + Boosts_LVL['Limit_LVL'] + '}'
        Headers = {'Host': 'api.dotcoin.bot', 'Content-Length': '9', 'x-client-info': 'postgrest-js/0.0.0-automated', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'sec-ch-ua-mobile': '?1', 'Authorization': f'Bearer {self.Token}', 'User-Agent': self.UA, 'Content-Type': 'application/json', 'Content-Profile': 'public', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'x-telegram-user-id': self.USER_ID, 'sec-ch-ua-platform': '"Android"', 'Accept': '*/*', 'Origin': 'https://dot.dapplab.xyz', 'X-Requested-With': 'org.telegram.plus', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://dot.dapplab.xyz/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            post(URL, headers=Headers, data=Data, proxies=self.Proxy).json()['success']
            return True
        except:
            return False



    def View_Ads(self) -> bool:
        '''Просмотр рекламы для получения дополнительной игры'''

        URL = 'https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/restore_attempt'
        Headers = {'x-client-info': 'postgrest-js/1.9.2', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'sec-ch-ua-mobile': '?1', 'authorization': f'Bearer {self.Token}', 'user-agent': self.UA, 'content-type': 'application/json', 'content-profile': 'public', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'x-telegram-user-id': self.USER_ID, 'sec-ch-ua-platform': '"Android"', 'accept': '*/*', 'origin': 'https://dot.dapplab.xyz', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://dot.dapplab.xyz/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = post(URL, headers=Headers, json={}, proxies=self.Proxy).json()['success']

            if HPV:
                self.Logging('Success', self.Name, '🟢', 'Реклама просмотрена! +1 игра')
                return True
            else:
                self.Logging('Error', self.Name, '🔴', 'Реклама не просмотрена!')
                return False
        except:
            self.Logging('Error', self.Name, '🔴', 'Реклама не просмотрена!')
            return False



    def Claim_Bonus(self) -> None:
        '''Получение бонуса'''

        URL = 'https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/try_your_luck'
        Headers = {'x-client-info': 'postgrest-js/1.9.2', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'sec-ch-ua-mobile': '?1', 'authorization': f'Bearer {self.Token}', 'user-agent': self.UA, 'content-type': 'application/json', 'content-profile': 'public', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8', 'x-telegram-user-id': self.USER_ID, 'sec-ch-ua-platform': '"Android"', 'accept': '*/*', 'origin': 'https://dot.dapplab.xyz', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://dot.dapplab.xyz/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = post(URL, headers=Headers, json={'coins': 150_000}, proxies=self.Proxy).json()['success']

            if HPV:
                self.Logging('Success', self.Name, '🟢', 'Бонус получен! +150,000')
            else:
                self.Logging('Warning', self.Name, '🟡', 'Бонус уже получен!')
        except:
            self.Logging('Error', self.Name, '🔴', 'Бонус не получен!')



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна
                    INFO = self.Get_Info()
                    Balance = INFO['Balance']
                    Get_plays = INFO['Plays']
                    Click_LVL = int(INFO['Click_LVL']) # Уровень силы клика
                    Limit_LVL = int(INFO['Limit_LVL']) # Уровень лимита энергии
                    DTC_LVL = INFO['DTC_LVL'] # Уровень фарма DTC


                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Balance} /// Баланс DTC: {self.Get_DTC_Balance()} /// Уровень DTC: {DTC_LVL}')
                    Changes = 0


                    self.Claim_Bonus() # Получение бонуса


                    # Улучшение буста `Multitap` (урон за один тап)
                    if Click_LVL < MAX_CLICK_LVL:
                        if self.Update_Boosts('Click_LVL'):
                            self.Logging('Success', self.Name, '⚡️', 'Буст `Multitap` улучшен!')
                            Changes += 1 # +1 если буст улучшится
                            sleep(randint(33, 103)) # Промежуточное ожидание

                    # Улучшение буста `Daily Attempts` (максимальная ёмкость энергии)
                    if Limit_LVL < MAX_LIMIT_LVL:
                        if self.Update_Boosts('Limit_LVL'):
                            self.Logging('Success', self.Name, '⚡️', 'Буст `Daily Attempts` улучшен!')
                            Changes += 1 # +1 если буст улучшится
                            sleep(randint(33, 103)) # Промежуточное ожидание


                    # Улучшение майнинга DTC
                    if self.DTC_Update():
                        self.Logging('Success', self.Name, '⚡️', 'Апгрейд майнинга успешен!')
                        Changes += 1 # +1 если буст улучшится
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    # Если произошли какие-либо изменения, апгрейд бустов и/или апгрейд босса
                    if Changes:
                        self.Logging('Success', self.Name, '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')


                    # Получение кол-ва доступных игр и запуск их прохождения
                    if Get_plays > 0:
                        self.Logging('Success', self.Name, '🎮', f'Игр доступно: {Get_plays}!')
                        for _ in range(Get_plays):
                            self.Play()
                            sleep(randint(12, 23))


                    # Просмотр рекламы и отыгрыш полученных игр
                    while True:
                        if self.View_Ads():
                            self.Play()
                            sleep(randint(12, 23))
                        else:
                            break


                    Waiting = randint(29_000, 32_500) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Success', self.Name, '💰', f'Баланс после игр: {self.Get_Info()["Balance"]} /// Баланс DTC: {self.Get_DTC_Balance()} /// Уровень DTC: {self.Get_Info()["DTC_LVL"]}')
                    self.Logging('Warning', self.Name, '⏳', f'Игр больше нет! Следующий старт игр: {Waiting_STR}!')

                    sleep(Waiting) # Ожидание от 8 до 9 часов
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта
            except:
                pass







if __name__ == '__main__':
    sys('cls') if s_name() == 'Windows' else sys('clear')

    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()

    def Start_Thread(Account, URL, Proxy = None):
        Dotcoin = HPV_Dotcoin(Account, URL, Proxy)
        Dotcoin.Run()

    if Proxy:
        DIVIDER = Fore.BLACK + ' | '
        Time = Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        Text = Fore.GREEN + f'Проверка прокси окончена! Работоспособные: {len(Proxy)}'
        print(Time + DIVIDER + '🌐' + DIVIDER + Text)
        sleep(5)

    try:
        for Account, URL in HPV_Get_Accounts().items():
            if Proxy:
                Proxy = cycle(Proxy)
                Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
            else:
                Thread(target=Start_Thread, args=(Account, URL,)).start()
    except:
        print(Fore.RED + '\n\tОшибка чтения `HPV_Account.json`, ссылки указаны некорректно!')


