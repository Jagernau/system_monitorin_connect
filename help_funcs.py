import json
def save_to_json(data, file_name: str):
    with open(f'json_data/{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
