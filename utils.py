import os
import random
import string
import time

import requests
from dotenv import load_dotenv

load_dotenv()


BESTPROXIES_APIKEY = os.getenv("BESTPROXIES_APIKEY")


def get_new_unused_proxies():
    headers = requests.utils.default_headers()

    headers.update({"User-Agent": "My User Agent 1.0"})

    result = requests.get(f"https://api.best-proxies.ru/proxylist.txt?key={BESTPROXIES_APIKEY}&uptime=1&limit=0", headers=headers)
    # print(result.text)
    # {"error":{"code":403,"message":"Ошибка авторизации: Период действия этого ключа окончен, Вы можете купить новый ключ"}}
    with open("conf_reg_proxies.txt") as file:
        conf_reg_proxies = [i.rstrip() for i in file.readlines()]
    data = list(
        filter(
            lambda x: len(x.split(":")) == 2
            and all(c in "0123456789" for c in x.rstrip().split(":")[1])
            and all(all(s in "0123456789" for s in c) for c in x.rstrip().split(":")[0].split("."))
            and x not in conf_reg_proxies,
            result.text.split(),
        )
    )
    random.shuffle(data)
    return data


def generate_text(tg_username: str, text_template: str):
    replacements = {  # 100% 1 в 1
        "Й": "Й И꙼",
        "К": "K 𝖪 Ⲕ ꓗ Κ К",
        "Е": "E Ε Е 𐊆 ꓰ ⴹ",
        "Н": "H 𝖧 Ⲏ 𐋏 Η Н ꓧ ᕼ",
        "Г": "Γ Г 𖼇",
        "З": "Ɜ З",
        "Х": "𐊐 X ⵝ Х Χ Ⅹ ꓫ Ⲭ ᙭ 𐊴 ᚷ 𝖷",
        "Ф": "Փ Ф Φ Ⲫ",
        "В": "B ꓐ Β В 𝖡 𐊂 𐊡",
        "А": "A 𝖠 А Α 𖽀 ꓮ 𐊠",
        "П": "Π Ⲡ П",
        "Р": "𝖯 P Р Ρ",
        "О": "O О Ο 𐐄",
        "С": "C С Ⅽ Ϲ",
        "М": "𝖬 M Μ М ꓟ Ⅿ Ϻ",
        "Т": "𝖳 𐊗 🝨 T ꓔ 𖼊 Т Τ 𐊱 𑢼",
        "й": "𐑍꙼ й ᴎ꙼",
        "у": "у 𝗒 y",
        "к": "ᴋ ⲕ ĸ κ к",
        "е": "e 𝖾 е",
        "н": "ʜ н",
        "г": "ᴦ г",
        "з": "з ᴈ",
        "х": "х 𝗑 x ⅹ",
        "ф": "ф ϕ",
        "в": "в ʙ",
        "а": "a а",
        "п": "ᴨ п",
        "р": "р p",
        "о": "𐓪 ⲟ 𝗈 о ο 𐐬 o ჿ",
        "л": "л ᴫ",
        "ё": "ë ё",
        "я": "ᴙ я",
        "с": "с c ᴄ ϲ 𝖼 ⅽ",
        "м": "м ᴍ",
        "и": "и ᴎ",
        "т": "т ᴛ",
    }
    message = ""
    # total_variants = 1
    for char in text_template:
        if char in replacements:
            message += random.choice(replacements[char].split(" "))
            # total_variants *= len(replacements[char].split(" "))
        else:
            message += char
    # print(total_variants)
    return message.replace("{}", tg_username)


def generate_nickname(tg_username: str):
    possible_characters = string.ascii_letters + string.digits + "[]/^{}_=`"
    print(len(possible_characters))
    if 14 - len(tg_username) > 3:
        random_characters = "".join(
            [random.choice(possible_characters)] + [random.choice(possible_characters + "-") for _ in range(14 - len(tg_username) - 1)]
        )
        n = random.randint(0, len(random_characters))
        if n == 0:
            return tg_username + random.choice("[]/^{}_=`-") + random_characters[n + 1 :]
        if n == 1:
            return random.choice("[]/^{}_=`") + tg_username + random.choice("[]/^{}_=`-") + random_characters[n + 1 :]
        if n == len(random_characters) - 1:
            return random_characters[: n - 1] + random.choice("[]/^{}_=`-") + tg_username + random.choice("[]/^{}_=`-")
        if n == len(random_characters):
            return random_characters[: n - 1] + random.choice("[]/^{}_=`-") + tg_username
        return random_characters[: n - 1] + random.choice("[]/^{}_=`-") + tg_username + random.choice("[]/^{}_=`-") + random_characters[n + 1 :]
    return "".join([random.choice(possible_characters)] + [random.choice(possible_characters + "-") for _ in range(13)])


