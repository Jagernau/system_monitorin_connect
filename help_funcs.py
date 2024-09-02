import json

from datetime import datetime, timezone, timedelta

import datetime as dt

import time

from jsonpath_ng import jsonpath, parse

def save_to_json(data, file_name: str):
    """ 
    Сохранение данных в JSON
    """
    with open(f'json_data/{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def reserv_data_to_json(data, file_name: str):
    """ 
    Сохранение данных в JSON для резервного восстановления
    """
    with open(f'reserv_json_data/{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def converting(data):
    """ 
    Конвертация в JSON
    """
    def clear_attr(items):
        return [
                attr for attr in dir(items)
                if "_" not in attr and "read" not in attr and "write" not in attr and "validate" not in attr]

    final_json = []

    for item in data:
        first_json = {}

        # Фильтруем аттрибуты, исключаем нежелательные
        clear_attributes = clear_attr(item)
        
        for attr in clear_attributes:
            value = getattr(item, attr)

            if value is None:
                first_json[attr] = None

            elif isinstance(value, (str, int, float, bool)):
                first_json[attr] = value

            elif isinstance(value, list):
                if len(value) >= 1 and isinstance(value[0], (str, int, float, bool)):
                    first_json[attr] = value
                else:
                    first_json[attr] = converting(value)

            elif isinstance(value, dict):
                first_json[attr] = value
                
            else:
                two_json = []
                two_clear = clear_attr(value)

                for tw in two_clear:

                    value_two = getattr(value, tw)

                    if value_two is None:
                        two_json.append({f'{tw}': None})

                    elif isinstance(value_two, (str, int, float, bool)):
                        two_json.append({f'{tw}': value_two})

                    elif isinstance(value_two[0], str):
                        two_json.append({f'{tw}': value_two})

                    else:
                        two_json.append({f"{tw}": converting(value_two)})

                first_json[attr] = two_json

        final_json.append(first_json)

    return final_json
        
            
            

def current_time():
    """ 
    Получение текущего времени, но + 3 часа тк время линукс всегда меньше на 3часа
    """
    current_time = datetime.now(timezone.utc)

    new_time = current_time + timedelta(hours=3)

    # Форматируем время в нужный формат
    formatted_time = new_time.strftime('%Y-%m-%dT%H:%M:%S')
    return formatted_time

def current_time_past_tree():
    """ 
    Получение прошедшего времени, но - 3 часа
    """
    current_time = datetime.now(timezone.utc)

    new_time = current_time - timedelta(hours=3)

    # Форматируем время в нужный формат
    formatted_time = new_time.strftime('%Y-%m-%dT%H:%M:%S')
    return formatted_time


def get_current_timestamp_utc() -> str:
    now = dt.datetime.utcnow()
    timestamp = "/Date(" + str(int(now.timestamp() * 1000)) + ")/"
    return timestamp


def sorting_obj_from_cl_name(data_objs, data_usrs, name_cl):
    sorted_objs = []
    for obj in data_objs:
        for usr in data_usrs:
            if obj["crt"] == usr['id'] and name_cl in usr['nm']:
                sorted_objs.append(obj)

    return sorted_objs

def adapt_wialon_fields_to_glonass(wialon_obj):
    """ 
    Преобразование из Wialon полей в Глонассофт
    wialon_obj: Объект Wialon
    return: произвольные поля в Глонассофт
    """

    fields_comments = None
    # Перекладывание полей
    if len(wialon_obj['flds']) >= 1:
        fields_comments = []
        for i in wialon_obj['flds']:
            fields_comments.append(
                    {
                    'name': str(wialon_obj["flds"][i]['n']),
                    'value': str(wialon_obj["flds"][i]['v']).replace('"', ' ') if str(wialon_obj["flds"][i]['v']) != "" else "_",
                    'forClient': True,
                    'forReport': True
                    }
            )
    return fields_comments

def remove_digits(input_string):
    """
    Удаляет все цифры из строки.
    
    input_string: str - входная строка
    Возвращает: str - строка без цифр
    """
    return input_string.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '')



def adapt_wialon_devices_to_glonass(wialon_types, glonass_types, curent_obj_type):
    """ 
    Выдаёт тип терминала для Glonasssoft соответствующий Wialon -> int|none
    wialon_types: типы терминалов Wialon
    glonass_types: типы терминалов Glonasssoft
    curent_obj_type: текущий тип терминала: int
    """
    similar_device_types = []
    for wialon_type in wialon_types:
        if curent_obj_type == wialon_type['id']:
            name_type_device_first_val = str(wialon_type['name']).split(' ')[0]
            for glonass_type in glonass_types:
                if remove_digits(name_type_device_first_val.lower()) in glonass_type['deviceTypeName'].lower():
                    similar_device_types.append(glonass_type["deviceTypeId"])

    if len(similar_device_types) >= 1:
        return similar_device_types[0]

    else:
        return None


def get_current_unix_time():
    # Получаем текущее время в формате Unix
    unix_time = int(time.time())
    return unix_time


def subtract_time_from_unix(unix_time, seconds):
    """
    Уменьшает заданное количество секунд от метки времени Unix.

    :param unix_time: Время в формате Unix (количество секунд с 1 января 1970 года).
    :param seconds: Количество секунд, которое нужно вычесть.
    :return: Обновленная метка времени Unix.
    """
    return unix_time - seconds

def search_get_comand_result(json_data):
    result = []
    for i in json_data["messages"]:
        if "cmd_ans" in i["p"]:
            result.append(i["p"]["cmd_ans"])
        
    if len(result) >= 1:
        return result[-1]

    else:
        return None


