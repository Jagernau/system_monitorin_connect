from help_funcs import save_to_json
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
era_port = config.ERA_PORT


class Era(mixins.MixInSystemMonitoring):
    """ 
    Получение данных с системы мониторинга ERA 
    """
    def __init__(self, login, password, based_adres, port: int):
        super().__init__(login, password, based_adres)
        self.port = port
        self.client_class = Client
        self.ssl_context = self._create_ssl_context()
        self.transport = None
        self.client = None


    def _create_ssl_context(self):
        """ 
        Создаёт и настраивает ssl-контекст.
        Returns:
            ssl.SSLContext: Настроенный ssl-контекст
        """
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    def _init_transport(self):
        """ 
        Инициализирует транспортный слой и клиента Trift.
        """



    
def get_era_data(login: str, password: str, thrif_class_client):

    url = "monitoring.aoglonass.ru"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE 

    transport = TSSLSocket.TSSLSocket(url, 19991, ssl_context=ssl_context)

    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    open = transport.open()
    client: Client = thrif_class_client(protocol)
    session_id = client.login(login, password, True)
    parent_id = client.getCurrentUser(session_id)
    objects = client.getChildrenMonitoringObjects(session_id, parent_id.parentGroupId, True)
    groups = client.getChildrenGroups(session_id, parent_id.parentGroupId, True)
    users = client.getChildrenUsers(session_id, parent_id.parentGroupId, True)
    transport.close()
    return [objects, groups, users]

era_data = get_era_data(login, password, Client)
print(era_data)
