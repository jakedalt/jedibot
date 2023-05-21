import requests

from constants import DD_KEY


def kanye():
    api_url = "https://api.kanye.rest/"
    response = requests.get(api_url)
    return response.json()


def background_check(discord_id):
    api_url = "https://dangerousdiscord.com/api/check"
    response = requests.get(api_url, headers={'Authorization': DD_KEY}, params={'id': discord_id})
    return response.json()
