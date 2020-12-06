from os import environ
from datetime import datetime
from time import sleep
from requests import get
import pandas as pd

# https://ambientweather.docs.apiary.io/

AMBIENTWEATHER_API_KEY = environ['AMBIENTWEATHER_API_KEY']
AMBIENTWEATHER_APP_KEY = environ['AMBIENTWEATHER_APP_KEY']
BASE_URI = 'https://api.ambientweather.net'


def validate_response(response: str):
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_devices() -> list:
    url = BASE_URI + f"/v1/devices?applicationKey={AMBIENTWEATHER_APP_KEY}&apiKey={AMBIENTWEATHER_API_KEY}"
    response = get(url)
    return validate_response(response)


def get_device_data(mac_address: str, end_date: str=None) -> list:
    if end_date:
        url = BASE_URI + f"/v1/devices/{mac_address}?endDate={end_date}&applicationKey={AMBIENTWEATHER_APP_KEY}&apiKey={AMBIENTWEATHER_API_KEY}"
    else:
        url = BASE_URI + f"/v1/devices/{mac_address}?applicationKey={AMBIENTWEATHER_APP_KEY}&apiKey={AMBIENTWEATHER_API_KEY}"
    response = get(url)
    return validate_response(response)


def get_my_data(end_date: str=None) -> pd.DataFrame:
    devices = get_devices()
    sleep(1.1)
    if end_date:
        ed = str(int(datetime.fromisoformat(end_date).timestamp()*1000))
    else:
        ed = None
    data = get_device_data(
        mac_address=devices[0]['macAddress'],
        end_date=ed,
        )
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df.date)
    df = df.set_index('date')
    return df.drop(columns='dateutc')
