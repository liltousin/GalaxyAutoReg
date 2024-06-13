import random
import string
import time
from typing import Callable

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class State:
    def __init__(
        self,
        state_function: Callable,
        delay: float,
        transitions: list[tuple[Callable[[], bool], Callable[[], None]]],
    ):
        self.state_function = state_function
        self.name = state_function.__name__
        self.transitions = transitions  # (функция, функция нового состояния)
        self.counter = 0
        self.delay = delay

    def run(self):
        new_state, transition_condition = self.check_conditions()
        while not (new_state and transition_condition):
            self.counter += 1
            try:
                self.state_function()
            except Exception as e:
                print(e)
            time.sleep(self.delay)
            new_state, transition_condition = self.check_conditions()
        self.counter = 0
        return new_state, transition_condition

    def check_conditions(self):
        for t in self.transitions:
            try:
                result = t[0]()
            except Exception as e:
                print(e)
            if result:
                return t[1].__name__, t[0].__name__
        return None, None

    def __str__(self) -> str:
        return self.name

    def __eq__(self, value: object) -> bool:
        return str(value) == str(self)


class SearchSpamStateMachine:
    def __init__(self, driver: webdriver.Remote, tg_username: str, process_id: int):
        self.driver = driver
        self.tg_username = tg_username
        self.process_id = process_id
        self.current_state = None
        self.states = [
            State(
                self.initial_state,
                1,
                [
                    (self.current_app_is_super_proxy, self.click_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu),
                    (self.found_galaxy_and_super_proxy, self.click_on_galaxy_app_to_check_current_galaxy_menu),
                    (
                        self.found_galaxy_image_button,
                        self.click_on_galaxy_image_button_to_display_menulist_to_log_out_of_account_while_checking_current_galaxy_menu,
                    ),
                    (self.found_login_new_character, self.сlick_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu),
                    (
                        self.found_galaxy_menulist,
                        self.scroll_down_menulist_looking_for_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                    ),
                ],
            ),
            State(
                self.click_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu,
                1,
                [(self.found_galaxy_and_super_proxy, self.click_on_galaxy_app_to_check_current_galaxy_menu)],
            ),
            State(
                self.click_on_galaxy_app_to_check_current_galaxy_menu,
                1,
                [
                    (
                        self.found_galaxy_image_button,
                        self.click_on_galaxy_image_button_to_display_menulist_to_log_out_of_account_while_checking_current_galaxy_menu,
                    ),
                    (self.found_login_new_character, self.сlick_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.click_on_galaxy_image_button_to_display_menulist_to_log_out_of_account_while_checking_current_galaxy_menu,
                1,
                [
                    (
                        self.found_galaxy_menulist,
                        self.scroll_down_menulist_looking_for_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                    )
                ],
            ),
            State(
                self.сlick_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu,
                1,
                [(self.found_galaxy_and_super_proxy, self.сlick_on_super_proxy_app)],
            ),
            State(
                self.scroll_down_menulist_looking_for_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                1,
                [(self.found_exit_button, self.сlick_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu)],
            ),
            State(
                self.сlick_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                1,
                [(self.found_login_new_character, self.сlick_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu)],
            ),
            State(
                self.сlick_on_super_proxy_app,
                1,
                [
                    (self.found_add_proxy_button_but_not_no_proxies_available, self.click_on_already_added_proxy_profile),
                    (self.found_stop_button, self.click_on_stop_button),
                    (self.found_no_proxies_available, self.сlick_on_add_proxy_button),
                    (self.found_start_button, self.сlick_on_edit_proxy_profile_button),
                    (self.found_default_profile_edit_text,),
                ],
            ),
            State(self.click_on_already_added_proxy_profile, 1, [(self.found_start_button, self.сlick_on_edit_proxy_profile_button)]),
            State(self.click_on_stop_button, 1, [(self.found_start_button, self.сlick_on_edit_proxy_profile_button)]),
            State(self.сlick_on_add_proxy_button, 1, [(self.found_default_profile_edit_text,)]),
            State(self.сlick_on_edit_proxy_profile_button, 1, [(self.found_default_profile_edit_text,)]),
            State(1, []),
        ]

    def draw_SM_diagram(self):
        pass

    def start(self):
        self.current_state = self.states[0]
        while True:
            new_state_name, transition_condition = self.current_state.run()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S MSK", time.localtime())
            print(f"{current_time}\t{self.current_state} ---{transition_condition}--> {new_state_name}")
            self.current_state = self.states[self.states.index(new_state_name)]

    def initial_state(self):
        pass

    def current_app_is_super_proxy(self):
        return self.driver.execute_script("mobile: getCurrentPackage") == "com.scheler.superproxy"

    def found_galaxy_and_super_proxy(self):
        return bool(
            self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy")
            and self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy")
        )

    def found_galaxy_image_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]'))

    def found_login_new_character(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"))

    def click_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_to_check_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_galaxy_image_button_to_display_menulist_to_log_out_of_account_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def сlick_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def found_galaxy_menulist(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="ru.mobstudio.andgalaxy:id/menulist"]'
            )
        )

    def scroll_down_menulist_looking_for_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu(self):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(510, 1150)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(510, 150)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def found_exit_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'))

    def сlick_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")').click()

    def сlick_on_super_proxy_app(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Super Proxy"]').click()

    def found_add_proxy_button_but_not_no_proxies_available(self):
        return bool(
            self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Add proxy"]')
            and not self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available.")
        )

    def found_no_proxies_available(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available."))

    def found_stop_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Stop"]'))

    def found_start_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Start"]'))

    def found_default_profile_edit_text(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@text="Default Profile"]'))

    def click_on_already_added_proxy_profile(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.view.View[1]",
        ).click()

    def click_on_stop_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Stop"]').click()

    def сlick_on_add_proxy_button(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Add proxy").click()

    def сlick_on_edit_proxy_profile_button(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]",
        ).click()

    def update_global_proxylist_if_necessary(self):
        pass
    
    
    def found_good_unused_proxies(self):
        pass