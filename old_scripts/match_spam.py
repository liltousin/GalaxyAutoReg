# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

import calendar
import os
import random
import string
import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from dotenv import load_dotenv

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

load_dotenv()


ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
DATING_BIO_TEXT = os.getenv("DATING_BIO_TEXT")
ACCOUNT_BIO_TEXT = os.getenv("ACCOUNT_BIO_TEXT")


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

    c = 0
    need_new_proxy = False
    if driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]'):
        el0 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]')
        el0.click()
    while c < 4 and not need_new_proxy:
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")') and not driver.find_elements(
            by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"
        ):
            time.sleep(1)
            print(1, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"):
            el31 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character")
            el31.click()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")'):
            time.sleep(1)
            print(2, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el1 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Female")')
        el1.click()
        el2 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")')
        el2.click()
        el3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
        el3.click()
        el3.send_keys("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)) + "123")
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")'):
            time.sleep(1)
            print(3, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el4 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")')
        el4.click()
        el5 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok")
        el5.click()

        while (
            not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Get started")')
            and not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("next_button")')
            and not driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/input")
        ):
            time.sleep(1)
            print(4, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        if driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/input"):
            el8 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
            el8.click()
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Find a Match")'):
                time.sleep(1)
                print(5, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el9 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Find a Match")')
            el9.click()
            while not driver.find_elements(
                by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Get started")'
            ) and not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("next_button")'):
                time.sleep(1)
                print(6, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("next_button")'):
            el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("next_button")')
            el10.click()
            el10.click()
        el11 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Get started")')
        el11.click()

        while not driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.EditText"):
            time.sleep(1)
            print(7, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el12 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
        el12.click()
        el12.send_keys(f"{ACCOUNT_NAME}")
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        el13 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("birthday_day_input-select")')
        el13.click()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("9")'):
            time.sleep(1)
            print(8, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        day = random.choice(string.digits[1:])
        el14 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().text("{day}")')
        el14.click()
        el15 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("birthday_month_input-select")')
        el15.click()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("September")'):
            time.sleep(1)
            print(9, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        month = random.choice(calendar.month_name[1:10])
        el16 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().text("{month}")')
        el16.click()
        el17 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("birthday_year_input-select")')
        el17.click()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("1998")'):
            time.sleep(1)
            print(10, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        year = random.randint(2003, 2005)
        el18 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().text("{year}")')
        el18.click()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Next")'):
            time.sleep(1)
            print(11, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Next")')
        el19.click()

        el20 = None
        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("No, select another")'):
            el20 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("No, select another")')
            el20.click()
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
            print(12, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el21 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
        el21.click()
        el21.send_keys(city)
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(1000, 1700)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)'):
            time.sleep(1)
            print(13, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el22 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("RU").instance(0)')
        el22.click()
        if not el20:
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Next")'):
                time.sleep(1)
                print(14, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            while not driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Next")').get_attribute("clickable"):
                time.sleep(1)
                print(15, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Next")')
            el23.click()
        else:
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(550, 850)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Add Photo")'):
            time.sleep(1)
            print(16, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el24 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Add Photo")')
        el24.click()
        while not driver.find_elements(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().className("android.widget.RelativeLayout").instance(0)',
        ):
            time.sleep(1)
            print(17, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        photo = random.randint(0, 5)
        el25 = driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value=f'new UiSelector().className("android.widget.RelativeLayout").instance({photo})',
        )
        el25.click()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("DONE")'):
            time.sleep(1)
            print(18, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el26 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("DONE")')
        el26.click()

        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("motto_input-textarea")'):
            time.sleep(1)
            print(19, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(701, 1770)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(701, 120)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
        el27 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("motto_input-textarea")')
        el27.click()
        el28 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
        el28.send_keys(f"{DATING_BIO_TEXT}")
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(905, 866)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(905, 99)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        time.sleep(1)
        el29 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Save")')
        el29.click()
        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Save")'):
            el29.click()
        time.sleep(1)

        while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
            time.sleep(1)
            print(20, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el30 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
        el30.click()
        time.sleep(1)
        while not driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/nav_item_profile_avatar"):
            time.sleep(1)
            print(21, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Confirm registration")'):
            need_new_proxy = True

        if not need_new_proxy:
            el31 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/nav_item_profile_avatar")
            el31.click()
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("EDIT")'):
                time.sleep(1)
                print(22, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el32 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("EDIT")')
            el32.click()
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("about-textarea")'):
                time.sleep(1)
                print(23, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el33 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("about-textarea")')
            el33.click()
            el33.send_keys(f"{ACCOUNT_BIO_TEXT}")
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(701, 1000)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(701, 51)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            time.sleep(1)
            el34 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("SAVE")')
            el34.click()
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                time.sleep(1)
                print(24, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el35 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
            el35.click()
            time.sleep(1)
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Find a Match")'):
                time.sleep(1)
                print(25, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el36 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Find a Match")')
            el36.click()

            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("js-like-btn")'):
                time.sleep(1)
                print(26, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.view.View").instance(19)'):
                time.sleep(1)
                print(27, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            likes = random.randint(100, 300)
            print(f"likes={likes}")
            for _ in range(likes):
                if not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.view.View").instance(19)'):
                    break
                if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Connection lost. Please re-enter")'):
                    el37 = driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel")
                    el37.click()
                    need_new_proxy = True
                    break
                if random.randint(0, 7):
                    el38 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("js-like-btn")')
                else:
                    el38 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("js-dislike-btn")')
                el38.click()
                time.sleep(random.randint(50, 150) / 100)

            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"):
                time.sleep(1)
                print(28, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
            el39 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
            el39.click()
            time.sleep(1)
            if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Confirm registration")'):
                need_new_proxy = True

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(515, 1740)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(515, 147)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'):
            time.sleep(1)
            print(29, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
        el40 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")')
        el40.click()
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
