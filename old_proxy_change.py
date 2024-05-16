# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

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


while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="VPN RU"):
    time.sleep(1)
    print(30, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
el41 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="VPN RU")
el41.click()
while not driver.find_elements(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl"):
    time.sleep(1)
    print(31, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
if driver.find_element(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl").get_attribute("text") == "DISCONNECT":
    el42 = driver.find_element(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl")
    el42.click()
    while not driver.find_elements(by=AppiumBy.ID, value="android:id/button1"):
        time.sleep(1)
        print(32, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
    el43 = driver.find_element(by=AppiumBy.ID, value="android:id/button1")
    el43.click()
while not driver.find_elements(by=AppiumBy.ID, value="com.giamping.russiavpn:id/editTextHostname"):
    time.sleep(1)
    print(33, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
el44 = driver.find_element(by=AppiumBy.ID, value="com.giamping.russiavpn:id/editTextHostname")
used_proxy = el44.get_attribute("text")
with open("used_proxies.txt") as file:
    used_proxies = [i.rstrip() for i in file.readlines()]
if used_proxy not in used_proxies:
    with open("used_proxies.txt", "a") as file:
        file.write(used_proxy + "\n")
    used_proxies.append(used_proxy)
el44.click()

for _ in range(15):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(1024, 344)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(1024, 701)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(1)
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(1024, 344)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.move_to_location(1024, 1201)
actions.w3c_actions.pointer_action.release()
actions.perform()
while not driver.find_elements(by=AppiumBy.ID, value="android:id/button1"):
    time.sleep(1)
    print(34, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
el45 = driver.find_element(by=AppiumBy.ID, value="android:id/button1")
el45.click()
time.sleep(1)
while driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Latency checking...")'):
    time.sleep(1)
    print(35, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")

found_proxy = False
while not found_proxy:
    while not driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("com.giamping.russiavpn:id/location")'):
        time.sleep(1)
        print(36, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
    els1 = driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("com.giamping.russiavpn:id/location")')
    for el in els1:
        if el.get_attribute("text").split()[-1] not in used_proxies and el.get_attribute("text").split()[0] == "RU":
            el46 = el
            el46.click()
            found_proxy = True
            break
    if not found_proxy:
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(1024, 521)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(1024, 344)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
while not driver.find_elements(by=AppiumBy.ID, value="android:id/button1"):
    time.sleep(1)
    print(37, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
el47 = driver.find_element(by=AppiumBy.ID, value="android:id/button1")
el47.click()

while not driver.find_elements(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl"):
    time.sleep(1)
    print(38, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
el48 = driver.find_element(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl")
el48.click()
while not driver.find_elements(by=AppiumBy.ID, value="android:id/button1"):
    time.sleep(1)
    print(39, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
el49 = driver.find_element(by=AppiumBy.ID, value="android:id/button1")
el49.click()

while not driver.find_elements(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl"):
    # time.sleep(1)
    # print(40, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
    # if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("skipButton")'):
    #     el50 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("skipButton")')
    #     el50.click()
    # if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("closeButton")'):
    #     el51 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("closeButton")')
    #     el51.click()
    # if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("mrail_close")'):
    #     el52 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("mrail_close")')
    #     el52.click()
    time.sleep(22)
    print(40, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, sep="\t")
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(1033, 39)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(8)
if driver.find_element(by=AppiumBy.ID, value="com.giamping.russiavpn:id/buttonControl").get_attribute("text") == "DISCONNECT":
    print("Proxy changed!!!")
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(542, 1857)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)
actions.w3c_actions.pointer_action.release()
actions.perform()
time.sleep(1)
