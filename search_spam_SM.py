import os
import time
from functools import wraps
from typing import Callable

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from utils import (
    choose_city_by_statistics,
    generate_nickname,
    generate_text,
    get_new_unused_proxies,
)


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
    def __init__(self, driver: webdriver.Remote, tg_username: str, text_template: str, process_id: int):
        self.driver = driver
        self.tg_username = tg_username
        self.text_template = text_template
        self.process_id = process_id
        self.current_state = None
        self.states = [  # чем больше состояний надо пройти тем выше состояние. Все условия переходов состояний записываюся, даже если они избыточны
            State(
                self.initial_state,
                1,
                [
                    (([self.current_app_is_super_proxy], []), self.press_home_button_before_checking_current_galaxy_menu),
                    (([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_to_check_current_galaxy_menu),
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (
                        ([self.found_galaxy_menulist], [self.found_exit_nav_item]),
                        self.scroll_down_menulist_looking_for_exit_nav_item_while_checking_current_galaxy_menu,
                    ),
                    (([self.found_galaxy_menulist, self.found_exit_nav_item], []), self.click_on_exit_nav_item_while_checking_current_galaxy_menu),
                    # (([self.current_app_is_galaxy])) #  кликаем назад
                    # (([self.found_browser_loader]))
                    (([self.found_login_new_character], []), self.press_home_button_after_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.press_home_button_before_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_to_check_current_galaxy_menu)],
            ),
            State(
                self.click_on_galaxy_app_to_check_current_galaxy_menu,
                1,
                [
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (([self.found_login_new_character], []), self.press_home_button_after_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.click_on_galaxy_image_button_while_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy_menulist], []), self.scroll_down_menulist_looking_for_exit_nav_item_while_checking_current_galaxy_menu)],
            ),
            State(
                self.scroll_down_menulist_looking_for_exit_nav_item_while_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy_menulist, self.found_exit_nav_item], []), self.click_on_exit_nav_item_while_checking_current_galaxy_menu)],
            ),
            State(
                self.click_on_exit_nav_item_while_checking_current_galaxy_menu,
                1,
                [(([self.found_login_new_character], []), self.press_home_button_after_checking_current_galaxy_menu)],
            ),
            State(
                self.press_home_button_after_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy, self.found_super_proxy], []), self.click_on_super_proxy_app)],
            ),
            State(
                self.click_on_super_proxy_app,
                1,
                [
                    (([self.found_add_proxy_button], [self.found_no_proxies_available]), self.click_on_already_added_proxy_profile),
                    (([self.found_stop_button], []), self.click_on_stop_button),
                    (([self.found_add_proxy_button, self.found_no_proxies_available], []), self.click_on_add_proxy_button),
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
            State(  # надо фиксить если случайно полетит ui и изза этого гг (пока не критично т.к и так работает норм)
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
                [(([self.found_proxy_in_used_proxies], [self.found_proxy_in_proxylist]), self.wait_for_proxy_connection_result_via_socks5)],
            ),
            State(
                self.wait_for_proxy_connection_result_via_socks5,
                1,
                [
                    (([self.found_proxy_connection_error], []), self.click_on_protocol_edit_text_to_select_http),
                    (([self.found_no_authentication_required], []), self.click_on_save_proxy_profile_button),
                ],
            ),
            State(self.click_on_protocol_edit_text_to_select_http, 1, [(([self.found_http_in_dropdown_list], []), self.click_on_http)]),
            State(self.click_on_http, 1, [(([self.found_http_in_protocol_edit_text], []), self.wait_for_proxy_connection_result_via_http)]),
            State(
                self.wait_for_proxy_connection_result_via_http,
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
                    (([self.found_start_button, self.reached_10_iterations_timeout], []), self.click_on_edit_proxy_profile_button),
                    (([self.found_stop_button], []), self.press_home_button_after_enabling_proxy_profile),
                ],
            ),
            # новое состояние нажать кнопку ок при старте прокси в первый раз
            State(
                self.press_home_button_after_enabling_proxy_profile,
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
                    (
                        ([self.reached_10_iterations_timeout], [self.found_female_radio_button, self.found_login_new_character]),
                        self.press_back_button_after_reaching_login_new_character_timeout,
                    ),
                    (([self.reached_10_iterations_timeout, self.found_login_new_character], []), self.initial_state),
                    (([self.found_female_radio_button, self.found_next_button], []), self.click_on_female_radio_button),
                ],
            ),
            State(
                self.press_back_button_after_reaching_login_new_character_timeout,
                1,
                [
                    (([self.found_login_new_character], []), self.initial_state),
                    (([self.found_galaxy, self.found_super_proxy], []), self.initial_state),
                ],
            ),
            State(
                self.click_on_female_radio_button,
                1,
                # добавить нажатие кнопки назад если появилась эта хуевая загрузка поставить таймаут просто и кнопка назад хотя возможно и не надо
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
                [(([self.found_nickname_in_nick_input_edit_text], []), self.press_enter_button_after_entering_nickname)],
            ),
            State(self.press_enter_button_after_entering_nickname, 1, [(([self.found_finish_button], []), self.wait_for_nickname_check_result)]),
            State(self.wait_for_nickname_check_result, 1, [(([self.found_username_available], []), self.click_on_finish_button)]),
            State(self.click_on_finish_button, 1, [(([self.found_confirm_button_ok], []), self.click_on_confirm_button_ok)]),
            State(
                self.click_on_confirm_button_ok, 1, [(([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_before_entering_city)]
            ),
            # TODO: вот тут надо провер очку на login_new_character
            State(
                self.click_on_galaxy_image_button_before_entering_city,
                1,
                [
                    (([self.found_galaxy_menulist, self.found_confirm_registration_nav_item], []), self.initial_state),  # TODO: перед этим лог
                    (
                        (
                            [self.found_galaxy_menulist, self.found_friends_nav_item],
                            [self.found_browser_loader, self.found_confirm_registration_nav_item],
                        ),
                        self.click_on_friends_nav_item,
                    ),
                ],
            ),
            State(
                self.click_on_friends_nav_item,
                1,
                [
                    (([self.found_no_firends_yet, self.found_your_location], []), self.click_on_your_location),
                    (
                        ([self.found_no_firends_yet, self.found_my_location, self.found_galaxy_image_button], [self.found_your_location]),
                        self.click_on_galaxy_image_button_before_entering_city,
                    ),
                ],
            ),
            State(self.click_on_your_location, 1, [(([self.found_city_input_edit_text], []), self.click_on_city_input_edit_text)]),
            State(self.click_on_city_input_edit_text, 1, [(([self.city_input_edit_text_is_focused], []), self.paste_city_into_city_input_edit_text)]),
            State(
                self.paste_city_into_city_input_edit_text,
                1,
                [(([self.found_city_in_city_input_edit_text], []), self.press_enter_button_after_entering_city)],
            ),
            State(self.press_enter_button_after_entering_city, 1, [(([self.found_first_ru_image_button], []), self.click_on_first_ru_image_button)]),
            State(
                self.click_on_first_ru_image_button, 1, [(([self.found_no_firends_yet], []), self.click_on_galaxy_image_button_after_entering_city)]
            ),
            State(
                self.click_on_galaxy_image_button_after_entering_city,
                1,
                [
                    (([self.found_galaxy_menulist], [self.found_search_nav_item]), self.scroll_down_menulist_looking_for_search_nav_item),
                    (([self.found_galaxy_menulist, self.found_search_nav_item], []), self.click_on_search_nav_item),
                ],
            ),
            State(
                self.scroll_down_menulist_looking_for_search_nav_item,
                1,
                [(([self.found_galaxy_menulist, self.found_search_nav_item], []), self.click_on_search_nav_item)],
            ),
            State(self.click_on_search_nav_item, 1, [(([self.found_search_people_button], []), self.click_on_search_people_button)]),
            State(
                self.click_on_search_people_button,
                1,
                [
                    (([self.found_users], [self.found_new_user]), self.scroll_down_looking_for_new_user),
                    (([self.found_users, self.found_new_user], []), self.click_on_new_user),
                ],
            ),
            State(self.scroll_down_looking_for_new_user, 1, [(([self.found_users, self.found_new_user], []), self.click_on_new_user)]),
            State(self.click_on_new_user, 1, [(([self.found_message_button], []), self.click_on_message_button)]),
            State(
                self.click_on_message_button,
                1,
                [
                    (([self.found_send_message_button], []), self.click_on_message_edit_text),
                    (([self.found_bad_user_text], []), self.add_user_to_bad_users),
                ],
            ),
            State(self.click_on_message_edit_text, 1, [(([self.message_edit_text_is_focused], []), self.paste_message_into_edit_text)]),
            State(self.add_user_to_bad_users, 1, [(([self.found_user_in_bad_users], []), self.click_on_galaxy_image_button_after_sending_message)]),
            State(self.paste_message_into_edit_text, 1, [(([self.found_message_in_edit_text], []), self.click_on_send_message_button)]),
            State(
                self.click_on_send_message_button,
                1,
                [
                    (([self.found_send_message_button, self.found_galaxy_image_button, self.found_online], []), self.add_user_to_online_spammed),
                    (([self.found_send_message_button, self.found_galaxy_image_button], [self.found_online]), self.add_user_to_offline_spammed),
                ],
            ),
            State(
                self.add_user_to_online_spammed,
                1,
                [(([self.found_user_in_online_spammed], []), self.click_on_galaxy_image_button_after_sending_message)],
            ),
            State(
                self.add_user_to_offline_spammed,
                1,
                [(([self.found_user_in_offline_spammed], []), self.click_on_galaxy_image_button_after_sending_message)],
            ),
            State(
                self.click_on_galaxy_image_button_after_sending_message,
                1,
                [
                    (
                        ([self.found_galaxy_menulist, self.user_counter_is_under_25], [self.found_search_nav_item]),
                        self.scroll_down_menulist_looking_for_search_nav_item,
                    ),
                    (([self.found_galaxy_menulist, self.found_search_nav_item, self.user_counter_is_under_25], []), self.click_on_search_nav_item),
                    (
                        ([self.found_galaxy_menulist], [self.user_counter_is_under_25, self.found_exit_nav_item]),
                        self.scroll_down_menulist_looking_for_exit_nav_item_after_city_spamming_stops,
                    ),
                    (
                        ([self.found_galaxy_menulist, self.found_exit_nav_item], [self.user_counter_is_under_25]),
                        self.click_on_exit_nav_item_after_city_spamming_stops,
                    ),
                ],
            ),
            State(
                self.scroll_down_menulist_looking_for_exit_nav_item_after_city_spamming_stops,
                1,
                [(([self.found_galaxy_menulist, self.found_exit_nav_item], [self.click_on_exit_nav_item_after_city_spamming_stops]))],
            ),
            State(
                self.click_on_exit_nav_item_after_city_spamming_stops, 1, []
            ),  # TODO: запись в статистику и как раз при записе character_counter += 1
        ]

    def draw_SM_diagram(self):
        pass

    @staticmethod
    def try_to_click_on_dialog_confirm_cancel(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel").click()
            except Exception:
                pass
            return method(self, *args, **kwargs)

        return wrapper

    # пока что нахуй не нужен и вообще в ряд ли понадобится но пусть будет тут
    # @staticmethod
    # def run_only_once(method):
    #     @wraps(method)
    #     def wrapper(self, *args, **kwargs):
    #         if self.current_state.counter > 1:
    #             return
    #         return method(self, *args, **kwargs)

    #     return wrapper

    def start(self):
        self.current_state = self.states[0]
        while True:
            new_state_name, transition_condition, iteration_counter = self.current_state.run()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{current_time}\t{iteration_counter}\t{self.current_state} ---{transition_condition}--> {new_state_name}")
            self.current_state = self.states[self.states.index(new_state_name)]

    @try_to_click_on_dialog_confirm_cancel.__func__
    def initial_state(self):
        self.character_counter = 0
        self.current_proxy = ""

    def current_app_is_super_proxy(self):
        return self.driver.execute_script("mobile: getCurrentPackage") == "com.scheler.superproxy"

    def found_galaxy(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy"))

    def found_super_proxy(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy"))

    def found_galaxy_image_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]'))

    def found_galaxy_menulist(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="ru.mobstudio.andgalaxy:id/menulist"]'
            )
        )

    def found_browser_loader(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/browser_loader"))

    def found_login_new_character(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"))

    def press_home_button_before_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_to_check_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_galaxy_image_button_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    @try_to_click_on_dialog_confirm_cancel.__func__
    def scroll_down_menulist_looking_for_exit_nav_item_while_checking_current_galaxy_menu(self):
        self.driver.find_elements(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/menulist").scrollable(true))'
            + '.scrollIntoView(new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/nav_item_text").text("Exit"))',
        )

    def press_home_button_after_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def found_exit_nav_item(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Exit"]'
            )
        )

    def click_on_exit_nav_item_while_checking_current_galaxy_menu(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Exit"]'
        ).click()

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
        # можно будет переписать так чтоб убирались повторения (не забывая про replace_local_proxies_with_new_ones)
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
        # короче вообще это хуйня но пока что лучше ничего нет
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            local_used_proxies = [i.rstrip() for i in file.readlines() if i.rstrip()]
        with open("used_proxies.txt") as file:
            used_proxies = file.readlines()
        if "\n".join(local_used_proxies) not in "\n".join(used_proxies):
            with open("used_proxies.txt", "a") as file:
                file.write("\n".join(local_used_proxies) + "\n")
        # хуйня окончена
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
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        self.current_proxy = proxies[0]
        with open(f"processes/{self.process_id}/used_proxies.txt", "a") as file:
            file.write(self.current_proxy)
        with open(f"processes/{self.process_id}/proxylist.txt", "w") as file:
            file.write("".join(proxies[1:]))

    def found_proxy_in_used_proxies(self):
        with open(f"processes/{self.process_id}/used_proxies.txt") as file:
            used_proxies = file.readlines()
        return self.current_proxy in used_proxies

    def found_proxy_in_proxylist(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        return self.current_proxy in proxies

    def wait_for_proxy_connection_result_via_socks5(self):
        pass

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

    def wait_for_proxy_connection_result_via_http(self):
        pass

    def click_on_save_proxy_profile_button(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]",
        ).click()

    def click_on_start_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Start"]').click()

    def reached_10_iterations_timeout(self):
        return self.current_state.counter > 10

    def press_home_button_after_enabling_proxy_profile(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def click_on_galaxy_app_after_enabling_proxy_profile(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    def click_on_login_new_character(self):
        self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character").click()
        self.city = ""
        self.user_counter = 0
        self.online_message_sent_counter = 0

    def found_female_radio_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]'))

    def found_next_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")'))

    def press_back_button_after_reaching_login_new_character_timeout(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 4})

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
            generate_nickname(self.tg_username)
        )

    def found_nickname_in_nick_input_edit_text(self):
        return bool(
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="nick_input-text"]').get_attribute("text")
        )

    def press_enter_button_after_entering_nickname(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 66})

    def found_finish_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")'))

    def wait_for_nickname_check_result(self):
        pass

    def found_username_available(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@text="Username available"]'))  # android 11

    def click_on_finish_button(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")').click()

    def found_confirm_button_ok(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok"))

    @try_to_click_on_dialog_confirm_cancel.__func__
    def click_on_confirm_button_ok(self):
        self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok").click()

    @try_to_click_on_dialog_confirm_cancel.__func__
    def click_on_galaxy_image_button_before_entering_city(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def found_confirm_registration_nav_item(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH,
                value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Confirm registration"]',
            )
        )

    def found_friends_nav_item(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Friends"]'
            )
        )

    def click_on_friends_nav_item(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Friends"]'
        ).click()

    def found_no_firends_yet(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@text="No friends yet"]'))

    def found_my_location(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@text="My Location"]'))

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

    def press_enter_button_after_entering_city(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 66})

    def found_first_ru_image_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='(//android.widget.Image[@text="RU"])[1]'))

    def click_on_first_ru_image_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Image[@text="RU"])[1]').click()

    def click_on_galaxy_image_button_after_entering_city(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def scroll_down_menulist_looking_for_search_nav_item(self):
        self.driver.find_elements(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/menulist").scrollable(true))'
            + '.scrollIntoView(new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/nav_item_text").text("Search"))',
        )

    def found_search_nav_item(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Search"]'
            )
        )

    @try_to_click_on_dialog_confirm_cancel.__func__
    def click_on_search_nav_item(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Search"]'
        ).click()

    def found_search_people_button(self):
        return bool(
            self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]')
        )

    def click_on_search_people_button(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]'
        ).click()

    def found_users(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH,
                value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View/android.widget.TextView[@text!=""]'
                + '|//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View[@text!=""]',
            )
        )

    def found_new_user(self):
        for el in self.driver.find_elements(
            by=AppiumBy.XPATH,
            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View/android.widget.TextView[@text!=""]'
            + '|//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View[@text!=""]',
        ):
            self.user = el.get_attribute("text")
            # сделать 3 отдельных файла онлайн, плохие и оффлайн пользоватлеи
            with open(f"processes/{self.process_id}/online_spammed.txt") as file:
                online_spammed = file.readlines()
            with open(f"processes/{self.process_id}/offline_spammed.txt") as file:
                offline_spammed = file.readlines()
            with open("bad_users.txt") as file:
                bad_users = file.readlines()
            if self.user + "\n" not in online_spammed and self.user + "\n" not in offline_spammed and self.user + "\n" not in bad_users:
                return True
        return False

    def scroll_down_looking_for_new_user(self):
        self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiScrollable(new UiSelector().scrollable(true)).scrollForward()")

    def click_on_new_user(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().text("{self.user}")').click()

    def found_message_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="MESSAGE"]'))

    def click_on_message_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="MESSAGE"]').click()

    def found_send_message_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.view.View'))

    def found_bad_user_text(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH,
                value='//android.view.View[@text="This user receives private messages only from Friends. You can send a request to private message"]',
            )
        )

    def click_on_message_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').click()

    def add_user_to_bad_users(self):
        self.user_counter += 1
        with open("bad_users.txt", "a") as file:
            file.write(self.user + "\n")

    def message_edit_text_is_focused(self):
        return bool(
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').get_attribute("focused")
            == "true"
        )

    def found_user_in_bad_users(self):
        with open("bad_users.txt") as file:
            bad_users = file.readlines()
        return self.user + "\n" in bad_users

    def paste_message_into_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').send_keys(
            generate_text(self.tg_username, self.text_template)
        )

    def found_message_in_edit_text(self):
        return bool(self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').get_attribute("text"))

    def click_on_send_message_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.view.View').click()

    def found_online(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Online"]'))

    def add_user_to_online_spammed(self):
        self.user_counter += 1
        self.online_message_sent_counter += 1
        with open(f"processes/{self.process_id}/online_spammed.txt", "a") as file:
            file.write(self.user + "\n")

    def found_user_in_online_spammed(self):
        with open(f"processes/{self.process_id}/online_spammed.txt") as file:
            online_spammed = file.readlines()
        return self.user + "\n" in online_spammed

    def add_user_to_offline_spammed(self):
        self.user_counter += 1
        with open(f"processes/{self.process_id}/offline_spammed.txt", "a") as file:
            file.write(self.user + "\n")

    def found_user_in_offline_spammed(self):
        with open(f"processes/{self.process_id}/offline_spammed.txt") as file:
            offline_spammed = file.readlines()
        return self.user + "\n" in offline_spammed

    def click_on_galaxy_image_button_after_sending_message(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def user_counter_is_under_25(self):
        return self.user_counter < 25

    def scroll_down_menulist_looking_for_exit_nav_item_after_city_spamming_stops(self):
        self.driver.find_elements(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/menulist").scrollable(true))'
            + '.scrollIntoView(new UiSelector().resourceId("ru.mobstudio.andgalaxy:id/nav_item_text").text("Exit"))',
        )

    def click_on_exit_nav_item_after_city_spamming_stops(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Exit"]'
        ).click()
