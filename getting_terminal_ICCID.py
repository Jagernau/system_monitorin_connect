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

# Запрос всех АГАТА

def get_iccid_imei_comand(
        objs, 
        usrs, 
        name_cl,
        limitation,
        comand_name,
        terminal_comand,
        addit_check=''
        ):
    """
    Получение всех ICCID, IMEI
    ob: Объекты wialon
    usrs: Юзеры wialon
    name_cl: Имя создателя объектов в Wialon (login)
    limitation: Лимит созданных объектов
    addit_check: Дополнительная проверка
    """
    sort_objs = sorting_obj_from_cl_name(data_objs=objs["items"], data_usrs=usrs["items"], name_cl=name_cl)
    count = 0 # Счётчик созданных объектов

    super_sort = sorted(sort_objs, key=lambda x: x['id'])

    for obj in tqdm.tqdm(super_sort, desc="Процесс получения ICCID..."):
        obj_id = obj['id']
        obj_imei = obj["uid"]
        obj_name = obj["nm"]

        if str(addit_check) not in obj["nm"]:
            continue

        with open('requested_terms.txt') as f:
            req_obj: list = f.read().split("\n")

        if str(obj_imei) in req_obj:
            continue

        count += 1 # Счётчик созданных объектов
        if count > int(limitation):
            break

        try:
            create_result = wialon_hosting.create_terminal_comand(wialon_hosting_token, obj_id, comand_name, terminal_comand)
            my_logger.logger.info(f"Созданна команда {create_result}")

        except (Exception, WialonError, SdkException) as e:
                my_logger.logger.error(e)

        finally:

            try:
                exec_result = wialon_hosting.exec_terminal_comand(wialon_hosting_token, obj_id, comand_name)
                my_logger.logger.info(f"Отправленна команда {exec_result}")
            except (Exception, WialonError, SdkException) as e:
                my_logger.logger.error(e)


            # finally:
        # request_time = int(get_current_unix_time()) - 3000
        # try:
        #     wialon_message_comand = wialon_hosting.get_last_masseges_data(wialon_hosting_token, obj_id, request_time)
        #     my_logger.logger.info(f"Ответ получен")
        # except (Exception, WialonError, SdkException) as e:
        #     my_logger.logger.error(e)
        # else:
        #     result_message = search_get_comand_result(wialon_message_comand)
        #     if result_message != None:
        #         with open("AGAT_Connect_IMEI_ICCID_NAME.txt", "a") as f:
        #             f.write(f"{obj_id};{obj_imei};{result_message};{obj_name}\n")
        #         with open("requested_terms.txt", "a") as f:
        #             f.write(f"{obj_imei}\n")



if __name__ == "__main__":


    # Получение всех Объектов, Пользователей, Типов терминалов
    try:
        objs = wialon_hosting.get_all_units(wialon_hosting_token)
        usrs = wialon_hosting.get_all_users(wialon_hosting_token)

    # Если в подключении к Wialon возникла ошибка
    except:
        # Объекты из файла JSON
        with open('reserv_json_data/wialon_hosting_all_objects.json', 'r', ) as file:
            file_obj = json.load(file)
        objs = file_obj


        # Пользователи из файла JSON
        with open('reserv_json_data/wialon_hosting_all_users.json', 'r', ) as file:
            file_usr = json.load(file)
        usrs = file_usr

#    dop_check = 'pagat_log'
    name_cl = "agat_autokonnekt" # Логин создателя объектов в Wialon
    limitation = 3000 # Ограничение выгрузки
    comand_name = "GET_ICCID"
    terminal_comand = "*?ICCID"
    

    get_iccid_imei_comand(
              objs=objs, 
              usrs=usrs, 
              name_cl=name_cl,
              limitation=limitation,
              comand_name=comand_name,
              terminal_comand=terminal_comand,
              addit_check=''
            )
    sys.exit()