def get_quarter_of_day(current_time: time.struct_time) -> int:
    hour = int(time.strftime("%H", current_time))
    if 6 <= hour < 12:
        return 2
    elif 12 <= hour < 18:
        return 3
    elif 18 <= hour < 24:
        return 4
    return 1


def get_statistic_row(
    city: str, good_messages: int, message_attempts: int, current_date_and_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), process_id=0
) -> str:
    # messages_per_minute = str(round((message_attempts) / ((city_end - city_start) / 60), 2)).replace(".", ",")
    return f"{city},{good_messages},{message_attempts},{current_date_and_time},{process_id}"


def choose_city_by_statistic() -> str:
    current_quarter_of_day = get_quarter_of_day(time.localtime())
    with open("statistic.csv") as file:
        # можно потом в теории по часу делать а не по времени суток
        # а что если сделать не по среднему значению а по последнему значению в определенный час или по среднему из трех последних в определенный час
        quarter_of_day_statistics = list(
            filter(
                lambda x: int(get_quarter_of_day(time.strptime(x[3], "%Y-%m-%d %H:%M:%S"))) == current_quarter_of_day,
                map(lambda x: x.rstrip().split(","), file.readlines()[1:]),
            )
        )
    city_probabilities = list(
        set(
            map(
                lambda x: (
                    x[0],
                    (
                        sum(map(lambda y: int(y[1]), filter(lambda y: x[0] == y[0], quarter_of_day_statistics)))
                        / sum(map(lambda y: int(y[2]), filter(lambda y: x[0] == y[0], quarter_of_day_statistics)))
                    )
                    * 100,
                ),
                quarter_of_day_statistics,
            )
        )
    )
    city_names = (
        "Москва, Санкт-Петербург, Новосибирск, Екатеринбург, Казань, Красноярск, Нижний Новгород, Челябинск, Самара, Ростов-на-Дону, "
        + "Краснодар, Омск, Воронеж, Пермь, Волгоград, Саратов, Тюмень, Тольятти, Махачкала, Барнаул, Ижевск, Хабаровск, Ульяновск, Иркутск, "
        + "Владивосток, Ярославль, Севастополь, Ставрополь, Томск, Кемерово, Набережные Челны, Оренбург, Новокузнецк, Балашиха, Рязань, Чебоксары, "
        + "Калининград, Пенза, Липецк, Киров, Астрахань, Тула, Сочи, Курск, Улан-Удэ, Сургут, Тверь, Магнитогорск, Брянск, Якутск, Иваново, "
        + "Владимир, Симферополь, Грозный, Чита, Нижний Тагил, Калуга, Белгород, Волжский, Подольск, Вологда, Саранск, Смоленск, Курган, Череповец, "
        + "Архангельск, Владикавказ, Орёл, Нижневартовск, Йошкар-Ола, Стерлитамак, Мытищи, Мурманск, Кострома, Новороссийск, Химки, Тамбов, Нальчик, "
        + "Таганрог, Нижнекамск, Благовещенск, Люберцы, Петрозаводск, Комсомольск-на-Амуре, Королёв, Энгельс, Великий Новгород, Шахты, Братск, "
        + "Сыктывкар, Ангарск, Старый Оскол, Дзержинск, Красногорск, Орск, Одинцово, Псков, Абакан, Армавир, Балаково"
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
    # k = 2.71828182846 TODO: сделать как аргумент
    k = 1
    return random.choices([i[0] for i in all_city_probabilities], [i[1] ** (k) for i in all_city_probabilities])[0]


if __name__ == "__main__":
    # print(get_text(input()))
    # print(generate_text(input(), input()))
    data = get_new_unused_proxies()

    with open("proxylist.txt", "w") as file:
        file.write(("\n".join(data) + "\n"))
