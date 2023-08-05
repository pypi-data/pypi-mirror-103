English | [简体中文](./README_zh-cn.md)

# genshinstats
This project is meant to be a wrapper for the Genshin Impact's [hoyolab.com](https://www.hoyolab.com/genshin/) api.
The api endpoints used in this project are not publicly known but are free to use for third part tools, so I have decided to get these a bit more publicity by making a wrapper for them.

You can pip install with [PyPI](https://pypi.org/project/genshinstats/)

Be aware that this project is currently still in development and therefore can change at any moment.
If you're making your own module that has genshinstats as a dependency, remember to explicitly set the version it should use.

# how to use
Import the `genshinstats` module and set the cookie to login.
To set the cookie use `set_cookie(account_id=..., cookie_token=...)`.
Pass your own cookie values into these fields. ([how can I get my cookie?](#how-can-I-get-my-cookie?))
The cookie is required and will raise an error if missing.

All functions are documented and type hinted.

[API documentation](https://thesadru.github.io/pdoc/genshinstats/)
# examples
Simple examples of usage:
```py
import genshinstats as gs # import module
gs.set_cookie(account_id=119480035, cookie_token="hEIIh08ghAIlHY1QQZBnsngVWXzaEMQtrSV0Bowu") # login

uid = 710785423
user_info = gs.get_user_info(uid) # get user info with a uid
total_characters = len(user_info['characters']) # get the amount of characters
print('user "sadru" has a total of',total_characters,'characters')
```
> Cookies should be your own. These are just some example cookies of an account that can be deleted at any time.
```py
stats = gs.get_user_info(uid)['stats']
for field,value in stats.items():
    print(f"{field.replace('_',' ')}: {value}")
# achievements: 210
# active days: 121
# characters: 19
# ...
```

```py
characters = gs.get_all_characters(uid)
for char in characters:
    print(f"{char['rarity']}* {char['name']:10} | lvl {char['level']:2} C{char['constellation']}")
# 4* Beidou     | lvl 80 C1
# 4* Fischl     | lvl 80 C1
# 4* Bennett    | lvl 80 C2
# 5* Mona       | lvl 80 C0
# ...
```

```py
spiral_abyss = gs.get_spiral_abyss(uid,previous=True)
stats = spiral_abyss['stats']
for field,value in stats.items():
    print(f"{field.replace('_',' ')}: {value}")
# total battles: 14
# total wins: 7
# max floor: 9-1
# total stars: 18
```

It's possible to set the cookies with a header
```py
gs.set_cookie_header("""
_MHYUUID=0110a95f-fbe9-41a3-a26a-5ed1d9e3a8f1; account_id=119480035; cookie_token=hEIIh08ghAIlHY1QQZBnsngVWXzaEMQtrSV0Bowu; ltoken=cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT; ltuid=119480035; mi18nLang=en-us
""")
```
Or set them automatically by getting them from a browser
```py
gs.set_cookie_auto() # search all browsers
gs.set_cookie_auto('chrome') # search specific browser
```
> requires `cookie-browser3`, can take up to 10s
## submodules
### gachalog
Gets your gacha pull logs.
For this you must first open the history/details page in genshin impact,
the script will then get all required data by itself.
```py
types = gs.get_gacha_types() # get all possible types
key = types[2]['key'] # name == "Character Event Wish", key == '301'
for i in gs.get_gacha_log(key): # get the gacha log
    print(f"{i['time']} - {i['name']} ({i['rarity']}* {i['type']})")
# 2021-03-22 09:50:12 - Razor (4* Character)
# 2021-03-22 09:50:12 - Harbinger of Dawn (3* Weapon)
# 2021-03-22 09:50:12 - Cool Steel (3* Weapon)
# 2021-03-22 09:50:12 - Emerald Orb (3* Weapon)
# ...
```
```py
# get all gacha pulls at once
for i in gs.get_entire_gacha_log():
    print(f"{i['time']} - {i['name']} ({i['rarity']}* {i['type']})")
```
```py
ids = gs.get_all_gacha_ids() # get all possible gacha ids (only counts opened details pages)
for i in ids:
    details = gs.get_gacha_details(i) 
    print(f"{details['gacha_type']} - {details['banner']}")
    print('5 stars:', ', '.join(i['name'] for i in details['r5_up_items']))
    print('4 stars:', ', '.join(i['name'] for i in details['r4_up_items']))
    print()
# Weapon Event Wish - Event Wish "Epitome Invocation"
# 5 stars: Elegy for the End, Skyward Blade
# 4 stars: The Alley Flash, Wine and Song, Favonius Greatsword, Favonius Warbow, Dragon's Bane
# ...
```
View other's history by passing in an authkey:
```py
authkey = "t5QMiyrenV50CFbqnB4Z+aG4ltprY1JxM5YoaChr9QH0Lp6rK5855xxa1P55..."
gs.get_gacha_log(301,20,authkey=authkey)
```
Or by directly setting the authkey:
```py
# directly with the token:
gs.set_authkey("D3ZYe49SUzpDgzrt/l00n2673Zg8N/Yd9OSc7NulRHhp8EhzlEnz2ISBtKBR0fZ/DGs8...")
# get from a url:
gs.set_authkey(url="https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?...")
# read from a custom file:
gs.set_authkey(logfile='other_output_log.txt')
```
> Since the authkey lasts only a day this is more like for exporting than for actual use.
### signin
Automatically get daily sign in rewards for the currently logged-in user.
```py
info = gs.get_daily_reward_info()
print('total rewards claimed:',info['total_sign_day'])
gs.sign_in() # signs you in, returns a bool whether it succeeded
```
### hoyolab
Miscalenious stuff for mihoyo's hoyolab. Has searching, auto check-in and code redemption.
```py
# search all users and get their nickname and uid
for user in gs.search('sadru'):
    print(f"{user['nickname']} ({user['uid']}) - \"{user['introduce']}\"")

# check in to hoyolab
gs.check_in() # raises in cannot check in

# try to redeem a code
gs.redeem_code("GENSHINGIFT")

# get a record card; has user nickname and game uid
card = gs.get_record_card(8366222)
print(f"{card['nickname']} ({card['game_role_id']}) - AR {card['level']}")

# get an in-game uid from a community uid directly
uid = 8366222
# if it's an actual community uid
if not gs.is_game_uid(uid): 
    uid = gs.get_uid_from_community(uid)
```

## change language
Some api endpoints support changing languages, you can see them listed here:
```py
genshinstats.get_all_characters(...,lang='fr-fr')

gachalog.get_gacha_types(lang='fr')
gachalog.get_gacha_log(...,lang='fr')
gachalog.get_gacha_items(lang='fr-fr')
gachalog.get_gacha_details(...,lang='fr-fr')
```
> endpoints can use two types of values, long and short. Long is the default value in `gs.get_langs()`, short is only the first part of a lang (`en-us` -> `en`).
> Chinese has simplified and traditional options, so if you use chinese the short version is the same as the long version (`zh-cn` -> `zh-cn`)

# faq
## How can I get my cookie?
1. go to [hoyolab.com](https://www.hoyolab.com/genshin/)
2. login to your account
3. press `F12` to open inspect mode (aka Developer Tools)
4. go to `Application`, `Cookies`, `https://www.hoyolab.com`.
5. copy `account_id` and `cookie_token`
6. use `set_cookie(account_id=..., cookie_token=...)` in your code

## Why do I keep getting `DataNotPublic` errors even though I'm trying to view my own account stats and didn't set anything to private?
The `DataNotPublic` is raised when a user has not made their data public, because the account visibility is set to private by default.
To solve this error You must go to [hoyolab.com](https://www.hoyolab.com/genshin/accountCenter/gameRecord) and make your account public by clicking [the toogle next to "public"](https://cdn.discordapp.com/attachments/529573765743509504/817509874417008759/make_account_public.png).

## How do the cookie token and authkey work?
Every endpoint in mihoyo's api requires authentication, this is in the form of a cookie token and an authkey.
User stats use a cookie token and gacha history uses an authkey.

The cookie token is bound to the user and as far as I know cannot be reset, so remember to never give your cookie token to anyone. For extra safety you may want to create an alt account, so your real account is never in any danger. This token will allow you to view public stats of all users and private stats of yourself.

The authkey is a temporary token to access your gacha history. It's unique for every user and is reset after 24 hours. It cannot be used to view the history of anyone else. It is fine to share this key with anyone you want, the only "private" data they will have access to is the gacha history.

## How do I get the gacha history of other players?
To get the gacha history of other players you must get their authkey and pass it as a keyword into `get_gacha_log` or `get_entire_gacha_log`. That will make the function return their gacha history instead of yours, it will also avoid the error when you try to run your project on a machine that doesn't have genshin installed.

To get the autkey you ask the player to press `ESC` while in the game and click the feedback button on the bottom left, then get them to send the url they get redirected to. You can then extract the authkey with `extract_authkey(url)` which you can then pass into the functions.

## Why do you call wish history "gacha log" or "gacha history"?.
In mihoyo's api the official name for the wish history is `GachaLog`, which is how I also decided to call my functions. The reason why I still call it gacha instead of wish is because I have played other gacha games before and got used to calling everything gacha.
If you feel like you want to change it then you can open and issue and if enough people disagree with it I'll just change it. 
For now the name will be staying fo backwards compatibility.

## What's the rate limit?
As far as I know there is no rate limit, however I recommend you avoid spamming the api, as mihoyo can still ip ban you. My guess is that if you try to make more than 1 request per second the chances are mihoyo is not going to appreciate it.

## How can I get an in-game uid from a hoyolab community uid?
`get_uid_from_community(community_uid)` can do that for you. It will return None if the user's data is private. To check whether a given uid is a game,  or a community one use `is_game_uid(uid)`.

It is impossible to get a community uid from an in-game uid.

## How can I get a user's username?
Getting the user's username and adventure rank is possible only with their community uid. You can get them with `get_record_card(community_uid)` along with a bunch of other data.

# project layout
```
genshinstats.py    user stats and characters
hoyolab.py         user hoyolab community info
gachalog.py        gacha history
signin.py          automatic sign in for hoyolabs
errors.py          errors used by genshinstats
```

# about this project
## contribution
All contributions are welcome as long as it's in a form of a clean PR.
Currently, I am looking for literally anyone who has a chinese genshin account to help me make this project work for all chinese endpoints (right now it's mostly guesswork).
## crediting
This project can be freely downloaded and distributed.
Crediting is appreciated.
