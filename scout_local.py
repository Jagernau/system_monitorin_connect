from time import sleep
from help_funcs import save_to_json, get_current_timestamp_utc
import mixins
import json
import requests
import config

user = str(config.SCOUT_LOCAL_LOGIN)
pas = str(config.SCOUT_LOCAL_PASSWORD)
bas = str(config.SCOUT_LOCAL_BASED_ADRESS)
port = int(config.SCOUT_LOCAL_PORT)

class ScoutLocal(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с системы мониторинга Скаут_локал
    """
    def __init__(self, login, password, based_adres, port: int):
        """ 
        При инициализации класса
        """
        super().__init__(login, password, based_adres)
        self.port = port


    def token(self):
        """
        Получение токена СКАУТ_локал
        """
        url = f'{self.based_adres}:{port}/spic/auth/rest/Login'
        payload = {
            "Login": f"{self.login}",
            "Password": f"{self.password}",
            "TimeStampUtc": f"{get_current_timestamp_utc()}",
            "TimeZoneOlsonId": "Europe/Moscow",
            "CultureName": "ru-ru",
            "UiCultureName": "ru-ru"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            token = response.json()["SessionId"]
            return token
        else:
            return None

    def _get_request(self, url, token, params=None):
        """Универсальный метод для выполнения GET-запросов"""
        headers = {
            "Content-Type": "application/json, text/json",
            "ScoutAuthorization": str(token),
        }
        if params:
            response = requests.get(url, headers=headers, data=params)
        else:
            response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def _post_request(self, url, token, data: dict):
        """Универсальный метод для выполнения POST """
        headers = {
            "Content-Type": "application/json, text/json",
            "ScoutAuthorization": str(token),
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return None

class ScoutLocalUnits(ScoutLocal):
    """ 
    Объекты Скаут_локал
    """

    def __init__(self, scoutlocal_class: ScoutLocal):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.scoutlocal_class = scoutlocal_class


    # Без лицензии пусто
    def get_all_units(self, token):
        """
        Все Объекты с СКАУТ_локал
        """
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}/spic/units/rest/getAllUnits", token)

    def get_detail_online_data(self, token, params): # Важный
        """
        Детально с онлайн данными по объектам

        """
        data = {
            "Id": params
        }
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}/spic/OnlineDataService/rest/GetOnlineData", token)



    def subscribe_detail_online_data(self, token, unitIds: list): # Важный
        """
        Подписка на получение данных с онлайн данными по объектам

        """
        body = {
            "UnitIds": list(unitIds)
        }
        return self._post_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}/spic/OnlineDataService/rest/Subscribe", token, body)


class ScoutLocalGroups(ScoutLocal):
    """ 
    Компании Скаут_локал они же группы объектов
    """
    def __init__(self, scoutlocal_class: ScoutLocal):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """

        self.scoutlocal_class = scoutlocal_class
        
    def get_all_groups_units(self, token): # Важный
        """
        Получение всех групп объектов вместе с родительскими компаниями
        """      
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}/spic/unitGroups/rest/", token)


scout_local = ScoutLocal(
        login=user,
        password=pas,
        based_adres=bas,
        port=port
        )

token = scout_local.token()

#Объекты
scout_units = ScoutLocalUnits(scout_local) # UNITS
all_units = scout_units.get_all_units(token) # Все объекты
detail_online = scout_units.get_detail_online_data(token, token) # Детально с онлайн данными по объектам
print(detail_online)

#detail_online = scout_units.get_detail_online_data(token)

#print(all_units)
#save_to_json(all_units,'scout_local_all_units')

#Группы объектов
#scout_groups = ScoutLocalGroups(scout_local)
#all_groups = scout_groups.get_all_groups_units(token)
# print(all_groups)
# save_to_json(all_groups,'scout_local_all_groups')
#print(scout_units.subscribe_detail_online_data(token, ["919", "920"]))
