from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time


login=config.GLONASS_LOGIN
password=config.GLONASS_PASSWORD
based_adres=config.GLONASS_BASED_ADRESS


class Glonasssoft(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с систем мониторинга Глонассофт
    """

    def token(self):
        """Получение Токена Глонассофт"""
        url = f'{self.based_adres}v3/auth/login'
        data = {'login': self.login, 'password': self.password}
        headers = {'Content-type': 'application/json', 'accept': 'json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.json()["AuthId"]
        else:
            return None

    def _get_request(self, url, token):
        """Универсальный метод для выполнения GET-запросов"""
        headers = {
            "X-Auth": f"{token}",
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def _post_request(self, url, token, data: dict):
        """Универсальный метод для выполнения POST """
        headers = {
            "X-Auth": f"{token}",
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.text
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     return None


class GlonasssUnits(Glonasssoft):
    """
    Объекты Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_vehicles(self, token: str):
        """
        Метод получения всех объектов glonasssoft
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}vehicles/", token)


    def get_detail_vehicle_by_vehicleid(self, token: str, vehicleId: str):
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/vehicles/{vehicleId}", token)

class GlonasssAgents(Glonasssoft):
    """
    Объекты Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_agents_old_method(self, token):
        """
        Метод получения всех клиентов старый метод
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}agents/", token)



    def get_all_agents_with_daughter_new(self, token, parentId: str):
        """
        Метод получения всех клиентов с дочерними
        """
        data = {
                "parentId": str(parentId)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/agents/find", token, data)



glonass = Glonasssoft(login, password, based_adres)

token = glonass.token()

#glonass_units = GlonasssUnits(glonass)
#all_vehicles = glonass_units.get_all_vehicles(token)
#details_vehicle = glonass_units.get_detail_vehicle_by_vehicleid(token,'302174')
glonass_agents = GlonasssAgents(glonass)
all_agents_old = glonass_agents.get_all_agents_old_method(token)
#all_agents_new_method = glonass_agents.get_agents_daughter_agents(token)

print(all_agents_old)

save_to_json(all_agents_old,'glonass_all_agents_old')

