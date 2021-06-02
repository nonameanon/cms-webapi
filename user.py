from req import request_access_token
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class User:
    def __init__(self):
        self.username = getenv('NAME')
        self.__password = getenv('PASSWORD')
        self.__new_password = getenv('NEW_PASSWORD')
        self.base_url = "https://uat-mm.srvdev.ru/passenger/api"
        self.image_id = None
        self.carriers = ()
        self.bank_cards = ()
        self.notifications = ()
        self.offers = ()
        self.votes = ()

        self.access_payload = f"grant_type=password&username={self.username}&password={self.__password}"

        self.access_token = request_access_token(self.access_payload).json()["access_token"]
        self.refresh_token = request_access_token(self.access_payload).json()["refresh_token"]

        self.test_json = {}

    def select_uat(self):
        self.base_url = "https://uat-mm.srvdev.ru/passenger/api"
        return self.base_url

    def select_staging(self):
        self.base_url = "https://staging-mm.srvdev.ru/passenger/api"
        return self.base_url

    def select_testing(self):
        self.base_url = "https://mm.srvdev.ru/passenger/api"
        return self.base_url

    def get_pass(self):
        return self.__password

    def get_new_pass(self):
        return self.__new_password

    def change_password(self, changed):
        if changed:
            self.__password, self.__new_password = self.__new_password, self.__password
            with open('.env', 'w') as f:
                f.write(f"NAME={self.username}\n")
                f.write(f"PASSWORD={self.__password}\n")
                f.write(f"NEW_PASSWORD={self.__new_password}\n")
