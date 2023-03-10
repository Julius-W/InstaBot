import os
import random
import time
import re
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


def waiting_time():
    return float(round(random.random() * 3 + 2, 2))


class InstaBot:
    """A Class for an InstaBot that can execute some simple tasks."""
    def __init__(self, username, password) -> None:
        """Initializes an instance of an InstaBot."""
        self.path: str = os.path.abspath(__file__)
        self.driver_name: str = os.path.join(os.path.dirname(self.path), "geckodriver")
        self.driver: webdriver = None
        self.__initialize_driver()
        self.url: str = "https://www.instagram.com/"
        self.username: str = username
        self.password: str = password

    def __initialize_driver(self) -> None:
        """Initializes a driver instance for selenium."""
        if not os.path.exists(self.driver_name):
            raise Exception("file does not exist.")
        ser = Service("geckodriver")
        op = webdriver.FirefoxOptions()
        # op.add_argument("--headless")
        self.driver = webdriver.Firefox(service=ser, options=op)

    def login(self) -> None:
        """Logs the bot into Instagram."""
        self.driver.get(self.url)
        time.sleep(waiting_time())
        self.driver.find_element(By.CLASS_NAME, "_a9--._a9_1").click()

        # login attempt
        time.sleep(waiting_time())
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys(self.username)
        time.sleep(waiting_time())
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(self.password)
        time.sleep(waiting_time())

        # click button
        button = self.driver.find_element(By.CLASS_NAME, "_acan._acap._acas._aj1-")
        button.click()
        time.sleep(waiting_time() + 5)

        try:
            self.driver.find_element(By.CLASS_NAME, "_acan._acao._acas._aj1-").click()
            time.sleep(waiting_time())
            self.driver.find_element(By.CLASS_NAME, "_a9--._a9_1").click()
            # last index is 0 or one - depending on the output btn
        except Exception as e:
            print(e)
        time.sleep(waiting_time())

    def search(self, query) -> None:
        """Searches the given username and opens the profile."""
        # getting search button
        search_button = self.driver.find_elements(By.CLASS_NAME, "x1i10hfl")[2]
        search_button.click()

        # start searching account
        time.sleep(waiting_time())
        search_input = self.driver.find_element(By.CLASS_NAME, "_aauy")
        search_input.send_keys(query)
        time.sleep(waiting_time())

        # get first element in search results
        class_string2 = "x9f619 x78zum5 xdt5ytf x6ikm8r x1odjw0f x4uap5 x18d9i69 xkhd6sd x5yr21d xocp1fn xh8yej3"\
            .replace(" ", ".")
        search_results = self.driver.find_element(By.CLASS_NAME, class_string2)
        children = search_results.find_elements(By.TAG_NAME, "div")
        time.sleep(waiting_time())
        element = children[0]
        element.click()
        time.sleep(waiting_time())

    def follow(self) -> None:
        """Follows the current profile."""
        if not re.match(f"{self.url}.+/".replace(".", "\\."), self.driver.current_url):
            raise Exception("You are currently not on the correct page.")
        # get follower button and follow account
        follow_btn = self.driver.find_element(By.CLASS_NAME, "_acan _acap _acas _aj1-".replace(" ", "."))
        follow_btn.click()
        time.sleep(waiting_time())

    def like_picture(self) -> None:
        """Like the first picture of the current profile."""
        if not re.match(f"{self.url}.+/".replace(".", "\\."), self.driver.current_url):
            raise Exception("You are currently not on the correct page.")
        y = 1000
        self.driver.execute_script(f"window.scrollTo(0, {y})")
        content = self.driver.find_element(By.TAG_NAME, "article").find_element(By.TAG_NAME, "div").find_element(
            By.TAG_NAME, "div")
        row = content.find_elements(By.TAG_NAME, "div")
        picture = row[0].find_element(By.TAG_NAME, "a")
        # range 0-2, technically same logic for content with unknown range
        picture.click()
        like_button = self.driver.find_elements(By.CLASS_NAME, "_abl-")[3]
        like_button.click()
        time.sleep(waiting_time())

    def get_followers(self, amount=50) -> List[str]:
        """Gets up to 50 followers from the current profile and returns usernames as a string list."""
        if amount < 1 or amount > 50:
            raise Exception("Minimum followers is one and maximum is 50.")
        print(self.driver.current_url)
        if not re.match(f"{self.url}.+/", self.driver.current_url):
            raise Exception("You are currently not on the correct page.")
        self.driver.get(f"{self.url}{self.current_username()}/followers/")
        time.sleep(2 * waiting_time())
        followers = self.driver.find_elements(By.CLASS_NAME, "_ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm")
        followers_list = list()
        for follower in followers:
            followers_list.append(follower.text)
        time.sleep(waiting_time())
        if amount - 1 <= len(followers_list):
            followers_list = followers_list[:amount - 1]
        return followers_list

    def current_username(self) -> str:
        """Gets the current username from the active url and returns the username as a string."""
        url = self.driver.current_url
        sub_url = url[url.find("com/") + 4:]
        return sub_url[:sub_url.find("/")]

    def send_dm(self, message: str) -> None:
        """Sends a dm to the user of the current profile."""
        wrapper = self.driver.find_element(By.CLASS_NAME, "_ab8w._ab94._ab99._ab9f._ab9m._ab9o._abb0._ab9s._abcm")
        dm_button = wrapper.find_element(By.TAG_NAME, "div")
        dm_button.click()
        time.sleep(2 * waiting_time())
        text_field = self.driver.find_element(By.CLASS_NAME, "_ab8w._ab94._ab99._ab9f._ab9m._ab9o._abbh._abcm")
        input_field = text_field.find_element(By.TAG_NAME, "textarea")
        input_field.send_keys(message)
        send_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acao._acas._aj1-")
        send_btn.click()
        print(f"Sent direct message to {self.current_username()} with this content:\n{message}")

    def close(self) -> None:
        """Closes current session"""
        self.driver.close()
