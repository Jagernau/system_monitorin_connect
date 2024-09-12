from time import sleep
import requests
from requests.auth import HTTPBasicAuth

import config
import json

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
    result = resp.json()

    with open("sends_messages.txt", "a") as f:
        f.write(f"{result}\n")

    return result
     
def check_message(login, password, message_id):
   url = 'https://omnichannel.mts.ru/http-api/v1/messages/info'
   body = {"int_ids": [message_id]}
   resp_info = requests.post(url , json=body, auth=HTTPBasicAuth(login, password))      
   return resp_info.json()
  




# # Параметры отправки
# login = config.MTS_API_SMS_LOGIN
# password = config.MTS_API_SMS_PASSWORD
# naming = config.MTS_API_SMS_NAMING
# text_message = '*!EDITS TRANS:SRV1(FLEX,,,gw1.glonasssoft.ru,15003)' # Команда на перезапись сервера на Глонассофт Навтелеком
# to = config.MTS_API_SMS_TEST_TEL
# # Отправка сообщения
# result_send = send_mts_message(login, password, naming, to, text_message)
# extracted_mess_id = result_send['messages'][0]['internal_id']
# print(extracted_mess_id)
# sleep(1)
# result_check = check_message(login, password, extracted_mess_id)
# print(type(result_check["events_info"][0]["events_info"][0]["status"]))


