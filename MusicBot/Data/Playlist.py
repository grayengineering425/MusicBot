from AppSettings import AppSettings

import requests
import enum
import json
import queue

class Playlist():
    def __init__(self, existingTracks):
        self.baseUrl                = "https://api.spotify.com/v1/"
        self.appSettings            = appSettings
        self.existingTracks         = existingTracks
        self.existingAlbumFile      = "./albums.txt"
        self.exisitingPlaylistFile  = "./playlists.txt"


        self.existingAlbums     = {}
        self.existingPlaylists  = {}

        def getExistingAlbums(self):
            with open(self.existingAlbumFile, "r") as albumFile:
                for line in albumFile:
                    self.existingAlbums[line.rstrip()] = True

        def getExistingPlaylists(self):
            with open(self.exisitingPlaylistFile, "r") as playlistFile:
                for line in playlistFile:
                    self.existingPlaylists[line.rstrip()] = True

        def addExistingPlaylist(self, playlistId):
            with open(self.existingPlaylistFile, "a") as playlistFile:
                playlistFile.write(playlistId)
                
                self.existingPlaylists[playlistId] = True

        def addExistingAlbum(self, albumId):
            with open(self.existingAlbumFile, "a") as albumFile:
                albumFile.write(albumId)

            self.existingAlbums[albumId] = True

        def doesPlaylistExist(self, playlistId):
            return playlistId in self.existingPlaylists

        def doesAlbumExist(self, albumId):
            return albumId in self.existingAlbums

        def doesTrackExist(self, trackId):
            return trackId in self.existingTracks