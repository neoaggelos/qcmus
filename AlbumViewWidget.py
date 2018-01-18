# AlbumViewWidget.py
# note:
#   if your band is called '__all__', then AlbumViewWidget not working is the least of your problems :) 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys, subprocess, time, threading, datetime, os, mutagen

from AlbumWidget import AlbumWidget

from _prefs import album_size, spacing, column_width, cmus_remote_cmd, default_albums_sort

class Album():
    def __init__(self, artist, album, widget):
        self.artist = artist
        self.album = album
        self.widget = widget

class AlbumViewWidget(QScrollArea):
        
    def __init__(self, parent, artist='__all__'):
        super().__init__()
        
        self.parent = parent
        
        self.columns = self.width()//column_width
        self.addAlbums(parent.cmus.files, artist)
        
    def addAlbums(self, files, from_artist):
        
        self.setWidget(QWidget())
        self.setWidgetResizable(True)
        
        self.widget().setLayout(QGridLayout())
        self.widget().layout().setSpacing(spacing)
        self.widget().layout().setAlignment(Qt.AlignCenter)
        
        self.albums = []
        albums_list = []
        for f in files:
            art = []
            try:
                mut = mutagen.File(f)
                album = mut.tags["TALB"].text[0]
                artist = mut.tags["TPE1"].text[0]
                try:
                    art = mut.tags["APIC:"]
                except:
                    art = []
            except:
                continue # do not add unknown crap
            
            if (not album in albums_list) and (from_artist == '__all__' or from_artist == artist):
                albums_list.append(album)
                
                w = AlbumWidget(artist, album, art)
                self.albums.append(Album(artist, album, w))
        
        if default_albums_sort == "artist":
            self.albums.sort(key=lambda album: album.artist)
        else:
            self.albums.sort(key=lambda album: album.album)
        
    def resizeEvent(self, event):
        self.refresh()
        event.accept()
    
    def contextMenuEvent(self, event):
        a = QMenu()
        by_name = a.addAction("Sort by album name")
        by_artist = a.addAction("Sort by artist name")
        res = a.exec_(self.mapToGlobal(event.pos()))
        
        if res == by_name:
            self.albums.sort(key=lambda album: album.album)
        elif res == by_artist:
            self.albums.sort(key=lambda album: album.artist)
        
        self.refresh()
    
    def refresh(self):
        self.columns = self.width()//column_width
        
        count = 0
        for a in self.albums:
            self.widget().layout().addWidget(a.widget, count//self.columns, count%self.columns)
            count = count + 1
        
    
    def makeButtonCallback(self, artist, album):
        def actualCallback(self):
            print("Playing: ", artist, album)
            subprocess.run([cmus_remote_cmd, '-C', 'view 1', 'filter', 'player-stop', '/{} {}'.format(artist, album), 'set play_sorted=false', 'set aaa_mode=album', 'win-activate'])
        
        return actualCallback
    
