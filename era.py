from help_funcs import save_to_json, converting, current_time, current_time_past_tree
import mixins
import json
import requests
import config
import time

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import ssl
from thrift.transport import TSSLSocket

from thrif.dispatch.server.thrif.backend.DispatchBackend import Client



login = config.ERA_LOGIN
password = config.ERA_PASSWORD
based_adres = config.ERA_BASED_ADRESS
era_port = int(config.ERA_PORT)


class Era(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с системы мониторинга ERA 
    """
    def __init__(self, login, password, based_adres, port: int):
        super().__init__(login, password, based_adres)
        self.port = port
        self.client_class = Client
        self.session_id = None
        self.transport = None


    def __era_session(self):
        """ 
        Открытие сессии, открытие SSL протокола
        """
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE 

        self.transport = TSSLSocket.TSSLSocket(self.based_adres, int(self.port), ssl_context=ssl_context)

        self.transport = TTransport.TFramedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.transport.open()
        self.client_class = Client(protocol)
        self.session_id = self.client_class.login(self.login, self.password, True)


    def get_era_objects(self):
        """ 
        Возвращает все объекты под заглавной 
        """
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        objects = self.client_class.getChildrenMonitoringObjects(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return converting(objects)

    def get_era_event_object(self, object_id: str):
        """ 
        Возвращает последнее событие объекта за последнее 3 часа 
        """
        self.__era_session()
        object_event = self.client_class.getMonitoringObjectEvents(
                self.session_id, 
                [object_id, ], 
                current_time_past_tree(), # Начало
                current_time()  # Конец
                )
        self.transport.close()
        object_info = converting(object_event)
        if len(object_info) >= 1:
            return object_info[-1]
        else:
            return []


    def get_era_groups(self):
        """ 
        Возвращает все группы объектов под заглавной
        """
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        groups = self.client_class.getChildrenGroups(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return converting(groups)


    def get_era_users(self):
        """ 
        Возвращает всех пользователей под заглавной
        """
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        users = self.client_class.getChildrenUsers(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return converting(users)

    def get_detail_user(self, user_id: str):
        """ 
        Возвращает детально по пользователю
        Принимает: ID пользователя
        Метод бесполезен, вся инфо есть в общей
        """
        self.__era_session()
        detail_user = self.client_class.getUser(self.session_id, user_id)
        self.transport.close()
        return converting(detail_user)

    def get_grops_users(self):
        """ 
        Возвращает все группы пользователей (Роли)
        """
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        roles = self.client_class.getGroupRoles(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return converting(roles)
        
    def get_era_relays(self):
        """ 
        Получение всех ретрансляторов
        """
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        relays = self.client_class.getChildRelays(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return converting(relays)




era = Era(login, password, based_adres, era_port)



# Группы объектов
# groups = era.get_era_groups()
# save_to_json(groups, "era_all_groups")


# Объекты
#objects = era.get_era_objects()
#event_obj = era.get_era_event_object("af254f72-3f56-44ea-848b-6c6bb5e2a673")
#save_to_json(event_obj, "era_detail_object_af254f72-3f56-44ea-848b-6c6bb5e2a673")
#print(objects)



# Юзеры
#users = era.get_era_users()
#users_json = converting(users)
#detail_user = era.get_detail_user("5c5f9075-707a-4d79-8b35-16d71617816a") # Нет полезного
#save_to_json(users_json, "era_all_users_2")


# Группы юзеров (Ролей)
# roles = era.get_grops_users()
# users_groups = converting(roles)
# print(users_groups)
# save_to_json(users_groups, "era_user_groups_roles")

# Ретрансляторы
# relays = era.get_era_relays()
# relays_json = converting(relays)
# print(relays_json)
# save_to_json(relays_json, "era_all_retranslators")

