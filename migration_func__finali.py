import os
from time import sleep
from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import (
    sorting_obj_from_cl_name,
    save_to_json, 
    adapt_wialon_fields_to_glonass,
    adapt_wialon_devices_to_glonass,
    get_wialon_devices_name
)
from glonasssoft import glonass_units, token, devices_types 
import my_logger
import tqdm
import sys
import crud
import mts_send_mes__2
import config
import json
import terminal_reprog
from wialon.sdk import WialonError, SdkException

# Constants
GLONASS_TOKEN = token
WIALON_HOSTING_TOKEN = wialon_hosting_token
PARENT_ID = "adb3a85c-b79e-44c1-bce5-dce6ef3ac00b"  # Glonass client ID
MODEL_ID = "d2c04fab-093a-4d35-a1f2-432a168800cb"  # Glonass model ID
LIMITATION = 50  # Object creation limit
SMS_API_LOGIN = config.MTS_API_SMS_LOGIN
SMS_API_PASSWORD = config.MTS_API_SMS_PASSWORD
SMS_API_NAME = config.MTS_API_SMS_NAMING
REPROG_DATA = {"adres": "gw1.glonasssoft.ru", "port": "15003"}
CONDIT_COMMAND = 'сервер на указанный'
NAME_CL = "test_"
DOP_CHECK = 'test_'
COMAND_NAME = "REPROG_SERV"


def load_data_from_wialon():
    """Загружает информацию из Wialon или из Файла резервной копии"""
    try:
        objs = wialon_hosting.get_all_units(WIALON_HOSTING_TOKEN)
        usrs = wialon_hosting.get_all_users(WIALON_HOSTING_TOKEN)
        wialon_devices = wialon_hosting.get_all_device_types(WIALON_HOSTING_TOKEN)
        my_logger.logger.info("Объекты из Wialon APi загруженны")
    except Exception:
        objs = _load_from_json('reserv_json_data/wialon_hosting_all_objects.json')
        usrs = _load_from_json('reserv_json_data/wialon_hosting_all_users.json')
        wialon_devices = _load_from_json('reserv_json_data/wialon_hosting_device_types.json')
        my_logger.logger.error("Объекты из Wialon APi загруженны из файла")
    return objs, usrs, wialon_devices


