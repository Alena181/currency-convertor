import requests
import psycopg2
import json

api_key = "KIf5FA7hHFImAcsyImIiSxOheVQtkleQ"
headers = {"apikey": api_key}

# Добавить подключение к базе Postgres
conn = psycopg2.connect("dbname=currency_converter_history user=alenasvinoboeva")
r = requests.get("https://api.apilayer.com/currency_data/list", headers=headers)
list_of_currencies = r.json()["currencies"].keys()

print("enter convertible currency code")
currency = input()
# list_of_currencies = ["USD", "RUB"]
if currency in list_of_currencies:
    print("enter the denomination of the currency")
    currency_denomination = input()
    if currency_denomination.isdigit():
        print("enter the currency you are converting to")
        target_currency = input()
        if target_currency in list_of_currencies:
            #rate = dictionary.get(currency + "/" + target_currency)
            #result = rate * int(currency_denomination)
            #print(str(result) + " " + target_currency)
            r1 = requests.get(f"https://api.apilayer.com/currency_data/convert?to={target_currency}&from={currency}&amount={currency_denomination}",
                          headers=headers)
            print(r1.json())
            # Open a cursor to perform database operations
            #cur = conn.cursor()
            success = r1.json()["success"]
            query = json.dumps(r1.json()["query"])
            info = json.dumps(r1.json()["info"])
            result = r1.json()["result"]
            # Execute a query
            # Добавить INSERT в базу данных из r1
            # Open a cursor to perform database operations
            cur = conn.cursor()

            cur.execute("INSERT INTO history (success, query, info, result) "
                        f"VALUES('{success}', '{query}', '{info}', '{result}');")
            conn.commit()

            print(str("%.2f" % r1.json()["result"]) + " " + target_currency)

        else:
            print("this currency is not supported")
    else:
        print("non-numeric value entered")
else:
    print("this currency is not supported")
