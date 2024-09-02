from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from help_funcs import clients_data_to_json
from wialon_host import wialon_hosting
from wialon.sdk import WialonError, SdkException
import config


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
    client_data = client_token.client_token
    try:
        obj_clients = wialon_hosting.get_all_units(str(client_data))
        clients_data_to_json(obj_clients, f"{client_data}_units")   
    except (Exception, WialonError, SdkException):
        raise HTTPException(status_code=404, detail="Not valid Client Token")

    else:
        try:
            return FileResponse(f'files/{client_data}_units.json')
        except:
            raise HTTPException(status_code=404, detail="File not found")


@app.post("/get_wialon_types_json/")
async def get_wialon_types_json_file(client_token: ClientToken, token: str = Depends(verify_token)):
    """ 
    Отдаёт файл типов объектов
    """
    client_data = client_token.client_token
    try:
        obj_clients = wialon_hosting.get_all_device_types(str(client_data))
        clients_data_to_json(obj_clients, f"{client_data}_types")   
    except (Exception, WialonError, SdkException):
        raise HTTPException(status_code=404, detail="Not valid Client Token")

    else:
        try:
            return FileResponse(f'files/{client_data}_types.json')
        except:
            raise HTTPException(status_code=404, detail="File not found")


@app.post("/get_wialon_users_json/")
async def get_wialon_users_json_file(client_token: ClientToken, token: str = Depends(verify_token)):
    """ 
    Отдаёт файл типов объектов
    """
    client_data = client_token.client_token
    try:
        obj_clients = wialon_hosting.get_all_device_types(str(client_data))
        clients_data_to_json(obj_clients, f"{client_data}_users")   
    except (Exception, WialonError, SdkException):
        raise HTTPException(status_code=404, detail="Not valid Client Token")

    else:
        try:
            return FileResponse(f'files/{client_data}_users.json')
        except:
            raise HTTPException(status_code=404, detail="File not found")
   
     
#    return {"client_token": client_token.client_token}
    
    
    # if os.path.exists(file_path):
    #     return FileResponse(file_path)
    # else:
    #     raise HTTPException(status_code=404, detail="File not found")
