import os

import requests
from dotenv import load_dotenv

load_dotenv()


BESTPROXIES_APIKEY = os.getenv("BESTPROXIES_APIKEY")


def get_proxies(TG_USERNAME: str):
    result = requests.get(f"https://api.best-proxies.ru/proxylist.txt?key={BESTPROXIES_APIKEY}&uptime=1&limit=0")

    data = "\n".join(filter(lambda x: ":4444" not in x, result.text.split())) + "\n"

    with open(f"{TG_USERNAME}/proxylist.txt", "a") as file:
        file.write(data)

    with open(f"{TG_USERNAME}/proxylist.txt") as file:
        newdata = "".join(set(file.readlines()))

    with open(f"{TG_USERNAME}/proxylist.txt", "w") as file:
        file.write(newdata)

    return data, newdata
