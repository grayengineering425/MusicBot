from AppSettings import AppSettings

import requests
import enum
import json
import queue

class ErrorCodes(enum.Enum):
    TokenExpired = "The access token expired"

class SpotifyApi():
    def __init__(self, appSettings):
        self.baseUrl            = "https://api.spotify.com/v1/"
        self.appSettings        = appSettings
        self.existingTracks     = {}
        self.existingPlaylists  = {}
        self.existingAlbums     = {}

        self.getExisitingTracks();

    def postSongToPlaylist(self, urlString):
        trackString     = "track"
        playlistString  = "playlist"
        albumString     = "album"

        startIndex  = urlString.find(trackString, 0)

        if startIndex != -1:
            return self.parseTrack(urlString, startIndex)

        startIndex = urlString.find(playlistString, 0)

        if startIndex != -1:
            return self.parsePlaylist(urlString, startIndex)

        startIndex = urlString.find(albumString, 0)

        if startIndex != -1:
            return self.parseAlbum(urlString, startIndex)

        return False


    def parseTrack(self, urlString, startIndex):
        songInfo        = urlString[startIndex + 6:]
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

    def parsePlaylist(self, urlString, startIndex):
        playlistInfo        = urlString[startIndex + 9:]
        playlistInfoList    = playlistInfo.split('?')
        playlistId          = playlistInfoList[0]

        if playlistId in self.existingPlaylists:
            return False

        requestUrl  = self.baseUrl + "playlists/" + playlistId
        headers     = { "Authorization" : "Bearer " + self.appSettings.spotifyAccessToken }

        responseJson = json.loads(requests.get(requestUrl, headers=headers).text)

        if 'error' in responseJson:
            message = responseJson["error"]["message"]
            
            if message == "The access token expired":
                self.refreshAccessCode()
                headers     ["Authorization"] = "Bearer " + self.appSettings.spotifyAccessToken
            
                responseJson = json.loads(requests.post(requestUrl, json=requestData, headers=headers).text)
            
                if 'error' in responseJson:
                    return False

        if "tracks" not in responseJson or "items" not in responseJson["tracks"]:
            return False

        trackItems = responseJson["tracks"]["items"]

        mostPopularTracks = queue.PriorityQueue()

        for item in trackItems:
            if "track" not in item:
                continue

            track = item["track"]

            if "popularity" not in track or "id" not in track:
                    continue

            if track["id"] not in self.existingTracks:
                mostPopularTracks.put( (-int(track["popularity"]), track["id"]) )

        self.postMostPopularTracks(mostPopularTracks)

        self.existingPlaylists[playlistId] = True
        
        return True

    def parseAlbum(self, urlString, startIndex):
        albumInfo        = urlString[startIndex + 6:]
        albumInfoList    = albumInfo.split('?')
        albumId          = albumInfoList[0]

        if albumId in self.existingAlbums:
            return False

        albumJson        = self.getAlbumInfo(albumId)

        if albumJson is None or "tracks" not in albumJson or "items" not in albumJson["tracks"]:
            return False
        
        trackItems = albumJson["tracks"]["items"]
        
        mostPopularTracks = queue.PriorityQueue()
        
        for item in trackItems:
            if "type" not in item or item["type"] != "track":
                continue
        
            if "id" not in item:
                    continue

            trackInfo = self.getTrackInfo(item["id"])

            if "popularity" not in trackInfo:
                continue

            if trackInfo["id"] not in self.existingTracks:
                print(str(trackInfo["popularity"]) + " " + str(trackInfo["track_number"]) + "\n")
                mostPopularTracks.put( (-int(trackInfo["popularity"]), trackInfo["id"]) )
        
        count = 0
        
        self.postMostPopularTracks(mostPopularTracks)
        
        self.existingAlbums[albumId] = True

        return True

    def getTrackInfo(self, trackId):
        requestUrl  = self.baseUrl + "tracks/" + trackId
        headers     = { "Authorization" : "Bearer " + self.appSettings.spotifyAccessToken }
        
        responseJson = json.loads(requests.get(requestUrl, headers=headers).text)
        
        if 'error' in responseJson:
            message = responseJson["error"]["message"]
            
            if message == "The access token expired":
                self.refreshAccessCode()
                headers     ["Authorization"] = "Bearer " + self.appSettings.spotifyAccessToken
            
                responseJson = json.loads(requests.post(requestUrl, json=requestData, headers=headers).text)
            
                if 'error' in responseJson:
                    return None
        
        return responseJson

    def getAlbumInfo(self, albumId):
        requestUrl  = self.baseUrl + "albums/" + albumId
        headers     = { "Authorization" : "Bearer " + self.appSettings.spotifyAccessToken }
        
        responseJson = json.loads(requests.get(requestUrl, headers=headers).text)
        
        if 'error' in responseJson:
            message = responseJson["error"]["message"]
            
            if message == "The access token expired":
                self.refreshAccessCode()
                headers     ["Authorization"] = "Bearer " + self.appSettings.spotifyAccessToken
            
                responseJson = json.loads(requests.post(requestUrl, json=requestData, headers=headers).text)
            
                if 'error' in responseJson:
                    return None

        return responseJson

    def postMostPopularTracks(self, mostPopularTracks):
        count = 0

        while mostPopularTracks.qsize() > 0 and count < 2:
            track   = mostPopularTracks.get()
            trackId = track[1]
            
            requestUrl  = self.baseUrl + "playlists/" + self.appSettings.spotifyPlaylistId + '/tracks/'
            
            requestData = { "uris"          : ["spotify:track:" + trackId] }
            headers     = { "Authorization" : "Bearer " + self.appSettings.spotifyAccessToken }
            
            responseJson = json.loads(requests.post(requestUrl, json=requestData, headers=headers).text)
            
            if 'error' not in responseJson:
                self.existingTracks[trackId] = True
            
            count += 1


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