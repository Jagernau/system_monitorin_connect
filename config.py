from dotenv import dotenv_values

val = dotenv_values(".env")

GLONASS_LOGIN = str(val["GLONASS_LOGIN"])
GLONASS_PASSWORD = str(val["GLONASS_PASSWORD"])
GLONASS_BASED_ADRESS = str(val["GLONASS_BASED_ADRESS"])

SCOUT_TREEHUNDRED_LOGIN = str(val["SCOUT_TREEHUNDRED_LOGIN"])
SCOUT_TREEHUNDRED_PASSWORD = str(val["SCOUT_TREEHUNDRED_PASSWORD"])
SCOUT_TREEHUNDRED_BASED_ADRESS = str(val["SCOUT_TREEHUNDRED_BASED_ADRESS"])
SCOUT_TREEHUNDRED_BASE_TOKEN = str(val["SCOUT_TREEHUNDRED_BASE_TOKEN"])

GELIOS_BASED_ADRES = str(val["GELIOS_BASED_ADRES"])
GELIOS_LOGIN = str(val["GELIOS_LOGIN"])
GELIOS_PASSWORD = str(val["GELIOS_PASSWORD"])

FORT_LOGIN = str(val["FORT_LOGIN"])
FORT_PASSWORD = str(val["FORT_PASSWORD"])
FORT_BASED_ADRESS = str(val["FORT_BASED_ADRESS"])

ERA_LOGIN = str(val["ERA_LOGIN"])
ERA_PASSWORD = str(val["ERA_PASSWORD"])
ERA_BASED_ADRESS = str(val["ERA_BASED_ADRESS"])
ERA_PORT = str(val["ERA_PORT"])

SCOUT_LOCAL_LOGIN = str(val["SCOUT_LOCAL_LOGIN"])
SCOUT_LOCAL_PASSWORD = str(val["SCOUT_LOCAL_PASSWORD"])
SCOUT_LOCAL_BASED_ADRESS = str(val["SCOUT_LOCAL_BASED_ADRESS"])
SCOUT_LOCAL_PORT = str(val["SCOUT_LOCAL_PORT"])

WIALON_LOCAL_TOKEN = str(val["WIALON_LOCAL_TOKEN"])
WIALON_LOCAL_BASED_ADRESS = str(val["WIALON_LOCAL_BASED_ADRESS"])
WIALON_LOCAL_PORT = str(val["WIALON_LOCAL_PORT"])

WIALON_HOSTING_TOKEN = str(val["WIALON_HOSTING_TOKEN"])
WIALON_HOSTING_BASED_ADRESS = str(val["WIALON_HOSTING_BASED_ADRESS"])
WIALON_HOSTING_PORT = str(val["WIALON_HOSTING_PORT"])


