import os
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

from utils import choose_city_by_statistics, get_new_unused_proxies


class State:
    def __init__(
        self,
        state_function: Callable,
        delay: float,
        transitions: list[tuple[tuple[list[Callable[[], bool]], list[Callable[[], bool]]], Callable[[], None]]],
    ):
        self.state_function = state_function
        self.name = state_function.__name__
        self.transitions = transitions  # (функция, функция нового состояния)
        self.counter = 0
        self.delay = delay

    def run(self):
        new_state, transition_condition = None, None
        while not (new_state and transition_condition):
            self.counter += 1
            try:
                self.state_function()
            except Exception:
                pass
            time.sleep(self.delay)
            new_state, transition_condition = self.check_conditions()
        iteration_counter = self.counter
        self.counter = 0
        return new_state, transition_condition, iteration_counter

    def check_conditions(self):
        for t in self.transitions:
            result = None
            try:
                result = all(map(lambda x: x(), t[0][0])) and all(map(lambda x: not x(), t[0][1]))
            except Exception:
                pass
            if result:
                return t[1].__name__, " and not ".join([" and ".join([i.__name__ for i in t[0][0]])] + [i.__name__ for i in t[0][1]])
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
        self.states = [  # чем больше состояний надо пройти тем выше состояние
            State(
                self.initial_state,
                1,
                [
                    (([self.current_app_is_super_proxy], []), self.click_on_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu),
                    (([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_to_check_current_galaxy_menu),
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (([self.found_login_new_character], []), self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu),
                    (([self.found_galaxy_menulist], []), self.scroll_down_menulist_looking_for_exit_button_while_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.click_on_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu,
                1,
                [(([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_to_check_current_galaxy_menu)],
            ),
            State(
                self.click_on_galaxy_app_to_check_current_galaxy_menu,
                1,
                [
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (([self.found_login_new_character], []), self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.click_on_galaxy_image_button_while_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy_menulist], []), self.scroll_down_menulist_looking_for_exit_button_while_checking_current_galaxy_menu)],
            ),
            State(
                self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy, self.found_super_proxy], []), self.click_on_super_proxy_app)],
            ),
            State(
                self.scroll_down_menulist_looking_for_exit_button_while_checking_current_galaxy_menu,
                1,
                [(([self.found_exit_button], []), self.click_on_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu)],
            ),
            State(
                self.click_on_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                1,
                [(([self.found_login_new_character], []), self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu)],
            ),
            State(
                self.click_on_super_proxy_app,
                1,
                [
                    (([self.found_add_proxy_button], [self.found_no_proxies_available]), self.click_on_already_added_proxy_profile),
                    (([self.found_stop_button], []), self.click_on_stop_button),
                    (([self.found_no_proxies_available], []), self.click_on_add_proxy_button),
                    (([self.found_start_button], []), self.click_on_edit_proxy_profile_button),
                    (
                        ([self.found_protocol_edit_text], [self.found_unused_local_proxies, self.global_proxylist_has_been_updated]),
                        self.update_global_proxlist,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.global_proxylist_has_been_updated], [self.found_unused_local_proxies]),
                        self.replace_local_proxies_with_new_ones,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.found_unused_local_proxies], [self.found_socks5_in_protocol_edit_text]),
                        self.click_on_protocol_edit_text_to_select_socks5,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.found_unused_local_proxies, self.found_socks5_in_protocol_edit_text], []),
                        self.click_on_server_edit_text,
                    ),
                ],
            ),
            State(self.click_on_already_added_proxy_profile, 1, [(([self.found_start_button], []), self.click_on_edit_proxy_profile_button)]),
            State(self.click_on_stop_button, 1, [(([self.found_start_button], []), self.click_on_edit_proxy_profile_button)]),
            State(
                self.click_on_add_proxy_button,
                1,
                [
                    (
                        ([self.found_protocol_edit_text], [self.found_unused_local_proxies, self.global_proxylist_has_been_updated]),
                        self.update_global_proxlist,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.global_proxylist_has_been_updated], [self.found_unused_local_proxies]),
                        self.replace_local_proxies_with_new_ones,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.found_unused_local_proxies], [self.found_socks5_in_protocol_edit_text]),
                        self.click_on_protocol_edit_text_to_select_socks5,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.found_unused_local_proxies, self.found_socks5_in_protocol_edit_text], []),
                        self.click_on_server_edit_text,
                    ),
                ],
            ),
            State(
                self.click_on_edit_proxy_profile_button,
                1,
                [
                    (
                        ([self.found_protocol_edit_text], [self.found_unused_local_proxies, self.global_proxylist_has_been_updated]),
                        self.update_global_proxlist,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.global_proxylist_has_been_updated], [self.found_unused_local_proxies]),
                        self.replace_local_proxies_with_new_ones,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.found_unused_local_proxies], [self.found_socks5_in_protocol_edit_text]),
                        self.click_on_protocol_edit_text_to_select_socks5,
                    ),
                    (
                        ([self.found_protocol_edit_text, self.found_unused_local_proxies, self.found_socks5_in_protocol_edit_text], []),
                        self.click_on_server_edit_text,
                    ),
                ],
            ),
            State(self.update_global_proxlist, 1, [(([self.global_proxylist_has_been_updated], []), self.replace_local_proxies_with_new_ones)]),
            State(
                self.replace_local_proxies_with_new_ones,
                1,
                [
                    (
                        ([self.found_unused_local_proxies], [self.found_socks5_in_protocol_edit_text]),
                        self.click_on_protocol_edit_text_to_select_socks5,
                    ),
                    (([self.found_unused_local_proxies, self.found_socks5_in_protocol_edit_text], []), self.click_on_server_edit_text),
                ],
            ),
            State(self.click_on_protocol_edit_text_to_select_socks5, 1, [(([self.found_socks5_in_dropdown_list], []), self.click_on_socks5)]),
            State(self.click_on_server_edit_text, 1, [(([self.server_edit_text_is_focused], []), self.clear_server_edit_text)]),
            State(self.click_on_socks5, 1, [(([self.found_socks5_in_protocol_edit_text], []), self.click_on_server_edit_text)]),
            State(self.clear_server_edit_text, 1, [(([self.server_edit_text_is_empty], []), self.paste_proxy_address_into_server_edit_text)]),
            State(
                self.paste_proxy_address_into_server_edit_text,
                1,
                [(([self.found_proxy_address_in_server_edit_text], []), self.click_on_port_edit_text)],
            ),
            State(self.click_on_port_edit_text, 1, [(([self.port_edit_text_is_focused], []), self.clear_port_edit_text)]),
            State(self.clear_port_edit_text, 1, [(([self.port_edit_text_is_empty], []), self.paste_proxy_port_into_port_edit_text)]),
            State(
                self.paste_proxy_port_into_port_edit_text,
                1,
                [(([self.found_proxy_port_in_port_edit_text], []), self.move_local_proxy_from_proxylist_to_used_proxies)],
            ),
            State(
                self.move_local_proxy_from_proxylist_to_used_proxies,
                1,
                [(([self.found_proxy_in_used_proxies], [self.found_proxy_in_proxylist]), self.hide_keyboard_after_entering_proxy_fields)],
            ),
            State(
                self.hide_keyboard_after_entering_proxy_fields,
                1,
                [
                    (([self.found_proxy_connection_error], []), self.click_on_protocol_edit_text_to_select_http),
                    (([self.found_no_authentication_required], []), self.click_on_save_proxy_profile_button),
                ],
            ),
            State(self.click_on_protocol_edit_text_to_select_http, 1, [(([self.found_http_in_dropdown_list], []), self.click_on_http)]),
            State(self.click_on_http, 1, [(([self.found_http_in_protocol_edit_text], []), self.wait_for_proxy_connection_result)]),
            State(
                self.wait_for_proxy_connection_result,
                1,
                [
                    (
                        ([self.found_proxy_connection_error], [self.found_unused_local_proxies, self.global_proxylist_has_been_updated]),
                        self.update_global_proxlist,
                    ),
                    (
                        ([self.found_proxy_connection_error, self.global_proxylist_has_been_updated], [self.found_unused_local_proxies]),
                        self.replace_local_proxies_with_new_ones,
                    ),
                    (
                        ([self.found_proxy_connection_error, self.found_unused_local_proxies], [self.found_socks5_in_protocol_edit_text]),
                        self.click_on_protocol_edit_text_to_select_socks5,
                    ),
                    (([self.found_no_authentication_required], []), self.click_on_save_proxy_profile_button),
                ],
            ),
            State(self.click_on_save_proxy_profile_button, 1, [(([self.found_start_button], []), self.click_on_start_button)]),
            State(
                self.click_on_start_button,
                1,
                [
                    (([self.found_start_button, self.reached_20_iterations_timeout], []), self.click_on_edit_proxy_profile_button),
                    (([self.found_stop_button], []), self.click_on_home_button_to_exit_super_proxy_app_after_enabling_proxy_profile),
                ],
            ),
            State(
                self.click_on_home_button_to_exit_super_proxy_app_after_enabling_proxy_profile,
                1,
                [(([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_after_enabling_proxy_profile)],
            ),
            State(
                self.click_on_galaxy_app_after_enabling_proxy_profile,
                1,
                [(([self.found_login_new_character], []), self.click_on_login_new_character)],
            ),
            State(
                self.click_on_login_new_character,
                1,
                [
                    (([self.found_female_radio_button], []), self.click_on_female_radio_button),
                    (([self.reached_20_iterations_timeout], []), self.initial_state),
                ],
            ),
            State(
                self.click_on_female_radio_button,
                1,
                [(([self.female_radio_button_is_checked], []), self.click_next_button_in_choose_your_caracter_menu)],
            ),
            State(
                self.click_next_button_in_choose_your_caracter_menu,
                1,
                [(([self.found_nick_input_edit_text], []), self.click_on_nick_input_edit_text)],
            ),
            State(
                self.click_on_nick_input_edit_text, 1, [(([self.nick_input_edit_text_is_focused], []), self.paste_nickname_into_nick_input_edit_text)]
            ),
            State(
                self.paste_nickname_into_nick_input_edit_text,
                1,
                [(([self.found_nickname_in_nick_input_edit_text], []), self.hide_keyboard_after_entering_nickname)],
            ),
            State(self.hide_keyboard_after_entering_nickname, 1, [(([self.found_username_available], []), self.click_on_finish_button)]),
            State(self.click_on_finish_button, 1, [(([self.found_confirm_button_ok], []), self.click_on_confirm_button_ok)]),
            State(
                self.click_on_confirm_button_ok, 1, [(([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_before_entering_city)]
            ),
            # вот тут надо бы провер очку на login_new_character а еще надо бы ебнуть декоратор
            State(
                self.click_on_galaxy_image_button_before_entering_city,
                1,
                [
                    (([self.found_confirm_registration], []), self.scroll_down_menulist_looking_for_exit_button_while_checking_current_galaxy_menu),
                    (
                        ([self.found_friends_button], [self.found_browser_loader, self.found_confirm_registration]),
                        self.click_on_friends_button_button_before_entering_city,
                    ),
                ],
            ),
            State(
                self.click_on_friends_button_button_before_entering_city,
                1,
                [(([self.found_no_firends_yet, self.found_your_location], []), self.click_on_your_location)],
            ),
            State(self.click_on_your_location, 1, [(([self.found_city_input_edit_text], []), self.click_on_city_input_edit_text)]),
            State(self.click_on_city_input_edit_text, 1, [(([self.city_input_edit_text_is_focused], []), self.paste_city_into_city_input_edit_text)]),
            State(
                self.paste_city_into_city_input_edit_text, 1, [(([self.found_city_in_city_input_edit_text], []), self.wait_for_city_choice_result)]
            ),
            State(self.wait_for_city_choice_result, 1, []),
        ]

    def draw_SM_diagram(self):
        pass

    def start(self):
        self.current_state = self.states[0]
        while True:
            new_state_name, transition_condition, iteration_counter = self.current_state.run()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{current_time}\t{iteration_counter}\t{self.current_state} ---{transition_condition}--> {new_state_name}")
            self.current_state = self.states[self.states.index(new_state_name)]

    def initial_state(self):
        self.city = ""

    def current_app_is_super_proxy(self):
        return self.driver.execute_script("mobile: getCurrentPackage") == "com.scheler.superproxy"

    def found_galaxy(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"))

    def found_super_proxy(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy"))

    def found_galaxy_image_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]'))

    def found_login_new_character(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"))

    def click_on_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_to_check_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_galaxy_image_button_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def found_galaxy_menulist(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="ru.mobstudio.andgalaxy:id/menulist"]'
            )
        )

    # Это будет как декоратор
    # def found_dialog_confirm_cancel(self):
    #     return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel"))
    def scroll_down_menulist_looking_for_exit_button_while_checking_current_galaxy_menu(self):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(510, 1150)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(510, 150)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def found_exit_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")'))

    def click_on_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")').click()

    def click_on_super_proxy_app(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Super Proxy"]').click()

    def found_add_proxy_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Add proxy"]'))

    def found_no_proxies_available(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No proxies available."))

    def found_stop_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Stop"]'))

    def found_start_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Start"]'))

    def found_protocol_edit_text(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]'))

    def found_unused_local_proxies(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            return bool([i.rstrip() for i in file.readlines() if i.rstrip()])

    def global_proxylist_has_been_updated(self):
        number_of_processes = len(os.listdir("processes"))
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            used_proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        with open("proxylist.txt") as file:
            proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        split_precise_proxies = [
            proxies[round(i * len(proxies) / number_of_processes) : round((i + 1) * len(proxies) / number_of_processes)]
            for i in range(number_of_processes)
        ]
        process_proxies = split_precise_proxies[self.process_id - 1] + split_precise_proxies[self.process_id % number_of_processes]
        return used_proxies != process_proxies

    def found_socks5_in_protocol_edit_text(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').get_attribute("text") == "SOCKS5"

    def click_on_already_added_proxy_profile(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.view.View[1]",
        ).click()

    def click_on_stop_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Stop"]').click()

    def click_on_add_proxy_button(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Add proxy").click()

    def click_on_edit_proxy_profile_button(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]",
        ).click()

    def update_global_proxlist(self):
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            used_proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        # можно будет переписать так чтоб убирались повторения
        with open("used_proxies.txt", "a") as file:
            file.write("\n".join(used_proxies) + "\n")
        proxies = get_new_unused_proxies()
        with open("proxylist.txt", "w") as file:
            file.write("\n".join(proxies) + "\n")

    def replace_local_proxies_with_new_ones(self):
        number_of_processes = len(os.listdir("processes"))
        with open("proxylist.txt") as file:
            proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        split_precise_proxies = [
            proxies[round(i * len(proxies) / number_of_processes) : round((i + 1) * len(proxies) / number_of_processes)]
            for i in range(number_of_processes)
        ]
        process_proxies = split_precise_proxies[self.process_id - 1] + split_precise_proxies[self.process_id % number_of_processes]
        with open(f"processes/{self.process_id}/proxylist.txt", "w") as file:
            file.write("\n".join(process_proxies) + "\n")
        with open(f"processes/{self.process_id}/used_proxies.txt", "w") as file:
            file.write("")

    def click_on_protocol_edit_text_to_select_socks5(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').click()

    def found_socks5_in_dropdown_list(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5"))

    def click_on_socks5(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5").click()

    def click_on_server_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').click()

    def server_edit_text_is_focused(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("focused") == "true"

    def clear_server_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').clear()

    def server_edit_text_is_empty(self):
        return not self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text")

    def paste_proxy_address_into_server_edit_text(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxy_address = file.readlines()[0].rstrip().split(":")[0]
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').send_keys(proxy_address)

    def found_proxy_address_in_server_edit_text(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxy_address = file.readlines()[0].rstrip().split(":")[0]
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text") == proxy_address

    def click_on_port_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').click()

    def port_edit_text_is_focused(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("focused") == "true"

    def clear_port_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').clear()

    def port_edit_text_is_empty(self):
        return not self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text")

    def paste_proxy_port_into_port_edit_text(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxy_port = file.readlines()[0].rstrip().split(":")[1]
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').send_keys(proxy_port)

    def found_proxy_port_in_port_edit_text(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxy_port = file.readlines()[0].rstrip().split(":")[1]
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text") == proxy_port

    def move_local_proxy_from_proxylist_to_used_proxies(self):
        # можно так же записывать в атрибут экземпляра current_proxy
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        proxy = proxies[0]
        with open(f"processes/{self.process_id}/used_proxies.txt", "a") as file:
            file.write(proxy)
        with open(f"processes/{self.process_id}/proxylist.txt", "w") as file:
            file.write("".join(proxies[1:]))

    def found_proxy_in_used_proxies(self):
        proxy_address = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text")
        proxy_port = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text")
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            used_proxies = file.readlines()
        proxy = proxy_address + ":" + proxy_port + "\n"
        return proxy in used_proxies

    def found_proxy_in_proxylist(self):
        proxy_address = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text")
        proxy_port = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text")
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        proxy = proxy_address + ":" + proxy_port + "\n"
        return proxy in proxies

    def hide_keyboard_after_entering_proxy_fields(self):
        self.driver.execute_script("mobile: hideKeyboard")

    def found_proxy_connection_error(self):
        return bool(
            self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5 protocol error (E7)")
            or self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Protocol error (E3)")
            or self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Connection unexpectedly closed (E2)")
            or self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Timeout connecting to the specified port. (E1)")
            or self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Timeout connecting to the specified port.")
            or self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Connection to the specified port was refused.")
            or self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Authentication required")
        )

    def found_no_authentication_required(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="No authentication required"))

    def click_on_protocol_edit_text_to_select_http(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').click()

    def found_http_in_dropdown_list(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP"))

    def click_on_http(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP").click()

    def found_http_in_protocol_edit_text(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').get_attribute("text") == "HTTP"

    def wait_for_proxy_connection_result(self):
        pass

    def click_on_save_proxy_profile_button(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]",
        ).click()

    def click_on_start_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Start"]').click()

    def reached_20_iterations_timeout(self):
        return self.current_state.counter > 20

    def click_on_home_button_to_exit_super_proxy_app_after_enabling_proxy_profile(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_after_enabling_proxy_profile(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_login_new_character(sefl):
        sefl.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character").click()

    def found_female_radio_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]'))

    def click_on_female_radio_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]').click()

    def female_radio_button_is_checked(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]').get_attribute("checked") == "true"

    def click_next_button_in_choose_your_caracter_menu(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")').click()

    def found_nick_input_edit_text(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="nick_input-text"]'))

    def click_on_nick_input_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="nick_input-text"]').click()

    def nick_input_edit_text_is_focused(self):
        return (
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="nick_input-text"]').get_attribute("focused")
            == "true"
        )

    def paste_nickname_into_nick_input_edit_text(self):
        # можно так же записывать в атрибут экземляра current_nick
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="nick_input-text"]').send_keys(
            "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        )

    def found_nickname_in_nick_input_edit_text(self):
        return bool(
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="nick_input-text"]').get_attribute("text")
        )

    def hide_keyboard_after_entering_nickname(self):
        self.driver.execute_script("mobile: hideKeyboard")

    def found_username_available(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Username available"]'))

    def click_on_finish_button(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")').click()

    def found_confirm_button_ok(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok"))

    def click_on_confirm_button_ok(self):
        self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok").click()

    def click_on_galaxy_image_button_before_entering_city(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def found_confirm_registration(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Confirm registration")'))

    def found_friends_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")'))

    def found_browser_loader(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/browser_loader"))

    def click_on_friends_button_button_before_entering_city(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Friends")').click()

    def found_no_firends_yet(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="No friends yet"]'))

    def found_your_location(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="your location"]'))

    def click_on_your_location(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="your location"]').click()

    def found_city_input_edit_text(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]'))

    def click_on_city_input_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]').click()

    def city_input_edit_text_is_focused(self):
        return bool(
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]').get_attribute("focused")
            == "true"
        )

    def paste_city_into_city_input_edit_text(self):
        self.city = choose_city_by_statistics()
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]').send_keys(self.city)

    def found_city_in_city_input_edit_text(self):
        return bool(
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]').get_attribute("text")
        )

    def wait_for_city_choice_result(self):
        pass
