import argparse

from appium import webdriver
from appium.options.common.base import AppiumOptions

from search_spam_SM import SearchSpamStateMachine


def get_driver(args: argparse.Namespace):
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
    return webdriver.Remote(f"http://127.0.0.1:{args.appium_port}", options=options)  # 4723 и как выяснилось можно все на один и тот же аппиум


def main(driver: webdriver.Remote, tg_username: str, text_template: str, process_id: int, user_counter_limit: int):
    # надо добавть проверку и создание всех необходимых файлов и директорий для корректной работы
    sssm = SearchSpamStateMachine(driver, tg_username, text_template, process_id, user_counter_limit)
    sssm.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--udid", required=True, help="UDID of the device.")
    parser.add_argument("--appium-port", type=int, default=4723, help="Appium server port.")
    parser.add_argument("--tg-username", required=True, help="Telegram username where traffic will go.")
    parser.add_argument("--text-template", required=True, help="Text template to be sent (the place to insert tg_username is marked as {}).")
    parser.add_argument("--process-id", type=int, required=True, help="Process sequence number (starting from 1).")
    parser.add_argument("--user-counter-limit", type=int, default=25, help="Limit the number of messages written from 1 account.")
    args = parser.parse_args()
    main(get_driver(args), args.tg_username, args.text_template, args.process_id, args.user_counter_limit)
