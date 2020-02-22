import os

class Users():
    def __init__(self):
        self.existingUserFile  = os.getcwd() + "/Data/users.txt"
        self.existingUsers     = {}

    def getExistingUsers(self):
        with open(self.existingUserFile, "r") as userFile:
            for line in userFile:
                self.existingUsers[line.rstrip()] = True

    def addExistingUser(self, userId):
        with open(self.existingUserFile, "a") as userFile:
            userFile.write(userId + "\n")
    
        self.existingUsers[userId] = True
    
    def doesUserExist(self, userId):
        return userId in self.existingUsers
