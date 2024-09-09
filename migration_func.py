from time import sleep
from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import (
        sorting_obj_from_cl_name,
        save_to_json, 
        adapt_wialon_fields_to_glonass,
        adapt_wialon_devices_to_glonass
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

# Миграция написанна

def migration(
        objs, 
        usrs, 
        parent_Id, 
        model_id, 
        name_cl, 
        token, 
        limitation: int,
        sms_api_login: str,
        sms_api_password: str,
        sms_api_name: str,
        sms_comand: str,
        comand_name,
        wialon_devices_types,
        addit_check=''
        ):
    """
    Миграция объектов на Глонассофт
    Создаёт копии объектов в Глонассофт
    obj: Объекты wialon
    usrs: Юзеры wialon
    parentId: ID родителя Глонассофт (Клиент)
    model_id: ID модели объекта Глонассофт
    name_cl: Имя создателя объектов в Wialon (login)
    token: Токен Глонассофт
    limitation: Лимит созданных объектов
    sms_api_login: Логин для отправки СМС
    sms_api_password: Пароль для отправки СМС
    sms_api_name: Имя для отправки СМС
    sms_comand: Команда для перепрограммирования
    wialon_devices_types: Типы оборудования Wialon
    addit_check: Дополнительная проверка
    """
    sort_objs = sorting_obj_from_cl_name(data_objs=objs["items"], data_usrs=usrs["items"], name_cl=name_cl)

    count = 0 # Счётчик созданных объектов

    for obj in tqdm.tqdm(sort_objs, desc="Процесс миграции..."):

        # проверяет наличие ID объекта в файле
        with open('created.txt') as f:
            created_obj: list = f.read().split("\n")

        # пропускает итерацию если такой объект есть в файле
        if str(obj['id']) in created_obj:
            continue

        
        if str(addit_check) in obj["nm"]:

            count += 1 # Счётчик созданных объектов
            if count > int(limitation):
                break

            # Перенос произвольных полей в Глонассофт
            # Из Wialon
            fields_comments = adapt_wialon_fields_to_glonass(obj)

            # Функция сопоставления оборудования
            #Из Wialon в Глонассофт
            glonass_devices = devices_types.get_all_devices_types(token)
            wialon_devices = wialon_devices_types
            wialon_obj_device_type = obj["hw"]
            adapt_device_type_to_glonass = adapt_wialon_devices_to_glonass(wialon_devices, glonass_devices, wialon_obj_device_type) # адаптация типа терминала под Глонассофт


            # если тип терминала не определился, делаем по BCE -- 64
            adap_type = int(adapt_device_type_to_glonass) if adapt_device_type_to_glonass != None else int(64)

            # Работа с датчиками
            # Датчик зажигания по умолчанию
            moto_sensor = [
            {
              "kind": "Simple",
              "type": "Ignition",
              "name": "Зажигание (0)",
              "inputType": "Digital",
              "inputNumber": 0,
              "isInverted": False,
              "disabled": False,
              "gradeType": "Digital",
              "showInTooltip": True,
              "showLastValid": False,
              "showAsDutOnGraph": False,
              "showWithoutIgn": True,
              "agrFunction": "SUM",
              "customParams": {
                "RemoveCode": "",
                "RemoveSeconds": "",
                "ValueOn": "Вкл.",
                "ValueOff": "Выкл."
              },
              "summaryMaxValue": None,
              "valueIntervals": []
            },
            ]



            # Создание объекта в Глонассофт
            try:
                result = glonass_units.create_unit(token, 
                                          parentId=parent_Id, 
                                          name=obj["nm"] + "_тест", 
                                          imei=obj["uid"], 
                                          device_type=adap_type, 
                                          model_id=model_id,
                                          fields=fields_comments,
                                          sensors=moto_sensor
                                          )
                my_logger.logger.info(f"Объект {obj['nm']}, создан {result}")
                with open("created.txt", "a") as f:
                    f.write(f"{obj['id']}\n")

            except Exception as e:
                my_logger.logger.error(e)
                with open("not_created.txt", "a") as f:
                    f.write(f"{obj['id']}\n")

            # Блок перепрограммирования терминала
            try:
                # Получение телефона из базы данных такого imei
                tel_num = crud.get_db_sim_tel_from_imei(imei=obj["uid"])

                if tel_num is not None:
                    try:
                        mts_send_mes__2.send_mts_message(login=sms_api_login,
                                                         password=sms_api_password,
                                                         naming=sms_api_name,
                                                         to=tel_num,
                                                         text_message=sms_comand)
                        my_logger.logger.info(f"Сообщение {obj['nm']}, отправлено {tel_num}")
                        sleep(5)
                        with open("send_sms.txt", "a") as f:
                            f.write(f"{obj['id']} {obj['uid']} {tel_num}\n")

                    except Exception as e:
                        my_logger.logger.error(e)
                        with open("not_send_sms.txt", "a") as f:
                            f.write(f"{obj['id']} {obj['uid']} {tel_num}\n")
                
                # если нет телефона в БД_2, перепрограммируем через API Wialon
                else:
                    terminal_reprog.reprog_terminal(
                            obj["id"],
                            comand_name=comand_name,
                            terminal_comand=sms_comand
                            )

            except Exception as e:
                my_logger.logger.error(e)



if __name__ == "__main__":


    # Получение всех Объектов, Пользователей, Типов терминалов
    try:
        objs = wialon_hosting.get_all_units(wialon_hosting_token)
        usrs = wialon_hosting.get_all_users(wialon_hosting_token)
        wialon_devices = wialon_hosting.get_all_device_types(wialon_hosting_token)

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


        # Типы терминалов из файла JSON
        with open('reserv_json_data/wialon_hosting_device_types.json', 'r', ) as file:
            file_types = json.load(file)
        wialon_devices = file_types



    parent_Id = "adb3a85c-b79e-44c1-bce5-dce6ef3ac00b" # ID клиента Глонассофт
    name_cl = "test_IT" # Логин создателя объектов в Wialon
    token_gl = token
    model_id="d2c04fab-093a-4d35-a1f2-432a168800cb" # ID модели ТС
    limitation = 10 # Ограничение выгрузки
    sms_api_login = config.MTS_API_SMS_LOGIN
    sms_api_password = config.MTS_API_SMS_PASSWORD
    sms_api_name = config.MTS_API_SMS_NAMING
    sms_comand = '*!EDITS TRANS:SRV1(FLEX,,,gw1.glonasssoft.ru,15003)'
    comand_name = "REPROG_SERV"
    dop_check = 'test_'


    # Миграция
    migration(
            objs=objs, 
            usrs=usrs, 
            parent_Id=parent_Id,
            model_id=model_id, 
            name_cl=name_cl,
            token=token_gl,
            limitation=limitation,
            sms_api_login=sms_api_login,
            sms_api_password=sms_api_password,
            sms_api_name=sms_api_name,
            sms_comand=sms_comand,
            comand_name=comand_name,
            wialon_devices_types=wialon_devices,
            addit_check=dop_check
            )
    sys.exit()

