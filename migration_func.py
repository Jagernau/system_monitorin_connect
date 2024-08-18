from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import sorting_obj_from_cl_name, save_to_json
from glonasssoft import glonass_units, token
import my_logger
import tqdm
import sys


# Миграция написанна

def migration(
        objs, 
        usrs, 
        parent_Id, 
        model_id, 
        name_cl, 
        token, 
        limitation: int = 3
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

            # Перекладывание полей
            if len(obj['flds']) >= 1:
                fields = []
                for i in obj['flds']:
                    fields.append(
                            {
                            'name': str(obj["flds"][i]['n']),
                            'value': str(obj["flds"][i]['v']),
                            'forClient': True,
                            'forReport': True,
                            'id': "ae955b54-0c15-4a41-b920-3c3aefc87a15"
                            }
                    )
            else:
                fields = None

            try:
                result = glonass_units.create_unit(token, 
                                          parentId=parent_Id, 
                                          name=obj["nm"] + "_тест", 
                                          imei=obj["uid"], 
                                          device_type=31, 
                                          model_id=model_id,
                                          fields=fields
                                          )
                my_logger.logger.info(f"Объект {obj['nm']}, создан {result}")
                with open("created.txt", "a") as f:
                    f.write(f"{obj['id']}\n")

            except Exception as e:
                my_logger.logger.error(e)
                with open("not_created.txt", "a") as f:
                    f.write(f"{obj['id']}\n")


if __name__ == "__main__":


# Получение всех Объектов Клиента Виалон
    objs = wialon_hosting.get_all_units(wialon_hosting_token)
    usrs = wialon_hosting.get_all_users(wialon_hosting_token)

# Сортировка по имени создателя
    parent_Id = "d086bd30-cf71-49da-8781-8cdb167007bb"
    name_cl = "agat"
    token_gl = token
    model_id="2a8c306b-fad0-45ff-addd-1bb0cdaea344"

# Миграция
    migration(objs, usrs, parent_Id, model_id, name_cl, token_gl)
    sys.exit()

