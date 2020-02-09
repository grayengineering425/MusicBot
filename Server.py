from Chat           import Chat, Emoji
from AppSettings    import AppSettings

class Server:
    def __init__(self, appSettings):
        self.name   = "MusicBot"
        self.token  = appSettings.verificationToken
        self.chat   = Chat(appSettings)

    def handleAppMention(self, payload):
        channel = payload['channel' ]
        userId  = payload['user'    ]
        blocks  = payload['blocks'  ]

        messageText = ""

        for block in blocks:
            if block['type'] == 'rich_text':
                elements = block['elements']
                
                for element in elements:
                    type = element['type']
                    
                    if type == 'rich_text_section':
                        subElements = element['elements']
                        
                        for subElement in subElements:
                            subType = subElement['type']
                            
                            if subType == 'text':
                                messageText = subElement['text']
                            elif subType == 'link':
                                messageLink = subElement['url']

        displayName = self.chat.getDisplayName(userId)
        
        message     = "Hello @" + displayName + ", nice to meet you!"
        status      = self.chat.sendMessage     (channel, message)

        if status == True:
            print('success')
        else:
            print('failure')

    def handleLinkPosted(self, payload):
        channel = payload['channel' ]
        userId  = payload['user'    ]

        urls = []

        links = payload["links"]

        for link in links:
            domain  = link["domain"]
            url     = link["url"]

            if domain == "open.spotify.com":
                urls.append(url)

        displayName = self.chat.getDisplayName(userId)
        message     = "Hello @" + displayName + ", I have archived this song for you! You can find the link using the /spotify command!"
        status      = self.chat.sendMessage     (channel, message)

        if status == True:
            print('success')
        else:
            print('failure')
