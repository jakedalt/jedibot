import os

import requests
from dotenv import load_dotenv

def kanye():
    api_url = "https://api.kanye.rest/"
    response = requests.get(api_url)
    return response.json()

def backgroundCheck(discord_id):
    load_dotenv()
    DD_KEY = os.getenv('DD_KEY')
    api_url = "https://dangerousdiscord.com/api/check"
    response = requests.get(api_url, headers={'Authorization': DD_KEY}, params={'id': discord_id})
    return response.json()
