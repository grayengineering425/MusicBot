import requests
import enum

from Chat           import Chat, Emoji
from AppSettings    import AppSettings
from SpotifyApi     import SpotifyApi
from Localization   import Localization

class SlashRequests(enum.Enum):
    Spotify         = 0
    MusicBotInfo    = 1
    Github          = 2

class Server:
    def __init__(self, appSettings):
        self.appSettings    = appSettings;
        self.name           = "MusicBot"
        self.chat           = Chat      (appSettings)
        self.spotify        = SpotifyApi(appSettings)
        self.localization   = Localization()

    def handleAppMention(self, payload):
        channel = payload['channel' ]
        userId  = payload['user'    ]
        blocks  = payload['blocks'  ]

        messageText = ""

        #for block in blocks:
        #    if block['type'] == 'rich_text':
        #        elements = block['elements']
        #        
        #        for element in elements:
        #            type = element['type']
        #            
        #            if type == 'rich_text_section':
        #                subElements = element['elements']
        #                
        #                for subElement in subElements:
        #                    subType = subElement['type']
        #                    
        #                    if subType == 'text':
        #                        messageText = subElement['text']
        #                    elif subType == 'link':
        #                        messageLink = subElement['url']

        displayName = self.chat.getDisplayName(userId)
        
        message     = "Hello @" + displayName + ", nice to meet you! Use /musicbotinfo to learn more about me!"
        status      = self.chat.sendMessage     (channel, message)

    def handleLinkPosted(self, payload):
        channel = payload['channel' ]
        userId  = payload['user'    ]

        if self.chat.checkInChannel(channel) == False:
            return

        urls = []

        links = payload["links"]

        for link in links:
            domain  = link["domain"]
            url     = link["url"]

            if domain == "open.spotify.com":
                urls.append(url)

        success = True

        for url in urls:
            success = self.spotify.postSongToPlaylist(url)

        #if success == True:
        #    displayName = self.chat.getDisplayName(userId)
        #    message     = "Hello @" + displayName + ", I have archived this song for you! You can find the link using the /spotify command!"
        #    status      = self.chat.sendMessage     (channel, message)


    def handleSlashRequest(self, slashType):
        response                = {}
        response["blocks"]      = []

        section                 = {}
        section["type"]         = "section"
        section["text"]         = {}
        section["text"]["type"] = "mrkdwn"

        if slashType == SlashRequests.Github:
            section["text"]["text"] = self.appSettings.githubLink

        elif slashType == SlashRequests.Spotify:
            section["text"]["text"] = self.appSettings.spotifyPlaylistLink

        else:
            section["text"]["text"] = "A bot designed so you can find all the music posted here in one place\nCommands\n\t/spotify\n\t/musicbotinfo\n\t/github\nDesigned and \"tested\" by Alex Gray"

        response["blocks"].append(section)

        return response
