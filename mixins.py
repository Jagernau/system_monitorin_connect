
class MixInSystemMonitoring:
    ''' 
    При инициализации класса
    Логин, пароль, основной адрес.
    '''
    def __init__(self, login: str, password: str, based_adres: str):
        self.login = login
        self.password = password
        self.based_adres = based_adres

