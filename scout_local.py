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

    def _get_request(self, url, token):
        """Универсальный метод для выполнения GET-запросов"""
        headers = {
            "Content-Type": "application/json, text/json",
            "ScoutAuthorization": str(token),
        }
        response = requests.get(url, headers=headers)
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
        На учётке suntel без лицензии пусто,
        На учётке demo данные идут

        """
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}/spic/units/rest/getAllUnits", token)


    def get_all_units_with_scopes(self, token): # Важный но не работает
        """
        Все Объекты со скоупами- группами объектов
        в случае на демо версии и аккаунта нашей фирмы: scopeIds- пусто
        """
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}", token)


    def get_detail_online_data(self, token, unitId): # Важный
        """
        Детально с онлайн данными по объекту по unit_id

        """    
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}", token)


class ScoutLocalScopes(ScoutLocal):
    """ 
    Компании Скаут_локал они же группы объектов
    """
    def __init__(self, scoutlocal_class: ScoutLocal):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """

        self.scoutlocal_class = scoutlocal_class


        
    def get_all_scopes_and_companys(self, token): # Важный
        """
        Получение подразделений вместе с родительскими компаниями
        если 

        если "companyId" и "id" совпадают то это компания
        если "parentId" = 3668(наша заглавная фирма) то такой скоуп холдинг
        """      
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}", token)


    def get_groups_with_units(self, token): # Важный рабочая
        """
        Группы с объектами
        """    
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}", token)

    # Пустой нет лицензий
    # def get_company_units(self, token):
    #     """
    #     Все компании с объектами
    #     """    
    #     return self._get_request(f"{self.scouttree_class.based_adres}v3/units/scopes-units", token)
    #


class ScoutLocalUsers(ScoutLocal):
    """ 
    Юзеры Скаут_локал
    Нет возможности получить пользователей
    """
    def __init__(self, scoutlocal_class: ScoutLocal):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.scoutlocal_class = scoutlocal_class

        
    def get_current_user(self, token): # Важный
        """
        Все Юзеры Скаут_локал
        """      
        return self._get_request(f"{self.scoutlocal_class.based_adres}:{self.scoutlocal_class.port}", token)



scout_local = ScoutLocal(
        login=user,
        password=pas,
        based_adres=bas,
        port=port
        )

token = scout_local.token()

#Объекты
scout_units = ScoutLocalUnits(scout_local) # UNITS
all_units = scout_units.get_all_units(token) # Все объекты без лицензии пусто на demo данные есть
#units_and_scopes = scout_units.get_all_units_and_scopes(token) # Все объекты с группами
#detail_online_data = scout_units.get_detail_online_data(token, 98825) # Детально с онлайн данными по объекту по unit_id пусто на suntel учётной записи без лицензии
print(all_units)
save_to_json(all_units,'scout_local_all_units')

#Группы объектов
#scout_scopes = ScoutTreeScopes(scout_365)
# all_scopes_and_companys = scout_scopes.get_all_scopes_and_companys(token) # Все компании с родителями
#all_groups_with_units = scout_scopes.get_groups_with_units(token) # Все группы объектов с объектами


#Юзеры
# scout_users = ScoutTreeUsers(scout_365)
# all_users = scout_users.get_all_users(token)

#save_to_json(detail_online_data,'scout_365_detail_unit__demo')

