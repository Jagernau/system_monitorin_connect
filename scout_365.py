from help_funcs import save_to_json
import mixins
import json
import requests
import config

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


    # Без лицензии пусто
    def get_all_units(self, token):
        """
        Все Объекты с СКАУТ_365
        На учётке suntel без лицензии пусто,
        На учётке demo данные идут

        """
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units", token)


    def get_all_units_with_scopes(self, token): # Важный но не работает
        """
        Все Объекты со скоупами- группами объектов
        в случае на демо версии и аккаунта нашей фирмы: scopeIds- пусто
        """
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units/units-previews", token)


    def get_detail_online_data(self, token, unitId): # Важный
        """
        Детально с онлайн данными по объекту по unit_id

        """    
        return self._get_request(f"{self.scouttree_class.based_adres}v3/online-data/{unitId}", token)


    # Пусто у аккаунта suntel, нет лицензий
    # def get_available_units(self, token):
    #     """
    #     Все доступные объекты
    #     """
    #     return self._get_request(f"{self.scouttree_class.based_adres}v3/units-info", token)



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


    def get_groups_with_units(self, token): # Важный рабочая
        """
        Группы с объектами
        """    
        return self._get_request(f"{self.scouttree_class.based_adres}v3/units/unit-group-ids", token)

    # Пустой нет лицензий
    # def get_company_units(self, token):
    #     """
    #     Все компании с объектами
    #     """    
    #     return self._get_request(f"{self.scouttree_class.based_adres}v3/units/scopes-units", token)
    #


class ScoutTreeUsers(ScoutTreeHundred):
    """ 
    Юзеры Скаут_365
    Нет возможности получить пользователей
    """
    def __init__(self, scouttree_class: ScoutTreeHundred):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.scouttree_class = scouttree_class

        
    def get_current_user(self, token): # Важный
        """
        Все Юзеры Скаут_365
        """      
        return self._get_request(f"{self.scouttree_class.based_adres}v3/user/profile", token)



scout_365 = ScoutTreeHundred(
        login=user,
        password=pas,
        based_adres=bas
        )

token = scout_365.token(bas_tok)

#Объекты
scout_units = ScoutTreeUnits(scout_365) # UNITS
#all_units = scout_units.get_all_units(token) # Все объекты без лицензии пусто на demo данные есть
#units_and_scopes = scout_units.get_all_units_and_scopes(token) # Все объекты с группами
detail_online_data = scout_units.get_detail_online_data(token, 98825) # Детально с онлайн данными по объекту по unit_id пусто на suntel учётной записи без лицензии


#Группы объектов
#scout_scopes = ScoutTreeScopes(scout_365)
# all_scopes_and_companys = scout_scopes.get_all_scopes_and_companys(token) # Все компании с родителями
#all_groups_with_units = scout_scopes.get_groups_with_units(token) # Все группы объектов с объектами


#Юзеры
# scout_users = ScoutTreeUsers(scout_365)
# all_users = scout_users.get_all_users(token)

print(detail_online_data)

save_to_json(detail_online_data,'scout_365_detail_unit__demo')

