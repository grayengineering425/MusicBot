import configparser

class AppSettings():
    def __init__(self):
        configPath = "./oath.ini"

        config = configparser.ConfigParser()

        config.read(configPath)

        self.verificationToken  = config["OATH"]["verificationToken"]
        self.webclientToken     = config["OATH"]["webclientToken"   ]
