from time import sleep

from wialon.sdk import WialonError, SdkException
from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import (
        sorting_obj_from_cl_name,
        get_current_unix_time,
        search_get_comand_result,
                        )
import my_logger
import tqdm
import sys
import config
import json

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
        my_logger.logger.error(e)
    try:
                exec_result = wialon_hosting.exec_terminal_comand(
                        wialon_hosting_token, 
                        obj_id, 
                        comand_name
                        )
                my_logger.logger.info(f"Отправленна команда {exec_result}")
    except (Exception, WialonError, SdkException) as e:
                my_logger.logger.error(e)





