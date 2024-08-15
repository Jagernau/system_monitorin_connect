from help_funcs import save_to_json
import mixins
import json
import requests
import config
import time

from wialon.sdk import WialonSdk

wialon_hosting_token = config.WIALON_HOSTING_TOKEN
wialon_hosting_based_adress = config.WIALON_HOSTING_BASED_ADRESS
wialon_hosting_port = config.WIALON_HOSTING_PORT


class WialonHosting:
    """ 
    Получение данных с систем мониторинга Wialon_hosting
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
        Метод получения всех объектов Wialon hosting способом поиска
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
        # 256 доп свойства +
        # 8 Произвольные поля
        'flags': 1421, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        units = self.sdk.core_search_items(parameters_unit)
        self.sdk.logout()
        return units

    def get_all_users(self, token: str):
        """
        Метод получения всех юзеров Wialon hosting способом поиска
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
        Метод получения всех групп объектов Wialon hosting способом поиска
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
        'flags': 5, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        groups = self.sdk.core_search_items(parameters_groups)
        self.sdk.logout()
        return groups

    def get_all_retrans(self, token: str):
        """
        Метод получения всех Ретрансляторов Wialon hosting способом поиска
        """
        parameters_retrans = {
        'spec':{
          'itemsType': "avl_retranslator",
          'propName': "sys_name",
          'propValueMask': "*",
          'sortType': "sys_name",
          'or_logic': 0
        },
        'force': 1,
        # 1 базовый +
        # 4 билинг
        # 256 конфигурация +
        # 512 объекты
        'flags': 773, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        groups = self.sdk.core_search_items(parameters_retrans)
        self.sdk.logout()
        return groups


    def get_all_resources(self, token: str):
        """
        Метод получения всех Ресурсов Wialon hosting способом поиска
        """
        parameters_resourc = {
        'spec':{
          'itemsType': "avl_resource",
          'propName': "sys_name",
          'propValueMask': "*",
          'sortType': "sys_name",
          'or_logic': 0
        },
        'force': 1,
        # 1 базовый +
        # 4 билинг
        'flags': 5, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        resources = self.sdk.core_search_items(parameters_resourc)
        self.sdk.logout()
        return resources



    def get_detail_bill_accounts(self, token: str, itemId: int):
        """
        Метод получения детализации по билингового аккаунта Wialon hosting способом поиска
        """
        self.sdk.login(str(token))
        acc = self.sdk.account_get_account_data({
            "itemId": itemId,
            "type": 5
            })
        self.sdk.logout()
        del acc["services"]
        return acc


wialon_hosting = WialonHosting(wialon_hosting_based_adress, int(wialon_hosting_port))

# Объекты
# hosting_units = wialon_hosting.get_all_units(wialon_hosting_token)
# print(hosting_units)
# save_to_json(hosting_units, "wialon_hosting_all_objects")

# Юзеры
# hosting_users = wialon_hosting.get_all_users(wialon_hosting_token)
# print(hosting_users)
# save_to_json(hosting_users, "wialon_hosting_all_users__2")
#
# Группы объектов
# hosting_groups = wialon_hosting.get_all_units_groups(wialon_hosting_token)
# print(hosting_groups)
# save_to_json(hosting_groups, "wialon_hosting_all_groups")

# Ретрансляторы
# hosting_retrans = wialon_hosting.get_all_retrans(wialon_hosting_token)
# print(hosting_retrans)
# save_to_json(hosting_retrans, "wialon_hosting_all_retrans")

# Ресурсы
# hosting_res = wialon_hosting.get_all_resources(wialon_hosting_token)
# print(hosting_res)
# save_to_json(hosting_res, "wialon_hosting_all_resources")



#Учётки билинга
# hosting_accs = wialon_hosting.get_detail_bill_accounts(wialon_hosting_token, 697)
# print(hosting_accs)
# save_to_json(hosting_accs, "wialon_hosting_detail_bill_account_697")


