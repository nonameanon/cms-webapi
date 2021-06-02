from req import *
from user import User
import pytest

u = User()


def test_request_access_token(extra):
    r = request_access_token(u.access_payload)
    assert r.status_code == 200
    u.access_token = r.json()['access_token']


def test_access_token():
    assert len(u.access_token) == 43


def test_get_accounts_info():
    r = get_accounts_info(u.base_url, u.access_token)
    assert r['success'] is True
    u.test_json = r['data']


def test_get_accounts_info_json():
    assert u.test_json['userName'] == u.username
    assert u.test_json['hasPassword'] is True
    try:
        u.image_id = u.test_json['imageId']
    except KeyError:
        u.image_id = None


def test_get_profile_image():
    assert u.image_id
    r = get_profile_image(u.base_url, u.access_token, u.image_id)
    assert r.status_code == 200


def test_get_carriers_list():
    r = get_carriers_list(u.base_url, u.access_token)
    assert r['success'] is True
    u.carriers = r['data']
