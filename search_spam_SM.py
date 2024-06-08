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
        transitions: list[tuple[Callable[..., bool], str]],
    ):
        self.state_function = state_function
        self.name = state_function.__name__
        self.transitions = transitions  # (функция, имя нового состояния
        self.counter = 0
        self.delay = delay

    def run(self):
        new_state, transition_condition = self.check_conditions()
        while not new_state:
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
                return t[1], t[0].__name__
        return None, None

    def __str__(self) -> str:
        return self.name

    def __eq__(self, value: object) -> bool:
        return str(value) == str(self)


class SearchSpamStateMachine:
    def __init__(self, driver: webdriver.Remote, tg_username: str):
        self.driver = driver
        self.tg_username = tg_username
        with open(f"{self.tg_username}/already_spammed.txt") as file:
            self.already_spammed_counter = len(file.readlines())
        self.current_state = None
        self.states = [State(self.initial_state, 1, [(self.found_galaxy_and_super_proxy,)])]

    def draw_SM_diagram(self):
        pass

    def start(self):
        self.current_state = self.states[0]
        while True:
            new_state_name = self.current_state.run()
            print(f"")
            self.current_state = self.states[self.states.index(new_state_name)]

    def initial_state(self):
        pass

    def found_galaxy_and_super_proxy(self):
        return self.driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Galaxy") and self.driver.find_elements(
            by=AppiumBy.ACCESSIBILITY_ID, value="Super Proxy"
        )
