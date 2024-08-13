from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time

from wialon.sdk import WialonSdk

wialon_local_token = config.WIALON_LOCAL_TOKEN
wialon_local_based_adress = config.WIALON_LOCAL_BASED_ADRESS
wialon_local_port = config.WIALON_LOCAL_PORT


class WialonLocal:
    """ 
    Получение данных с систем мониторинга Wialon_local
    """
    _scheme = 'https'

    def __init__(self, based_adres, port: int):
        """ 
        При инициализации принимает адресс, порт
        """
        self.sdk = WialonSdk(                
                is_development=True,
                scheme=self._scheme,
                host=str(based_adres),
                port=int(port),
                )

    def get_all_units(self, token: str):
        """
        Метод получения всех объектов Wialon Local способом поиска
        """
        parameters_unit = {
        'spec':{
          'itemsType': "avl_unit",
          'propName': "sys_name",
          'propValueMask': "*",
          'sortType': "sys_name",
          'or_logic': 0
        },
        'force': 1,
        # 1024 последнее местопол +
        # 1 базовый +
        # 4 свойства билинга +
        # 128 админ записи +
        # 256 доп свойства 
        'flags': 1413, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        units = self.sdk.core_search_items(parameters_unit)
        self.sdk.logout()
        return units

    def get_all_users(self, token: str):
        """
        Метод получения всех юзеров Wialon Local способом поиска
        """
        parameters_user = {
        'spec':{
          'itemsType': "user",
          'propName': "sys_name",
          'propValueMask': "*",
          'sortType': "sys_name",
          'or_logic': 0
        },
        'force': 1,
        # 1 базовый +
        # 4 билинг
        # 256 другие св-ва 
        # 
        # 
        'flags': 261, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        units = self.sdk.core_search_items(parameters_user)
        self.sdk.logout()
        return units


    def get_all_units_groups(self, token: str):
        """
        Метод получения всех групп объектов Wialon Local способом поиска
        """
        parameters_groups = {
        'spec':{
          'itemsType': "avl_unit_group",
          'propName': "sys_name",
          'propValueMask': "*",
          'sortType': "sys_name",
          'or_logic': 0
        },
        'force': 1,
        # 1 базовый +
        # 4 билинг
        # 
        # 
        # 
        'flags': 5, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        groups = self.sdk.core_search_items(parameters_groups)
        self.sdk.logout()
        return groups

    def get_all_accounts(self, token: str, itemId: int):
        """
        Метод получения всех аккаунтов Wialon Local способом поиска
        """
        self.sdk.login(str(token))
        reso = self.sdk.account_get_account_data({
            "itemId": itemId,
            "type": 5
            })
        self.sdk.logout()
        del reso["services"]
        return reso


wialon_local = WialonLocal(wialon_local_based_adress, int(wialon_local_port))

# Объекты
#local_units = wialon_local.get_all_units(wialon_local_token)
#print(local_units)
#save_to_json(local_units, "wialon_local_all_objects")

# Юзеры
# local_users = wialon_local.get_all_users(wialon_local_token)
# print(local_users)
# save_to_json(local_users, "wialon_local_all_users__2")

# Группы объектов
# local_groups = wialon_local.get_all_units_groups(wialon_local_token)
# print(local_groups)
# save_to_json(local_groups, "wialon_local_all_groups")

#Учётки билинга
local_accs = wialon_local.get_all_accounts(wialon_local_token, 26)
print(local_accs)
save_to_json(local_accs, "wialon_local_all_accounts")
