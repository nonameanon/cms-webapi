from req import *


def main_cycle(u, rep):
    response = get_accounts_info(u.base_url, u.access_token)
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
        response = get_profile_image(u.base_url, u.access_token, u.image_id)
        if response.status_code == 200:
            rep.add_test(True, title='Image found', description=f'ID: {u.image_id}')
            print(f"PASS: Image found")
        else:
            rep.add_test(False, title='Image not found', description=f'ID: {u.image_id}\n{response.json()}')
            print(f"FAILED: Image not found")
    else:
        rep.add_test('B', title='Image not set')
        print("BLOCKED: Image not set")

    response = get_carriers_list(u.base_url, u.access_token)
    if response['success']:
        u.carriers = [c['card']['linkedCardId'] for c in response['data']['cards']]
        rep.add_test(True, 'Carriers list', u.carriers)
        print(f'PASS: carriers')
    else:
        rep.add_test(False, 'Carriers list', response)

    response = get_bank_cards_list(u.base_url, u.access_token)
    if response['success']:
        u.bank_cards = [c['linkedBankCardId'] for c in response['data']]
        rep.add_test(True, 'Bank Cards', u.bank_cards)
        print(f'PASS: Bank cards')
    else:
        rep.add_test(False, 'Bank Cards', response)

    response = get_feeds_list(u.base_url, u.access_token)
    if response['success']:
        u.notifications = [n['id'] for n in response['data']['notifications']['notifications']]
        rep.add_test(True, 'Notifications', u.notifications)
        print(f"PASS: notifications")

        u.offers = [o['id'] for o in response['data']['offers']]
        rep.add_test(True, 'Offers', u.offers)
        print(f"PASS: offers")

        u.votes = [v['id'] for v in response['data']['votes']]
        rep.add_test(True, 'Votes', u.votes)
        print(f"PASS: votes")
    else:
        rep.add_test(False, 'Live Feed', response)

    response = get_tickets_list(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Tickets List', [r['title'] for r in response['data']['items']])
        print(f"PASS: Tickets")
    else:
        rep.add_test(False, 'Tickets List', response)

    response = get_operations_list(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Operations List', [r['displayName'] for r in response['data']['items']])
        print(f"PASS: Operations")
    else:
        rep.add_test(False, 'Operations List', response)

    response = get_trips_list(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Trips', [r['displayName'] for r in response['data']['items']])
        print(f"PASS: Trips")
    else:
        rep.add_test(False, 'Trips', response)
        print(f"FAILED: Trips")

    response = get_stations_list(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Stations List', len(response['data']))
        print(f"PASS: Stations")
    else:
        rep.add_test(False, 'Stations List', response)

    print(f"PASSED: MAIN INFO")
    print("-"*50)


def change_data_cycle(u, rep):
    if u.image_id:
        response = delete_profile_image(u.base_url, u.access_token, u.image_id)
        if response['success']:
            rep.add_test(True, 'Delete Image', u.image_id)
            print(f"PASS: Delete image")
        else:
            rep.add_test(False, 'Delete Image', response)
    else:
        rep.add_test('B', 'Delete Image', 'Image is not set')

    response = update_user_info(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Update User Info')
        print("PASS: Update user info")
    else:
        rep.add_test(False, 'Update User Info', response)

    response = turn_off_notifications(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Turn Off Notifications')
        print("PASS: Turn off notifications")
    else:
        rep.add_test(False, 'Turn Off Notifications', response)

    response = turn_on_notifications(u.base_url, u.access_token)
    if response['success']:
        rep.add_test(True, 'Turn On Notifications')
        print("PASS: Turn on notifications")
    else:
        rep.add_test(False, 'Turn On Notifications', response)

    print("PASS: CHANGE PERSONAL DATA")
    print('-'*50)


def change_carriers_cycle(u, rep):
    if u.carriers:
        response = change_carriers_names(u.base_url, u.access_token, u.carriers)
        if response[0]['success']:
            rep.add_test(True, "Changed Names")
            print("PASS: Changed names")
        else:
            rep.add_test(False, "Changed Names", response)

        response = get_carriers_info(u.base_url, u.access_token, u.carriers)
        for r in response:
            if r['success']:
                desc = r['data']['card']['card']['displayName']+' | '
                desc += r['data']['card']['status']+' | '
                desc += str(r['data']['card']['balance']['balance'])
                rep.add_test(True, f"Carrier Info {r['data']['card']['card']['cardNumber']}", desc)
                print("PASS: Carriers info")
            else:
                rep.add_test(False, 'Carriers Info', r)

        response = validate_carrier_payment(u.base_url, u.access_token, u.carriers)
        for r in response:
            if r['success']:
                rep.add_test(True, "Carrier has no unwritten tickets")
                print("PASS: Carrier has no unwritten tickets")
            else:
                rep.add_test(False, "Carrier has unwritten tickets", r)
                print("PASS: Carrier has unwritten tickets")

        response = bind_carrier(u.base_url, u.access_token)
        if response['success']:
            card_id = response['data']['card']['card']['linkedCardId']
            rep.add_test(True, "Carrier Bind", card_id)
            print("PASS: Carrier bind")
        else:
            rep.add_test(False, "Carrier Bind", response)
            card_id = None

        response = unbind_carrier(u.base_url, u.access_token, card_id)
        if response['success']:
            rep.add_test(True, 'Carrier Unbind')
            print(f"PASS: Carrier unbind")
        else:
            rep.add_test(False, "Carrier Unbind", response)

        response = turn_on_balance_notifications(u.base_url, u.access_token, u.carriers[0])
        if response['success']:
            rep.add_test(True, 'Enable Balance Notifications')
            print("PASS: Enable balance notifications")
        else:
            rep.add_test(False, "Enable Balance Notifications", response)

        response = turn_on_auto_recharge(u.base_url, u.access_token, u.carriers[0], u.bank_cards[0])
        if response['success']:
            rep.add_test(True, "Enable Auto Recharge")
            print("PASS: Enable auto recharge")
        else:
            rep.add_test(False, "Enable Auto Recharge", response)

        response = turn_off_auto_recharge(u.base_url, u.access_token, u.carriers[0], u.bank_cards[0])
        if response['success']:
            rep.add_test(True, "Disable Auto Recharge")
            print("PASS: Disable auto recharge")
        else:
            rep.add_test(False, "Disable Auto Recharge", response)

        response = delete_auto_recharge(u.base_url, u.access_token, u.carriers[0])
        if response['success']:
            rep.add_test(True, "Delete Auto Recharge")
            print("PASS: Delete auto recharge")
        else:
            rep.add_test(False, "Delete Auto Recharge", response)

        response = block_carrier(u.base_url, u.access_token, u.unblocked_card)
        if response['success']:
            rep.add_test(True, "Block Carrier")
            print("PASS: Block carrier")
        else:
            rep.add_test(False, "Block Carrier", response)

        response = unblock_carrier(u.base_url, u.access_token, u.blocked_card)
        if response['success']:
            rep.add_test(True, "Unblock Carrier")
            print("PASS: Unlock carrier")
        else:
            rep.add_test(False, "Unlock Carrier", response)

        print("PASS: CARRIER ACTIONS")
        print("-"*50)

    else:
        rep.add_test("B", "No Linked Carriers")


def change_password_cycle(u, rep):
    response = create_security_token(u.base_url, u.access_token, u.get_pass())
    if response['success']:
        security_token = response['data']['securityToken']
        rep.add_test(True, "Security Token Generated", f"{'*'*len(security_token[:-7])}{security_token[-7:]}")
        print("PASS: Security token generated")
    else:
        security_token = None
        rep.add_test(False, "Security Token is None", response)
        print("FAIL: Security token is None")

    response = change_password(u.base_url, u.access_token, security_token, u.get_new_pass())
    if response['success']:
        rep.add_test(True, "Password Changed")
        print("PASS: PASSWORD CHANGED")
        print("-" * 50)
        return True
    else:
        rep.add_test(False, "Password is not Changed")
        return False


def live_feed_cycle(u, rep):
    if u.offers:
        response = get_offers(u.base_url, u.access_token, u.offers)
        for r in response:
            if r['success']:
                rep.add_test(True, f"Offer {r['data']['id']}", r['data']['title'])
                print(f"PASS: Offer {r['data']['id']} | {r['data']['title']}")
            else:
                rep.add_test(False, "Offer", r)
    else:
        rep.add_test('B', "No Available Offers")

    if u.votes:
        response = get_votes(u.base_url, u.access_token, u.votes)
        for r in response:
            if r['success']:
                rep.add_test(True, "Vote", [v['title'] for v in r['data']])
                print(f"PASS: Vote questions {len(r['data'])}")
            else:
                rep.add_test(False, "Vote", r)
    else:
        rep.add_test('B', "No Available Votes")

    if u.notifications:
        response = get_notifications(u.base_url, u.access_token, u.notifications)
        for r in response:
            if r['success']:
                rep.add_test(True, f"Notification {r['data']['id']}", r['data']['title'])
                print(f"PASS: Notification {r['data']['id']} | {r['data']['title']}")
            else:
                rep.add_test(False, "Notification", r)
    else:
        rep.add_test(False, "No Available Notifications")

    print("PASS: LIVE FEED ITEMS")
    print("-"*50)


def maps_cycle(u, rep):
    response = get_places_on_map(u.base_url, u.access_token)
    if response['success']:
        print("PASS: Places on maps")
        for p in response['data']:
            rep.add_test(True, f"Place On Map {p['id']}", f"{p['address']}")
            print(f"\t{p['id']} | {p['address']}")
    else:
        rep.add_test(False, "Places On Map", response)

    print("PASS: PLACES ON MAP")
    print("-"*50)

