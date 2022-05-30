import json

import requests
import aiohttp
import asyncio
import re


url = "https://auth.riotgames.com/api/v1/authorization"


payload = {
    "client_id":"play-valorant-web-prod",
    "nonce":"1",
    "redirect_uri":"https://playvalorant.com/opt_in",
    "response_type":"token id_token",
}

data = {
    "type":"auth",
    "username":"Nekoziller",
    "password":"Kirito31415",
    "remember":"True",
    "language":"en-US"
}

headers = {'Content-Type':'application/json',
           'User-agent':'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64'}

#response = requests.request("POST", url, data=payload, headers=headers)

class API():
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.cookies = {}
        self.cookies['cookie'] = {}
        self.access_token = ""
        self.output = {}
        self.entitlements_token = ""
        self.puuid = ""
        self.uuid= ""

    def _extract_tokens(self, data: str) -> str:
        """Extract tokens from data"""

        pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        response = pattern.findall(data['response']['parameters']['uri'])[0]
        return response

    def get_skin(self, uuid: str):
        '''Get Skin data'''
        with open("cache" + ".json", "r", encoding='utf-8') as json_file:
            tmp = json.load(json_file)
            try:
                skindata = tmp
                skin = skindata["skins"][uuid]
            except KeyError:
                raise RuntimeError('Some skin data is missing, plz use `/fix cache`')
        return skin

    async def post(self):
        async with await self.session.post('https://auth.riotgames.com/api/v1/authorization', json=payload, headers=headers) as r:
            pass
        #print(response)

    async def put(self):
        async with self.session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers) as r:
            self.output = await r.json()
            #print(output)
            #print(response.cookies)
            #print(response.cookies.items())
            for cookie in r.cookies.items():
                self.cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]
        #print(self.cookies['cookie'])

        response = self._extract_tokens(self.output)
        self.access_token = response[0]

    async def entitlement(self):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        async with self.session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
            self.output = await r.json()

        self.entitlements_token = self.output['entitlements_token']
        #print(self.entitlements_token)

    async def user(self):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        async with self.session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
            self.output = await r.json()
            self.puuid = self.output['sub']
        #print('User ID: ' + self.puuid)

    async def store(self):
        headers = {'X-Riot-Entitlements-JWT': f'{self.entitlements_token}', 'Authorization': f'Bearer {self.access_token}'}
        async with self.session.get(f'https://pd.ap.a.pvp.net/store/v2/storefront/{self.puuid}', headers=headers, json={}) as r:
            self.output = await r.json()

            for f in self.output["SkinsPanelLayout"]["SingleItemOffers"]:
                self.uuid = f
                tmp = self.get_skin(self.uuid)
                name_store = tmp['names']['ja-JP']
                print(name_store)
            #print(self.output)
        await self.session.close()


if __name__ == '__main__':
    hoge = API()
    asyncio.get_event_loop().run_until_complete(hoge.post())
    asyncio.get_event_loop().run_until_complete(hoge.put())
    asyncio.get_event_loop().run_until_complete(hoge.entitlement())
    asyncio.get_event_loop().run_until_complete(hoge.user())
    asyncio.get_event_loop().run_until_complete(hoge.store())
