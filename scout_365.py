from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time

class ScoutTreeHundred(mixins.MixInSystemMonitoring):

    def token(self, base_token):
        """Login to Scout_365"""
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



scout_365 = ScoutTreeHundred(
        login=config.SCOUT_TREEHUNDRED_LOGIN,
        password=config.SCOUT_TREEHUNDRED_PASSWORD,
        based_adres=config.SCOUT_TREEHUNDRED_BASED_ADRESS
        )

token = scout_365.token(config.SCOUT_TREEHUNDRED_BASE_TOKEN)




#save_to_json(vehicles,'glonass_vehicles')

