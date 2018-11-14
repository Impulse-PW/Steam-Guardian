from steampy.client import SteamClient as steamclient
from .database import *
from steampy.login import InvalidCredentials

class api(object):
    #Initialize
    def __init__(self, apiKey):
        #Declare class variables
        self.apiKey = apiKey
        self.steam_client = steamclient(apiKey)

    #Testing api key method
    def check_api_key(self):
        #My steamid in the paramaters, feel free to add me lol
        self.params = {'key': self.apiKey, "steamids": "76561198099040521"}
        #Try the API to make sure our key is valid
        try:
            self.steam_client.api_call('GET', 'ISteamUser', 'GetPlayerSummaries', 'v2', self.params)
        except InvalidCredentials:
            #Invalid Api Key
            return False
        else:
            return True
