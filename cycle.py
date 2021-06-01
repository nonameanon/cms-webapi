from req import *


def main_cycle(base_url, access_token):
    image_id = None
    carriers = ()
    bank_cards = ()
    offers = ()
    votes = ()
    notifications = ()

    response = accounts_info(base_url, access_token)
    if response["success"]:
        print("PASS: Main account info")
        if response["data"]["imageId"]:
            image_id = response["data"]["imageId"]

    if image_id:
        response = get_profile_image(base_url, access_token, image_id)
        if response.status_code == 200:
            print(f"PASS: Image found\nID: {image_id}")
        else:
            print(f"FAILED: Image not found\nID: {image_id}")
    else:
        print("BLOCKED: Image not set")

