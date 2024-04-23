# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger

def create_api_session(token_id, username, pwd, smartApi):
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

    return data

def connect_api(api_key):
    smartApi = SmartConnect(api_key)
    return smartApi

