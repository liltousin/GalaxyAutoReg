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

from get_proxylist_by_api import get_new_unused_proxies


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
        iteration_counter = self.counter
        self.counter = 0
        return new_state, transition_condition, iteration_counter

    def check_conditions(self):
        for t in self.transitions:
            result = None
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
                    (self.current_app_is_super_proxy, self.click_on_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu),
                    (self.found_galaxy_and_super_proxy, self.click_on_galaxy_app_to_check_current_galaxy_menu),
                    (
                        self.found_galaxy_image_button,
                        self.click_on_galaxy_image_button_to_display_menulist_to_log_out_of_account_while_checking_current_galaxy_menu,
                    ),
                    (self.found_login_new_character, self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu),
                    (
                        self.found_galaxy_menulist,
                        self.scroll_down_menulist_looking_for_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                    ),
                ],
            ),
            State(
                self.click_on_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu,
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
                    (self.found_login_new_character, self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu),
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
                self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu,
                1,
                [(self.found_galaxy_and_super_proxy, self.click_on_super_proxy_app)],
            ),
            State(
                self.scroll_down_menulist_looking_for_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                1,
                [(self.found_exit_button, self.click_on_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu)],
            ),
            State(
                self.click_on_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu,
                1,
                [(self.found_login_new_character, self.click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu)],
            ),
            State(
                self.click_on_super_proxy_app,
                1,
                [
                    (self.found_add_proxy_button_but_not_no_proxies_available, self.click_on_already_added_proxy_profile),
                    (self.found_stop_button, self.click_on_stop_button),
                    (self.found_no_proxies_available, self.click_on_add_proxy_button),
                    (self.found_start_button, self.click_on_edit_proxy_profile_button),
                    (self.found_protocol_edit_text, self.update_global_proxlist_if_necessary_and_replace_local_proxies_with_new_ones),
                ],
            ),
            State(self.click_on_already_added_proxy_profile, 1, [(self.found_start_button, self.click_on_edit_proxy_profile_button)]),
            State(self.click_on_stop_button, 1, [(self.found_start_button, self.click_on_edit_proxy_profile_button)]),
            State(
                self.click_on_add_proxy_button,
                1,
                [(self.found_protocol_edit_text, self.update_global_proxlist_if_necessary_and_replace_local_proxies_with_new_ones)],
            ),
            State(
                self.click_on_edit_proxy_profile_button,
                1,
                [(self.found_protocol_edit_text, self.update_global_proxlist_if_necessary_and_replace_local_proxies_with_new_ones)],
            ),
            State(
                self.update_global_proxlist_if_necessary_and_replace_local_proxies_with_new_ones,
                0,
                [(self.found_unused_local_proxies, self.click_on_protocol_edit_text_to_select_socks5)],
            ),
            State(self.click_on_protocol_edit_text_to_select_socks5, 0, [(self.found_socks5_in_dropdown_list, self.click_on_socks5)]),
            State(self.click_on_socks5, 0, [(self.found_socks5_in_protocol_edit_text, self.click_on_server_edit_text)]),
            State(
                self.click_on_server_edit_text,
                0,
                [(self.server_edit_text_is_focused, self.clear_server_edit_text)],
            ),
            State(
                self.clear_server_edit_text,
                0,
                [(self.server_edit_text_is_empty, self.paste_proxy_ip_address_into_server_edit_text)],
            ),
            State(
                self.paste_proxy_ip_address_into_server_edit_text,
                0,
                [(self.found_proxy_ip_address_in_server_edit_text, self.click_on_port_edit_text)],
            ),
            State(
                self.click_on_port_edit_text,
                0,
                [(self.port_edit_text_is_focused, self.clear_port_edit_text)],
            ),
            State(self.clear_port_edit_text, 0, [(self.port_edit_text_is_empty, self.paste_proxy_port_into_port_edit_text)]),
            State(
                self.paste_proxy_port_into_port_edit_text,
                0,
                [(self.found_proxy_port_in_port_edit_text, self.move_local_proxy_from_proxylist_to_used_proxies)],
            ),
            State(
                self.move_local_proxy_from_proxylist_to_used_proxies,
                0,
                [(self.found_proxy_in_used_proxies_and_not_found_in_proxylist, self.hide_keyboard_after_entering_proxy_fields)],
            ),
            State(
                self.hide_keyboard_after_entering_proxy_fields,
                0,
                [
                    (self.found_proxy_connection_error, self.click_on_protocol_edit_text_to_select_http),
                    (self.found_no_authentication_required, self.click_on_save_proxy_profile_button),
                ],
            ),
            State(self.click_on_protocol_edit_text_to_select_http, 0, [(self.found_http_in_dropdown_list, self.click_on_http)]),
            State(self.click_on_http, 0, [(self.found_http_in_protocol_edit_text, self.wait_for_proxy_connection_result)]),
            State(
                self.wait_for_proxy_connection_result,
                0,
                [
                    (self.found_proxy_connection_error, self.update_global_proxlist_if_necessary_and_replace_local_proxies_with_new_ones),
                    (self.found_no_authentication_required, self.click_on_save_proxy_profile_button),
                ],
            ),
            State(self.click_on_save_proxy_profile_button, 0, [(self.found_start_button, self.click_on_start_button)]),
            State(
                self.click_on_start_button,
                1,
                [(self.found_stop_button, self.click_on_home_button_to_exit_superproxy_app_after_enabling_proxy_profile), ()],
            ),
            State(
                self.click_on_home_button_to_exit_superproxy_app_after_enabling_proxy_profile,
                1,
                [(self.found_galaxy_and_super_proxy, self.click_on_galaxy_app_after_enabling_proxy_profile)],
            ),
            State(
                self.click_on_galaxy_app_after_enabling_proxy_profile,
                1,
                [
                    (self.found_login_new_character, self.click_on_login_new_character),
                ],
            ),
            State(self.click_on_login_new_character, 1, [()])
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

    def click_on_home_button_to_exit_superproxy_app_to_check_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_to_check_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_galaxy_image_button_to_display_menulist_to_log_out_of_account_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def click_on_home_button_to_exit_galaxy_app_after_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def found_galaxy_menulist(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="ru.mobstudio.andgalaxy:id/menulist"]'
            )
        )

    # def found_dialog_confirm_cancel(self):
    #     return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel"))
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

    def click_on_exit_button_to_log_out_of_account_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Exit")').click()

    def click_on_super_proxy_app(self):
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

    def found_protocol_edit_text(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]'))

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

    def update_global_proxlist_if_necessary_and_replace_local_proxies_with_new_ones(self):
        number_of_processes = len(os.listdir("processes"))
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            used_proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        with open("used_proxies.txt", "a") as file:
            file.write("\n".join(used_proxies) + "\n")
        with open("proxylist.txt") as file:
            proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        split_precise_proxies = [
            proxies[round(i * len(proxies) / number_of_processes) : round((i + 1) * len(proxies) / number_of_processes)]
            for i in range(number_of_processes)
        ]
        process_proxies = split_precise_proxies[self.process_id - 1] + split_precise_proxies[self.process_id % number_of_processes]
        if used_proxies == process_proxies:
            proxies = get_new_unused_proxies()
            with open("proxylist.txt", "w") as file:
                file.write("\n".join(proxies) + "\n")
            split_precise_proxies = [
                proxies[round(i * len(proxies) / number_of_processes) : round((i + 1) * len(proxies) / number_of_processes)]
                for i in range(number_of_processes)
            ]
            process_proxies = split_precise_proxies[self.process_id - 1] + split_precise_proxies[self.process_id % number_of_processes]
        with open(f"processes/{self.process_id}/proxylist.txt", "w") as file:
            file.write("\n".join(process_proxies) + "\n")
        with open(f"processes/{self.process_id}/used_proxies.txt", "w") as file:
            file.write("")

    def found_unused_local_proxies(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            return bool([i.rstrip() for i in file.readlines() if i.rstrip()])

    def click_on_protocol_edit_text_to_select_socks5(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').click()

    def found_socks5_in_dropdown_list(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5"))

    def click_on_socks5(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5").click()

    def found_socks5_in_protocol_edit_text(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').get_attribute("text") == "SOCKS5"

    def click_on_server_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').click()

    def server_edit_text_is_focused(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("focused") == "true"

    def clear_server_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').clear()

    def server_edit_text_is_empty(self):
        return not self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text")

    def paste_proxy_ip_address_into_server_edit_text(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxy_adress = file.readlines()[0].split(":")[0]
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').send_keys(proxy_adress)

    def found_proxy_ip_address_in_server_edit_text(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxy_adress = file.readlines()[0].split(":")[0]
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text") == proxy_adress

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
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        proxy = proxies[0]
        with open(f"processes/{self.process_id}/used_proxies.txt", "a") as file:
            file.write(proxy)
        with open(f"processes/{self.process_id}/proxylist.txt", "w") as file:
            file.write("".join(proxies[1:]))

    def found_proxy_in_used_proxies_and_not_found_in_proxylist(self):
        proxy_adress = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text")
        proxy_port = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text")
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            used_proxies = file.readlines()
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        proxy = proxy_adress + ":" + proxy_port + "\n"
        return proxy in used_proxies and proxy not in proxies

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

    def click_on_home_button_to_exit_superproxy_app_after_enabling_proxy_profile(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_after_enabling_proxy_profile(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_login_new_character(sefl):
        sefl.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character").click()
