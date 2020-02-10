import configparser

class AppSettings():
    def __init__(self):
        configPath = "./oath.ini"

        config = configparser.ConfigParser()

        config.read(configPath)

        #SLACK SETTINGS
        self.slackVerificationToken  = config["SLACK"]["verificationToken"]
        self.slackWebclientToken     = config["SLACK"]["webclientToken"   ]

        #SPOTIFY SETTINGS
        self.spotifyAccessToken      = config["SPOTIFY"]["accessToken"  ]
        self.spotifyRefreshToken     = config["SPOTIFY"]["accessToken"  ]
        self.spotifyUserId           = config["SPOTIFY"]["userId"       ]
        self.spotifyPlaylistId       = config["SPOTIFY"]["playlistId"   ]

    def updateSetting(self, section, settingId, value):
        if section not in self.config:
            return

        currentSection = self.config[section]

        if settingId not in currentSection:
            return

        currentSection[settingId] = value