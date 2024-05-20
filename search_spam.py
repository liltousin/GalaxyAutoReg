# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

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
from text_generator import get_text

options = AppiumOptions()
options.load_capabilities(
    {
        "appium:deviceName": "Google_Pixel_2",
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
    }
)


driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
c = 0
gc = 0
mc = 0
mac = 0
asc = 0
with open("already_spammed.txt") as file:
    asc = len(file.readlines())


for _ in range(1000):
    proxy_data = change_proxy(driver, c, gc, mc, mac, asc)

    c = 0
    need_new_proxy = False
    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
    while not driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]'):
        time.sleep(1)
        print(6, st, c, gc, mc, mac, asc, sep="\t")
    el14 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]')
    el14.click()
    while c < 4 and not need_new_proxy:
        # так же проверить driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
        tc = 0
        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")') or driver.find_elements(
            by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"
        ):
            time.sleep(1)
            print(7, st, c, gc, mc, mac, asc, sep="\t")
            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                el15 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character")
                el15.click()
            tc += 1
            if tc > 100:
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
            el18 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            el18.click()
            el18.send_keys("".join(random.choice(string.ascii_letters + string.digits) for _ in range(12)))
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")'):
                time.sleep(1)
                print(9, st, c, gc, mc, mac, asc, sep="\t")
            el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")')
            el19.click()
            el20 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok")
            el20.click()

            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                time.sleep(1)
                print(10, st, c, gc, mc, mac, asc, sep="\t")
            el21 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
            el21.click()
            time.sleep(1)
            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")') or driver.find_elements(
                by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/browser_loader"
            ):
                time.sleep(1)
                print(11, st, c, gc, mc, mac, asc, sep="\t")
            if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Confirm registration")'):
                need_new_proxy = True

            if not need_new_proxy:
                el22 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")')
                el22.click()
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                # пофиксить выход из такой хуйни
                while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="your location") and not driver.find_elements(
                    by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("My Location")'
                ):
                    time.sleep(1)
                    print(12, st, c, gc, mc, mac, asc, sep="\t")
                if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="your location"):
                    el23 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="your location")
                else:
                    el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("My Location")')
                el23.click()
                cities = [
                    "Москва",
                    "Санкт-Петербург",
                    "Новосибирск",
                    "Екатеринбург",
                    "Казань",
                    "Нижний Новгород",
                    "Красноярск",
                    "Челябинск",
                    "Самара",
                    "Уфа",
                    "Ростов-на-Дону",
                    "Краснодар",
                    "Омск",
                    "Воронеж",
                    "Пермь",
                    "Волгоград",
                    "Саратов",
                    "Тюмень",
                    "Тольятти",
                    "Махачкала",
                    "Барнаул",
                    "Ижевск",
                    "Хабаровск",
                    "Ульяновск",
                    "Иркутск",
                    "Владивосток",
                    "Ярославль",
                    "Севастополь",
                    "Ставрополь",
                    "Томск",
                ]
                cities_by_probability = [cities[j] for j in range(len(cities)) for _ in range(len(cities) - j)]
                city = random.choice(cities_by_probability)
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText"):
                    time.sleep(1)
                    print(13, st, c, gc, mc, mac, asc, sep="\t")
                el24 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                el24.click()
                el24.send_keys(city)
                actions = ActionChains(driver)
                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)'):
                    time.sleep(1)
                    print(14, st, c, gc, mc, mac, asc, sep="\t")
                el25 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)')
                el25.click()

                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(
                    by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Find friends")'
                ) and not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("About me")'):
                    time.sleep(1)
                    print(15, st, c, gc, mc, mac, asc, sep="\t")
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                    time.sleep(1)
                    print(16, st, c, gc, mc, mac, asc, sep="\t")
                el26 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
                el26.click()
                time.sleep(1)

                actions = ActionChains(driver)
                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(515, 1740)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.move_to_location(515, 147)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")'):
                    time.sleep(1)
                    print(17, st, c, gc, mc, mac, asc, sep="\t")
                el27 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")')
                el27.click()

                for _ in range(25):
                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    while not driver.find_elements(
                        by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
                    ):
                        time.sleep(0.1)
                        print(18, st, c, gc, mc, mac, asc, sep="\t")
                    el28 = driver.find_element(
                        by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
                    )
                    el28.click()

                    found_new_user = False
                    while not found_new_user:
                        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("people_near_loader")'):
                            el29 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("people_near_loader")')
                            el29.click()
                        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                        while not driver.find_elements(
                            by=AppiumBy.XPATH,
                            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.widget.TextView',
                        ):
                            time.sleep(0.1)
                            print(19, st, c, gc, mc, mac, asc, sep="\t")
                        els1 = driver.find_elements(
                            by=AppiumBy.XPATH,
                            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.widget.TextView',
                        )
                        for el in els1:
                            nickname = el.get_attribute("text")
                            with open("already_spammed.txt") as file:
                                already_spammed = file.readlines()
                            if nickname + "\n" in already_spammed:
                                continue
                            else:
                                with open("already_spammed.txt", "a") as file:
                                    file.write(nickname + "\n")
                                    asc += 1
                                el.click()
                                found_new_user = True
                                break
                        if not found_new_user:
                            actions = ActionChains(driver)
                            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                            actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
                            actions.w3c_actions.pointer_action.pointer_down()
                            actions.w3c_actions.pointer_action.move_to_location(1000, 900)
                            actions.w3c_actions.pointer_action.release()
                            actions.perform()

                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="MESSAGE"):
                        time.sleep(0.1)
                        print(20, st, c, gc, mc, mac, asc, sep="\t")
                    el30 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="MESSAGE")
                    el30.click()
                    mac += 1

                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
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
                        print(21, st, c, gc, mc, mac, asc, sep="\t")
                    if driver.find_elements(
                        by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                    ):
                        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                        while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText"):
                            time.sleep(0.1)
                            print(22, st, c, gc, mc, mac, asc, sep="\t")
                        el31 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                        el31.send_keys(get_text())
                        mc += 1
                        el32 = driver.find_element(
                            by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                        )
                        el32.click()
                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                        time.sleep(0.1)
                        print(23, st, c, gc, mc, mac, asc, sep="\t")
                    el33 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
                    if el33:
                        el33[0].click()

                    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                    # можно педелать так чтобы не чекалось прям меню а просто если сломалось то фиксилось для повышения скорости
                    tc = 0
                    while not driver.find_elements(
                        by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")'
                    ) or not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("MENU")'):
                        time.sleep(0.1)
                        print(24, st, c, gc, mc, mac, asc, sep="\t")
                        tc += 1
                        if tc > 100:
                            el33 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
                            if el33:
                                el33[0].click()
                    el34 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")')
                    el34.click()

                st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
                while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                    time.sleep(1)
                    print(25, st, c, gc, mc, mac, asc, sep="\t")
                el35 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
                el35.click()
                time.sleep(1)

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
                print(26, st, c, gc, mc, mac, asc, sep="\t")
            el36 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")')
            el36.click()
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
    actions.w3c_actions.pointer_action.move_to_location(542, 1857)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(1)

    with open("used_proxies.txt", "a") as file:
        file.write(proxy_data + "\n")
