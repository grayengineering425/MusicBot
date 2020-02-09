import slack
from slack          import WebClient
from AppSettings    import AppSettings


import enum

class Emoji(enum.Enum):
    Smile = ":smile:" 
    Empty = ""

class Chat():
    def __init__(self, appSettings):
        self.client = WebClient(appSettings.webclientToken)


    def getDisplayName(self, userId):
        response = self.client.users_profile_get(user=userId)

        if response["ok"]:
            return response["profile"]["display_name"]
        
        else:
            return ""

    def sendMessage(self, channel, text):
        response = self.client.chat_postMessage(channel=channel, text=text)

        return response["ok"]
