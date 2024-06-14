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
    return webdriver.Remote(f"http://127.0.0.1:{args.appium_port}", options=options)  # 4723


def main(driver: webdriver.Remote, tg_username: str, process_id: int):
    # надо добавть проверку и создание всех необходимых файлов и директорий для корректной работы
    sssm = SearchSpamStateMachine(driver, tg_username, process_id)
    sssm.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--udid", required=True, help="UDID of the device.")
    parser.add_argument("--appium-port", type=int, required=True, help="Appium server port.")
    parser.add_argument("--tg-username", required=True, help="Telegram username where traffic will go.")
    parser.add_argument("--process-id", type=int, required=True, help="Process sequence number (starting from 1).")
    args = parser.parse_args()
    main(get_driver(args), args.tg_username, args.process_id)
