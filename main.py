import argparse
import random
import string
import time
from typing import Callable

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from search_spam_SM import SearchSpamStateMachine
from text_generator import get_text


def get_driver_and_tg_username(args: argparse.Namespace):
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
    tg_username = args.tg_username
    return driver, tg_username


def main(driver: webdriver.Remote, tg_username: str):
    sssm = SearchSpamStateMachine(driver, tg_username)
    sssm.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--udid", required=True, help="UDID of the device.")
    parser.add_argument("--appium-port", type=int, required=True, help="Appium server port.")
    parser.add_argument("--tg-username", required=True, help="Telegram username where traffic will go.")
    main(*get_driver_and_tg_username(parser.parse_args()))
