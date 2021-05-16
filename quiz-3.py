# api docs: https://www.coingecko.com/en/api#explore-api
import sqlite3

import requests
import json

from datetime import datetime

url = 'https://api.coingecko.com/api/v3/coins'

conn = sqlite3.connect("history-date.sqlite")
cursor = conn.cursor()

try:
    cursor.execute('''create table crypto (token_id TEXT, date TEXT, price NUMERIC)''')
except:
    pass

list_response = requests.get(url + "/list")
list_data = json.loads(list_response.text)

print("Data received!" if list_response.status_code == 200 else "Something went wrong while receiving data!")
print("Date: " + list_response.headers['Date'])


def format_token_listing(token):
    name = token["name"]
    symbol = token["symbol"]
    id = token["id"]

    formatted_name = (name[:20] + ".." if len(name) > 20 else name).ljust(22)

    full_name = f'{formatted_name} ({symbol})'.ljust(30)

    return f'{full_name} -> id: {id}'


def fetch_token(token_id):
    parameters = {
        'vs_currency': 'usd',
        'id': token_id,
        "localization": False,
        "tickers": False,
        "market_data": True,
        "community_data": False,
        "developer_data": False,
        "sparkline": False
    }

    market_response = requests.get(url+f'/{token_id}', params=parameters)

    market_data = market_response.json()

    return market_data


def dump_token_data(token_name, token_data):
    date = datetime.now().strftime("%d_%m_%Y %H-%M-%S")

    with open(f'{token_name}-{date}.txt', 'w') as outfile:
        json.dump(token_data, outfile, indent=4)


def save_token(token_id, price):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("insert into crypto (token_id, date, price) values(?, ?, ?)", (token_id, date, price))
    conn.commit()


# def format_token(token_data):

#
# --------------------------------------------------
#

state_code = 0

while state_code == 0:
    user_input = input("\nEnter command: ")
    args = user_input.split()

    command = args[0]

    if command == "help":
        print("""
        help () -> displays all available commands
        exit () -> stops and exits out of the program
        
        find (string: name) -> finds token with similar name
        view (string: token_id) -> gets and displays info for specified token
        dump (string: token_id) -> gets and dump json info for specified token
        save (string: token_id) -> saves given tokens current data to database
        """)
    elif command == "find":
        for token in list_data:
            if args[1].lower() in token['name'].lower():
                print(format_token_listing(token))
    elif command == "dump":
        token_id = args[1]

        dump_token_data(token_id, fetch_token(token_id))
    elif command == "view":
        print(fetch_token(args[1]))
    elif command == "save":
        token_id = args[1]

        data = fetch_token(token_id)

        save_token(token_id, data["market_data"]["current_price"]['usd'])
    elif command == "exit":
        state_code = -1

conn.close()
