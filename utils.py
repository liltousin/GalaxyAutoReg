import os
import random
import time

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


def get_text(TG_USERNAME: str):
    with open(f"{TG_USERNAME}/text_template.txt") as file:
        data = "".join(file.readlines()).replace("*", " ").format(TG_USERNAME)
    return "".join([random.choice(i.split(";")) for i in data.split("\n")])


def get_quarter_of_day(current_time: time.struct_time) -> int:
    hour = int(time.strftime("%H", current_time))
    if 6 <= hour < 12:
        return 2
    elif 12 <= hour < 18:
        return 3
    elif 18 <= hour < 24:
        return 4
    return 1


def add_data_to_statistics(city: str, good_messages: int, message_attempts: int):
    # messages_per_minute = str(round((message_attempts) / ((city_end - city_start) / 60), 2)).replace(".", ",")
    current_time = time.localtime()
    quarter_of_day = get_quarter_of_day(current_time)
    date_and_time = time.strftime("%Y.%m.%d %H:%M:%S", current_time)
    profit = f"{((good_messages/message_attempts)*100):.2f}%".replace(".", ",")
    with open("statistics.txt", "a") as file:
        file.write(f"{city}\t{good_messages}\t{message_attempts}\t{profit}\t{date_and_time}\t{quarter_of_day}\n")


def choose_city_by_statistics() -> str:
    current_quarter_of_day = get_quarter_of_day(time.localtime())
    with open("statistics.txt") as file:
        # можно потом в теории по часу делать а не по времени суток
        # а что если сделать не по среднему значению а по последнему значению в определенный час или по среднему из трех последних в определенный час
        quarter_of_day_statistics = list(
            filter(lambda x: int(x[5]) == current_quarter_of_day, map(lambda x: x.rstrip().split("\t"), file.readlines()))
        )
    city_probabilities = list(
        set(
            map(
                lambda x: (
                    x[0],
                    (
                        sum(map(lambda y: int(y[1]), filter(lambda y: x[0] == y[0], quarter_of_day_statistics)))
                        / sum(map(lambda y: int(y[2]), filter(lambda y: x[0] == y[0], quarter_of_day_statistics)))
                    ),
                ),
                quarter_of_day_statistics,
            )
        )
    )
    city_names = (
        "Москва, Санкт-Петербург, Новосибирск, Екатеринбург, Казань, Красноярск, Нижний Новгород, Челябинск, Уфа, Самара, Ростов-на-Дону, "
        + "Краснодар, Омск, Воронеж, Пермь, Волгоград, Саратов, Тюмень, Тольятти, Махачкала, Барнаул, Ижевск, Хабаровск, Ульяновск, Иркутск, "
        + "Владивосток, Ярославль, Севастополь, Ставрополь, Томск, Кемерово, Набережные Челны, Оренбург, Новокузнецк, Балашиха, Рязань, Чебоксары, "
        + "Калининград, Пенза, Липецк, Киров, Астрахань, Тула, Сочи, Курск, Улан-Удэ, Сургут, Тверь, Магнитогорск, Брянск, Якутск, Иваново, "
        + "Владимир, Симферополь, Грозный, Чита, Нижний Тагил, Калуга, Белгород, Волжский, Подольск, Вологда, Саранск, Смоленск, Курган, Череповец, "
        + "Архангельск, Владикавказ, Орёл, Нижневартовск, Йошкар-Ола, Стерлитамак, Мытищи, Мурманск, Кострома, Новороссийск, Химки, Тамбов, Нальчик, "
        + "Таганрог, Нижнекамск, Благовещенск, Люберцы, Петрозаводск, Комсомольск-на-Амуре, Королёв, Энгельс, Великий Новгород, Шахты, Братск, "
        + "Сыктывкар, Ангарск, Старый Оскол, Дзержинск, Красногорск, Орск, Одинцово, Псков, Абакан, Армавир"
    ).split(", ")
    all_city_probabilities = []
    for i in city_names:
        t = (i, 100)
        for j in city_probabilities:
            if i == j[0]:
                t = j
                break
        if t[1] == 0:
            t = (t[0], 1)
        all_city_probabilities.append(t)
    return random.choices([i[0] for i in all_city_probabilities], [i[1] ** (2.71828182846) for i in all_city_probabilities])[0]


if __name__ == "__main__":
    print(get_text(input()))
    data = get_new_unused_proxies()

    with open("proxylist.txt", "w") as file:
        file.write(("\n".join(data) + "\n"))
