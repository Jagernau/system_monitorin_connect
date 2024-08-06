import json

from thrif.dispatch.server.thrif.backend.DispatchBackend import Client


def save_to_json(data, file_name: str):
    """ 
    Сохранение данных в JSON
    """
    with open(f'json_data/{file_name}.json', 'w', encoding='utf-8') as file:
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
                first_json[attr] = value

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
        
            
            
    
