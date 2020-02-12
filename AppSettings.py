import configparser

class AppSettings():
    def __init__(self):
        configPath = "./oath.ini"

        self.config = configparser.ConfigParser()

        self.config.read(configPath)
        self.readSettings()

    def updateSetting(self, section, settingId, value):
        if section not in self.config or settingId not in self.config[section]:
            return

        self.config[section][settingId] = value

        with open('./oath.ini', 'w') as configfile:
            self.config.write(configfile)

        self.readSettings()

    def readSettings(self):
        #SLACK SETTINGS
        self.slackVerificationToken  = self.config["SLACK"]["verificationToken"]
        self.slackWebclientToken     = self.config["SLACK"]["webclientToken"   ]

        #SPOTIFY SETTINGS
        self.spotifyAccessToken      = self.config["SPOTIFY"]["accessToken"  ]
        self.spotifyRefreshToken     = self.config["SPOTIFY"]["refreshToken" ]
        self.spotifyClientSecret     = self.config["SPOTIFY"]["clientSecret" ]
        self.spotifyUserId           = self.config["SPOTIFY"]["userId"       ]
        self.spotifyPlaylistId       = self.config["SPOTIFY"]["playlistId"   ]