import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from utils import get_new_unused_proxies


def change_proxy(driver: webdriver.Remote, TG_USERNAME: str, c: int, gc: int, mc=0, mac=0, asc=0):
    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy"):
        time.sleep(1)
        print(0, st, c, gc, mc, mac, asc, sep="\t")
    el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy")
    el1.click()
    st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available.") and not driver.find_elements(
        by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Default Profile")'
    ):
        time.sleep(1)
        print(1, st, c, gc, mc, mac, asc, sep="\t")
    if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available."):
        el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Add proxy")
        el3.click()
    else:
        while driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Stop") or not driver.find_elements(
            by=AppiumBy.ACCESSIBILITY_ID, value="Start"
        ):
            time.sleep(1)
            print(2, st, c, gc, mc, mac, asc, sep="\t")
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(544, 1405)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
        el5 = driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]",
        )
        el5.click()

    found_good_proxy = False
    while not found_good_proxy:
        with open(f"{TG_USERNAME}/used_proxies.txt") as file:
            used_proxies = [i.rstrip() for i in file.readlines()]

        with open(f"{TG_USERNAME}/bad_proxies.txt") as file:
            bad_proxies = [i.rstrip() for i in file.readlines()]

        with open(f"{TG_USERNAME}/proxylist.txt") as file:
            proxies_data = [
                i.rstrip()
                for i in file.readlines()
                if i.rstrip() not in used_proxies and i.rstrip() not in bad_proxies and len(i.rstrip().split(":")) == 2
            ]

        if proxies_data:
            proxy_data = proxies_data[0]
            proxy_ip, proxy_port = proxy_data.split(":")
        else:
            print("NEED NEW PROXIES!!!", time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, mac, asc, sep="\t")
            with open(f"{TG_USERNAME}/used_proxies.txt") as file:
                used_proxies = [i.rstrip() for i in file.readlines()]

            with open(f"{TG_USERNAME}/bad_proxies.txt") as file:
                bad_proxies = [i.rstrip() for i in file.readlines()]

            with open("proxylist.txt") as file:
                data = [
                    i.rstrip()
                    for i in file.readlines()
                    if i.rstrip() not in used_proxies
                    and i.rstrip() not in bad_proxies
                    and len(i.rstrip().split(":")) == 2
                    and i.rstrip().split(":")[1]
                    and "(" not in i
                    and ")" not in i
                ]
            if not data:
                data = get_new_unused_proxies()

            with open(f"{TG_USERNAME}/proxylist.txt", "w") as file:
                file.write("\n".join(data) + "\n")

            with open("proxylist.txt", "a") as file:
                file.write("\n".join(data) + "\n")

            with open("proxylist.txt") as file:
                newdata = "".join(set(file.readlines()))

            with open("proxylist.txt", "w") as file:
                file.write(newdata)
            time.sleep(5)
            continue
        el6 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.Button").instance(2)')
        el6.click()
        time.sleep(1)
        el7 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5")
        el7.click()
        time.sleep(1)
        el8 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.EditText").instance(2)')
        el8.click()
        time.sleep(1)
        el8.clear()
        el8.clear()
        el8.clear()
        el8.send_keys(proxy_ip)
        time.sleep(1)
        el9 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.EditText").instance(3)')
        el9.click()
        el9.clear()
        el9.clear()
        el9.clear()
        el9.send_keys(proxy_port)
        time.sleep(1)
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(1000, 1701)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        time.sleep(1)

        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
        while (
            not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5 protocol error (E7)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Protocol error (E3)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Connection unexpectedly closed (E2)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Timeout connecting to the specified port. (E1)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Timeout connecting to the specified port.")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Connection to the specified port was refused.")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Authentication required")
        ):
            time.sleep(1)
            print(3, st, c, gc, mc, mac, asc, sep="\t")
        if not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required"):
            el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.Button").instance(2)')
            el10.click()
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP"):
                time.sleep(1)
                print(4, st, c, gc, mc, mac, asc, sep="\t")
            el11 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP")
            el11.click()
        time.sleep(1)
        st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
        while (
            not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5 protocol error (E7)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Protocol error (E3)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Connection unexpectedly closed (E2)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Timeout connecting to the specified port. (E1)")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Timeout connecting to the specified port.")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Connection to the specified port was refused.")
            and not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Authentication required")
        ):
            time.sleep(1)
            print(5, st, c, gc, mc, mac, asc, sep="\t")
        if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required"):
            found_good_proxy = True
        else:
            with open(f"{TG_USERNAME}/bad_proxies.txt", "a") as file:
                file.write(proxy_data + "\n")

            with open(f"{TG_USERNAME}/proxylist.txt", "w") as file:
                proxies_data = proxies_data[1:]
                file.write("\n".join(proxies_data) + "\n")

        if found_good_proxy:
            el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.Button").instance(1)')
            el12.click()
            el13 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Start")
            el13.click()

            st = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            tc = 0
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Stop"):
                time.sleep(1)
                print(6, st, c, gc, mc, mac, asc, sep="\t")
                tc += 1
                if tc % 50 == 0:
                    found_good_proxy = False
                    while driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Start"):
                        time.sleep(1)
                        print(7, st, c, gc, mc, mac, asc, sep="\t")
                        el14 = driver.find_element(
                            by=AppiumBy.XPATH,
                            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
                            + "android.view.View/android.view.View/android.view.View[1]/"
                            + "android.view.View/android.view.View[1]/android.widget.Button[2]",
                        )
                        el14.click()
                    with open(f"{TG_USERNAME}/bad_proxies.txt", "a") as file:
                        file.write(proxy_data + "\n")
                    with open(f"{TG_USERNAME}/proxylist.txt", "w") as file:
                        proxies_data = proxies_data[1:]
                        file.write("\n".join(proxies_data) + "\n")
                    break
                if tc % 10 == 0:
                    el15 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Start")
                    if el15:
                        el15[0].click()

            if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Stop"):
                print(f"NEW PROXY ADDRESS: {proxy_data}", time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, mac, asc, sep="\t")

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(542, 1851)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(1)

    return proxy_data


if __name__ == "__main__":
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

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    c = 0
    gc = 0
    change_proxy(driver, c, gc)
