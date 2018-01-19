# AlbumViewWidget.py
# note:
#   if your band is called '__all__', then AlbumViewWidget not working is the least of your problems :) 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys, subprocess, time, threading, datetime, os, mutagen

from AlbumWidget import AlbumWidget

from _prefs import album_size, spacing, column_width, cmus_remote_cmd, default_albums_sort

class AlbumViewWidget(QScrollArea):
        
    def __init__(self, parent, artist='__all__'):
        super().__init__()
        
        self.parent = parent
        
        self.columns = self.width()//column_width
        self.addAlbums(artist)
        
    def addAlbums(self, from_artist):
        lib = self.parent.library
        
        self.setWidget(QWidget())
        self.setWidgetResizable(True)
        
        self.widget().setLayout(QGridLayout())
        self.widget().layout().setSpacing(spacing)
        self.widget().layout().setAlignment(Qt.AlignCenter)
        
        self.widgets = []
        for a in lib.albums:
            w = AlbumWidget(a.artist, a.album, a.art)
            self.widgets.append(w)
        
        if default_albums_sort == 'album':
            self.widgets.sort(key=lambda w: w.album)
        elif default_albums_sort == 'artist':
            self.widgets.sort(key=lambda w: w.artist)
        
    def resizeEvent(self, event):
        self.refresh()
        event.accept()
    
    def contextMenuEvent(self, event):
        a = QMenu()
        by_name = a.addAction("Sort by album name")
        by_artist = a.addAction("Sort by artist name")
        res = a.exec_(self.mapToGlobal(event.pos()))
        
        if res == by_name:
            self.widgets.sort(key=lambda w: w.album)
        elif res == by_artist:
            self.widgets.sort(key=lambda w: w.artist)
        
        self.refresh()
    
    def refresh(self):
        self.columns = self.width()//column_width
        
        count = 0
        for w in self.widgets:
            self.widget().layout().addWidget(w, count//self.columns, count%self.columns)
            count = count + 1

