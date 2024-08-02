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


    def get_objects_tree(self, token: str):
        """
        Запросить дерево объектов
        Не приминяемо
        """
        params = {
                'SessionId': str(token),
                'companyId': 0
        }
        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/gettree?all=true", token, params=params)


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
        Метод получения всех Доступных объектов
        """
        params = {
                'SessionId': str(token),
                'oid': str(object_id)
        }

        time.sleep(1)
        return self._get_request(f"{self.fort_class.based_adres}v1/fullobjinfo", token, params=params)


fort = Fort(login, password, based_adres)
token = fort.token()

# Объекты
fort_objects = FortObjects(fort)
#objects_tree = fort_objects.get_objects_tree(token)
#all_objects = fort_objects.get_all_objects(token) # Нужен


print()
#save_to_json(all_objects,'fort_objects_all')

