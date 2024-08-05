from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time


login=config.FORT_LOGIN
password=config.FORT_PASSWORD
based_adres=config.FORT_BASED_ADRESS

class Fort(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с систем мониторинга Fort
    """
    def token(self) -> str | None:
        url = f'{self.based_adres}v1/connect'
        params = {
                'login': self.login,
                'password': self.password,
                'lang': 'ru-ru',
                'timezone': '+3'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.headers['SessionId']
        else:
            return None

    def _get_request(self, url, token, params):
        """Универсальный метод для выполнения GET-запросов"""
        headers = {
                    'Content-type': 'application/json', 
                    'Accept': 'application/json', 
                    'SessionId': token
                }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

class FortObjects(Fort):
    """
    Объекты Fort
    """
    def __init__(self, fort_class: Fort ):
        """
        При инициализации класса
        """
        self.fort_class = fort_class


    def get_all_objects(self, token: str):
        """
        Метод получения всех Доступных объектов
        """
        params = {
                'SessionId': str(token),
                'companyId': 0
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/getobjectslist", token, params=params)


    def get_detail_object(self, token: str, object_id):
        """
        Метод получения детализации по объекту
        """
        params = {
                'SessionId': str(token),
                'oid': str(object_id)
        }
        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/fullobjinfo", token, params=params)



class FortTerminalModels(Fort):
    """
    Модели терминалов Fort
    """
    def __init__(self, fort_class: Fort ):
        """
        При инициализации класса
        """
        self.fort_class = fort_class


    def get_terminals_models(self, token: str):
        """
        Получение списка поддерживаемых типов терминалов
        Не работает
        """
        params = {
                'SessionId': str(token),
                'companyId': 0
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/getsupportedprotocols", token, params=params)



class FortCompanies(Fort):
    """
    Компании Fort
    """
    def __init__(self, fort_class: Fort ):
        """
        При инициализации класса
        """
        self.fort_class = fort_class


    def get_all_companies(self, token: str):
        """
        Запрос списка доступных компаний - краткая информация
        """
        params = {
                'SessionId': str(token),
                'companyId': 0
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/getcompanieslist", token, params=params)



class FortObjectsGroups(Fort):
    """
    Группы объектов Fort
    """
    def __init__(self, fort_class: Fort ):
        """
        При инициализации класса
        """
        self.fort_class = fort_class


    def get_all_objects_groups(self, token: str):
        """
        Запрос списка доступных групп объектов
        """
        params = {
                'SessionId': str(token),
                'companyId': 0
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/getobjectgroupslist", token, params=params)



class FortUsers(Fort):
    """
    Пользователи Fort
    """
    def __init__(self, fort_class: Fort ):
        """
        При инициализации класса
        """
        self.fort_class = fort_class


    def get_all_users(self, token: str):
        """
        Получение списка пользователей
        groupId у логина указывает на id группы пользователей
        """
        
        params = {
                'SessionId': str(token),
                'companyId': 0
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/users", token, params=params)


    def get_all_users_groups(self, token: str):
        """
        Получение списка групп пользователей
        id это id группировок пользователей
        """
        params = {
                'SessionId': str(token),
                'companyId': 0
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/usergroups", token, params=params)


fort = Fort(login, password, based_adres)
token = fort.token()

# Объекты
#fort_objects = FortObjects(fort)
#objects_tree = fort_objects.get_objects_tree(token)
#all_objects = fort_objects.get_all_objects(token) # Нужен
#detail_object = fort_objects.get_detail_object(token, 747) # Нужен 

# Модели терминалов
# fort_terminal_models = FortTerminalModels(fort)
# terminals_models = fort_terminal_models.get_terminals_models(token) # Не работает

# Компании
#fort_companies = FortCompanies(fort)
#all_companies = fort_companies.get_all_companies(token)


# Группы объектов
#fort_objects_groups = FortObjectsGroups(fort)
#all_objects_groups = fort_objects_groups.get_all_objects_groups(token)


# Пользователи
fort_users = FortUsers(fort)
#all_users = fort_users.get_all_users(token)
all_users_groups = fort_users.get_all_users_groups(token)

print(all_users_groups)
save_to_json(all_users_groups,'fort_all_users_groups')

