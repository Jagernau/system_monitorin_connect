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
        time.sleep(1)
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
            raise Exception(response.text)


class GlonasssUnits(Glonasssoft):
    """
    Объекты Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_vehicles_old(self, token: str):
        """
        Метод получения всех объектов glonasssoft
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}vehicles/", token)


    def get_all_vehicles_new(self, token: str, parentId: str):
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

    def create_unit(
            self, 
            token, 
            parentId: str, 
            name: str, 
            imei: str, 
            device_type, 
            model_id, 
            fields,
            sensors
            ):
        """ 
        Метод создания объектов
        """
        time.sleep(1)
        data = {
                "parentId": parentId,
                "name": name,
                "imei": imei,
                "deviceTypeId": device_type,
                "modelId": model_id,
#                "customFields": fields
                }

        if fields != None:
            data["customFields"] = fields

        if sensors != None:
            data["sensors"] = sensors

        return self._post_request(f"{self.glonass_class.based_adres}v3/vehicles", token, data)


class GlonasssAgents(Glonasssoft):
    """
    Группы объектов Глонассофт
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_agents_old(self, token):
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


    def get_all_users_old(self, token):
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

    def get_client_retranlators(self, token, client_name: str):
        """
        Метод получения всех ретрансляторов клиента
        """
        data = {
                "search": str(client_name)
            }
        time.sleep(1)
        return self._post_request(f"{self.glonass_class.based_adres}v3/retranslations/find", token, data)

    def get_detail_client_retranlators_id(self, token, retrans_id: str):
        """
        Метод получения детальной информации по ретрансляции
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/retranslations/{retrans_id}", token)


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

class GlonasssDeviceTypes(Glonasssoft):
    """
    Получить список типов устройств
    """
    def __init__(self, glonass_class: Glonasssoft ):
        """
        При инициализации класса
        """
        self.glonass_class = glonass_class


    def get_all_devices_types(self, token):
        """
        Метод получения всех типов устройств Глонассофт
        """
        time.sleep(1)
        return self._get_request(f"{self.glonass_class.based_adres}v3/devices/types", token)


glonass = Glonasssoft(login, password, based_adres)

token = glonass.token()

glonass_units = GlonasssUnits(glonass)
# all_vehicles = glonass_units.get_all_vehicles_old(token)
# details_vehicle = glonass_units.get_detail_vehicle_by_vehicleid(token,'429052')
# save_to_json(details_vehicle, "glonass_detail_vehicle")
# all_vehicles_new = glonass_units.get_all_vehicles_new(token,"80eb1587-12cf-44d4-b0d0-c09b7ddf6110")


#glonass_agents = GlonasssAgents(glonass)
#all_agents_old = glonass_agents.get_all_agents_old_method(token)
# "80eb1587-12cf-44d4-b0d0-c09b7ddf6110" головная группа
#all_agents_new_method = glonass_agents.get_all_agents_with_daughter_new(token,"80eb1587-12cf-44d4-b0d0-c09b7ddf6110")
#details_agent = glonass_agents.get_detail_agent_by_agentid(token,"4244ba44-f60d-471b-95c7-1269cdd8d979")

#glonass_users = GlonasssUsers(glonass)
#all_users_old = glonass_users.get_all_users_old_method(token)
# "80eb1587-12cf-44d4-b0d0-c09b7ddf6110" головная группа
#all_users_new_method = glonass_users.get_all_users_with_daughter_new(token,"80eb1587-12cf-44d4-b0d0-c09b7ddf6110")
#detail_user = glonass_users.get_detail_user_by_userid(token, "9c813a6a-7af6-422f-af34-738b35faa806")

#models = GlonasssModels(glonass)
#client_models = models.get_client_models(token, "4244ba44-f60d-471b-95c7-1269cdd8d979") # нужно обращаться по конкретному клиенту
#details_model = models.get_detail_model_by_modelid(token, "f8f5b6f5-5f27-4c3a-9e6f-6d2e0d0e0c9e")


# retranlators = GlonasssRetranlators(glonass)
# client_retranlators = retranlators.get_client_retranlators(token, "Нижегородский_лесопожарный_центр") # нужно обращаться по конкретному клиенту
#detail_retrans = retranlators.get_client_retranlators(token, "42e4cc27-f964-4aab-bbbd-62b216184c85")


#obj_rec = GlonasssRecyclebin(glonass)
#all_vehicles_recyclebin = obj_rec.get_all_recyclebin(token)

devices_types = GlonasssDeviceTypes(glonass)
#all_devices_types = devices_types.get_all_devices_types(token)

# print(client_retranlators)

#save_to_json(client_retranlators,'glonasss_all_client_retranslators_Нижегородский_лесопожарный_центр')

