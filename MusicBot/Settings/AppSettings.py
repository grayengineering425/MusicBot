import configparser
import sys
import os

class AppSettings():
    def __init__(self):
        self.oathConfigPath = os.getcwd() + "/Settings/oath.ini"

        self.oathConfig = configparser.ConfigParser()
        self.oathConfig.read( self.oathConfigPath)

        self.readOathSettings()

    def updateSetting(self, section, settingId, value):
        if section not in self.oathConfig or settingId not in self.oathConfig[section]:
            return

        self.oathConfig[section][settingId] = value

        with open(self.oathConfigPath, 'w') as configfile:
            self.oathConfig.write(configfile)

        self.readOathSettings()

    def readOathSettings(self):
        #SLACK SETTINGS
        self.slackVerificationToken  = self.oathConfig["SLACK"]["verificationToken"]
        self.slackWebclientToken     = self.oathConfig["SLACK"]["webclientToken"   ]

        #SPOTIFY SETTINGS
        self.spotifyAccessToken      = self.oathConfig["SPOTIFY"]["accessToken"  ]
        self.spotifyRefreshToken     = self.oathConfig["SPOTIFY"]["refreshToken" ]
        self.spotifyClientSecret     = self.oathConfig["SPOTIFY"]["clientSecret" ]
        self.spotifyUserId           = self.oathConfig["SPOTIFY"]["userId"       ]
        self.spotifyPlaylistId       = self.oathConfig["SPOTIFY"]["playlistId"   ]
        self.spotifyPlaylistLink     = self.oathConfig["SPOTIFY"]["playlistLink" ]

        #GITHUB SETTINGS
        self.githubLink              = self.oathConfig["GITHUB" ]["link"]