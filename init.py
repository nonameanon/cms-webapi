from cycle import *
from req import request_access_token
from dotenv import load_dotenv
from os import getenv


load_dotenv()
USERNAME = getenv('NAME')
PASSWORD = getenv('PASSWORD')
NEW_PASSWORD = getenv('NEW_PASSWORD')
BASE_URL = "https://uat-mm.srvdev.ru/passenger/api"

PAYLOAD = f"grant_type=password&username={USERNAME}&password={PASSWORD}"

ACCESS_TOKEN = request_access_token(PAYLOAD)["access_token"]
REFRESH_TOKEN = request_access_token(PAYLOAD)["refresh_token"]


test_main_cycle(BASE_URL, ACCESS_TOKEN)
change_data_cycle(BASE_URL, ACCESS_TOKEN)
change_carriers_cycle(BASE_URL, ACCESS_TOKEN)
if change_password_cycle(BASE_URL, ACCESS_TOKEN, PASSWORD, NEW_PASSWORD):
    PASSWORD, NEW_PASSWORD = NEW_PASSWORD, PASSWORD
    with open('.env', 'w') as f:
        f.write(f"NAME={USERNAME}\n")
        f.write(f"PASSWORD={PASSWORD}\n")
        f.write(f"NEW_PASSWORD={NEW_PASSWORD}\n")
live_feed_cycle(BASE_URL, ACCESS_TOKEN)
maps_cycle(BASE_URL, ACCESS_TOKEN)
