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

for _ in range(100):
    proxy_data = change_proxy(driver, c, gc)

    c = 0
    need_new_proxy = False
    while not driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]'):
        time.sleep(1)
        print(6, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
    el14 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]')
    el14.click()
    while c < 4 and not need_new_proxy:
        # так же проверить driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
        tc = 0
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")') or driver.find_elements(
            by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"
        ):
            time.sleep(1)
            print(7, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
                el15 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character")
                el15.click()
            tc += 1
            if tc > 300:
                need_new_proxy = True
                break

        if not need_new_proxy:
            el16 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")')
            el16.click()
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")'):
                time.sleep(1)
                print(8, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
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
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")'):
                time.sleep(1)
                print(9, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")')
            el19.click()
            el20 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok")
            el20.click()

            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                time.sleep(1)
                print(10, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el21 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
            el21.click()
            time.sleep(1)
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")'):
                time.sleep(1)
                print(11, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Confirm registration")'):
                need_new_proxy = True

            if not need_new_proxy:
                el22 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")')
                el22.click()
                while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="your location"):
                    time.sleep(1)
                    print(12, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                el23 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="your location")
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
                while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText"):
                    time.sleep(1)
                    print(13, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
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
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)'):
                    time.sleep(1)
                    print(14, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                el25 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)')
                el25.click()

                while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                    time.sleep(1)
                    print(15, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
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
                while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")'):
                    time.sleep(1)
                    print(16, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                el27 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")')
                el27.click()

                for _ in range(25):
                    while not driver.find_elements(
                        by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
                    ):
                        time.sleep(1)
                        print(17, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                    el28 = driver.find_element(
                        by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
                    )
                    el28.click()

                    found_new_user = False
                    while not found_new_user:
                        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("people_near_loader")'):
                            el29 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("people_near_loader")')
                            el29.click()
                        while not driver.find_elements(
                            by=AppiumBy.XPATH,
                            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.widget.TextView',
                        ):
                            time.sleep(1)
                            print(18, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                        els1 = driver.find_elements(
                            by=AppiumBy.XPATH,
                            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.widget.TextView',
                        )
                        for el in els1:
                            nickname = el.get_attribute("text")
                            with open("already_spammed.txt") as file:
                                already_spammed = [i.rstrip() for i in file.readlines()]
                            if nickname in already_spammed:
                                continue
                            else:
                                with open("already_spammed.txt", "a") as file:
                                    file.write(nickname + "\n")
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

                    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="MESSAGE"):
                        time.sleep(1)
                        print(19, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                    el30 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="MESSAGE")
                    el30.click()
                    while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText"):
                        time.sleep(1)
                        print(20, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                    el31 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                    el31.click()
                    el31.send_keys(get_text())
                    while not driver.find_elements(
                        by=AppiumBy.ANDROID_UIAUTOMATOR,
                        value='new UiSelector().text("This user receives private messages only from Friends. '
                        + 'You can send a request to private message")',
                    ) and not driver.find_elements(
                        by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                    ):
                        time.sleep(1)
                        print(21, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                    if driver.find_elements(
                        by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                    ):
                        el32 = driver.find_element(
                            by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.widget.TextView'
                        )
                        el32.click()
                    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                        time.sleep(1)
                        print(21, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                    el33 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
                    el33.click()
                    time.sleep(1)

                    actions = ActionChains(driver)
                    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                    actions.w3c_actions.pointer_action.move_to_location(515, 1740)
                    actions.w3c_actions.pointer_action.pointer_down()
                    actions.w3c_actions.pointer_action.move_to_location(515, 147)
                    actions.w3c_actions.pointer_action.release()
                    actions.perform()
                    while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")'):
                        time.sleep(1)
                        print(22, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
                    el34 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Search")')
                    el34.click()

                while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                    time.sleep(1)
                    print(23, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
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
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'):
                time.sleep(1)
                print(24, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el36 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")')
            el36.click()
            time.sleep(1)
            if not need_new_proxy:
                c += 1
                gc += 1

    print(f"Акков зарегано на проксю: {c}")
    print(f"Акков зарегано всего: {gc}")
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
