from time import sleep

from wialon.sdk import WialonError, SdkException
from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import (
        get_current_unix_time,
        search_get_comand_result,
                        )
import my_logger

def reprog_terminal(
        obj_id, 
        comand_name,
        terminal_comand,
        ):
    """
    obj_id: Объекты wialon
    comand_name: Название команды
    terminal_comand: Команда на терминал
    """
    try:
        create_result = wialon_hosting.create_terminal_comand(
                wialon_hosting_token,
                obj_id,
                comand_name,
                terminal_comand
                )
        my_logger.logger.info(f"Созданна команда {create_result}")

    except (Exception, WialonError, SdkException) as e:
        my_logger.logger.error("Произошла ошибка при формировании команды: " + str(e))
    try:
                exec_result = wialon_hosting.exec_terminal_comand(
                        wialon_hosting_token, 
                        obj_id, 
                        comand_name
                        )
                my_logger.logger.info(f"Отправленна команда {exec_result}")
    except (Exception, WialonError, SdkException) as e:
        my_logger.logger.error("Произошла ошибка при отправки команды: " + str(e))
        return False
    try:
        sleep(5)
        request_time = int(get_current_unix_time()) - 300
        wialon_message_comand = wialon_hosting.get_last_masseges_data(
                wialon_hosting_token, 
                obj_id, 
                request_time
                )
        result_message = search_get_comand_result(wialon_message_comand)
        if result_message != None:
            return True
        else:
            return False

    except (Exception, WialonError, SdkException) as e:
                my_logger.logger.error(e)
                return False







