import sqlite3
import os.path
import steam.webauth as wa
from steam.guard import SteamAuthenticator

#Database access and control class
class dataBase(object):
    #Initialize
    def __init__ (self, databaseName="secrets.db"):
        #Declare class variables
        self.databaseName = databaseName

        if not os.path.isfile(self.databaseName):
            self.create_database()
    #Create database method
    def create_database(self):
        self.exec_query("CREATE TABLE Secrets (secret varchar(1024), isactive boolean, steamid varchar(1024), steamapi varchar(1024), steamuser varchar, steampass varchar)")
    #Create user method
    def create_user(self, secret, steamid, steamuser, steampass):
        self.exec_query("SELECT 1 FROM Secrets WHERE isactive='1'")
        #If active account is found set it to inactive
        if len(self.response) > 0:
            self.exec_query("UPDATE Secrets SET isactive = '0' WHERE isactive = '1'")
        #Insert our new account secrets and set it as our active account
        self.exec_query("INSERT INTO Secrets (secret, isactive, steamid, steamapi, steamuser, steampass) VALUES ('{}', '1', '{}', '', '{}', '{}')".format(secret, steamid, steamuser, steampass))
    #User counting method
    def count_users(self):
        self.exec_query("SELECT 1 FROM Secrets")
        return(len(self.response))
    #Execute query(s) method
    def exec_query(self, query=None, queries=None):
        #Connect to database
        self.queries = queries
        self.connection = sqlite3.connect(self.databaseName)
        self.cur = self.connection.cursor()
        while True:
            try:
                #Execute all querie(s)
                if self.queries:
                    for q in self.queries:
                        self.cur.execute(q)
                else:
                    self.cur.execute(query)
            except sqlite3.ProgrammingError:
                pass
            else:
                break
        #Commit and cleanup
        self.response = self.cur.fetchall()
        self.connection.commit()
        self.connection.close()
    #Get active user secrets method
    def get_active_secrets(self):
        self.exec_query("SELECT secret FROM Secrets WHERE isactive='1'")
        return self.response[0][0]
    #Get all secrets method
    def get_secrets(self):
        self.exec_query("SELECT secret FROM Secrets")
        return self.response
    #Read active user's api key method
    def get_api_key(self):
        self.exec_query("SELECT steamapi FROM Secrets WHERE isactive = '1'")
        #If key is set
        if len(self.response) > 0:
            return self.response[0][0]
        else:
            #Key not set
            return False
    #Active user check method
    def has_active_user(self):
        self.exec_query("SELECT 1 FROM Secrets WHERE isactive='1'")
        #If active account is set
        if len(self.response) > 0:
            return True
        else:
            #No active account set
            return False
    #Remove Steam Guard method
    def remove_guard(self, twofactor, activeSecrets):
        #Query username and password
        self.exec_query("SELECT steamuser, steampass FROM Secrets WHERE isactive ='1'")
        username, password = self.response[0][0], self.response[0][1]
        #Login like a mobile phone
        medium = wa.MobileWebAuth(username, password)
        medium.login(twofactor_code=twofactor)
        sa = SteamAuthenticator(secrets=activeSecrets, medium=medium)
        #Remove Steam Guard from the account and from the database
        sa.remove()
        self.exec_query("DELETE FROM Secrets WHERE isactive = '1'")
    #Update active user's api key method
    def update_api_key(self, apiKey):
        self.exec_query("UPDATE Secrets SET steamapi = '{}' WHERE isactive = '1'".format(apiKey))
    #Update active user method
    def update_active_user(self, secret):
        self.exec_query("UPDATE Secrets SET isactive = '0' WHERE isactive = '1'")
        self.exec_query("UPDATE Secrets SET isactive = '1' WHERE secret = '{}'".format(secret))
