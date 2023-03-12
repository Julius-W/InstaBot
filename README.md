# InstaBot
InstaBot is a Python library that provides some automation for simple tasks on Instagram like following accounts and sending DMs on Instagram using Selenium.

## Installation
You can install the library from the [GitHub repository](https://github.com/Julius-W/InstaBot) or by using pip:

```
pip install InstaWebBot
```

## Usage
**_IMPORTANT:_** The driver file for Selenium must be located in the current working directory of your project. You can download the driver [here](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/). Please provide the driver name if you are not using the recommended geckodriver.

Initialize the bot by passing in your Instagram username and password as parameters:

```py
from InstaWebBot import InstaBot
bot = InstaBot('your_username', 'your_password')
```

Here is an example with some optional arguments (using their default value):
```py
from InstaWebBot import InstaBot
bot = InstaBot('your_username', 'your_password', headless=False, driver="geckodriver", output=False)
```


To login to Instagram with the given username and password use

```py
bot.login()
```

Once you have created an instance of the InstaBot class, you can use its methods to automate some simple tasks on Instagram.

## Functions
Search for a username by using

```py
bot.search(query)
```

After that you can peform various actions on a user profile:

```py
bot.follow()
bot.unfollow()
bot.send_dm(message)
bot.like_picture()
```

It is also possible to get data from the profile once it has been searched with `bot.search(q)`:
```py
user_data = bot.get_data('instagram')
# user_data contains various counters as well as a link to the profile picture, homepage and bio
print(f"Follower count of @instagram: {user_data['followers']})
```



This is a small example program to get 50 followers of a given profile (50 is the maximum amount, because Instagram limits the visibility of followers/following lists):
```py
from InstaWebBot import InstaBot
bot = InstaBot('username', 'password')
bot.login()
bot.search('instagram')
followers = bot.get_followers()
for follower in followers:
    print(follower)
```


## Future functionality:
- [x] Get follower and following counter
- [x] Get post counter
- [x] Allow commenting on posts
- [x] Send direct messages to user
- [ ] Like different images than just the first image
- [ ] Download images
- [ ] Improve usability

## LICENSE
InstaBot is licensed under the GNU General Public License v2.0.

## Help & Contribution
If you find an error please feel free to open an issue [here](https://github.com/Julius-W/InstaBot/issues).
