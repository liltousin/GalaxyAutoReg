import os
from random import choice

from dotenv import load_dotenv

load_dotenv()


TG_USERNAME = os.getenv("TG_USERNAME")


def get_text():
    with open(f"{TG_USERNAME}/text_template.txt") as file:
        data = "".join(file.readlines()).replace("*", " ").format(TG_USERNAME)
    return "".join([choice(i.split(";")) for i in data.split("\n")])
