import requests

def print_players():
    response = requests.get("http://127.0.0.1:5000/api/players")

    print(response.json())

    return response.json()