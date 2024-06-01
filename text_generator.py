from random import choice


def get_text(TG_USERNAME: str):
    with open(f"{TG_USERNAME}/text_template.txt") as file:
        data = "".join(file.readlines()).replace("*", " ").format(TG_USERNAME)
    return "".join([choice(i.split(";")) for i in data.split("\n")])


if __name__ == "__main__":
    print(get_text(input()))
