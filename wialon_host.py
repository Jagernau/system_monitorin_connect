from help_funcs import save_to_json, reserv_data_to_json, get_current_unix_time, search_get_comand_result
import config
import time
from wialon.sdk import WialonSdk


wialon_hosting_token = config.WIALON_HOSTING_TOKEN
wialon_hosting_based_adress = config.WIALON_HOSTING_BASED_ADRESS
wialon_hosting_port = config.WIALON_HOSTING_PORT if config.WIALON_HOSTING_PORT else 443


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
        # 8 Произвольные поля +
        # 4096 датчики
        'flags': 5517, 
        'from': 0,
        'to': 0
        }
        self.sdk.login(str(token))
        units = self.sdk.core_search_items(parameters_unit)
        self.sdk.logout()
        return units



    def get_all_device_types(self, token: str):
        """
        Метод получения всех Типов терминалов
        """
        parameters_types = {
          'filterType': "name",
        }
        self.sdk.login(str(token))
        device_types = self.sdk.core_get_hw_types(parameters_types)
        self.sdk.logout()
        return device_types

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

    def create_terminal_comand(self, token: str, obj_id, comand_name, terminal_comand):
        """
        Метод создания комманды для отправки через Wialon
        """
        self.sdk.login(str(token))
        acc = self.sdk.unit_update_command_definition({
             "itemId": int(obj_id),
#             "id":<long>,
             "callMode": "create",
             "n": str(comand_name),
             "c": 'custom_msg',
             "l": '',
             "p": str(terminal_comand),
             # 34359738368 + создание редактирование команд
             # 17179869184 + просмотр команд
             # 16777216 + выполнение команд
             "a": int(51556384768)})
        time.sleep(2)
        self.sdk.logout()
        return acc

    def exec_terminal_comand(self, token: str, obj_id, comand_name):
        """
        Метод отправки комманды команды через Wialon
        """
        time.sleep(2)
        self.sdk.login(str(token))
        comand = self.sdk.unit_exec_cmd({
            "itemId": int(obj_id),
            "commandName": str(comand_name),
            "linkType": '',
            "param": "",
            "timeout": int(10),
            "flags": int(0)
             })
        time.sleep(2)
        self.sdk.logout()
        return comand


    def get_last_masseges_data(self, token: str, obj_id, curent_time):
        """
        Метод получение сообщений от терминала Wialon
        """
        time.sleep(2)
        self.sdk.login(str(token))
        comand_result = self.sdk.messages_load_last({
            "itemId": int(obj_id),
            "lastTime": curent_time,
            "lastCount": 300,
            "flags": 512,
            "flagsMask": int(0),
            "loadCount": 300
             })
        self.sdk.logout()
        return comand_result


wialon_hosting = WialonHosting(wialon_hosting_based_adress, int(wialon_hosting_port))

#Объекты
# hosting_units = wialon_hosting.get_all_units(wialon_hosting_token)
# print(hosting_units)
# save_to_json(hosting_units, "wialon_hosting_all_objects")
# reserv_data_to_json(hosting_units, "wialon_hosting_all_objects") # Резервные файлы Wialon


#Типы терминалов
# hosting_devices_types = wialon_hosting.get_all_device_types(wialon_hosting_token)
# print(hosting_devices_types)
# save_to_json(hosting_devices_types, "wialon_hosting_device_types")
# reserv_data_to_json(hosting_devices_types, "wialon_hosting_device_types")

#Юзеры
# hosting_users = wialon_hosting.get_all_users(wialon_hosting_token)
# print(hosting_users)
# save_to_json(hosting_users, "wialon_hosting_all_users")
# reserv_data_to_json(hosting_users, "wialon_hosting_all_users")


# Группы объектов
# hosting_groups = wialon_hosting.get_all_units_groups(wialon_hosting_token)
# print(hosting_groups)
# save_to_json(hosting_groups, "wialon_hosting_all_groups")
# reserv_data_to_json(hosting_groups, "wialon_hosting_all_groups")

# Ретрансляторы
# hosting_retrans = wialon_hosting.get_all_retrans(wialon_hosting_token)
# print(hosting_retrans)
# save_to_json(hosting_retrans, "wialon_hosting_all_retrans")
# reserv_data_to_json(hosting_retrans, "wialon_hosting_all_retrans")

# Ресурсы
# hosting_res = wialon_hosting.get_all_resources(wialon_hosting_token)
# print(hosting_res)
# save_to_json(hosting_res, "wialon_hosting_all_resources")
# reserv_data_to_json(hosting_res, "wialon_hosting_all_resources")

#Учётки билинга
# hosting_accs = wialon_hosting.get_detail_bill_accounts(wialon_hosting_token, 697)
# print(hosting_accs)
# save_to_json(hosting_accs, "wialon_hosting_detail_bill_account_697")

#Создание команды
# wialon_create_comand = wialon_hosting.create_terminal_comand(wialon_hosting_token, 27471923)
# print(wialon_create_comand)
# save_to_json(wialon_create_comand, "wialon_create_comand_27471923")


# #Отправка команды
# wialon_exec_comand = wialon_hosting.exec_terminal_comand(wialon_hosting_token, 27471923)
# print(wialon_exec_comand)
# save_to_json(wialon_create_comand, "wialon_create_comand_27471923")

# # # Получение ответа
# wialon_result_comand = wialon_hosting.get_terminal_result_data(wialon_hosting_token, 27471923, 1)
# print(wialon_result_comand)
# save_to_json(wialon_create_comand, "wialon_create_comand_27471923")


# # Получение сообщений
# request_time = int(get_current_unix_time()) - 9000
# wialon_message_comand = wialon_hosting.get_last_masseges_data(wialon_hosting_token, 27471923, request_time)
# search_get_comand_result(wialon_message_comand)

# print(wialon_message_comand)
# save_to_json(wialon_message_comand, "wialon_messages_27471923")
#
