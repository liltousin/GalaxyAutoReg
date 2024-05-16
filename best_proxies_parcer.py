import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH")

with open(f"{DOWNLOADS_PATH}/Список прокси (прокси лист).html") as fp:
    soup = BeautifulSoup(fp, "lxml")

data = ""

for i in soup.find_all("tbody")[1].find_all("tr"):
    if i.find_all("td")[1].find_all("i"):
        data_ip = i.find_all("td")[0].find_all("div")[0].find_all("a")[1].get("data-ip")
        data_port = i.find_all("td")[0].find_all("div")[0].find_all("a")[1].get("data-port")
        data += data_ip + ":" + data_port + "\n"

with open("proxylist.txt", "a") as file:
    file.write(data)

with open("proxylist.txt") as file:
    newdata = "".join(set(file.readlines()))

with open("proxylist.txt", "w") as file:
    file.write(newdata)

print(data)
print(newdata)
