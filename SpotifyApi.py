from AppSettings import AppSettings

import requests
import enum
import json

class ErrorCodes(enum.Enum):
    TokenExpired = "The access token expired"

class SpotifyApi():
    def __init__(self, appSettings):
        self.baseUrl            = "https://api.spotify.com/v1/"
        self.appSettings        = appSettings
        self.existingTracks     = {}

        self.getExisitingTracks();

    def getExisitingTracks(self):
        requestUrl = self.baseUrl + "playlists/" + self.appSettings.spotifyPlaylistId + '/tracks'
        headers    = { "Authorization" : "Bearer " + self.appSettings.spotifyAccessToken }

        responseJson = json.loads(requests.get(requestUrl, headers=headers).text)

        if 'error' in responseJson:
            message = responseJson["error"]["message"]

            if message == "The access token expired":
                self.refreshAccessCode()
                headers     ["Authorization"] = "Bearer " + self.appSettings.spotifyAccessToken

                responseJson = json.loads(requests.get(requestUrl, headers=headers).text)

                if 'error' in responseJson:
                    return False

        for item in responseJson["items"]:
            if "track" not in item:
                continue

            self.existingTracks[item["track"]["id"]] = True

    def postSongToPlaylist(self, songUrl):
        trackString = "track"
        startIndex  = songUrl.find(trackString, 0)

        if startIndex == -1:
            return False

        songInfo        = songUrl[startIndex + 6:]
        songInfoList    = songInfo.split('?')
        songId          = songInfoList[0]

        if songId in self.existingTracks:
            return False

        requestUrl  = self.baseUrl + "playlists/" + self.appSettings.spotifyPlaylistId + '/tracks/'

        requestData = { "uris"          : ["spotify:track:" + songId] }
        headers     = { "Authorization" : "Bearer " + self.appSettings.spotifyAccessToken }

        responseJson = json.loads(requests.post(requestUrl, json=requestData, headers=headers).text)

        if 'error' in responseJson:
            message = responseJson["error"]["message"]

            if message == "The access token expired":
                self.refreshAccessCode()
                headers     ["Authorization"] = "Bearer " + self.appSettings.spotifyAccessToken

                responseJson = json.loads(requests.post(requestUrl, json=requestData, headers=headers).text)

                if 'error' in responseJson:
                    return False

        self.existingTracks[songId] = True

        return True

    def refreshAccessCode(self):
        data =      {
                            "grant_type"    : "refresh_token"
                        ,   "refresh_token" : self.appSettings.spotifyRefreshToken
                    }

        header =    {
                        "Authorization" : "Basic " + self.appSettings.spotifyClientSecret
                    }

        responseJson = json.loads(requests.post("https://accounts.spotify.com/api/token", data, headers=header).text)

        if 'error' in responseJson:
            return

        newToken = responseJson["access_token"]

        self.appSettings.updateSetting("SPOTIFY", "accessToken", newToken)