def _load_from_json(file_path: str):
    """
    Загрузка JSON из файла
    file_path: имя файла
    -> JSON
    """
    directory = file_path.split("/")[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
        my_logger.logger.error("Не было директории для резервных копий, директория была созданна")
    else:
        pass
    try:
        my_logger.logger.info("Загруженны данные из резервных копий")
        with open(file_path, 'r') as file:
            return json.load(file)
    except:
        my_logger.logger.error("Не загрузилась данные из резервных копий")
        print("Не загрузилась данные из резервных копий")
        print("Никаких данных нет из Wialon. Программа завершает работу")
        sys.exit()


def should_skip_full_object(obj_imei: str) -> bool:
    """
    Проверка есть ли полноценно созданный объект IMEI
    obj_imei: IMEI объекта
    -> BOOL
    """
    file_name = 'full_created.txt'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write("Файл созданн")
        my_logger.logger.error("Не было файла full_created.txt, файл созданн")
    else:
        pass

    with open(file_name) as f:
        created_objs = f.read().split("\n")
    return obj_imei in created_objs


def should_skip_not_full_object(obj_imei: str) -> bool:
    """
    Проверка есть ли не полноценно созданный объект IMEI
    obj_imei: IMEI объекта
    -> BOOL
    """
    file_name = 'not_full_created.txt'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write("Файл созданн")
        my_logger.logger.error("Не было файла not_full_created.txt, файл созданн")
    else:
        pass

    with open(file_name) as f:
        not_full_created_objs = f.read().split("\n")
    return obj_imei in not_full_created_objs


def get_ready_command(device_name, reprog_data, condit_com):
    """
    Отдаёт подготовленную команду для типа терминала
    device_name: название типа девайса вынутого из Wialon
    reprog_data: данные для изменения сырой команды
    condit_com: маска по какому условию нужно отфильтровать команду
    -> отдаёт полностью сформированную команду str|none
    """
    commands_from_device = crud.get_terminal_comand_from_wialon_types(device_name)
    clear_command = [cmd for cmd in commands_from_device if condit_com in cmd['desc']]
    if len(clear_command) == 0:
        my_logger.logger.error(f"Команда не найденна под {device_name}")
        return None

    my_logger.logger.info(f"Команда найденна под {device_name}")
    return clear_command[0]['command'].replace('XXX', reprog_data["adres"]).replace('YYY', reprog_data["port"])


def create_glonass_object_from_wialon(glonass_token, obj, adapt_fields_comments, adapt_type, adapt_sensors, prefix):
    """
    Создание объекта в Глонассофт
    token: Токен Глонассофт - str
    obj: Объект из Wialon - dict
    fields_comments: Адаптированные коментарии под Глонассофт от Виалон - []|None
    adapt_type: Адаптированный тип девайса - int|None
    adapt_sensors: Адаптированные сенсоры из Виалон - []|Датчик по умолчанию [] 
    """
    try:
        if str(prefix) == "_":
            result = glonass_units.create_unit(
                glonass_token,
                parentId=PARENT_ID,
                name=f"{obj['nm']}{prefix}",
                imei=obj["uid"],
                device_type=adapt_type,
                model_id=MODEL_ID,
                fields=adapt_fields_comments,
                sensors=adapt_sensors
            )
            my_logger.logger.info(f"Создан объект в Глонассофт и переведён {obj['nm']}_{prefix} {result}")
            with open('full_created.txt', "a") as f:
                f.write(f"{obj['uid']}\n")
        else:
            result = glonass_units.create_unit(
                glonass_token,
                parentId=PARENT_ID,
                name=f"{obj['nm']}{prefix}",
                imei=obj["uid"],
                device_type=adapt_type,
                model_id=MODEL_ID,
                fields=adapt_fields_comments,
                sensors=adapt_sensors
            )
            my_logger.logger.info(f"Создан объект в Глонассофт но не переведён {obj['nm']}{prefix} {result}")
            with open('not_full_created.txt', "a") as f:
                f.write(f"{obj['uid']}\n")

    except Exception as e:
        my_logger.logger.error(e)
        with open('not_created.txt', "a") as f:
            f.write(f"{obj['uid']}\n")

def del_val_from_non_full_obj(imei):
    """ 
    Удаление объекта из неполного списка
    imei: IMEI объекта
    """

    # Открываем файл для чтения
    file_name = 'not_full_created.txt'
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Записываем обратно все строки, кроме той, которую нужно удалить
    with open(file_name, 'w') as file:
        for line in lines:
            if line.strip('\n') != str(imei):
                file.write(line)


def reprogramming_sms(obj, tel_num, ready_command):
    """
    Перепрограммирование терминала через СМС, возвращает успешно ли перепрог Bool
    obj: объект Виалон - dict
    tel_num: номер телефона сим карты на терминале - 000000000
    ready_command: сформированная команда для перепрограммирования
    -> bool
    """
    login = SMS_API_LOGIN
    password = SMS_API_PASSWORD
    naming = SMS_API_NAME
    try:
        result_send = mts_send_mes__2.send_mts_message(
            login=login,
            password=password,
            naming=naming,
            to=tel_num,
            text_message=ready_command
        )
        extracted_mess_id = result_send['messages'][0]['internal_id']
        sleep(2)
        result_check = mts_send_mes__2.check_message(login, password, extracted_mess_id)
        if result_check["events_info"][0]["events_info"][0]["status"] == 200:
            my_logger.logger.info(f"Терминал с IMEI {obj['uid']} и Телефоном {tel_num} успешно перепрограмировался через СМС")
            return True
        else:
            my_logger.logger.info(f"Терминал с IMEI {obj['uid']} и Телефоном {tel_num} не перепрограмировался через СМС")
            return False
    except Exception as e:        
            my_logger.logger.error(f"Терминал с IMEI {obj['uid']} и Телефоном {tel_num} не перепрограмировался через СМС {e}")
            return False


def migration(
        glonass_token, 
        limitation: int,
        reprog_data: dict,
        comand_name,
        condit_command: str,
        addit_check=''
        ):
    """
    Миграция объектов на Глонассофт
    Создаёт копии объектов в Глонассофт
    token: Токен Глонассофт
    limitation: Лимит созданных объектов
    reprog_data: Адрес и порт для переноса куда переносится
    condit_command: Тип для комманды
    addit_check: Дополнительная проверка
    """
    # Получаем объекты, юзеров, типы девайсов из Wialon
    objs, usrs, wialon_devices = load_data_from_wialon()
    # Фильтруем объекты клиента по Логину
    filter_objs = sorting_obj_from_cl_name(data_objs=objs["items"], data_usrs=usrs["items"], name_cl=NAME_CL)
    # Фильтруем дополнительно список объектов по доп. параметру
    clear_filter_objs = [i for i in filter_objs if str(addit_check) in i['nm']]
    # Получаем типы девайсов Глонассофт
    glonass_devices = devices_types.get_all_devices_types(token)

    count = 0

    for obj in tqdm.tqdm(clear_filter_objs, desc="Процесс миграции..."):
        current_wialon_imei = obj["uid"]

        if should_skip_full_object(str(current_wialon_imei)):
            continue

        if count > int(limitation):
            break

        current_wialon_name = obj["nm"]
        current_wialon_id = obj["id"]
        current_wialon_device_type = obj["hw"]
        
        # Адаптация типа девайса на Глонассофт из Wialon int|none 
        adapt_device_type_to_glonass = adapt_wialon_devices_to_glonass(
                wialon_devices,
                glonass_devices, 
                current_wialon_device_type
                )
        adapt_device_type_to_glonass = int(adapt_device_type_to_glonass) if adapt_device_type_to_glonass != None else int(64)

        # Адаптация произвольных полей в Глонассофт -> []|none
        fields_comments = adapt_wialon_fields_to_glonass(obj)

        # Название модели девайса
        device_name = get_wialon_devices_name(wialon_devices, current_wialon_device_type)
        print(device_name)



        # Логика переноса
        prefix = "_"

        # Формировании команды для перепрограммирования
        ready_command = get_ready_command(
                device_name=device_name, 
                reprog_data=reprog_data, 
                condit_com=condit_command
                )
        if ready_command == None:
            prefix = "_ппрог"
        else:
            tel_num = crud.get_db_sim_tel_from_imei(imei=obj["uid"])
            if tel_num == None:
                result_command = terminal_reprog.reprog_terminal(
                        current_wialon_id,
                        comand_name=comand_name, 
                        terminal_comand=ready_command
                        )
                if result_command == False:
                    prefix = "_ппрог"
                else:
                    prefix = "_"
            else:
                result_reprog_sms = reprogramming_sms(
                        obj, 
                        tel_num, 
                        ready_command
                        )
                if result_reprog_sms == False:
                    result_command = terminal_reprog.reprog_terminal(
                            current_wialon_id,
                            comand_name, 
                            terminal_comand=ready_command
                            )
                    if result_command == False:
                        prefix = "_ппрог"
                    else:
                        prefix = "_"
                else:
                    prefix = "_"

        # Объект создаётся в любом случае
        # Но меняется префикс.


        if not should_skip_not_full_object(str(current_wialon_imei)):
            create_glonass_object_from_wialon(
                    glonass_token=glonass_token,
                    obj=obj, 
                    adapt_fields_comments=fields_comments,
                    adapt_type=adapt_device_type_to_glonass,
                    adapt_sensors=None,
                    prefix=prefix
                    )
        # если в файле имеется объект созданный в Глонасс, но не перепрограммированный
        # Начинаем заново.
        else:
            tqdm.tqdm.write(f"Пытаюсь перепрограммировать {current_wialon_name} (IMEI: {current_wialon_imei}) который до этого не перепрограммировался, но был создан в Глонассофт")
            ready_command = get_ready_command(
                    device_name=device_name, 
                    reprog_data=reprog_data, 
                    condit_com=condit_command
                    )
            if ready_command == None:
                pass
            else:
                tel_num = crud.get_db_sim_tel_from_imei(imei=obj["uid"])
                if tel_num == None:
                    result_command = terminal_reprog.reprog_terminal(
                            current_wialon_id,
                            comand_name=comand_name, 
                            terminal_comand=ready_command
                            )
                    if result_command == False:
                        pass
                    else:
                        # вставить логику удаления из файла
                        del_val_from_non_full_obj(imei=current_wialon_imei)
                        with open('full_created.txt', 'a') as file:
                            file.write(f"{current_wialon_imei}\n")
                else:
                    result_reprog_sms = reprogramming_sms(
                            obj, 
                            tel_num, 
                            ready_command
                            )
                    if result_reprog_sms == False:
                        result_command = terminal_reprog.reprog_terminal(
                                current_wialon_id,
                                comand_name, 
                                terminal_comand=ready_command
                                )
                        if result_command == False:
                            pass
                        else:
                            # вставить логику удаления из файла
                            del_val_from_non_full_obj(imei=current_wialon_imei)
                            with open('full_created.txt', 'a') as file:
                                file.write(f"{current_wialon_imei}\n")
                    else:
                        # вставить логику удаления из файла
                        del_val_from_non_full_obj(imei=current_wialon_imei)
                        with open('full_created.txt', 'a') as file:
                            file.write(f"{current_wialon_imei}\n")



        count += 1


if __name__ == "__main__":
    migration(
            glonass_token=GLONASS_TOKEN, 
            limitation=LIMITATION, 
            reprog_data=REPROG_DATA, 
            comand_name=COMAND_NAME, 
            condit_command=CONDIT_COMMAND,
            addit_check=DOP_CHECK
            )


