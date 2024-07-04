# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

import argparse
import random
import string
import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from new_proxy_change import change_proxy
from utils import choose_city_by_statistics, get_text, get_time_of_day

parser = argparse.ArgumentParser()
parser.add_argument("--udid", required=True, help="UDID of the device.")
parser.add_argument("--appium-port", type=int, default=4723, help="Appium server port.")
parser.add_argument("--tg-username", required=True, help="Telegram username where traffic will go.")
args = parser.parse_args()

options = AppiumOptions()
options.load_capabilities(
    {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "udid": args.udid,  # 127.0.0.1:6555
    }
)

driver = webdriver.Remote(f"http://127.0.0.1:{args.appium_port}", options=options)  # 4723
c = 0
gc = 0
mc = 0
mac = 0
asc = 0

TG_USERNAME = args.tg_username
with open(f"{TG_USERNAME}/already_spammed.txt") as file:
    asc = len(file.readlines())


for _ in range(1000):
    proxy_data = change_proxy(driver, TG_USERNAME, c, gc, mc, mac, asc)

    c = 0
    need_new_proxy = False
    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
    while not driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]'):
        time.sleep(1)
        print(6, st, c, gc, mc, mac, asc, sep="\t")
    el14 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]')
    el14.click()
    while c < 4 and not need_new_proxy:
        tc = 0
        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")') or driver.find_elements(
            by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"
        ):
            time.sleep(1)
            print(7, st, c, gc, mc, mac, asc, sep="\t")
            # driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/panel_chat")
            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                el15 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character")
                el15.click()
            tc += 1
            # надо ебануть проверку а не на акке ли он уже
            if tc > 20:
                # может хуйня выйти просто потому что не вышел с акка (однако может быть залупная загрузка поэтому все правильно)
                # если залупная загрузка то лучше просто назад нажать и все пройдет (только хуй знает как ее вычислить)
                # может меньше чем за 10 секунд нахуй послать
                # может почему то с прошлой хуйни остаться dialog confirm cancel иззач его будет бесконечно скипать прокси
                # надо добавить проверку
                need_new_proxy = True
                break

        if not need_new_proxy:
            el16 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")')
            el16.click()
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")'):
                time.sleep(1)
                print(8, st, c, gc, mc, mac, asc, sep="\t")
            el17 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")')
            el17.click()
            # может ебануться хуевая загрузка и краш
            el18 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            el18.click()
            # может нихуя не кликнуться из-за хуевой загрузки
            # ОПЯТЬ ТАКАЯ ХУЙНЯ
            el18.send_keys("".join(random.choice(string.ascii_letters + string.digits) for _ in range(12)))
            driver.execute_script("mobile: hideKeyboard")
            tc = 0
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            # и одновременно с этим username avalible
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("registration_button")'):
                time.sleep(1)
                print(9, st, c, gc, mc, mac, asc, sep="\t")
                tc += 1
                if tc > 10:
                    need_new_proxy = True
                    actions = ActionChains(driver)
                    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                    actions.w3c_actions.pointer_action.move_to_location(231, 1851)
                    actions.w3c_actions.pointer_action.pointer_down()
                    actions.w3c_actions.pointer_action.pause(0.1)
                    actions.w3c_actions.pointer_action.release()
                    actions.perform()

                    actions = ActionChains(driver)
                    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                    actions.w3c_actions.pointer_action.move_to_location(231, 1851)
                    actions.w3c_actions.pointer_action.pointer_down()
                    actions.w3c_actions.pointer_action.pause(0.1)
                    actions.w3c_actions.pointer_action.release()
                    actions.perform()

                    # driver.execute_script('mobile: pressKey', {"keycode": 4})

                    break

        if not need_new_proxy:
            # почему то модет на нажаться финиш
            time.sleep(1)
            el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("registration_button")')
            el19.click()
            el20 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok")
            el20.click()

            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            # driver.find_elements(
            #     by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="ru.mobstudio.andgalaxy:id/menulist"]'
            # )

            while not driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]'):
                time.sleep(1)
                print(10, st, c, gc, mc, mac, asc, sep="\t")
                if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel"):
                    el21 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                    el21.click()
                    need_new_proxy = True
                    break

        if not need_new_proxy:
            time.sleep(1)
            # вообще в идеале тут ебануть цикл
            el22 = driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]')
            if el22:
                el22[0].click()
            else:
                driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel").click()
                time.sleep(5)
                if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                    need_new_proxy = True
                    break

            # бля надо фиксить уже 3 раз такая хуйня тут
            # и файнд элемент хуево и клик хуево ошибка нахоженения элемента
            # может не нажаться какогото хуя хз почему (изза сонекш лост)
            time.sleep(1)
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")') or driver.find_elements(
                by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/browser_loader"
            ):
                time.sleep(1)
                print(11, st, c, gc, mc, mac, asc, sep="\t")
            if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Confirm registration")'):
                need_new_proxy = True
                actions = ActionChains(driver)
                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(515, 1740)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.move_to_location(515, 147)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'):
                    time.sleep(1)
                    print(12, st, c, gc, mc, mac, asc, sep="\t")
                el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")')
                el23.click()
                time.sleep(1)

        if not need_new_proxy:
            el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")')
            el23.click()
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            # должно прогрузиться все полностью перед нажатием иначе будет клик по какому-то челу
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="your location") and not driver.find_elements(
                by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("My Location")'
            ):
                time.sleep(1)
                print(13, st, c, gc, mc, mac, asc, sep="\t")
                # зависло на френдс
                # просто нахуй белый экран вместо френдс
                # надо диалог конфирм
            if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="your location"):
                el24 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="your location")
                el24.click()
            else:
                el25 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("My Location")')
                el25.click()
            cities = [
                ("Москва", 13150),
                ("Санкт-Петербург", 5598),
                ("Новосибирск", 1634),
                ("Екатеринбург", 1536),
                ("Казань", 1319),
                ("Красноярск", 1205),
                ("Нижний Новгород", 1205),
                ("Челябинск", 1177),
                ("Уфа", 1163),
                ("Самара", 1159),
                ("Ростов-на-Дону", 1140),
                ("Краснодар", 1139),
                ("Омск", 1104),
                ("Воронеж", 1046),
                ("Пермь", 1027),
                ("Волгоград", 1019),
                ("Саратов", 887),
                ("Тюмень", 861),
                ("Тольятти", 668),
                ("Махачкала", 622),
                ("Барнаул", 620),
                ("Ижевск", 619),
                ("Хабаровск", 616),
                ("Ульяновск", 612),
                ("Иркутск", 606),
                ("Владивосток", 592),
                ("Ярославль", 567),
                ("Севастополь", 561),
                ("Ставрополь", 557),
                ("Томск", 545),
                ("Кемерово", 545),
                ("Набережные Челны", 544),
                ("Оренбург", 537),
                ("Новокузнецк", 531),
                ("Балашиха", 530),
                ("Рязань", 521),
                ("Чебоксары", 496),
                ("Калининград", 490),
                ("Пенза", 488),
                ("Липецк", 485),
                ("Киров", 475),
                ("Астрахань", 466),
                ("Тула", 462),
                ("Сочи", 445),
                ("Курск", 437),
                ("Улан-Удэ", 436),
                ("Сургут", 420),
                ("Тверь", 413),
                ("Магнитогорск", 409),
                ("Брянск", 373),
                ("Якутск", 368),
                ("Иваново", 358),
                ("Владимир", 344),
                ("Симферополь", 337),
                ("Грозный", 334),
                ("Чита", 333),
                ("Нижний Тагил", 331),
                ("Калуга", 330),
                ("Белгород", 328),
                ("Волжский", 315),
                ("Подольск", 313),
                ("Вологда", 312),
                ("Саранск", 311),
                ("Смоленск", 311),
                ("Курган", 302),
                ("Череповец", 299),
                ("Архангельск", 297),
                ("Владикавказ", 293),
                ("Орёл", 292),
                ("Нижневартовск", 291),
                ("Йошкар-Ола", 285),
                ("Стерлитамак", 280),
                ("Мытищи", 275),
                ("Мурманск", 267),
                ("Кострома", 266),
                ("Новороссийск", 262),
                ("Химки", 257),
                ("Тамбов", 256),
                ("Нальчик", 246),
                ("Таганрог", 242),
                ("Нижнекамск", 240),
                ("Благовещенск", 240),
                ("Люберцы", 236),
                ("Петрозаводск", 236),
                ("Комсомольск-на-Амуре", 235),
                ("Королёв", 226),
                ("Энгельс", 223),
                ("Великий Новгород", 222),
                ("Шахты", 221),
                ("Братск", 220),
                ("Сыктывкар", 220),
                ("Ангарск", 217),
                ("Старый Оскол", 217),
                ("Дзержинск", 215),
                ("Красногорск", 193),
                ("Орск", 188),
                ("Одинцово", 187),
                ("Псков", 187),
                ("Абакан", 186),
                ("Армавир", 185),
            ]
            cities_by_probability = [cities[j][0] for j in range(len(cities)) for _ in range(cities[j][1] // 10)]
            city = random.choice(cities_by_probability)
            city = choose_city_by_statistics()
            print(f"NEW CHOSEN CITY: {city}", time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, mac, asc, sep="\t")
            city_is_entered = False
            while not city_is_entered:
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText"):
                    time.sleep(1)
                    print(14, st, c, gc, mc, mac, asc, sep="\t")
                    # могут прогрузиться люди и кликнуться на чела (надо проверку сделать если вдруг будет видно message то это все гг)
                    # может быть error while loading
                el26 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                el26.click()
                el26.send_keys(city)
                # пиздец теперь сенд кей крашит если хуйня вылезла
                actions = ActionChains(driver)
                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                tc = 0
                city_is_entered = True
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)'):
                    time.sleep(1)
                    print(15, st, c, gc, mc, mac, asc, sep="\t")
                    # может тут стопнуться и нихуя не введя город и хуй вообще зает как это фиксить вообще и чтоб не криво все было (вроде пофиксил)
                    tc += 1
                    # может конекшн эррор еабнуться
                    if tc > 20 and driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText").get_attribute("text") == "":
                        # краш потому что find element
                        # а еще надо ебануть dialog confirm button
                        city_is_entered = False
                        break
            el27 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)')
            el27.click()

            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(
                by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Find friends")'
            ) and not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("No friends yet")'):
                time.sleep(1)
                print(16, st, c, gc, mc, mac, asc, sep="\t")
                # сюда тоже может прилететь конекшн лост ааааааааааааа
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]'):
                time.sleep(1)
                print(17, st, c, gc, mc, mac, asc, sep="\t")
            el28 = driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]')
            if el28:
                el28[0].click()
            # может не нажаться если пидорасы и тогда с экзитом траблы будут (надо убедиться что до экзита пролистнул)
            time.sleep(1)
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(515, 1740)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(515, 147)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            city_start = time.time()
            good_messages = 0
            for _ in range(25):
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")'):
                    time.sleep(0.1)
                    print(18, st, c, gc, mc, mac, asc, sep="\t")
                el29 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")')
                # может не кликнуться из-за авторитета (я ебал то есть он вообще в любом месте может быть ахуеть)
                el29.click()
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                tc = 0
                while not driver.find_elements(
                    by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
                ):
                    time.sleep(0.1)
                    print(19, st, c, gc, mc, mac, asc, sep="\t")
                    tc += 1
                    if tc > 50:
                        tc = 0
                        el30 = driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                        if el30:
                            el30[0].click()
                        if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                            need_new_proxy = True
                            break
                        # может на страницу с планетой выкинуть почему то видимо не прогрузилось как то или хз непонятно в общем

                if not need_new_proxy:
                    el31 = driver.find_element(
                        by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
                    )
                    el31.click()
                    # не прокликнулось чет хз почему
                    # может вылетететь конекшн лост надо try except
                    found_new_user = False
                    while not found_new_user and not need_new_proxy:
                        # может зависнуть тут если кончится прокся в процессе
                        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("people_near_loader")'):
                            el32 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("people_near_loader")')
                            el32.click()
                        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                        tc = 0
                        while not driver.find_elements(
                            by=AppiumBy.XPATH,
                            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.widget.TextView',
                        ):
                            time.sleep(0.1)
                            print(20, st, c, gc, mc, mac, asc, sep="\t")
                            tc += 1
                            if tc > 50:
                                tc = 0
                                el33 = driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                                if el33:
                                    el33[0].click()
                                if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                    need_new_proxy = True
                                    break
                        if need_new_proxy:
                            break
                        els1 = driver.find_elements(
                            by=AppiumBy.XPATH,
                            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View/android.widget.'
                            + 'TextView[1]|//android.view.View[@resource-id="people_near_content"]/android.view.View/android.widget.TextView',
                        )
                        for el in els1:
                            # может наебнуться если дарят авторитет надо try except (вроде пофиксил но не точно) (теперь вроде точно)
                            try:
                                nickname = el.get_attribute("text")
                            except Exception:
                                time.sleep(5)
                                driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel").click()
                                time.sleep(5)
                                if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                    need_new_proxy = True
                                    break
                                nickname = el.get_attribute("text")
                            with open(f"{TG_USERNAME}/already_spammed.txt") as file:
                                already_spammed = file.readlines()
                            if nickname + "\n" not in already_spammed:
                                with open(f"{TG_USERNAME}/already_spammed.txt", "a") as file:
                                    file.write(nickname + "\n")
                                    asc += 1
                                el.click()
                                found_new_user = True
                                break
                        if not found_new_user and not need_new_proxy:
                            # надо какой то таймаут еьануть чтоб было понятно что проксе пизда
                            # ну или нажать кнопку вверх (если все слишком хуево то вот так и делаем)
                            # но нахуй проксю менять понадежнее будет
                            # можно попробовать сделать пролистывание с помощью кнопки вниз
                            actions = ActionChains(driver)
                            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                            actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
                            actions.w3c_actions.pointer_action.pointer_down()
                            actions.w3c_actions.pointer_action.move_to_location(1000, 900)
                            actions.w3c_actions.pointer_action.release()
                            actions.perform()

                if not need_new_proxy:
                    # может вылетететь нахуй прилодение
                    # опять сука вылетело
                    # может наебнуться так что не нажмется почему-то
                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    tc = 0
                    app_crashed = False
                    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="MESSAGE"):
                        time.sleep(0.1)
                        print(21, st, c, gc, mc, mac, asc, sep="\t")
                        # может нахуй не кликунтсья на чела надо фиксить
                        # надо принтить чела которрого выбрало
                        # (это все изза Error while loading но по чему то он не выбрасывает на login_new_character)
                        tc += 1
                        if tc > 50:
                            tc = 0
                            el34 = driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]')
                            if el34:
                                el34[0].click()
                                app_crashed = True
                            el35 = driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]')
                            if app_crashed and el35:
                                el35[0].click()
                                time.sleep(1)
                                need_new_proxy = True
                                actions = ActionChains(driver)
                                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                                actions.w3c_actions.pointer_action.move_to_location(515, 1740)
                                actions.w3c_actions.pointer_action.pointer_down()
                                actions.w3c_actions.pointer_action.move_to_location(515, 147)
                                actions.w3c_actions.pointer_action.release()
                                actions.perform()
                                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'):
                                    time.sleep(1)
                                    print(22, st, c, gc, mc, mac, asc, sep="\t")
                                driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")').click()
                                break
                            el36 = driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                            if el36:
                                el36[0].click()
                            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                need_new_proxy = True
                                break

                if not need_new_proxy:
                    el37 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="MESSAGE")
                    el37.click()
                    # тоже может нихуя не кликнуться из-за конекшн лост надо try except
                    # а может просто нихуя не кликнуться пиздец
                    mac += 1

                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    tc = 0
                    while (
                        not driver.find_elements(
                            by=AppiumBy.ANDROID_UIAUTOMATOR,
                            value='new UiSelector().text("This user receives private messages only from Friends. '
                            + 'You can send a request to private message")',
                        )
                        and not driver.find_elements(
                            by=AppiumBy.ANDROID_UIAUTOMATOR,
                            value='new UiSelector().text("You can\'t private message this user because they have punishment")',
                        )
                        and not driver.find_elements(
                            by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                        )
                    ):
                        time.sleep(0.1)
                        # нахуй вылетело приложение хуй знает почему
                        print(23, st, c, gc, mc, mac, asc, sep="\t")
                        tc += 1
                        if tc > 50:
                            tc = 0
                            el38 = driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                            if el38:
                                el38[0].click()
                            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                need_new_proxy = True
                                break
                    if driver.find_elements(
                        by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                    ):
                        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                        while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText") or not driver.find_elements(
                            by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/ab_galaxy_subtitle")'
                        ):
                            time.sleep(0.1)
                            print(24, st, c, gc, mc, mac, asc, sep="\t")
                        if (
                            driver.find_element(
                                by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/ab_galaxy_subtitle")'
                            ).get_attribute("text")
                            == "Online"
                        ):
                            good_messages += 1
                        el39 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                        el39.send_keys(get_text(TG_USERNAME))
                        el40 = driver.find_element(
                            by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                        )
                        # тут может нихуя не кликнуться и крашнуться (уже 2 раз такое)
                        try:
                            el40.click()
                        except Exception:
                            time.sleep(5)
                            driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel").click()
                            time.sleep(5)
                            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                need_new_proxy = True
                                break
                        mc += 1

                if not need_new_proxy:
                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    tc = 0
                    while not driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]'):
                        time.sleep(0.1)
                        print(25, st, c, gc, mc, mac, asc, sep="\t")
                        tc += 1
                        if tc > 10:
                            tc = 0
                            el41 = driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                            if el41:
                                el41[0].click()
                            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                need_new_proxy = True
                                break

                if not need_new_proxy:
                    el42 = driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]')
                    if el42:
                        el42[0].click()
                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    tc = 0
                    while not driver.find_elements(
                        by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")'
                    ) or not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("MENU")'):
                        time.sleep(0.1)
                        # вылетело приложение с нихуя
                        # виснит пиздец не грузт чет нихуя какогото хуя
                        print(26, st, c, gc, mc, mac, asc, sep="\t")
                        tc += 1
                        if tc > 50:
                            tc = 0
                            el43 = driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                            if el43:
                                el43[0].click()
                            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                                need_new_proxy = True
                                break
                            el44 = driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]')
                            if el44:
                                el44[0].click()

                if need_new_proxy:
                    break
            city_end = time.time()

            if not need_new_proxy:
                messages_per_minute = str(round(25 / ((city_end - city_start) / 60), 2)).replace(".", ",")
                current_time = time.localtime()
                time_of_day = get_time_of_day(current_time)

                ts = time.strftime("%Y.%m.%d %H:%M", current_time)
                profit = f"{int((good_messages/25)*100)},00%"
                # days_from_the_start = 0
                # with open("statistics.txt") as file:
                #     initial_row = file.readline().rstrip()
                # if initial_row:
                #     days_from_the_start = (time.mktime(current_time) - time.mktime(time.strptime(initial_row.split("\t")[2], "%Y.%m.%d %H:%M"))) / (
                #         60 * 60 * 24
                #     )
                # days_from_the_start_formatted = f"{days_from_the_start:.4f}".replace(".", ",")
                with open("statistics.txt", "a") as file:
                    file.write(f"{city}\t{profit}\t{ts}\t{time_of_day}\n")

        # if need_to_exit:
        # хотя блять нахуй мозги себе ебать когда всего 2 раза такая залупа
        # похуй пусть для надежнрсоти будет епта
        if not need_new_proxy:
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(515, 1740)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(515, 147)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'):
                time.sleep(1)
                print(27, st, c, gc, mc, mac, asc, sep="\t")
            el45 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")')
            el45.click()
            time.sleep(1)
            if not need_new_proxy:
                c += 1
                gc += 1

    print(f"Акков зарегано на проксю: {c}")
    print(f"Акков зарегано всего: {gc}")
    print(f"Сообщений отправлено: {mc}")
    print(f"Попыток отправки сообщений: {mac}")
    print(f"Сообщений отправлено за все время: {asc}")
    print(f"need_new_proxy={need_new_proxy}")
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(542, 1851)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(1)

    with open(f"{TG_USERNAME}/used_proxies.txt", "a") as file:
        file.write(proxy_data + "\n")
