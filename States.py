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


class State:
    def __init__(
        self,
        state_function: Callable,
        delay: float,
        transitions: list[tuple[Callable[..., bool], int | str | tuple[str] | None, str]],
        driver: webdriver.Remote,
    ):
        self.state_function = state_function
        self.name = state_function.__name__
        self.transitions = transitions  # (функция, таймер или путь к элементу или список путей к элементам или None, имя нового состояния
        self.counter = 0
        self.delay = delay
        self.result = None
        self.driver = driver

    def run(self):
        while not (new_state := self.check_conditions()):
            self.counter += 1
            self.result = self.state_function(self.driver)
        self.counter = 0
        return new_state

    def check_conditions(self):
        for t in self.transitions:
            if type(t[1]) is list:
                result = t[0](self.driver, *t[1])
            elif type(t[1]) is str:
                result = t[0](self.driver, t[1])
            elif type(t[1]) is int:
                result = t[0](self.counter, t[1])
            else:
                result = t[0](self.result)
            if result:
                return t[2]

    def __str__(self) -> str:
        return self.name

    def __eq__(self, value: object) -> bool:
        return str(value) == str(self)
