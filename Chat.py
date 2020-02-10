import slack
from slack          import WebClient
from AppSettings    import AppSettings

import enum

class Emoji(enum.Enum):
    Smile = ":smile:" 
    Empty = ""

class Chat():
    def __init__(self, appSettings):
        self.client = WebClient(appSettings.slackWebclientToken)


    def getDisplayName(self, userId):
        response = self.client.users_profile_get(user=userId)

        if response["ok"]:
            return response["profile"]["display_name"]
        
        else:
            return ""

    def sendMessage(self, channel, text):
        response = self.client.chat_postMessage(channel=channel, text=text)

        return response["ok"]

    def checkInChannel(self, channel):
        response = self.client.conversations_info(channel=channel)

        if response["ok"] == False:
            return False

        channelInfo = response["channel"]

        if channelInfo["is_channel"] == False or channelInfo["is_member"] == False:
            return False

        return True
