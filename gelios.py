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

    def get_all_units(self, token):
        """
        Все ТС Гелиос

        """
        
        url = f"{self.based_adres}v1/units"
        headers = {
            "Content-Type": "application/json, text/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_all_units_groups(self, token):
        """
        Все группировки объектов

        """
        
        url = f"{self.based_adres}v1/units/groups"
        headers = {
            "Content-Type": "application/json, text/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_detail_unit_from_id(self, token, unit_id):
        """
        Детально по объекту по Id

        """
        
        url = f"{self.based_adres}v1/units/{unit_id}"
        headers = {
            "Content-Type": "application/json, text/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_detail_unit_group_from_unit_id(self, token, unit_id):
        """
        Выдать к каким группам пренадлежит объект, по unit_id

        """
        
        url = f"{self.based_adres}v1/units/{unit_id}/groups"
        headers = {
            "Content-Type": "application/json, text/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None


    def get_all_users(self, token):
        """
        Все Создатели

        """
        
        url = f"{self.based_adres}v1/users"
        headers = {
            "Content-Type": "application/json, text/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None


gelios = Gelios(user, pas, bas)
token = gelios.token()
#all_vehicles = gelios.get_all_vehicles(token)
#all_unit_groups = gelios.get_all_units_groups(token)
#detail_unit_group_id = gelios.get_detail_unit_group_from_unit_id(token, 797051)
all_users = gelios.get_all_users(token)
print(all_users)


save_to_json(all_users,'gelios_all_users.json')

