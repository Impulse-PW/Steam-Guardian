from steam import SteamClient

#Steam client control class
class clientData(object):
    #Initialize
    def __init__(self, username, password, guardCode, twoFactorCode):
        #Declare class variables
        self.client = SteamClient()
        self.guardCode = guardCode
        self.loginResult = "Not logged in"
        self.twoFactorCode = twoFactorCode
        self.username, self.password = username, password
    #Client login method
    def login(self):
        #Login to steam
        self.loginResult = self.client.login(self.username, self.password, None, self.guardCode, self.twoFactorCode)
