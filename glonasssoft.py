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
        if response.status_code == 200:
            return response.json()
        else:
            return None


class GlonasssUnits(Glonasssoft):
    """
    Объекты Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_vehicles_old_method(self, token: str):
        """
        Метод получения всех объектов glonasssoft
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}vehicles/", token)


    def get_all_vehicles__new(self, token: str, parentId: str):
        """
        Метод получения всех объектов glonasssoft
        """
        data = {
                "parentId": str(parentId)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/vehicles/find", token, data)


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
        Полные данные с родителями
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}agents/", token)


    def get_all_agents_with_daughter_new(self, token, parentId: str):
        """
        Метод получения всех клиентов с дочерними новый метод
        """
        data = {
                "parentId": str(parentId)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/agents/find", token, data)


    def get_detail_agent_by_agentid(self, token, agentId: str):
        """
        Метод получения деталей клиента
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/agents/{agentId}", token)


class GlonasssUsers(Glonasssoft):
    """
    Учётки Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_users_old_method(self, token):
        """
        Метод получения всех учёток старый метод
        Полные данные с родителями
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}users/", token)


    def get_all_users_with_daughter_new(self, token, parentId: str):
        """
        Метод получения всех учёток с дочерними новый метод
        По клиенту
        """
        data = {
                "parentId": str(parentId)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/users/find", token, data)

    def get_detail_user_by_userid(self, token, userId: str):
        """
        Метод получения деталей учётки
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/users/{userId}", token)



class GlonasssModels(Glonasssoft):
    """
    Модели Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class

    def get_client_models(self, token, parentId: str):
        """
        Метод получения всех моделей объектов клиента
        По клиенту
        """
        data = {
                "parentId": str(parentId)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/models/find", token, data)


    def get_detail_model_by_modelid(self, token, modelId: str):
        """
        Метод получения деталей модели
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/models/{modelId}", token)


class GlonasssRetranlators(Glonasssoft):
    """
    Ретрансляторы Глонассофт не работает
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class

    def get_client_retranlators(self, token, parentId: str):
        """
        Метод получения всех ретрансляторов клиента
        """
        data = {
                "parentId": str(parentId)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/retranslations/find", token, data)



class GlonasssRecyclebin(Glonasssoft):
    """
    Корзина Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_recyclebin(self, token):
        """
        Метод получения всех объектов в корзине
        Полные данные с родителями
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/Vehicles/recyclebin/all", token)



glonass = Glonasssoft(login, password, based_adres)

token = glonass.token()

#glonass_units = GlonasssUnits(glonass)
#all_vehicles = glonass_units.get_all_vehicles(token)
#details_vehicle = glonass_units.get_detail_vehicle_by_vehicleid(token,'302174')
#all_vehicles__new = glonass_units.get_all_vehicles__new(token,"80eb1587-12cf-44d4-b0d0-c09b7ddf6110")


#glonass_agents = GlonasssAgents(glonass)
#all_agents_old = glonass_agents.get_all_agents_old_method(token)
# "80eb1587-12cf-44d4-b0d0-c09b7ddf6110" головная группа
#all_agents_new_method = glonass_agents.get_all_agents_with_daughter_new(token,"80eb1587-12cf-44d4-b0d0-c09b7ddf6110")
#details_agent = glonass_agents.get_detail_agent_by_agentid(token,"57382190-3f5d-4472-83e5-82c9ab31098f")

#glonass_users = GlonasssUsers(glonass)
#all_users_old = glonass_users.get_all_users_old_method(token)
# "80eb1587-12cf-44d4-b0d0-c09b7ddf6110" головная группа
#all_users_new_method = glonass_users.get_all_users_with_daughter_new(token,"80eb1587-12cf-44d4-b0d0-c09b7ddf6110")
#details_user = glonass_users.get_detail_user_by_userid(token, "ba1354c4-d4d9-4d18-bca7-7fcb65c8599e")

#models = GlonasssModels(glonass)
#client_models = models.get_client_models(token, "4d943187-83d3-4a36-a2c4-3ffcecd7744d") # нужно обращаться по конкретному клиенту
#details_model = models.get_detail_model_by_modelid(token, "f8f5b6f5-5f27-4c3a-9e6f-6d2e0d0e0c9e")


# retranlators = GlonasssRetranlators(glonass)
# client_retranlators = retranlators.get_client_retranlators(token, "27eb4840-d5da-471c-8c6b-0723c1bc9fce") # нужно обращаться по конкретному клиенту

obj_rec = GlonasssRecyclebin(glonass)
all_vehicles_recyclebin = obj_rec.get_all_recyclebin(token)

print(all_vehicles_recyclebin)

#save_to_json(all_vehicles__new,'glonass_all_vehicles__new_method')

