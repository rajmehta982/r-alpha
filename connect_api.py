# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger

api_key = '2VTNvx7z'
username = 'R258447'
pwd = '1499'
token_id = "3URP5C2ZUQSYTSEFELMM2CFJGM"

def connect_api(api_key, token_id, username, pwd):
    smartApi = SmartConnect(api_key)
    try:
        token = token_id
        totp = pyotp.TOTP(token).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    correlation_id = "abcde"
    data = smartApi.generateSession(username, pwd, totp)

    if data['status'] == False:
        logger.error(data)


