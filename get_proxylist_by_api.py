import os

import requests
from dotenv import load_dotenv

load_dotenv()


BESTPROXIES_APIKEY = os.getenv("BESTPROXIES_APIKEY")


def get_proxies(TG_USERNAME: str):
    # сначала смотрим глобальный проксилист, потом если все прокси из этого листа уже юзаные или хуевые то обновляем глобальный проксилист и локальный
    with open(f"{TG_USERNAME}/used_proxies.txt") as file:
        used_proxies = [i.rstrip() for i in file.readlines()]

    with open(f"{TG_USERNAME}/bad_proxies.txt") as file:
        bad_proxies = [i.rstrip() for i in file.readlines()]

    with open("proxylist.txt") as file:
        data = [
            i.rstrip()
            for i in file.readlines()
            if i.rstrip() not in used_proxies and i.rstrip() not in bad_proxies and len(i.rstrip().split(":")) == 2
        ]
    if not data:
        result = requests.get(f"http://api.best-proxies.ru/proxylist.txt?key={BESTPROXIES_APIKEY}&uptime=1&limit=0")
        data = list(filter(lambda x: ":4444" not in x and len(x.split(":")) == 2, result.text.split()))

    with open(f"{TG_USERNAME}/proxylist.txt", "w") as file:
        file.write("\n".join(data) + "\n")

    with open("proxylist.txt", "a") as file:
        file.write("\n".join(data) + "\n")

    with open("proxylist.txt") as file:
        newdata = "".join(set(file.readlines()))

    with open("proxylist.txt", "w") as file:
        file.write(newdata)

    return data
