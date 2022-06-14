from __future__ import annotations

# Standard
import requests
import os
import json
from typing import Dict, Optional

from dotenv import load_dotenv
import dotenv

def get_valorant_version():
    """ Get the valorant version from valorant-api.com """

    resp = requests.get('https://valorant-api.com/v1/version')

    return resp.json()['data']['version']


def reload_skin_cache():
    """ Fetch the skin from valorant-api.com """
    with open("./utils/" + "cache" + ".json", "r", encoding='utf-8') as f:
        data = json.load(f)

    resp = requests.get(f'https://valorant-api.com/v1/weapons/skins?language=ja-JP')
    if resp.status_code == 200:
        tmp = {}
        for skin in resp.json()['data']:
            skinone = skin['levels'][0]
            tmp[skinone['uuid']] = {
                'uuid': skinone['uuid'],
                'names': skin['displayName'],
                'icon': skinone['displayIcon'],
            }
        data['skins'] = tmp
    with open("./utils/" + "cache" + ".json", 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
    print("complete")