# Library.py

import mutagen, os

from _prefs import cmus_lib_path, default_albums_sort

def read_tag(tags, one, default, raw = False):
    try:
        if raw:
            ret = tags[one]
        else:
            ret = tags[one].text[0]
    except:
        ret = default
    
    return ret

class Album():
    def __init__(self, album, artist, art):
        # album info
        self.album = album
        self.artist = artist
        self.art = art # art.data and art.mime from mutagen
        self.genre = ''
        
        # song list
        self.songs = [] # list of Song() objects

class Song():
    def __init__(self, title, track, fname):
        self.fname = fname
        self.title = title
        self.track = track
    
    def __repr__(self):
        return '{} {} {}'.format(self.fname, self.title, self.track)

class Library():
    def __init__(self):
        fp = open(os.path.expandvars(cmus_lib_path), 'r')
        
        self.albums = []
        
        for _, line in enumerate(fp):
            line = line[:-1]    # strip newline
            
            try:
                tags = mutagen.File(line).tags
                
                album = read_tag(tags, 'TALB', 'Unknown Album')
                artist = read_tag(tags, 'TPE1', 'Unknown Artist')
                title = read_tag(tags, 'TIT2', os.path.basename(line))
                track = read_tag(tags, 'TRCK', '0')
                art = read_tag(tags, 'APIC:', [], raw=True)
                
                found = False
                for a in self.albums:
                    if a.album == album:
                        found=True
                        a.songs.append(Song(title, track, line))
                
                if not found:
                    a = Album(album, artist, art)
                    a.songs.append(Song(title, track, line))
                    self.albums.append(a)
                
            except:
                pass
    
