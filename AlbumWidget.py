# AlbumWidget.py

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import subprocess

from _prefs import album_size, spacing, cmus_remote_cmd

class AlbumWidget(QWidget):
    def __init__(self, artist, album, art):
        super().__init__()
        
        self.setMaximumWidth(album_size+spacing)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(2)
        
        self.artist = artist
        self.album = album
        
        btn = QPushButton()
        if art == []:
            btn.setText(artist + '\n' + album)
        else:
            pix = QPixmap()
            pix.loadFromData(art.data, art.mime)
            
            btn.setIcon(QIcon(pix.scaled(album_size, album_size)))
            btn.setIconSize(QSize(album_size, album_size))
            btn.setToolTip(artist + ' - ' + album)
        
        btn.setFixedSize(QSize(album_size+spacing, album_size+spacing))
        btn.clicked.connect(self.makeButtonCallback(artist, album))
        self.layout().addWidget(btn)
        
        def add_label(text, bold=True, scale=1):
            if bold:
                text = '<b>{}</b>'.format(text)
                
            label = QLabel(text)
            
            #label.setWordWrap(True)
            label.setAlignment(Qt.AlignCenter)
            
            self.layout().addWidget(label)
            self.layout().setAlignment(label, Qt.AlignCenter)
            
            font = label.font()
            font.setPointSize(font.pointSize() * scale)
            label.setFont(font)
        
        add_label(album)
        add_label(artist, bold=False, scale=0.8)
        
        self.resize(self.sizeHint())
        
    #TODO no artist / album name?
    def makeButtonCallback(self, artist, album):
        def callback(self):
            subprocess.run([cmus_remote_cmd, '-C', 'view 2', 'player-stop', 'filter artist="{}" & album="{}"'.format(artist, album), 'set play_sorted=false', 'set aaa_mode=album', 'win-activate'])
        
        return callback
        
