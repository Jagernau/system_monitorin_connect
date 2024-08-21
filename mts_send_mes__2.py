import requests
from requests.auth import HTTPBasicAuth

import config

def send_mts_message(login, password, naming, to, text_message):
    """ 
    Отправляет сообщение-команду на терминал по СМС API
    login: Логин МТС АПИ
    password: ПАРОЛЬ МТС АПИ
    naming: Имя отправителя МТС АПИ
    to: Номер телефона куда
    text_message: Команда
    """
    url = 'https://omnichannel.mts.ru/http-api/v1/messages'
    body = {
    "messages": [
    {
    "content": {
    "short_text": text_message
    },
    "from": {
    "sms_address": naming
    },
    "to": [
    {
    "msisdn": to
    }
    ]
    }]
    }
    resp = requests.post(url , json=body, auth = HTTPBasicAuth(login, password))
    result = resp.json()['messages'][0]['internal_id']

    with open("sends_messages.txt", "a") as f:
        f.write(f"{result}\n")

    return result
     
def check_message(login, password, message_id):
   url = 'https://omnichannel.mts.ru/http-api/v1/messages/info'
   body = {"int_ids": [str(message_id)]}
   resp_info = requests.post(url , json=body, auth = HTTPBasicAuth(login, password))      
   return resp_info.text  
  
# def check_message__get(login, password, naming, message_id):
#     """Не работает"""
#     url = "https://api-adapter.marketolog.mts.ru/get/sms-info"
#
#     querystring = {
#         "login": login,
#         "password": password,
#         "msg_ids": message_id,
#         "from": naming
#     }
#
#     response = requests.request("GET", url, params=querystring)
#     return response.text

# Параметры отправки
login = config.MTS_API_SMS_LOGIN
password = config.MTS_API_SMS_PASSWORD
naming = config.MTS_API_SMS_NAMING
text_message = '*!EDITS TRANS:SRV1(FLEX,,,gw1.glonasssoft.ru,15003)' # Команда на перезапись сервера на Глонассофт Навтелеком
to = config.MTS_API_SMS_TEST_TEL
# Отправка сообщения
message_id = send_mts_message(login, password, naming, to, text_message)
print(message_id)
