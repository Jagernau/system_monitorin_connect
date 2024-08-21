from time import sleep
from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import sorting_obj_from_cl_name, save_to_json, adapt_wialon_fields_to_glonass
from glonasssoft import glonass_units, token
import my_logger
import tqdm
import sys
import crud
import mts_send_mes__2
import config

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
        sms_comand: str
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

        if "agat" in obj["nm"]:

            count += 1 # Счётчик созданных объектов
            if count > int(limitation):
                break

            # Перенос произвольных полей в Глонассофт
            # Из Wialon
            fields_comments = adapt_wialon_fields_to_glonass(obj)

            # Создание объекта в Глонассофт
            try:
                result = glonass_units.create_unit(token, 
                                          parentId=parent_Id, 
                                          name=obj["nm"] + "_тест", 
                                          imei=obj["uid"], 
                                          device_type=31, 
                                          model_id=model_id,
                                          fields=fields_comments
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

            except Exception as e:
                my_logger.logger.error(e)



if __name__ == "__main__":


# Получение всех Объектов Клиента Виалон
    objs = wialon_hosting.get_all_units(wialon_hosting_token)
    usrs = wialon_hosting.get_all_users(wialon_hosting_token)

    parent_Id = "d086bd30-cf71-49da-8781-8cdb167007bb"
    name_cl = "  " # Логин создателя объектов в Wialon
    token_gl = token
    model_id="2a8c306b-fad0-45ff-addd-1bb0cdaea344"
    limitation = 10
    sms_api_login = config.MTS_API_SMS_LOGIN
    sms_api_password = config.MTS_API_SMS_PASSWORD
    sms_api_name = config.MTS_API_SMS_NAMING
    sms_comand = '*!EDITS TRANS:SRV1(FLEX,,,gw1.glonasssoft.ru,15003)'


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
            sms_comand=sms_comand
            )
    sys.exit()

