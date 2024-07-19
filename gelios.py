from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time

user = str(config.GELIOS_LOGIN)
pas = str(config.GELIOS_PASSWORD)
bas = str(config.GELIOS_BASED_ADRES)



class Gelios(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с систем мониторинга Гелиос
    """
    def token(self):
        """Аутентификация в Гелиос"""
        url = f'{self.based_adres}v1/auth/login'
        data = {
                "grant_type": "password",
                "password": str(self.password),
                "username": str(self.login)
        }
        headers = {
                    "accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"
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


class GeliosUnit(Gelios):
    """
    Объекты Гелиос
    """
    def __init__(self, gelios_class: Gelios):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.gelios_class = gelios_class



    def get_all_units(self, token):
        """
        Все ТС Гелиос

        """
        return self._get_request(f"{self.gelios_class.based_adres}v1/units", token)
        

    def get_all_units_groups(self, token):
        """
        Все группировки объектов

        """
        return self._get_request(f"{self.gelios_class.based_adres}v1/units/groups", token)
        

    def get_detail_unit_from_id(self, token, unit_id):
        """
        Детально по объекту по Id

        """
        return self._get_request(f"{self.gelios_class.based_adres}v1/units/{unit_id}", token)

    def get_detail_unit_group_from_unit_id(self, token, unit_id):
        """
        Выдать к каким группам пренадлежит объект, по unit_id

        """
        return self._get_request(f"{self.gelios_class.based_adres}v1/units/{unit_id}/groups", token)


class GeliosUser(Gelios):
    """
    Пользователи Гелиос
    """
    def __init__(self, gelios_class: Gelios):
        """
        При инициализации класса
        Логин, пароль, основной адрес.
        """
        self.gelios_class = gelios_class
        
    def get_all_users(self, token):
        """
        Все Создатели

        """
        return self._get_request(f"{self.gelios_class.based_adres}v1/users", token)
        


gelios = Gelios(user, pas, bas)
token = gelios.token()
#gelios_unit = GeliosUnit(gelios)
#all_vehicles = gelios_unit.get_all_vehicles(token)
#all_unit_groups = gelios_unit.get_all_units_groups(token)
#detail_unit_group_id = gelios_unit.get_detail_unit_group_from_unit_id(token, 797051)
gelios_user = GeliosUser(gelios)
all_users = gelios_user.get_all_users(token)
print(all_users)


save_to_json(all_users,'gelios_all_users.json')

