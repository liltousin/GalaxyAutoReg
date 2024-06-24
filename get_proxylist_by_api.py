import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()


BESTPROXIES_APIKEY = os.getenv("BESTPROXIES_APIKEY")


def get_new_unused_proxies():
    headers = requests.utils.default_headers()

    headers.update({"User-Agent": "My User Agent 1.0"})

    result = requests.get(f"https://api.best-proxies.ru/proxylist.txt?key={BESTPROXIES_APIKEY}&uptime=1&limit=0", headers=headers)
    print(result.text)
    with open("used_proxies.txt") as file:
        used_proxies = [i.rstrip() for i in file.readlines()]
    data = list(
        filter(
            lambda x: len(x.split(":")) == 2 and x.rstrip().split(":")[1] and ")" not in x and "(" not in x and x not in used_proxies,
            result.text.split(),
        )
    )
    random.shuffle(data)
    return data


if __name__ == "__main__":
    data = get_new_unused_proxies()

    with open("proxylist.txt", "w") as file:
        file.write(("\n".join(data) + "\n"))
