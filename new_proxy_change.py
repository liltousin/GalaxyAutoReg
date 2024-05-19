import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def change_proxy(driver: webdriver.Remote, c: int, gc: int, mc=0):
    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy"):
        time.sleep(1)
        print(0, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
    el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy")
    el1.click()
    while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available.") and not driver.find_elements(
        by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Default Profile")'
    ):
        time.sleep(1)
        print(1, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
    if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available."):
        el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Add proxy")
        el3.click()
    else:
        if not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Start"):
            el4 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Stop")
            el4.click()
        el5 = driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]",
        )
        el5.click()

    found_good_proxy = False
    while not found_good_proxy:
        with open("used_proxies.txt") as file:
            used_proxies = [i.rstrip() for i in file.readlines()]

        with open("bad_proxies.txt") as file:
            bad_proxies = [i.rstrip() for i in file.readlines()]

        with open("proxylist.txt") as file:
            proxies_data = [i.rstrip() for i in file.readlines() if i.rstrip() not in used_proxies and i.rstrip() not in bad_proxies]

        if proxies_data:
            proxy_data = proxies_data[0]
            proxy_ip, proxy_port = proxy_data.split(":")
        else:
            print("NEED NEW PROXIES!!!", time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
            time.sleep(1)
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
        for _ in range(16):
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1000, 1531)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
        el8.send_keys(proxy_ip)
        time.sleep(1)
        el9 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.EditText").instance(3)')
        el9.click()
        for _ in range(5):
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1000, 1531)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
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
            print(2, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
        if not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required"):
            el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.Button").instance(2)')
            el10.click()
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP"):
                time.sleep(1)
                print(3, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
            el11 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP")
            el11.click()
        time.sleep(1)
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
            print(4, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
        if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required"):
            found_good_proxy = True
        else:
            with open("bad_proxies.txt", "a") as file:
                file.write(proxy_data + "\n")

            with open("proxylist.txt", "w") as file:
                proxies_data = proxies_data[1:]
                file.write("\n".join(proxies_data) + "\n")

        if found_good_proxy:
            el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.Button").instance(1)')
            el12.click()
            el13 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Start")
            el13.click()

            # добавить код который если че стопает все driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="An unknown error occured.")
            while not driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Stop"):
                time.sleep(1)
                print(5, time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")
            if driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Stop"):
                print(f"NEW PROXY ADDRESS: {proxy_data}", time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime()), c, gc, mc, sep="\t")

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(542, 1857)
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

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    c = 0
    gc = 0
    change_proxy(driver, c, gc)
