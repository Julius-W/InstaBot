import os
import random
import time
import re
import locale
from typing import List, Tuple, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


def waiting_time() -> float:
    return float(round(random.random() * 3 + 2, 2))


def warning(message: str) -> None:
    err = "\033[93m"
    end_err = "\033[0m"
    print(f"{err}Warning: {message}{end_err}")


class InstaBot:
    """A Class for an InstaBot that can execute some simple tasks."""

    def __init__(self, username: str, password: str, headless: bool = False) -> None:
        """Initializes an instance of an InstaBot."""
        self.path: str = os.path.abspath(__file__)
        self.__session_data = dict()
        self.__decimal = locale.localeconv()["decimal_point"]
        self.__headless = headless
        self.__driver_name: str = os.path.join(os.path.dirname(self.path), "geckodriver")
        self.driver: Optional[webdriver] = None
        self.__initialize_driver()
        self.base_url: str = "https://www.instagram.com/"
        self.username: str = username
        self.__password: str = password
        if self.__headless:
            warning("Using the headless option makes it easier to be detected by Instagram.")

    def __initialize_driver(self) -> None:
        """Initializes a driver instance for selenium."""
        if not os.path.exists(self.__driver_name):
            raise FileNotFoundError("File does not exist.")
        service = Service("geckodriver")
        options = webdriver.FirefoxOptions()
        # I strongly suggest to not use the headless option (Instagram might detect a headless browser)
        if self.__headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=service, options=options)

    def login(self) -> None:
        """Logs the bot into Instagram."""
        self.driver.get(self.base_url)
        time.sleep(waiting_time())
        self.driver.find_element(By.CLASS_NAME, "_a9--._a9_1").click()

        # login attempt
        time.sleep(waiting_time())
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys(self.username)
        time.sleep(waiting_time())
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(self.__password)
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

    def on_profile(self):
        if not re.match(f"{self.base_url}.+/", self.driver.current_url):
            raise Exception("You are currently not on the correct page.")

    def search(self, query: str) -> None:
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
        class_string2 = "x9f619.x78zum5.xdt5ytf.x6ikm8r.x1odjw0f.x4uap5.x18d9i69.xkhd6sd.x5yr21d.xocp1fn.xh8yej3"
        search_results = self.driver.find_element(By.CLASS_NAME, class_string2)
        children = search_results.find_elements(By.TAG_NAME, "div")
        time.sleep(waiting_time())
        element = children[0]
        element.click()
        time.sleep(waiting_time())
        try:
            follower = self.get_follower_count()
            following = self.get_following_count()
            posts = self.get_posts_count()
            self.__session_data[self.get_current_username()] = (follower, following, posts)
        except ValueError:
            pass

    def follow(self) -> None:
        """Follows the current profile."""
        self.on_profile()
        # get follow button and follow account
        follow_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acap._acas._aj1-")
        if len(follow_btn) == 0:
            warning(f"You are already following this profile ({self.get_current_username()}).")
            return
        follow_btn[0].click()
        time.sleep(waiting_time())

    def follow(self) -> None:
        """Unfollows the current profile."""
        self.on_profile()
        # get unffollow button and unfollow account
        unfollow_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acap._acat._aj1-")
        if len(unfollow_btn) == 0:
            warning(f"You are not following this profile ({self.get_current_username()}).")
            return
        unfollow_btn[0].click()
        time.sleep(waiting_time())

    def like_picture(self) -> None:
        """Like the first picture of the current profile."""
        self.on_profile()
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

    def get_follower_count(self) -> int:
        """Gets the counter of the followers of the current profile as an integer."""
        self.on_profile()
        counters = self.driver.find_elements(By.CLASS_NAME, "_ac2a")
        title = counters[1].get_attribute("title")
        counter_string = title.replace(self.__decimal, "")
        if not counter_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {title}")
        return int(counter_string)

    def get_following_count(self) -> int:
        """Gets the counter of all followed accounts of the current profile as an integer."""
        self.on_profile()
        counters = self.driver.find_elements(By.CLASS_NAME, "_ac2a")
        content = counters[2].find_element(By.TAG_NAME, "span").text
        counter_string = content.replace(self.__decimal, "")
        if not counter_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {content}")
        return int(counter_string)

    def get_posts_count(self) -> int:
        """Gets the counter of the followers of the current profile as an integer."""
        self.on_profile()
        counters = self.driver.find_elements(By.CLASS_NAME, "_ac2a")
        content = counters[0].find_element(By.TAG_NAME, "span").text
        counter_string = content.replace(self.__decimal, "")
        if not counter_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {content}")
        return int(counter_string)

    def get_name(self) -> str:
        """Gets the name of the current profile (not ig-username)."""
        self.on_profile()
        full_bio = self.driver.find_element(By.CLASS_NAME, "_aa_c")
        name = full_bio.find_element(By.TAG_NAME, "span").text
        return name

    def get_bio(self) -> str:
        """Gets the bio of the current profile."""
        self.on_profile()
        full_bio = self.driver.find_element(By.CLASS_NAME, "_aa_c")
        bio = full_bio.find_element(By.TAG_NAME, "h1").text.replace("<br>", "\n")
        return bio

    def get_homepage(self) -> str:
        """Gets the url to the homepage of the current profile."""
        self.on_profile()
        full_bio = self.driver.find_element(By.CLASS_NAME, "_aa_c")
        url = full_bio.find_element(By.TAG_NAME, "div").text
        return url

    def get_profile_picture(self) -> str:
        """Gets the url to the profile picture of the current profile."""
        self.on_profile()
        frame = self.driver.find_element(By.CLASS_NAME, "_aarf")
        picture = frame.find_element(By.TAG_NAME, "img").get_attribute("src")
        return picture[:picture.find("?")]

    def get_data(self, username: str) -> Tuple[int, int, int]:
        """Returns a tuple with counters for (follower, following, posts)"""
        if username not in self.__session_data:
            raise Exception("User has not been searched yet.")
        return self.__session_data[username]

    def get_followers(self, amount: int = 50) -> List[str]:
        """Gets up to 50 followers from the current profile and returns usernames as a string list."""
        if amount < 1 or amount > 50:
            raise Exception("Minimum followers is one and maximum is 50.")
        print(self.driver.current_url)
        if not re.match(f"{self.base_url}.+/", self.driver.current_url):
            raise Exception("You are currently not on the correct page.")
        self.driver.get(f"{self.base_url}{self.get_current_username()}/followers/")
        time.sleep(2 * waiting_time())
        followers = self.driver.find_elements(By.CLASS_NAME, "_ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm")
        followers_list = list()
        for follower in followers:
            followers_list.append(follower.text)
        time.sleep(waiting_time())
        if amount - 1 <= len(followers_list):
            followers_list = followers_list[:amount - 1]
        return followers_list

    def get_current_username(self) -> str:
        """Gets the current username from the active url and returns the username as a string."""
        url = self.driver.current_url
        sub_url = url[url.find("com/") + 4:]
        return sub_url[:sub_url.find("/")]

    def send_dm(self, message: str) -> None:
        """Sends a dm to the user of the current profile."""
        typing_time = 0.1
        wrapper = self.driver.find_element(By.CLASS_NAME, "_ab8w._ab94._ab99._ab9f._ab9m._ab9o._abb0._ab9s._abcm")
        dm_button = wrapper.find_element(By.TAG_NAME, "div")
        dm_button.click()
        time.sleep(2 * waiting_time())
        text_field = self.driver.find_element(By.CLASS_NAME, "_ab8w._ab94._ab99._ab9f._ab9m._ab9o._abbh._abcm")
        input_field = text_field.find_element(By.TAG_NAME, "textarea")
        for word in message:
            if len(word) > 2:
                input_field.send_keys(word[:1])
                time.sleep(typing_time)
                input_field.send_keys(word[1:2])
                time.sleep(typing_time + random.random() / 3)
                input_field.send_keys(word[2:])
            else:
                input_field.send_keys(word)
            time.sleep(typing_time + random.random() / 3)
            input_field.send_keys(" ")
        send_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acao._acas._aj1-")
        send_btn.click()
        print(f"Sent direct message to {self.get_current_username()} with this content:\n{message}")

    def close(self) -> None:
        """Closes current session"""
        self.driver.close()
