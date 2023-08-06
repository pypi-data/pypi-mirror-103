# Package usage
First of all you need a **api key** from [itch.io](https://itch.io/user/settings/api-keys). Then you can come back here.

## First code
1. import api
    ```
    from itch import Itch
    ```
2. set your variable for Itch
    ```
    itch = Itch("YOUR_APIKEY_HERE")
    ```
3. get your informations
    * if you want to pull your user informations...
        1. create a variable as user
            ```
            user = itch.user()
            ```
        2. print your page url
            ```
            print(user["url"])
            ```
        3. now you can get more informations about your account with dict keys (_the dict keys bottom of page_)
    * or your game's informations
        1. create a variable as games
            ```
            games = itch.games()
            ```
        2. for use this we can make a for loop 
            ```
            for game in games:
                print(game["title"])
            ```
        3. by this you can get titles of your games (_the dict keys bottom of page_)




### Dict Keys
* Keys of user object:

    **Variable name** | **Explanation**
    ------------- | ----------
    cover_url | url for profile image
    display_name | user name
    developer | is developer
    id | user id
    url | user account url
    gamer | is gamer
    username | nickname
    press_user | is press user


* Keys of game's object (*for each array element*):
    **Variable name** | **Explanation**
    ------------- | ----------
    purchases_count | number of purchases
    p_osx | is there available any version for OSX
    p_linux | is there available any version for linux
    p_windows | is there available any version for windows
    p_android | is there available any version for android
    id | game id
    published | if game is published this value takes True
    published_at | published date
    views_count | number of views
    url | url for game page
    can_be_bought | is this game have a price
    created_at | date of created
    in_press_system | is this game in press system
    user | this return a dict object of game's author's informations
    has_demo | is has a demo
    downloads_count | number of downloads
    title | game's title
    cover_url | this return a url for game's banner photograph
    min_price | this is return price of game (*if game hasn't any price this takes 0*)
    classification | genre of game
    short_title | game's short title
    type | game's type