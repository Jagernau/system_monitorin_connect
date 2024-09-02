#from dotenv import dotenv_values
from os import environ as envi


#val = dotenv_values(".env")

GLONASS_LOGIN = envi.get("GLONASS_LOGIN")
GLONASS_PASSWORD = envi.get("GLONASS_PASSWORD")
GLONASS_BASED_ADRESS = envi.get("GLONASS_BASED_ADRESS")

SCOUT_TREEHUNDRED_LOGIN = envi.get("SCOUT_TREEHUNDRED_LOGIN")
SCOUT_TREEHUNDRED_PASSWORD = envi.get("SCOUT_TREEHUNDRED_PASSWORD")
SCOUT_TREEHUNDRED_BASED_ADRESS = envi.get("SCOUT_TREEHUNDRED_BASED_ADRESS")
SCOUT_TREEHUNDRED_BASE_TOKEN = envi.get("SCOUT_TREEHUNDRED_BASE_TOKEN")

GELIOS_BASED_ADRES = envi.get("GELIOS_BASED_ADRES")
GELIOS_LOGIN = envi.get("GELIOS_LOGIN")
GELIOS_PASSWORD = envi.get("GELIOS_PASSWORD")

FORT_LOGIN = envi.get("FORT_LOGIN")
FORT_PASSWORD = envi.get("FORT_PASSWORD")
FORT_BASED_ADRESS = envi.get("FORT_BASED_ADRESS")

ERA_LOGIN = envi.get("ERA_LOGIN")
ERA_PASSWORD = envi.get("ERA_PASSWORD")
ERA_BASED_ADRESS = envi.get("ERA_BASED_ADRESS")
ERA_PORT = envi.get("ERA_PORT")

SCOUT_LOCAL_LOGIN = envi.get("SCOUT_LOCAL_LOGIN")
SCOUT_LOCAL_PASSWORD = envi.get("SCOUT_LOCAL_PASSWORD")
SCOUT_LOCAL_BASED_ADRESS = envi.get("SCOUT_LOCAL_BASED_ADRESS")
SCOUT_LOCAL_PORT = envi.get("SCOUT_LOCAL_PORT")

WIALON_LOCAL_TOKEN = envi.get("WIALON_LOCAL_TOKEN")
WIALON_LOCAL_BASED_ADRESS = envi.get("WIALON_LOCAL_BASED_ADRESS")
WIALON_LOCAL_PORT = envi.get("WIALON_LOCAL_PORT")

WIALON_HOSTING_TOKEN = envi.get("WIALON_HOSTING_TOKEN")
WIALON_HOSTING_BASED_ADRESS = envi.get("WIALON_HOSTING_BASED_ADRESS")
WIALON_HOSTING_PORT = envi.get("WIALON_HOSTING_PORT")

MTS_API_SMS_LOGIN=envi.get("MTS_API_SMS_LOGIN")
MTS_API_SMS_PASSWORD=envi.get("MTS_API_SMS_PASSWORD")
MTS_API_SMS_NAMING=envi.get("MTS_API_SMS_NAMING")
MTS_API_SMS_TEST_TEL=envi.get("MTS_API_SMS_TEST_TEL")


# MYSQL
DB_HOST=envi.get('DB_HOST')
MYSQL_USER=envi.get('MYSQL_USER')
MYSQL_DB_NAME=envi.get('MYSQL_DB_NAME')
MYSQL_PASSWORD=envi.get('MYSQL_PASSWORD')
MYSQL_PORT=envi.get('MYSQL_PORT')

connection_mysql = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{DB_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}"

API_TOKEN=envi.get('API_TOKEN')

