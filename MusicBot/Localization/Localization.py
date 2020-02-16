class Localization:
    instance            = None
    conversationStrings = []


    @staticmethod
    def getInstance():
        if Localization.instance == None:
            Localization()

        return Localization.instance

    def __init__(self):
        Localization.instance = self

