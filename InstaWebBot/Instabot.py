import os
import random
import time
import re
import locale
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


def waiting_time() -> float:
    return float(round(random.random() * 3 + 2, 2))


def warning(message: str) -> None:
    err: str = "\033[93m"
    end_err: str = "\033[0m"
    print(f"{err}Warning: {message}{end_err}")


def write(input_field, message: str) -> None:
    """Simulates user text input."""
    typing_time: float = 0.1
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


class InstaBot:
    """A Class for an InstaBot that can execute some simple tasks."""

    def __init__(self, username: str, password: str, **kwargs) -> None:
        """Initializes an instance of an InstaBot."""
        self.__headless: bool = kwargs.get("headless", False)
        selenium_driver: str = kwargs.get("driver", "geckodriver")
        self.__allow_output: bool = kwargs.get("output", False)
        self.success(f"Using {selenium_driver} as driver for selenium.")
        if not self.__headless:
            self.success(f"Running in normal mode (headless: {self.__headless}")
        self.path: str = os.path.abspath(__file__)
        self.__session_data: dict = dict()
        self.__decimal: str = locale.localeconv()["decimal_point"]
        self.__driver_name: str = os.path.join(os.getcwd(), selenium_driver)
        self.driver: Optional[webdriver] = None
        self.__initialize_driver()
        self.base_url: str = "https://www.instagram.com/"
        self.username: str = username
        self.__password: str = password

    def __initialize_driver(self) -> None:
        """Initializes a driver instance for selenium."""
        if not os.path.exists(self.__driver_name):
            raise FileNotFoundError("File does not exist.")
        service = Service("geckodriver")
        options = webdriver.FirefoxOptions()
        # I strongly suggest to not use the headless option (Instagram might detect a headless browser)
        if self.__headless:
            warning("Using the headless option makes it easier to be detected by Instagram.")
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=service, options=options)

    def success(self, message: str) -> None:
        if not self.__allow_output:
            return
        succ: str = "\033[92m"
        end_err: str = "\033[0m"
        print(f"{succ}Info: {message}{end_err}")

    def login(self) -> None:
        """Logs the bot into Instagram."""
        self.driver.get(self.base_url)
        time.sleep(waiting_time())
        # cookies
        try:
            self.driver.find_element(By.CLASS_NAME, "_a9--._a9_1").click()
        except Exception as e:
            warning(e.__str__())

        # login attempt
        time.sleep(waiting_time())
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys(self.username)
        time.sleep(waiting_time())
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(self.__password)
        time.sleep(waiting_time())

        # click button
        button = self.driver.find_element(By.CLASS_NAME, "_acan._acap._acas._aj1-")
        button.click()
        self.success(f"Logged in @{self.username}")
        time.sleep(waiting_time() + 2.5)

        try:
            self.driver.find_element(By.CLASS_NAME, "_acan._acao._acas._aj1-").click()
            time.sleep(waiting_time())
        except Exception as e:
            warning(e.__str__())
        try:
            self.driver.find_element(By.CLASS_NAME, "_a9--._a9_1").click()
            time.sleep(waiting_time())
            # last index is 0 or one - depending on the output btn
        except Exception as e:
            warning(e.__str__())

    def __on_profile(self) -> None:
        """Checks if the driver is currently on a profile."""
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
        write(search_input, query)
        time.sleep(waiting_time())

        # get first element in search results
        class_string2: str = "x9f619.x78zum5.xdt5ytf.x6ikm8r.x1odjw0f.x4uap5.x18d9i69.xkhd6sd.x5yr21d.xocp1fn.xh8yej3"
        search_results = self.driver.find_element(By.CLASS_NAME, class_string2)
        children = search_results.find_elements(By.TAG_NAME, "div")
        time.sleep(waiting_time())
        element = children[0]
        element.click()
        self.success("Found profile")
        time.sleep(waiting_time())
        try:
            self.__session_data[self.get_current_username()]["follower"]: int = self.get_follower_count()
            self.__session_data[self.get_current_username()]["following"]: int = self.get_following_count()
            self.__session_data[self.get_current_username()]["posts"]: int = self.get_posts_count()
            self.__session_data[self.get_current_username()]["name"]: str = self.get_name()
            self.__session_data[self.get_current_username()]["bio"]: str = self.get_bio()
            self.__session_data[self.get_current_username()]["profile_picture"]: str = self.get_profile_picture
            self.__session_data[self.get_current_username()]["homepage"]: str = self.get_homepage()
            self.success("Fetched data")
        except ValueError:
            pass

    def follow(self) -> None:
        """Follows the current profile."""
        self.__on_profile()
        # get follow button and follow account
        follow_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acap._acas._aj1-")
        if len(follow_btn) == 0:
            warning(f"You are already following this profile ({self.get_current_username()}).")
            return
        follow_btn[0].click()
        time.sleep(waiting_time())

    def unfollow(self) -> None:
        """Unfollows the current profile."""
        self.__on_profile()
        # get unfollow button and unfollow account
        unfollow_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acap._acat._aj1-")
        if len(unfollow_btn) == 0:
            warning(f"You are not following this profile ({self.get_current_username()}).")
            return
        unfollow_btn[0].click()
        time.sleep(waiting_time())

    def get_picture(self, number: int = 1) -> None:
        """Opens one of the last recent pictures on the current profile."""
        self.__on_profile()
        if number > 12:
            raise Exception("Can not fetch this picture.")
        row: int = (number + 2) // 3
        column: int = ((number - 1) % 3) + 1
        article = self.driver.find_element(By.TAG_NAME, "article").find_elements(By.CLASS_NAME, "_ac7v._aang")
        image = article[row - 1].find_elements(By.TAG_NAME, "a")[column - 1]
        # currently the image is opened without a click
        self.driver.get(image.get_attribute("href"))
        time.sleep(waiting_time())

    def get_liked_by(self, amount: int = 50) -> List[str]:
        """Gets up to 50 users that liked the post from the current picture and returns usernames as a string list."""
        liked_by_btn = self.driver.find_elements(By.CLASS_NAME, "_aacl._aaco._aacu._aacx._aad6._aade")[9]
        liked_by_btn.find_element(By.TAG_NAME, "a").click()
        time.sleep(waiting_time())
        fetched: list = []
        index: int = 0
        class_name = "x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f." \
                     "x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1"
        scroll_name = "x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x6ikm8r.x10wlt62.x1iyjqo2." \
                      "x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1"
        while len(fetched) < amount:
            index += 1
            if index > 10:
                return fetched
            liked_by = self.driver.find_elements(By.CLASS_NAME, class_name)
            for user in liked_by:
                fetched.append(user.text)
            if len(fetched) < amount:
                build = self.driver.find_element(By.CLASS_NAME, scroll_name)
                scroll_element = build.find_element(By.TAG_NAME, "div")
                self.driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scroll_element)
                time.sleep(waiting_time())
        return list(set(fetched))

    def get_followers(self, amount: int = 50) -> List[str]:
        """Gets up to 50 followers from the current profile and returns usernames as a string list."""
        if amount < 1 or amount > 50:
            raise Exception("Minimum followers is one and maximum is 50.")
        if not re.match(f"{self.base_url}.+/", self.driver.current_url):
            raise Exception("You are currently not on the correct page.")
        self.driver.get(f"{self.base_url}{self.get_current_username()}/followers/")
        time.sleep(2 * waiting_time())
        followers = self.driver.find_elements(By.CLASS_NAME, "_ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm")
        followers_list: list = list()
        for follower in followers:
            followers_list.append(follower.text)
        time.sleep(waiting_time())
        if amount - 1 <= len(followers_list):
            followers_list: List[str] = followers_list[:amount - 1]
        return followers_list

    def get_likes(self):
        """Gets the likes of the current picture."""
        button = self.driver.find_element(By.CLASS_NAME, "_aacl._aaco._aacw._aacx._aada._aade")
        like_content = button.find_element(By.TAG_NAME, "span").text
        like_string = like_content.replace(self.__decimal, "")
        if not like_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {like_content}")
        return int(like_string)

    def like_picture(self) -> None:
        """Like the first picture of the current profile."""
        self.__on_profile()
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
        self.__on_profile()
        counters = self.driver.find_elements(By.CLASS_NAME, "_ac2a")
        title = counters[1].get_attribute("title")
        counter_string = title.replace(self.__decimal, "")
        if not counter_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {title}")
        return int(counter_string)

    def get_following_count(self) -> int:
        """Gets the counter of all followed accounts of the current profile as an integer."""
        self.__on_profile()
        counters = self.driver.find_elements(By.CLASS_NAME, "_ac2a")
        content = counters[2].find_element(By.TAG_NAME, "span").text
        counter_string = content.replace(self.__decimal, "")
        if not counter_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {content}")
        return int(counter_string)

    def get_posts_count(self) -> int:
        """Gets the counter of the followers of the current profile as an integer."""
        self.__on_profile()
        counters = self.driver.find_elements(By.CLASS_NAME, "_ac2a")
        content = counters[0].find_element(By.TAG_NAME, "span").text
        counter_string = content.replace(self.__decimal, "")
        if not counter_string.isdigit():
            raise ValueError(f"The follower count can't be converted to an int. String representation: {content}")
        return int(counter_string)

    def get_name(self) -> str:
        """Gets the name of the current profile (not ig-username)."""
        self.__on_profile()
        full_bio = self.driver.find_element(By.CLASS_NAME, "_aa_c")
        name = full_bio.find_element(By.TAG_NAME, "span").text
        return name

    def get_bio(self) -> str:
        """Gets the bio of the current profile."""
        self.__on_profile()
        full_bio = self.driver.find_element(By.CLASS_NAME, "_aa_c")
        bio = full_bio.find_element(By.TAG_NAME, "h1").text.replace("<br>", "\n")
        return bio

    def get_homepage(self) -> str:
        """Gets the url to the homepage of the current profile."""
        self.__on_profile()
        full_bio = self.driver.find_element(By.CLASS_NAME, "_aa_c")
        url = full_bio.find_element(By.TAG_NAME, "div").text
        return url

    def get_profile_picture(self) -> str:
        """Gets the url to the profile picture of the current profile."""
        self.__on_profile()
        frame = self.driver.find_element(By.CLASS_NAME, "_aarf")
        picture = frame.find_element(By.TAG_NAME, "img").get_attribute("src")
        return picture[:picture.find("?")]

    def get_data(self, username: str) -> dict:
        """Returns a dictionary with data about a given profile."""
        if username not in self.__session_data:
            raise Exception("User has not been searched yet.")
        return self.__session_data[username]

    def get_current_username(self) -> str:
        """Gets the current username from the active url and returns the username as a string."""
        url = self.driver.current_url
        sub_url = url[url.find("com/") + 4:]
        return sub_url[:sub_url.find("/")]

    def write_comment(self, message: str) -> None:
        """Writes a comment for the currently opened post."""
        textfield = self.driver.find_element(By.CLASS_NAME, "_akhn").find_element(By.TAG_NAME, "textarea")
        write(textfield, message)
        divs = self.driver.find_element(By.CLASS_NAME, "_akhn").find_elements(By.TAG_NAME, "div")
        print(len(divs))
        post_btn = divs[1].find_element(By.TAG_NAME, "div")
        post_btn.click()

    def send_dm(self, message: str) -> None:
        """Sends a dm to the user of the current profile."""
        wrapper = self.driver.find_element(By.CLASS_NAME, "_ab8w._ab94._ab99._ab9f._ab9m._ab9o._abb0._ab9s._abcm")
        dm_button = wrapper.find_element(By.TAG_NAME, "div")
        dm_button.click()
        time.sleep(2 * waiting_time())
        text_field = self.driver.find_element(By.CLASS_NAME, "_ab8w._ab94._ab99._ab9f._ab9m._ab9o._abbh._abcm")
        input_field = text_field.find_element(By.TAG_NAME, "textarea")
        write(input_field, message)
        send_btn = self.driver.find_elements(By.CLASS_NAME, "_acan._acao._acas._aj1-")
        send_btn.click()
        print(f"Sent direct message to {self.get_current_username()} with this content:\n{message}")

    def close(self) -> None:
        """Closes current session"""
        self.driver.close()
        self.success("Session closed.")
