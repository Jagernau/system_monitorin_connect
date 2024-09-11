
from os.path import join
import mysql_models as models
from db_connect import MysqlDatabase
from sqlalchemy import func


def get_db_sim_tel_from_imei(imei: str):
    """ 
    Метод получения телефонного номера сим карты по IMEI
    Из базы данных
    imei: Принимает IMEI терминала
    """
    db = MysqlDatabase()
    session = db.session
    sim = session.query(models.SimCard).filter_by(terminal_imei=imei).first()
    if sim is None:
        return None
    sim = sim.sim_tel_number
    session.close()
    return str(sim).replace(" ", "").replace("-", "").replace("+", "")


def get_terminal_comand_from_wialon_types(device_name: str):
    """ 
    Метод получения 
    Из базы данных
    : Принимает device_name терминала
    """
#    result_name = ''
    adapting_name_to_db = device_name.split(' ')
    if len(adapting_name_to_db) > 1:
        resul_array = [adapting_name_to_db[-2], str(adapting_name_to_db[-1]).replace("xx", '')]
        resul_name = " ".join(resul_array)
    else:
        resul_name = adapting_name_to_db[0]
    # elif len(adapting_name_to_db) == 1:
    #     resul_name = adapting_name_to_db[0]

    db = MysqlDatabase()
    session = db.session
    data_commands = session.query(models.DevicesCommand).filter(
#            func.lower(models.DevicesCommand.device_brand.name).like(resul_name)
            models.DevicesCommand.command != None, 
            models.DevicesCommand.device_brand != None 
            ).all()
#    result_comand = [i.devices_brand.name for i in data_commands]
    result_comand = []
    for i in data_commands:
        if str(resul_name) in str(i.devices_brand.name).lower():
            result_comand.append({
                "command": i.command,
                "metod": i.method,
                "desc": i.description
                })
    session.close()
    return result_comand

