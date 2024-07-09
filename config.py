from dotenv import dotenv_values

val = dotenv_values(".env")

GLONASS_LOGIN = str(val["GLONASS_LOGIN"])
GLONASS_PASSWORD = str(val["GLONASS_PASSWORD"])
GLONASS_BASED_ADRESS = str(val["GLONASS_BASED_ADRESS"])


