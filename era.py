from help_funcs import save_to_json, converting
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
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        objects = self.client_class.getChildrenMonitoringObjects(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return objects


    def get_era_groups(self):
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        groups = self.client_class.getChildrenGroups(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return groups


    def get_era_users(self):
        self.__era_session()
        parent_id = self.client_class.getCurrentUser(self.session_id)
        users = self.client_class.getChildrenUsers(self.session_id, parent_id.parentGroupId, True)
        self.transport.close()
        return users
        


era = Era(login, password, based_adres, era_port)

objects = era.get_era_objects()
groups = era.get_era_groups()
users = era.get_era_users()

#groups_json = converting(groups)
#objects_json = converting(objects)
users_json = converting(users)
    
#print(groups_json)
#print(objects_json)
print(users_json)


#save_to_json(groups_json, "era_all_groups_3")
#save_to_json(objects_json, "era_all_objects_3")
save_to_json(users_json, "era_all_users_3")

