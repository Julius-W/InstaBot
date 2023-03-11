# InstaBot
InstaBot is a Python library that provides some automation for simple tasks on Instagram like following and sending dms on Instagram.

## Installation

You can install the library from the [GitHub repository](https://github.com/Julius-W/InstaBot) using the following command:

```
pip install git+https://github.com/Julius-W/InstaBot.git
```

## Usage

To use the InstaBot class, you can create an instance of the class by passing in your Instagram username and password as parameters:

```py
from instabot import InstaBot
bot = InstaBot('your_username', 'your_password')
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
bot.send_dm(message)
bot.like_picture()
```

It is also possible to get data from the profile:

```py
followers = bot.get_followers()  # get up to 50 followers
for follower in followers:
    print(follower)
```


## Future functionality:
- [ ] Get follower and following counter-
- [ ] Get post counter-
- [ ] Like different images than just the first image-
- [ ] Allow commenting on posts
- [ ] Download images
- [x] Send direct messages to user

## LICENSE
InstaBot is licensed under the GNU General Public License v2.0.
