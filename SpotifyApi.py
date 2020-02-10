from AppSettings import AppSettings

import requests
import enum

class ErrorCodes(enum.Enum):
    TokenExpired = "The access token has expired"

class SpotifyApi():
    def __init__(self, appSettings):
        self.baseUrl            = "https://api.spotify.com/v1/"
        self.appSettings        = appSettings

        self.errors = {""}


    def postSongToPlaylist(self, songUrl):
        trackString = "track"
        startIndex  = songUrl.find(trackString, 0)

        if startIndex == -1:
            return False

        songInfo        = songUrl[startIndex + 6:]
        songInfoList    = songInfo.split('?')
        songId          = songInfo[0]

        print(songId)

        requestUrl  = self.baseUrl + "playlists/" + self.appSettings.spotifyPlaylistId + '/tracks/'

        print(requestUrl)

        requestData = { "playlist_id"   : songId }
        headers     = { "Authorization" : self.appSettings.spotifyAccessToken}

        response = requests.post(requestUrl, json=requestData, headers=headers)

        print(response)

        if 'error' in response:
            message = response["error"]["message"]

            if message == ErrorCodes.TokenExpired:
                self.refreshAccessCode()
                requestData ["playlist_id"  ] = songId
                headers     ["Authorization"] = self.appSettings.spotifyAccessToken

                response = requests.post(requestUrl, json=requestData, headers=headers)

                print(response)

                if 'error' in response:
                    return False

        return True

    def refreshAccessCode(self):
        data =      {
                            "grant_type"    : "refresh_token"
                        ,   "refresh_token" : self.appSettings.spotifyRefreshToken
                    }

        header =    {
                        "Authorization" : "NjE0Y2Y5N2I0ZDcxNDNkMGIxOTc5OGZiODNmYmZhMWM6OWYwM2U0MGRiODM5NDhiZjk5MTBmZDA2YzMyMjRmOTE="
                    }

        response = requests.post("https://accounts.spotify.com/api/token", data, header=header)