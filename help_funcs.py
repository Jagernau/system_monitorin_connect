import json

def save_to_json(data, file_name: str):
    """ 
    Сохранение данных в JSON
    """
    with open(f'json_data/{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def conversion_class_to_json(data):
    """ 
    Преобразование данных из классов в JSON
    """
    final_json = []

    for item in data:
        first_json = {}

        # Получаем атрибуты объекта
        attributes = dir(item)

        # Фильтруем аттрибуты, исключаем нежелательные
        clear_attributes = [
                attr for attr in attributes 
                if "_" not in attr and "read" not in attr and "write" not in attr and "validate" not in attr]
        
        for attr in clear_attributes:
            value = getattr(item, attr)

            # Проверяем тип значения и добавляем в JSON
            if isinstance(value, (str, int)):
                first_json[attr] = value
                
            else:
                two_json = []
                two_clear = [attr for attr in dir(value) if "_" not in attr and "read" not in attr and "write" not in attr and "validate" not in attr]
                for tw in two_clear:

                    value_two = getattr(value, tw)
                    if isinstance(value_two, (str, int)):
                        two_json.append({f'{tw}': str(value_two)})
                    else:
                        two_json.append({f"{tw}": str(value_two)})

                first_json[attr] = two_json

        final_json.append(first_json)

    return final_json
        

        
    
