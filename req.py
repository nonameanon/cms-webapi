import requests
import json
from string import ascii_letters
from random import choice, randint
from requests_toolbelt.multipart.encoder import MultipartEncoder


def request_access_token(payload):

    """
    Генерация токена доступа
    """

    url = "https://uat-mm.srvdev.ru/passenger/auth/connect/token"

    # payload = 'grant_type=password&username=79876187492&password=1234Test'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ZjFkYWM2MDgtZGQzNS00NzE3LThjYmItMThlMmY3YTFkNTIyOnRoZV9zZWNyZXQ='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


# Основная информация

def get_accounts_info(base_url, access_token):

    """
    Возвращает основную информацию об аккаунте
    """

    url = f"{base_url}/accounts/v1.0/info"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_profile_image(base_url, access_token, image_field_id=None):

    """
    Возвращает файл аватара профиля, при наличии.
    При отсутствии возвращает 404
    """

    url = f"{base_url}/accounts/v1.0/user/photo?imageFileId={image_field_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def get_carriers_list(base_url, access_token):

    """
    Возвращает список привязанных носителей
    """

    url = f"{base_url}/carriers/v1.0/linked"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_bank_cards_list(base_url, access_token):

    """
    Возвращает список привязанных банковских карт
    """

    url = f"{base_url}/bankCards/v1.0"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_feeds_list(base_url, access_token, page=0, size=20, qfilter=None, retrieveBody=False,
                   retrieveOfferBody=False):

    """
    Возвращает все элементы живой ленты
    """

    url = f"{base_url}/feeds/v1.0?page={page}&size={size}&retrieveBody={retrieveBody}&retrieveOfferBody={retrieveOfferBody}"
    if qfilter:
        url += f"&filter={qfilter}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_tickets_list(base_url, access_token, page=0, size=20):

    """
    Возвращает все существующие и доступные билеты
    """

    url = f"{base_url}/tickets/v1.0?page={page}&size={size}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_operations_list(base_url, access_token, page=None, size=20, linked_cards=(), linked_bank_cards=(),
                        operationTypes=(), start_date=None, end_date=None):

    """
    Возвращает список операций по картам
    """

    url = f"{base_url}/operations/v1.0?size={size}"
    if page:
        url += f"&pageToken={page}"

    payload = json.dumps({
        "linkedCardIds": linked_cards,
        "linkedBankCardId": linked_bank_cards,
        "operationTypes": operationTypes,
        "periodStartDateUtc": start_date,
        "periodEndDateUtc": end_date
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def get_trips_list(base_url, access_token, page=None, size=20, linked_cards=(), start_date=None, end_date=None):

    """
    Возвращает список поездок
    """

    url = f"{base_url}/trips/v1.0?size={size}"
    if page:
        url += f"&pageToken={page}"
    if linked_cards:
        for i in linked_cards:
            url += f"&linkedCardIds={i}"
    if start_date:
        url += f"&periodFrom={start_date}"
    if end_date:
        url += f"&periodTo={end_date}"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_stations_list(base_url, access_token):

    """
    Возвращает список всех станций
    """

    url = f"{base_url}/references/v1.0/stations"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


# Изменение личных данных

def download_file(base_url, access_token, fileid=None):

    """
    Загружает файл через fileId
    Возвращает response
    """

    url = f"{base_url}/files/v1.0/download/{fileid}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def upload_profile_image(base_url, access_token, file=None):
    url = f"{base_url}/accounts/v1.0/user/photo"

    if file is None:
        file = open('test.png', 'rb')

    mp_e = MultipartEncoder(fields={
        'file': ('test.png', file, 'image/png'),
    })

    payload = {'file': file}

    headers = {
        'Content-Type': mp_e.content_type,
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=file)

    return response.json()


def delete_profile_image(base_url, access_token, image_field_id=None):

    """
    Удаляет аватар профиля
    """

    url = f"{base_url}/accounts/v1.0/user/photo/{image_field_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json()


def update_user_info(base_url, access_token, firstName='Test', middleName='Test', lastName='Test',
                     birthDate='01.09.1939', gender='male', homeStationId="812", preferredLanguageCode='ru'):

    """
    Обновляет данные профиля:
    :param base_url:
    :param access_token:
    :param firstName:
    :param middleName:
    :param lastName:
    :param birthDate:
    :param gender:
    :param homeStationId:
    :param preferredLanguageCode:
    :return response.json:
    """

    url = f"{base_url}/accounts/v1.0/user"

    payload = json.dumps({
        "firstName": firstName,
        "middleName": middleName,
        "lastName": lastName,
        "birthDate": birthDate,
        "gender": gender,
        "homeStationId": homeStationId,
        "preferredLanguageCode": preferredLanguageCode
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


def turn_off_notifications(base_url, access_token):

    """
    Выключает настройки уведомлений
    """

    url = f"{base_url}/accounts/v1.0/settings"

    payload = json.dumps({
        "notificationChannelStates": [
            {
                "id": "1",
                "enabled": False
            },
            {
                "id": "2",
                "enabled": False
            }
        ],
        "notificationTypeStates": [
            {
                "id": "1",
                "enabled": False
            },
            {
                "id": "2",
                "enabled": False
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


def turn_on_notifications(base_url, access_token):

    """
    Включает настройки уведомлений
    """

    url = f"{base_url}/accounts/v1.0/settings"

    payload = json.dumps({
        "notificationChannelStates": [
            {
                "id": "1",
                "enabled": True
            },
            {
                "id": "2",
                "enabled": True
            }
        ],
        "notificationTypeStates": [
            {
                "id": "1",
                "enabled": True
            },
            {
                "id": "2",
                "enabled": True
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


# Действия с носителями

def get_carriers_info(base_url, access_token, carrier_ids=None):

    """
    Возвращает список подробной информации по каждой карте
    """

    responses = []
    for c in carrier_ids:
        url = f"{base_url}/carriers/v1.0/linked/{c}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        responses.append(requests.request("GET", url, headers=headers, data=payload).json())

    return responses


def change_carriers_names(base_url, access_token, carrier_ids=None, name=None):

    """
    Изменяет имена носителей
    Возвращает список ответов
    """

    def get_random_string(length):
        letters = ascii_letters
        result_str = ''.join(choice(letters) for i in range(length))
        return result_str

    responses = []
    for c in carrier_ids:
        if not name:
            name = get_random_string(randint(1, 11))
        url = f"{base_url}/carriers/v1.0/{c}?name={name}({c})"
        name = None

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        responses.append(requests.request("PUT", url, headers=headers, data=payload).json())

    return responses


def validate_carrier_payment(base_url, access_token, carrier_ids=None):

    """
    Возвращает данные о незаписанных билетах по каждой карте
    """

    responses = []
    for c in carrier_ids:
        url = f"{base_url}/carriers/v1.0/{c}/validate/payment"

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        responses.append(requests.request("GET", url, headers=headers, data=payload).json())

    return responses


def bind_carrier(base_url, access_token, card_number="3932016009", name="bind test", stations=(10224, 10224),
                 type="LAST_STATIONS", phone="79876187492"):

    """
    Привязывает носитель к аккаунту
    """

    url = f"{base_url}/carriers/v1.0/bind"

    payload = json.dumps({
        "cardNumber": card_number,
        "name": name,
        "stationIds": stations,
        "type": type,
        "phoneNumber": phone
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def unbind_carrier(base_url, access_token, card_number="3932016009"):

    """
    Отвязывает носитель от аккаунта
    """

    url = f"{base_url}/carriers/v1.0/{card_number}"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json()


def turn_on_balance_notifications(base_url, access_token, card_id=None):

    """
    Создаёт уведомление о необходимости пополнить баланс
    """

    url = f"{base_url}/carriers/v1.0/{card_id}/autoRecharge"

    payload = json.dumps({
        "threshold": 1000,
        "mode": "notificationOnly"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


def turn_on_auto_recharge(base_url, access_token, card_id=None, bank_card_id=None):

    """
    Создаёт автопополнение
    """

    url = f"{base_url}/carriers/v1.0/{card_id}/autoRecharge"

    payload = json.dumps({
        "linkedBankCardId": bank_card_id,
        "threshold": 1000,
        "paymentSum": 100,
        "mode": "enabled"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


def turn_off_auto_recharge(base_url, access_token, card_id=None, bank_card_id=None):

    """
    Отключает автопополнение
    """

    url = f"{base_url}/carriers/v1.0/{card_id}/autoRecharge"

    payload = json.dumps({
        "linkedBankCardId": bank_card_id,
        "threshold": 1000,
        "paymentSum": 100,
        "mode": "disabled"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


def delete_auto_recharge(base_url, access_token, card_id=None):

    """
    Удаляет автопополнение
    """

    url = f"{base_url}/carriers/v1.0/{card_id}/autoRecharge"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json()


# Смена пароля

def create_security_token(base_url, access_token, password=None):

    """
    Создаёт токен безопасности
    """

    url = f"{base_url}/accounts/v1.0/securityToken?password={password}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def change_password(base_url, access_token, security_token, new_password=None):

    """
    Меняет пароль аккаунта
    """

    url = f"{base_url}/accounts/v1.0/password"

    payload = json.dumps({
        "newPassword": new_password,
        "securityToken": security_token
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


# Живая лента

def get_offers(base_url, access_token, offers=()):

    """
    Возвращает детальную информацию по всем предложениям
    """

    responses = []
    for o in offers:
        url = f"{base_url}/feeds/offers/v1.0/{o}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        responses.append(requests.request("GET", url, headers=headers, data=payload).json())

    return responses


def get_votes(base_url, access_token, votes=()):

    """
    Возвращает детальную информацию по всем опросам
    """

    responses = []
    for v in votes:
        url = f"{base_url}/feeds/votes/v1.0/{v}/questions"

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        responses.append(requests.request("GET", url, headers=headers, data=payload).json())

    return responses


def get_notifications(base_url, access_token, notifications=()):

    """
    Возвращает детальную информацию по всем оповещениям
    """

    responses = []
    for v in notifications:
        url = f"{base_url}/feeds/notifications/v1.0/{v}?read=false"

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        responses.append(requests.request("GET", url, headers=headers, data=payload).json())

    return responses


# Карты и терминалы

def get_places_on_map(base_url, access_token, lat=55.75830929718952, lon=37.61971450262452,
                      rad=0.6210346151841654, qfilter=("BUY_TICKET", "DOWN_LOYALTY")):

    """
    Находит места на карте и возвращает информацию о них
    """

    url = f"{base_url}/places/v1.0/search?lat={lat}&lon={lon}&rad={rad}"
    if qfilter:
        for f in qfilter:
            url += f"&filter={f}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
