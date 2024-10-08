import os
import time
from functools import wraps
from typing import Callable

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from utils import (
    choose_city_by_statistic,
    generate_nickname,
    generate_text,
    get_new_unused_proxies,
    get_statistic_row,
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
        self.transitions = transitions
        self.counter = 0
        self.delay = delay

    def run(self):
        new_state, transition_condition = self.check_conditions()
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
    def __init__(self, driver: webdriver.Remote, tg_username: str, text_template: str, process_id: int, user_counter_limit: int):
        self.driver = driver
        self.tg_username = tg_username
        self.text_template = text_template
        self.process_id = process_id
        self.user_counter_limit = user_counter_limit
        self.current_state = None

        # делать состояния и переходы с учетом того что состояние может не выполнится ни разу и сразу перейти на другое

        self.states = [  # чем больше состояний надо пройти тем выше состояние. Все условия переходов состояний записываюся, даже если они избыточны
            State(
                self.initial_state,
                1,
                [
                    (
                        ([self.character_counter_is_zeroed, self.current_proxy_is_zeroed, self.user_counter_is_zeroed], []),
                        self.wait_for_ui_determination,
                    )
                ],
            ),
            State(
                self.wait_for_ui_determination,
                1,
                [
                    (([self.current_app_is_super_proxy], []), self.press_home_button_before_checking_current_galaxy_menu),
                    (
                        (
                            [self.current_app_is_galaxy, self.reached_10_iterations_timeout],
                            [self.found_login_new_character, self.found_galaxy_menulist, self.found_galaxy_image_button],
                        ),
                        self.press_back_button_before_checking_current_galaxy_menu,
                    ),
                    (([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_to_check_current_galaxy_menu),
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (
                        ([self.found_galaxy_menulist], [self.found_exit_nav_item]),
                        self.scroll_down_menulist_looking_for_exit_nav_item_while_checking_current_galaxy_menu,
                    ),
                    (([self.found_galaxy_menulist, self.found_exit_nav_item], []), self.click_on_exit_nav_item_while_checking_current_galaxy_menu),
                    (([self.found_login_new_character], []), self.press_home_button_after_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.press_home_button_before_checking_current_galaxy_menu,
                1,
                [(([self.found_galaxy, self.found_super_proxy], []), self.click_on_galaxy_app_to_check_current_galaxy_menu)],
            ),
            State(
                self.press_back_button_before_checking_current_galaxy_menu,
                1,
                [
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (
                        ([self.found_galaxy_menulist], [self.found_exit_nav_item]),
                        self.scroll_down_menulist_looking_for_exit_nav_item_while_checking_current_galaxy_menu,
                    ),
                    (([self.found_galaxy_menulist, self.found_exit_nav_item], []), self.click_on_exit_nav_item_while_checking_current_galaxy_menu),
                    (([self.found_login_new_character], []), self.press_home_button_after_checking_current_galaxy_menu),
                ],
            ),
            State(
                self.click_on_galaxy_app_to_check_current_galaxy_menu,
                1,
                [
                    (([self.found_galaxy_image_button], []), self.click_on_galaxy_image_button_while_checking_current_galaxy_menu),
                    (([self.found_login_new_character], []), self.press_home_button_after_checking_current_galaxy_menu),
                    (
                        (
                            [self.current_app_is_galaxy, self.reached_10_iterations_timeout],
                            [self.found_login_new_character, self.found_galaxy_image_button],
                        ),
                        self.press_back_button_before_checking_current_galaxy_menu,
                    ),
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
            State(  # надо фиксить если случайно полетит ui и изза этого гг (пока не критично т.к и так работает норм) (вроде пофиксил)
                self.replace_local_proxies_with_new_ones,
                1,
                [
                    (
                        ([self.found_unused_local_proxies, self.found_http_in_protocol_edit_text], [self.found_socks5_in_protocol_edit_text]),
                        self.click_on_protocol_edit_text_to_select_socks5,
                    ),
                    (
                        ([self.found_unused_local_proxies, self.found_socks5_in_protocol_edit_text], [self.found_http_in_protocol_edit_text]),
                        self.click_on_server_edit_text,
                    ),
                ],
            ),
            State(self.click_on_protocol_edit_text_to_select_socks5, 1, [(([self.found_socks5_in_dropdown_list], []), self.click_on_socks5)]),
            State(self.click_on_server_edit_text, 1, [(([self.server_edit_text_is_focused], []), self.clear_server_edit_text)]),
            State(self.click_on_socks5, 1, [(([self.found_socks5_in_protocol_edit_text], []), self.click_on_server_edit_text)]),
            State(self.clear_server_edit_text, 1, [(([self.server_edit_text_is_empty], []), self.set_new_current_proxy)]),
            State(self.set_new_current_proxy, 1, [(([self.new_current_proxy_is_set], []), self.paste_proxy_address_into_server_edit_text)]),
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
                        ([self.reached_login_new_character_timeout], [self.found_female_radio_button, self.found_login_new_character]),
                        self.press_back_button_after_reaching_login_new_character_timeout,
                    ),
                    (([self.reached_login_new_character_timeout, self.found_login_new_character], []), self.initial_state),
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
            # TODO: вот тут надо провер очку на login_new_character (но потом надо не забывать про статсистику (после ввода города))
            State(
                self.click_on_galaxy_image_button_before_entering_city,
                1,
                [
                    (([self.found_galaxy_menulist, self.found_confirm_registration_nav_item], []), self.add_current_proxy_to_conf_reg_proxies),
                    (
                        (
                            [self.found_galaxy_menulist, self.found_friends_nav_item],
                            [self.found_browser_loader, self.found_confirm_registration_nav_item],
                        ),
                        self.click_on_friends_nav_item,
                    ),
                ],
            ),
            State(self.add_current_proxy_to_conf_reg_proxies, 1, [(([self.found_current_proxy_in_conf_reg_proxies], []), self.initial_state)]),
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
            State(self.click_on_city_input_edit_text, 1, [(([self.city_input_edit_text_is_focused], []), self.choose_new_city)]),
            State(self.choose_new_city, 1, [(([self.new_city_is_chosen], []), self.paste_city_into_city_input_edit_text)]),
            State(
                self.paste_city_into_city_input_edit_text,
                1,
                [(([self.found_city_in_city_input_edit_text], []), self.press_enter_button_after_entering_city)],
            ),
            State(self.press_enter_button_after_entering_city, 1, [(([self.found_first_ru_image], []), self.click_on_first_ru_image)]),
            State(self.click_on_first_ru_image, 1, [(([self.found_no_firends_yet], []), self.click_on_galaxy_image_button_after_entering_city)]),
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
            State(
                self.click_on_search_nav_item, 1, [(([self.found_search_people_button], []), self.click_on_search_people_button)]
            ),  # начиная отсюда имеест смысл добавлять в статистику вместе с user_counter_greater_than_1
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
                    (([self.found_send_message_button, self.found_no_msg_image], []), self.click_on_message_edit_text),
                    (([self.found_bad_user_text, self.found_no_msg_image], []), self.add_user_to_bad_users),
                    # found_character_ban_text (на айпи похуй) TODO
                    # //android.view.View[@text="You have punishment and not allowed to private message anyone except your friends"]
                ],
            ),
            State(self.click_on_message_edit_text, 1, [(([self.message_edit_text_is_focused], []), self.paste_message_into_edit_text)]),
            State(self.add_user_to_bad_users, 1, [(([self.found_user_in_bad_users], []), self.click_on_galaxy_image_button_after_sending_message)]),
            State(self.paste_message_into_edit_text, 1, [(([self.found_message_in_edit_text], []), self.click_on_send_message_button)]),
            State(
                self.click_on_send_message_button,
                1,
                [
                    (
                        ([self.found_send_message_button, self.found_galaxy_image_button, self.found_online], [self.found_no_msg_image]),
                        self.add_user_to_online_spammed,
                    ),
                    (
                        ([self.found_send_message_button, self.found_galaxy_image_button], [self.found_online, self.found_no_msg_image]),
                        self.add_user_to_offline_spammed,
                    ),
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
                self.click_on_galaxy_image_button_after_sending_message,  # после этого не надо self.user_counter_greater_than_1
                1,
                [
                    (
                        ([self.found_galaxy_menulist, self.user_counter_limit_reached], [self.found_search_nav_item]),
                        self.scroll_down_menulist_looking_for_search_nav_item,
                    ),
                    (([self.found_galaxy_menulist, self.found_search_nav_item, self.user_counter_limit_reached], []), self.click_on_search_nav_item),
                    (
                        ([self.found_galaxy_menulist], [self.user_counter_limit_reached, self.found_exit_nav_item]),
                        self.scroll_down_menulist_looking_for_exit_nav_item_after_city_spamming_stops,
                    ),
                    (
                        ([self.found_galaxy_menulist, self.found_exit_nav_item], [self.user_counter_limit_reached]),
                        self.click_on_exit_nav_item_after_city_spamming_stops,
                    ),
                ],
            ),
            State(
                self.scroll_down_menulist_looking_for_exit_nav_item_after_city_spamming_stops,
                1,
                [(([self.found_galaxy_menulist, self.found_exit_nav_item], []), self.click_on_exit_nav_item_after_city_spamming_stops)],
            ),
            State(self.click_on_exit_nav_item_after_city_spamming_stops, 1, [(([self.found_login_new_character], []), self.add_data_to_statistics)]),
            State(
                self.add_data_to_statistics,
                1,
                [
                    (([self.found_data_in_statistics, self.character_counter_limit_reached], []), self.click_on_login_new_character),
                    (([self.found_data_in_statistics], [self.character_counter_limit_reached]), self.initial_state),
                ],
            ),
        ]
        for i in range(1, len(self.states)):
            self.states[i].transitions.append((([self.reached_100_iterations_timeout], [self.user_counter_greater_than_1]), self.initial_state))
            self.states[i].transitions.append(
                (([self.reached_100_iterations_timeout, self.user_counter_greater_than_1], []), self.add_data_to_statistics)
            )
        # TODO сделать при инициализации проверку всех файлов процесса и создание при необзодимости

    def draw_SM_diagram(self):
        pass

    @staticmethod
    def try_to_click_on_dialog_confirm_cancel(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/dialog_confirm_cancel").click()
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"{current_time}\t{self.try_to_click_on_dialog_confirm_cancel.__name__}")
            except Exception:
                return method(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def try_to_click_on_aerr_wait(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                self.driver.find_element(by=AppiumBy.ID, value="android:id/aerr_wait").click()
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"{current_time}\t{self.try_to_click_on_aerr_wait.__name__}")
            except Exception:
                return method(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def try_to_click_on_load_more(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                self.driver.find_element(
                    by=AppiumBy.XPATH, value='//android.view.View[@resource-id="people_near_loader" and @text="LOAD MORE"]'
                ).click()
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"{current_time}\t{self.try_to_click_on_load_more.__name__}")
            except Exception:
                return method(self, *args, **kwargs)

        return wrapper

    def start(self):
        self.current_state = self.states[0]
        while True:
            new_state_name, transition_condition, iteration_counter = self.current_state.run()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{current_time}\t{iteration_counter}\t{self.user_counter}\t{self.current_state} ---{transition_condition}--> {new_state_name}")
            # TODO: log to file
            self.current_state = self.states[self.states.index(new_state_name)]

    def initial_state(self):
        self.character_counter = 0
        self.current_proxy = ""
        self.user_counter = 0

    def character_counter_is_zeroed(self):
        return self.character_counter == 0

    def current_proxy_is_zeroed(self):
        return self.current_proxy == ""

    def user_counter_is_zeroed(self):
        return self.user_counter == 0

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def wait_for_ui_determination(self):
        pass

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

    def current_app_is_galaxy(self):
        return self.driver.execute_script("mobile: getCurrentPackage") == "ru.mobstudio.andgalaxy"

    def found_browser_loader(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/browser_loader"))

    def found_login_new_character(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character"))

    def press_home_button_before_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    def press_back_button_before_checking_current_galaxy_menu(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 4})

    def click_on_galaxy_app_to_check_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    @try_to_click_on_dialog_confirm_cancel
    def click_on_galaxy_image_button_while_checking_current_galaxy_menu(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def reached_100_iterations_timeout(self):
        return self.current_state.counter > 100

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
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

    @try_to_click_on_aerr_wait
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
        # TODO: сделать отдеьный параметр сколько наложений прокси будет
        # TODO: сделать отдельную функцию под получение прокей для процесса get_process_proxies
        return used_proxies != process_proxies

    def found_socks5_in_protocol_edit_text(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').get_attribute("text") == "SOCKS5"

    def click_on_already_added_proxy_profile(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/'
            + "android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.view.View[1]",
        ).click()

    @try_to_click_on_aerr_wait
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
        # Возможно стоит это убрать и оставить только split_precise_proxies[self.process_id - 1]
        # TODO: сделать отдеьный параметр сколько наложений прокси будет
        with open(f"processes/{self.process_id}/proxylist.txt", "w") as file:
            file.write("\n".join(process_proxies) + "\n")
        with open(f"processes/{self.process_id}/used_proxies.txt", "w") as file:
            file.write("")

    def click_on_protocol_edit_text_to_select_socks5(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').click()

    def found_socks5_in_dropdown_list(self):
        return bool(self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5"))

    @try_to_click_on_aerr_wait
    def click_on_socks5(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="SOCKS5").click()

    @try_to_click_on_aerr_wait
    def click_on_server_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').click()

    def server_edit_text_is_focused(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("focused") == "true"

    @try_to_click_on_aerr_wait
    def clear_server_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').clear()

    def server_edit_text_is_empty(self):
        return not self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text")

    def set_new_current_proxy(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        self.current_proxy = proxies[0]

    def new_current_proxy_is_set(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
        return self.current_proxy == proxies[0]

    @try_to_click_on_aerr_wait
    def paste_proxy_address_into_server_edit_text(self):
        proxy_address = self.current_proxy.rstrip().split(":")[0]
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').send_keys(proxy_address)

    def found_proxy_address_in_server_edit_text(self):
        proxy_address = self.current_proxy.rstrip().split(":")[0]
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Server"]').get_attribute("text") == proxy_address

    @try_to_click_on_aerr_wait
    def click_on_port_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').click()

    def port_edit_text_is_focused(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("focused") == "true"

    @try_to_click_on_aerr_wait
    def clear_port_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').clear()

    def port_edit_text_is_empty(self):
        return not self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text")

    @try_to_click_on_aerr_wait
    def paste_proxy_port_into_port_edit_text(self):
        proxy_port = self.current_proxy.rstrip().split(":")[1]
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').send_keys(proxy_port)

    def found_proxy_port_in_port_edit_text(self):
        proxy_port = self.current_proxy.rstrip().split(":")[1]
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Port"]').get_attribute("text") == proxy_port

    def move_local_proxy_from_proxylist_to_used_proxies(self):
        with open(f"processes/{self.process_id}/proxylist.txt") as file:
            proxies = file.readlines()
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

    @try_to_click_on_aerr_wait
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

    @try_to_click_on_aerr_wait  # не имеет смысла т.к сбивает dropdown menu и по хорошему вот это вот все надо как то в 1 действие сделать как то
    def click_on_http(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="HTTP").click()

    def found_http_in_protocol_edit_text(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@hint="Protocol"]').get_attribute("text") == "HTTP"

    @try_to_click_on_aerr_wait
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

    @try_to_click_on_aerr_wait
    def press_home_button_after_enabling_proxy_profile(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 3})

    @try_to_click_on_aerr_wait
    def click_on_galaxy_app_after_enabling_proxy_profile(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Galaxy"]').click()

    @try_to_click_on_aerr_wait
    def click_on_login_new_character(self):
        self.city = ""
        self.user_counter = 0
        self.online_message_counter = 0
        self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/login_new_character").click()

    def reached_login_new_character_timeout(self):
        return self.current_state.counter > 20  # TODO: отдельный аргумент

    def found_female_radio_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]'))

    def found_next_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("NEXT")'))

    @try_to_click_on_aerr_wait
    def press_back_button_after_reaching_login_new_character_timeout(self):
        self.driver.execute_script("mobile: pressKey", {"keycode": 4})

    @try_to_click_on_aerr_wait
    def click_on_female_radio_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]').click()

    def female_radio_button_is_checked(self):
        return self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Female"]').get_attribute("checked") == "true"

    @try_to_click_on_aerr_wait
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

    @try_to_click_on_aerr_wait
    def wait_for_nickname_check_result(self):
        pass

    def found_username_available(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@text="Username available"]'))  # android 11

    @try_to_click_on_aerr_wait
    def click_on_finish_button(self):
        self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("FINISH")').click()

    def found_confirm_button_ok(self):
        return bool(self.driver.find_elements(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok"))

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_confirm_button_ok(self):
        self.driver.find_element(by=AppiumBy.ID, value="ru.mobstudio.andgalaxy:id/confirm_button_ok").click()

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
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

    def add_current_proxy_to_conf_reg_proxies(self):
        with open("conf_reg_proxies.txt", "a") as file:
            file.write(self.current_proxy)

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_friends_nav_item(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Friends"]'
        ).click()

    def found_current_proxy_in_conf_reg_proxies(self):
        with open("conf_reg_proxies.txt") as file:
            conf_reg_proxies = file.readlines()
        return self.current_proxy in conf_reg_proxies

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

    def choose_new_city(self):
        self.city = choose_city_by_statistic()

    def new_city_is_chosen(self):
        return self.city != ""

    def paste_city_into_city_input_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]').send_keys(self.city)

    def found_city_in_city_input_edit_text(self):
        return (
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="city_input-text"]').get_attribute("text")
            == self.city  # TODO: переписать все нахер сделать вставку в 1 состояние, при этом добавить предварительную отчистку полей
            # TODO: проверить все get_attribute и нет ои там такого же говна которое может привести к потенциальным ошибкам
        )

    def press_enter_button_after_entering_city(self):  # может быть бага изза того что всему пиздец и он изза этого будет кликать на акки
        # (можно попробовать будет обьеденить все в 1)
        self.driver.execute_script("mobile: pressKey", {"keycode": 66})

    def found_first_ru_image(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='(//android.widget.Image[@text="RU"])[1]'))

    @try_to_click_on_aerr_wait
    def click_on_first_ru_image(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Image[@text="RU"])[1]').click()

    def click_on_galaxy_image_button_after_entering_city(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
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

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_search_nav_item(self):
        self.driver.find_element(
            by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.mobstudio.andgalaxy:id/nav_item_text" and @text="Search"]'
        ).click()

    def found_search_people_button(self):
        return bool(
            self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@resource-id="search"]/android.view.View[2]/android.view.View[2]')
        )

    def user_counter_greater_than_1(self):
        return self.user_counter > 1

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
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

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    @try_to_click_on_load_more
    def scroll_down_looking_for_new_user(self):
        self.driver.find_elements(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().className("android.webkit.WebView").scrollable(true)).scrollForward())',
        )

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_new_user(self):
        self.driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View/android.widget.TextView[@text='
            + f'"{self.user}"]|//android.view.View[@resource-id="people_near_content"]/android.view.View/android.view.View[@text="{self.user}"]',
        ).click()

    def found_message_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="MESSAGE"]'))

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_message_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="MESSAGE"]').click()

    def found_send_message_button(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.view.View'))

    def found_bad_user_text(self):
        return bool(
            self.driver.find_elements(
                by=AppiumBy.XPATH,
                value='//android.view.View[@text="This user receives private messages only from Friends. You can send a request to private message"]'
                + '|//android.view.View[@text="You can\'t private message this user because they have punishment"]',
            )
        )

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_message_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').click()

    def add_user_to_bad_users(self):
        with open("bad_users.txt", "a") as file:
            file.write(self.user + "\n")
        self.user_counter += 1

    def message_edit_text_is_focused(self):
        return bool(
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').get_attribute("focused")
            == "true"
        )

    def found_user_in_bad_users(self):
        with open("bad_users.txt") as file:
            bad_users = file.readlines()
        return self.user + "\n" in bad_users

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def paste_message_into_edit_text(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').send_keys(
            generate_text(self.tg_username, self.text_template)
        )

    def found_message_in_edit_text(self):
        return bool(self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]').get_attribute("text"))

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_send_message_button(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="text_input"]/../android.view.View').click()

    def found_online(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Online"]'))

    def found_no_msg_image(self):
        return bool(self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.Image[@text="no_msg@2x"]'))

    def add_user_to_online_spammed(self):
        with open(f"processes/{self.process_id}/online_spammed.txt", "a") as file:
            file.write(self.user + "\n")
        self.user_counter += 1
        self.online_message_counter += 1

    def found_user_in_online_spammed(self):
        with open(f"processes/{self.process_id}/online_spammed.txt") as file:
            online_spammed = file.readlines()
        return self.user + "\n" in online_spammed

    def add_user_to_offline_spammed(self):
        with open(f"processes/{self.process_id}/offline_spammed.txt", "a") as file:
            file.write(self.user + "\n")
        self.user_counter += 1

    def found_user_in_offline_spammed(self):
        with open(f"processes/{self.process_id}/offline_spammed.txt") as file:
            offline_spammed = file.readlines()
        return self.user + "\n" in offline_spammed

    @try_to_click_on_aerr_wait
    @try_to_click_on_dialog_confirm_cancel
    def click_on_galaxy_image_button_after_sending_message(self):
        self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Galaxy"]').click()

    def user_counter_limit_reached(self):
        return self.user_counter < self.user_counter_limit

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

    def add_data_to_statistics(self):
        self.current_date_and_time = time.localtime()
        with open("statistic.csv", "a") as file:
            file.write(get_statistic_row(self.city, self.online_message_counter, self.user_counter, self.current_date_and_time, self.process_id))
        self.character_counter += 1

    def found_data_in_statistics(self):
        data = get_statistic_row(self.city, self.online_message_counter, self.user_counter, self.current_date_and_time, self.process_id)
        with open("statistic.csv") as file:
            return data in file.readlines()

    def character_counter_limit_reached(self):
        return self.character_counter < 4  # TODO: сделтаь тоже как отдельный аргумент
