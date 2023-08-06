import json # We need this library to return the website to dict
from requests import get # We will use this library to get information from the website.


class Itch():
    def __init__(self, token):
        self.url = "https://itch.io/api/1/" + token + "/" # we define our ulr for api website


    def user(self): # We create a function named user and return the user information as dict from it.
        url = get(self.url + "me").text # We pull user information from api
        user = json.loads(url)["user"] # And we convert this user information from text to dict 
        # (If you look at the api page, you will understand why I typed ["user"]) 
        return user # Finally, we return the user value to use it.

    def games(self): # We created a function called games to get game data
        url = get(self.url + "my-games").text # Then we pulled the information from the api as text
        games_dict = json.loads(url)["games"] # We assign them to a dict object
        index = len(games_dict) - 1 # And we created an index and gave one less of the value of the list
        # With this index we reverse the list as follows (we did it this way because we wanted to do it according to the historical order)
        games = [] # And assigning a variable to create the ordered list
        while index >= 0: # Then we will use values greater than -1 to reduce the index.
            games.append(games_dict[index]) # In the games object, we give the index object of the games_dict list
            index -= 1 # Then we continued the loop by reducing the index by one
        return games

# Official api usage link
#! https://itch.io/docs/api/overview