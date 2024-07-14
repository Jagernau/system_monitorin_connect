import json


def collect_keys    (data, keys=None):
    """ 
    Функция для получения всех ключей
    :param data: dict
    :param keys: set
    :return: set
    """
    if keys is None:
        keys = set()
    
    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            collect_keys(value, keys)
    elif isinstance(data, list):
        for item in data:
            collect_keys(item, keys)
    
    return keys

with open('glonass_vehicles.json', 'r') as file:
    json_data = json.load(file)

keys = collect_keys(json_data)

# save to text file, split by \n ", "
with open('all_keys_glonass_vehicles.txt', 'w') as file:
    file.write('\n'.join(keys))


def collect_level_keys(data, keys=None, structure=None, level=0):
    """ 
    Функция для получения всех ключей и уровней
    :param data: dict
    :param keys: set
    :param structure: dict
    :param level: int
    :return: set, dict
    """
    if keys is None:
        keys = set()
    if structure is None:
        structure = {}
    
    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            structure[key] = {"level": level}
            collect_level_keys(value, keys, structure[key], level + 1)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            keys.add(str(i))
            structure[str(i)] = {"level": level}
            collect_level_keys(item, keys, structure[str(i)], level + 1)
    
    return keys, structure

# save to json file
with open('all_keys_glonass_vehicles.json', 'w') as file:
    json.dump(collect_level_keys(json_data)[1], file, indent=4)
