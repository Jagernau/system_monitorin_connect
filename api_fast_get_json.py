from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from help_funcs import clients_data_to_json, get_time
from wialon_host import wialon_hosting
from wialon.sdk import WialonError, SdkException
import config
import os
import uuid

app = FastAPI()

# Задаем токен для проверки
fake_token = str(config.API_TOKEN)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ClientToken(BaseModel):
    client_token: str

# Функция для проверки токена
def verify_token(token: str = Depends(oauth2_scheme)):
    if token != fake_token:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/get_wialon_units_json/")
async def get_wialon_units_json_file(client_token: ClientToken, token: str = Depends(verify_token)):
    """ 
    Отдаёт файл объектов
    """
    time_now = str(get_time())
    unique_num = str(uuid.uuid4())
    client_data = client_token.client_token
    try:
        obj_clients = wialon_hosting.get_all_units(str(client_data))
        clients_data_to_json(obj_clients, f"{time_now}_{unique_num}_{client_data}_units")   
    except (Exception, WialonError, SdkException):
        raise HTTPException(status_code=404, detail="Not valid Client Token")

    else:
        try:
            resp = FileResponse(f'files/{time_now}_{unique_num}_{client_data}_units.json', media_type='application/json')
            resp.headers["Content-Disposition"] = f"attachment; filename={time_now}_{unique_num}_{client_data}_units.json"
            return resp

        except:
            raise HTTPException(status_code=404, detail="File not found")



@app.post("/get_wialon_users_json/")
async def get_wialon_users_json_file(client_token: ClientToken, token: str = Depends(verify_token)):
    """ 
    Отдаёт файл типов объектов
    """
    time_now = str(get_time())
    unique_num = str(uuid.uuid4())
    client_data = client_token.client_token
    try:
        obj_clients = wialon_hosting.get_all_device_types(str(client_data))
        clients_data_to_json(obj_clients, f"{time_now}_{unique_num}_{client_data}_users")   
    except (Exception, WialonError, SdkException):
        raise HTTPException(status_code=404, detail="Not valid Client Token")

    else:
        try:
            resp = FileResponse(f'files/{time_now}_{unique_num}_{client_data}_users.json', media_type='application/json')
            resp.headers["Content-Disposition"] = f"attachment; filename={time_now}_{unique_num}_{client_data}_users.json"
            return resp


        except:
            raise HTTPException(status_code=404, detail="File not found")
   

@app.post("/get_wialon_groups_json/")
async def get_wialon_groups_json_file(client_token: ClientToken, token: str = Depends(verify_token)):
    """ 
    Отдаёт файл групп объектов
    """
    time_now = str(get_time())
    unique_num = str(uuid.uuid4())
    client_data = client_token.client_token
    try:
        obj_clients = wialon_hosting.get_all_device_types(str(client_data))
        clients_data_to_json(obj_clients, f"{time_now}_{unique_num}_{client_data}_groups")   
    except (Exception, WialonError, SdkException):
        raise HTTPException(status_code=404, detail="Not valid Client Token")

    else:
        try:
            resp = FileResponse(f'files/{time_now}_{unique_num}_{client_data}_groups.json', media_type='application/json')
            resp.headers["Content-Disposition"] = f"attachment; filename={time_now}_{unique_num}_{client_data}_groups.json"
            return resp


        except:
            raise HTTPException(status_code=404, detail="File not found")



