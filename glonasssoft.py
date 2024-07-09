from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time

class Glonasssoft(mixins.MixInSystemMonitoring):

    @property
    def token(self):
        """Login to glonasssoft"""
        url = f'{self.based_adres}v3/auth/login'
        data = {'login': self.login, 'password': self.password}
        headers = {'Content-type': 'application/json', 'accept': 'json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.json()["AuthId"]
        else:
            return None

    def get_glonasssoft_vehicles(self, token: str):
        """
        get all glonass objects (vehicles)
        """
        url = f"{self.based_adres}v3/vehicles/find"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None


glonass = Glonasssoft(
        login=config.GLONASS_LOGIN,
        password=config.GLONASS_PASSWORD,
        based_adres=config.GLONASS_BASED_ADRESS
        )

token = glonass.token

time.sleep(3)
vehicles = glonass.get_glonasssoft_vehicles(token=token)

save_to_json(vehicles,'vehicles')

