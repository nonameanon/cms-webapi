from cycle import main_cycle
from req import request_access_token

USERNAME = "79876187492"
PASSWORD = "1234Test"
NEW_PASSWORD = "1234Testt"
BASE_URL = "https://uat-mm.srvdev.ru/passenger/api"

PAYLOAD = f"grant_type=password&username={USERNAME}&password={PASSWORD}"

ACCESS_TOKEN = request_access_token(PAYLOAD)["access_token"]
REFRESH_TOKEN = request_access_token(PAYLOAD)["refresh_token"]


main_cycle(BASE_URL, ACCESS_TOKEN)
