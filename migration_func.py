from wialon_host import wialon_hosting, wialon_hosting_token
from help_funcs import sorting_obj_from_cl_name, save_to_json
from glonasssoft import glonass_units, token


# Получение всех Объектов Клиента Виалон
objs = wialon_hosting.get_all_units(wialon_hosting_token)
usrs = wialon_hosting.get_all_users(wialon_hosting_token)

sort_objs = sorting_obj_from_cl_name(data_objs=objs["items"], data_usrs=usrs["items"], name_cl="agat")
# print(sort_objs)
# save_to_json(sort_objs, "sorted_wialon_host__by_agat")

# Создание объекта в Глонасс
# print(glonass_units.create_unit(
#         token, 
#         parentId="d086bd30-cf71-49da-8781-8cdb167007bb", 
#         name="py_api_migrate_test_тест", 
#         imei="777", 
#         device_type=31, 
#         model_id="2a8c306b-fad0-45ff-addd-1bb0cdaea344"
#         ))


# Миграция написанна
for obj in sort_objs:
    count = 1
    if "agat" in obj["nm"]:
        count += 1
        print(glonass_units.create_unit(token, 
                                  parentId="d086bd30-cf71-49da-8781-8cdb167007bb", 
                                  name=obj["nm"], 
                                  imei=obj["uid"], 
                                  device_type=31, 
                                  model_id="2a8c306b-fad0-45ff-addd-1bb0cdaea344", 
                                  ))
    if count >= 10:
        break

