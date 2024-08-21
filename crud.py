
import mysql_models as models
from db_connect import MysqlDatabase


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

