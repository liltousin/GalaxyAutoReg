import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()


BESTPROXIES_APIKEY = os.getenv("BESTPROXIES_APIKEY")


def get_new_unused_proxies():
    result = requests.get(f"http://api.best-proxies.ru/proxylist.txt?key={BESTPROXIES_APIKEY}&uptime=1&limit=0")
    print(result.text)
    with open("used_proxies.txt") as file:
        used_proxies = [i.rstrip() for i in file.readlines()]
    data = list(
        filter(
            lambda x: ":4444" not in x
            and len(x.split(":")) == 2
            and x.rstrip().split(":")[1]
            and ")" not in x
            and "(" not in x
            and x not in used_proxies,
            result.text.split(),
        )
    )
    random.shuffle(data)
    return data
