from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time

user = str(config.SCOUT_TREEHUNDRED_LOGIN)
pas = str(config.SCOUT_TREEHUNDRED_PASSWORD)
bas = str(config.SCOUT_TREEHUNDRED_BASED_ADRESS)
bas_tok = str(config.SCOUT_TREEHUNDRED_BASE_TOKEN)

class ScoutTreeHundred(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с системы мониторинга Скаут_365
    """

    def token(self, base_token):
        """
        Login to Scout_365
        Get access_token
        """
        url = f'{self.based_adres}auth/token'
        data = {
                'grant_type': 'password',
                'username': self.login,
                'password': self.password,
                'locale': 'ru-RU',
                'zoneinfo': 'Europe/Moscow'
        }
        headers = {
                'Accept': 'application/json',
                'Authorization': f'Basic {base_token}',
                'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            return None

    def _get_request(self, url, token):
        """Универсальный метод для выполнения GET-запросов"""
        headers = {
            "Content-Type": "application/json, text/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

class ScoutTreeUnits(ScoutTreeHundred):
    """ 
    Объекты Скаут_365
    """

    def __init__(self, scouttree_class: ScoutTreeHundred):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.scouttree_class = scouttree_class

    def get_all_units(self, token):
        """
        Все Объекты с СКАУТ_365 

        """
        
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units", token)

    def get_all_units_and_scopes(self, token): # Важный но не работает
        """
        Все Объекты со скоупами- группами объектов
        в случае на демо версии и аккаунта нашей фирмы: scopeIds- пусто
        """
        
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units/units-previews", token)


    def get_all_units_and_groups(self, token):
        """
        Все Объекты с группами
        в случае на демо версии и аккаунта нашей фирмы: scopeIds- пусто
        """
        
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units/unit-group-ids", token)


    def get_detail_online_data(self, token, unitId): # Важный
        """
        Детально с онлайн данными по объекту по unit_id

        """
        
        return self._get_request(f"{self.scouttree_class.based_adres}v3/online-data/{unitId}", token)


class ScoutTreeScopes(ScoutTreeHundred):
    """ 
    Компании Скаут_365 они же группы объектов
    """

    def __init__(self, scouttree_class: ScoutTreeHundred):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.scouttree_class = scouttree_class

        
    def get_all_scopes_and_companys(self, token): # Важный
        """
        Получение подразделений вместе с родительскими компаниями
        если 

        если "companyId" и "id" совпадают то это компания
        если "parentId" = 3668(наша заглавная фирма) то такой скоуп холдинг
        """      
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units/scope-with-parents", token)



scout_365 = ScoutTreeHundred(
        login=user,
        password=pas,
        based_adres=bas
        )

token = scout_365.token(bas_tok)

#Объекты
scout_units = ScoutTreeUnits(scout_365) # UNITS
units_and_scopes = scout_units.get_all_units_and_scopes(token) # Все скоупы- группы объектов не показывает

#Группы объектов
# scout_scopes = ScoutTreeScopes(scout_365)
# all_scopes_and_companys = scout_scopes.get_all_scopes_and_companys(token) # Все компании с родителями


print(units_and_scopes)


save_to_json(units_and_scopes,'scout_365_all_units_and_scopes_demo')

