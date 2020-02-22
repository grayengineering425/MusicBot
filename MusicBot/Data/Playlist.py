import os

class Playlist():
    def __init__(self, existingTracks):
        self.existingTracks         = existingTracks
        self.existingAlbumFile      = os.getcwd() + "/Data/albums.txt"
        self.existingPlaylistFile   = os.getcwd() + "/Data/playlists.txt"

        self.existingAlbums     = {}
        self.existingPlaylists  = {}

        self.getExistingAlbums   ()
        self.getExistingPlaylists()

    def getExistingAlbums(self):
        with open(self.existingAlbumFile, "r") as albumFile:
            for line in albumFile:
                self.existingAlbums[line.rstrip()] = True
    
    def getExistingPlaylists(self):
        with open(self.existingPlaylistFile, "r") as playlistFile:
            for line in playlistFile:
                self.existingPlaylists[line.rstrip()] = True
    
    def addExistingPlaylist(self, playlistId):
        with open(self.existingPlaylistFile, "a") as playlistFile:
            playlistFile.write(playlistId + "\n")
            
            self.existingPlaylists[playlistId] = True
    
    def addExistingAlbum(self, albumId):
        with open(self.existingAlbumFile, "a") as albumFile:
            albumFile.write(albumId + "\n")
    
            self.existingAlbums[albumId] = True
    
    def addExistingTrack(self, trackId):
        self.existingTracks[trackId] = True
    
    def doesPlaylistExist(self, playlistId):
        return playlistId in self.existingPlaylists
    
    def doesAlbumExist(self, albumId):
        return albumId in self.existingAlbums
    
    def doesTrackExist(self, trackId):
        return trackId in self.existingTracks

    def reset(self):
        self.existingTracks     = {}
        self.existingAlbums     = {}
        self.existingPlaylists  = {}

        open(self.existingAlbumFile,    'w').close()
        open(self.existingPlaylistFile, 'w').close()