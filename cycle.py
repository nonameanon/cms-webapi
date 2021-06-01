from req import *

image_id = None
carriers = ()
bank_cards = ()
offers = ()
votes = ()
notifications = ()


def test_main_cycle(base_url, access_token):
    global image_id, carriers, bank_cards, offers, votes, notifications
    response = accounts_info(base_url, access_token)
    if response["success"]:
        print("PASS: Main account info")
        try:
            if response["data"]["imageId"]:
                image_id = response["data"]["imageId"]
        except KeyError:
            pass

    if image_id:
        response = get_profile_image(base_url, access_token, image_id)
        if response.status_code == 200:
            print(f"PASS: Image found\n\tID: {image_id}")
        else:
            print(f"FAILED: Image not found\n\tID: {image_id}")
    else:
        print("BLOCKED: Image not set")

    response = get_carriers_list(base_url, access_token)
    if response['success']:
        carriers = [c['card']['linkedCardId'] for c in response['data']['cards']]
        print(f'PASS: Carriers \n\tIDs: {carriers}')

    response = get_bank_cards_list(base_url, access_token)
    if response['success']:
        bank_cards = [c['linkedBankCardId'] for c in response['data']]
        print(f'PASS: Bank cards \n\tIDs: {bank_cards}')

    response = get_feeds_list(base_url, access_token)
    if response['success']:
        notifications = [n['id'] for n in response['data']['notifications']['notifications']]
        print(f"PASS: Notifications\n\tIDs: {notifications}")
        offers = [o['id'] for o in response['data']['offers']]
        print(f"PASS: Offers\n\tIDs: {offers}")
        votes = [v['id'] for v in response['data']['votes']]
        print(f"PASS: Votes\n\tIDs: {votes}")

    response = get_tickets_list(base_url, access_token)
    if response['success']:
        print(f"PASS: Tickets\n\tQty: {len(response['data']['items'])}")

    response = get_operations_list(base_url, access_token)
    if response['success']:
        print(f"PASS: Operations\n\tQty: {len(response['data']['items'])}")

    response = get_trips_list(base_url, access_token)
    if response['success']:
        print(f"PASS: Trips\n\tQty: {len(response['data']['items'])}")

    response = get_stations_list(base_url, access_token)
    if response['success']:
        print(f"PASS: Stations\n\tQty: {len(response['data'])}")

    print(f"PASSED: MAIN INFO")
    print("-"*50)


def change_data_cycle(base_url, access_token):
    if image_id:
        response = delete_profile_image(base_url, access_token, image_id)
        if response['success']:
            print(f"PASS: Delete image\n\tID: {image_id}")

    response = update_user_info(base_url, access_token, firstName="AAAAA", middleName="BBBBBBB",
                                lastName="CCCCCCCC", gender="female")
    if response['success']:
        print("PASS: Update user info")

    response = turn_off_notifications(base_url, access_token)
    if response['success']:
        print("PASS: Turn off notifications")

    response = turn_on_notifications(base_url, access_token)
    if response['success']:
        print("PASS: Turn on notifications")

    print("PASS: CHANGE PERSONAL DATA")
    print('-'*50)


def change_carriers_cycle(base_url, access_token):
    if carriers:
        response = change_carriers_names(base_url, access_token, carriers)
        if response[0]['success']:
            print("PASS: Changed names")

        response = get_carriers_info(base_url, access_token, carriers)
        if response[0]['success']:
            print("PASS: Carriers info")
            for r in response:
                print(f"\tNumber: {r['data']['card']['card']['cardNumber']} | "
                      f"{r['data']['card']['card']['displayName']}")

        response = validate_carrier_payment(base_url, access_token, carriers)
        for r in response:
            if r['success']:
                print("PASS: Carrier has no unwritten tickets\n\t"
                      f"Available tickets: {len(r['data']['availableProducts'])}")
            else:
                print("PASS: Carrier has unwritten tickets\n\t"
                      f"Message: {r['error']['message']}")

        response = bind_carrier(base_url, access_token)
        if response['success']:
            card_id = response['data']['card']['card']['linkedCardId']
            print("PASS: Carrier bind\n\t"
                  f"Card: {response['data']['card']['card']['cardNumber']} | "
                  f"{response['data']['card']['card']['displayName']}")
        else:
            card_id = None

        response = unbind_carrier(base_url, access_token, card_id)
        if response['success']:
            print(f"PASS: Carrier unbind\n\tID: {card_id}")

        response = turn_on_balance_notifications(base_url, access_token, carriers[0])
        if response['success']:
            print("PASS: Enable balance notifications")

        response = turn_on_auto_recharge(base_url, access_token, carriers[0], bank_cards[0])
        if response['success']:
            print("PASS: Enable autorecharge")

        response = turn_off_auto_recharge(base_url, access_token, carriers[0], bank_cards[0])
        if response['success']:
            print("PASS: Disable autorecharge")

        response = delete_auto_recharge(base_url, access_token, carriers[0])
        if response['success']:
            print("PASS: Delete autorecharge")

        print("PASS: CARRIER ACTIONS")
        print("-"*50)


def change_password_cycle(base_url, access_token, password, new_password):
    response = create_security_token(base_url, access_token, password)
    if response['success']:
        security_token = response['data']['securityToken']
        print("PASS: Security token generated\n\t"
              f"{'*'*len(security_token[:-6])}{security_token[-6:]}")
    else:
        security_token = None
        print("FAIL: Security token is None")

    response = change_password(base_url, access_token, security_token, new_password)
    if response['success']:
        print("PASS: PASSWORD CHANGED")
        print("-" * 50)
        return True


def live_feed_cycle(base_url, access_token):
    if offers:
        response = get_offers(base_url, access_token, offers)
        for r in response:
            if r['success']:
                print(f"PASS: Offer {r['data']['id']} | {r['data']['title']}")
    if votes:
        response = get_votes(base_url, access_token, votes)
        for r in response:
            if r['success']:
                print(f"PASS: Vote questions {len(r['data'])}")
    if notifications:
        response = get_notifications(base_url, access_token, notifications)
        for r in response:
            if r['success']:
                print(f"PASS: Notification {r['data']['id']} | {r['data']['title']}")
    print("PASS: LIVE FEED ITEMS")
    print("-"*50)


def maps_cycle(base_url, access_token):
    response = get_places_on_map(base_url, access_token)
    if response['success']:
        print("PASS: Places on maps")
        for p in response['data']:
            print(f"\t{p['id']} | {p['address']}")
    print("PASS: PLACES ON MAP")
    print("-"*50)
