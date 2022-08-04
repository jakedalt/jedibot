import requests

def kanye():
    api_url = "https://api.kanye.rest/"
    response = requests.get(api_url)
    return response.json()