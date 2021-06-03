from req import *
from user import User
from reporter import Reporter


u = User()


def main_cycle(base_url, access_token):
    response = get_accounts_info(base_url, access_token)
    if response["success"]:
        rep.add_test(True, title='Main account info',
                     description=f"{response['data']}")
        print("PASS: Main account info")
        try:
            if response["data"]["imageId"]:
                u.image_id = response["data"]["imageId"]
        except KeyError:
            pass
    else:
        rep.add_test(False, title='Main account info')

    if u.image_id:
        response = get_profile_image(base_url, access_token, u.image_id)
        if response.status_code == 200:
            rep.add_test(True, title='Image found', description=f'ID: {u.image_id}')
            print(f"PASS: Image found\n\tID: {u.image_id}")
        else:
            rep.add_test(False, title='Image not found', description=f'ID: {u.image_id}\n{response.json()}')
            print(f"FAILED: Image not found\n\tID: {u.image_id}")
    else:
        rep.add_test('B', title='Image not set')
        print("BLOCKED: Image not set")

    response = get_carriers_list(base_url, access_token)
    if response['success']:
        u.carriers = [c['card']['linkedCardId'] for c in response['data']['cards']]
        rep.add_test(True, 'Carriers list', u.carriers)
        print(f'PASS: carriers \n\tIDs: {u.carriers}')
    else:
        rep.add_test(False, 'Carriers list', response)

    response = get_bank_cards_list(base_url, access_token)
    if response['success']:
        u.bank_cards = [c['linkedBankCardId'] for c in response['data']]
        rep.add_test(True, 'Bank Cards', u.bank_cards)
        print(f'PASS: Bank cards \n\tIDs: {u.bank_cards}')
    else:
        rep.add_test(False, 'Bank Cards', response)

    response = get_feeds_list(base_url, access_token)
    if response['success']:
        u.notifications = [n['id'] for n in response['data']['notifications']['notifications']]
        rep.add_test(True, 'Notifications', u.notifications)
        print(f"PASS: notifications\n\tIDs: {u.notifications}")

        u.offers = [o['id'] for o in response['data']['offers']]
        rep.add_test(True, 'Offers', u.offers)
        print(f"PASS: offers\n\tIDs: {u.offers}")

        u.votes = [v['id'] for v in response['data']['votes']]
        rep.add_test(True, 'Votes', u.votes)
        print(f"PASS: votes\n\tIDs: {u.votes}")
    else:
        rep.add_test(False, 'Live Feed', response)

    response = get_tickets_list(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Tickets List', [r['title'] for r in response['data']['items']])
        print(f"PASS: Tickets\n\tQty: {len(response['data']['items'])}")
    else:
        rep.add_test(False, 'Tickets List', response)

    response = get_operations_list(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Operations List', [r['displayName'] for r in response['data']['items']])
        print(f"PASS: Operations\n\tQty: {len(response['data']['items'])}")
    else:
        rep.add_test(False, 'Operations List', response)

    response = get_trips_list(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Trips', [r['displayName'] for r in response['data']['items']])
        print(f"PASS: Trips\n\tQty: {len(response['data']['items'])}")
    else:
        rep.add_test(False, 'Trips', response)
        print(f"FAILED: Trips\n\t{response}")

    response = get_stations_list(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Stations List', len(response['data']))
        print(f"PASS: Stations\n\tQty: {len(response['data'])}")
    else:
        rep.add_test(False, 'Stations List', response)

    print(f"PASSED: MAIN INFO")
    print("-"*50)


def change_data_cycle(base_url, access_token):
    if u.image_id:
        response = delete_profile_image(base_url, access_token, u.image_id)
        if response['success']:
            rep.add_test(True, 'Delete Image', u.image_id)
            print(f"PASS: Delete image\n\tID: {u.image_id}")
        else:
            rep.add_test(False, 'Delete Image', response)
    else:
        rep.add_test(False, 'Delete Image', 'Image is not set')

    response = update_user_info(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Update User Info')
        print("PASS: Update user info")
    else:
        rep.add_test(False, 'Update User Info', response)

    response = turn_off_notifications(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Turn Off Notifications')
        print("PASS: Turn off notifications")
    else:
        rep.add_test(False, 'Turn Off Notifications', response)

    response = turn_on_notifications(base_url, access_token)
    if response['success']:
        rep.add_test(True, 'Turn On Notifications')
        print("PASS: Turn on notifications")
    else:
        rep.add_test(False, 'Turn On Notifications', response)

    print("PASS: CHANGE PERSONAL DATA")
    print('-'*50)


def change_carriers_cycle(base_url, access_token):
    if u.carriers:
        response = change_carriers_names(base_url, access_token, u.carriers)
        if response[0]['success']:
            print("PASS: Changed names")

        response = get_carriers_info(base_url, access_token, u.carriers)
        if response[0]['success']:
            print("PASS: u.carriers info")
            for r in response:
                print(f"\tNumber: {r['data']['card']['card']['cardNumber']} | "
                      f"{r['data']['card']['card']['displayName']}")

        response = validate_carrier_payment(base_url, access_token, u.carriers)
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

        response = turn_on_balance_notifications(base_url, access_token, u.carriers[0])
        if response['success']:
            print("PASS: Enable balance u.notifications")

        response = turn_on_auto_recharge(base_url, access_token, u.carriers[0], u.bank_cards[0])
        if response['success']:
            print("PASS: Enable auto recharge")

        response = turn_off_auto_recharge(base_url, access_token, u.carriers[0], u.bank_cards[0])
        if response['success']:
            print("PASS: Disable auto recharge")

        response = delete_auto_recharge(base_url, access_token, u.carriers[0])
        if response['success']:
            print("PASS: Delete auto recharge")

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
    if u.offers:
        response = get_offers(base_url, access_token, u.offers)
        for r in response:
            if r['success']:
                print(f"PASS: Offer {r['data']['id']} | {r['data']['title']}")
    if u.votes:
        response = get_votes(base_url, access_token, u.votes)
        for r in response:
            if r['success']:
                print(f"PASS: Vote questions {len(r['data'])}")
    if u.notifications:
        response = get_notifications(base_url, access_token, u.notifications)
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


rep = Reporter(name='Change Data Cycle')
rep.title = 'MM LKP CYCLES'
rep.start()
change_data_cycle(u.base_url, u.access_token)
rep.end()
