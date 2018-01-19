# SongsViewWidget.py

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import subprocess, mutagen, os

from _prefs import cmus_remote_cmd, songs_tab_show_full_name, songs_tab_cover_size, songs_tab_sort_by

class SongsViewWidget(QScrollArea):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.setWidget(QWidget())
        self.setWidgetResizable(True)
        
        self.widget().setLayout(QVBoxLayout())
        self.widget().layout().setContentsMargins(0,0,0,0)
        self.widget().layout().setSpacing(0)
        
        self.items = []
        for a in parent.library.albums:
            try:
                pix = QPixmap()
                pix.loadFromData(a.art.data, a.art.mime)
            except:
                pass
            
            for s in a.songs:
                if songs_tab_show_full_name:
                    text = s.fname
                else:
                    text = os.path.basename(s.fname)
                
                btn = QPushButton(text)
                btn.setToolTip(s.fname)
                btn.setFlat(True)
                btn.clicked.connect(self.itemClicked(s.fname, s.title, a.album, a.artist))
                
                if songs_tab_cover_size > 0:
                    try:
                        btn.setIcon(QIcon(pix.scaled(songs_tab_cover_size, songs_tab_cover_size)))
                        btn.setIconSize(QSize(songs_tab_cover_size, songs_tab_cover_size))
                    except:
                        pass
                
                btn.setFixedSize(btn.sizeHint())
                btn.setFocusPolicy(Qt.NoFocus)
                btn.setContextMenuPolicy(Qt.CustomContextMenu)
                btn.customContextMenuRequested.connect(self.contextMenu(btn))
                
                self.items.append( {'widget':btn, 'album':a.album, 'title':s.title, 'artist':a.artist, 'fname':os.path.basename(s.fname)} )
        
        if songs_tab_sort_by == "album":
            self.items.sort(key=lambda i : i['album'])
        elif songs_tab_sort_by == "artist":
            self.items.sort(key=lambda i : i['artist'])
        elif songs_tab_sort_by == "title":
            self.items.sort(key=lambda i : i['title'])
        elif songs_tab_sort_by == "filename":
            self.items.sort(key=lambda i : i['fname'])
        
        for i in self.items:
            self.widget().layout().addWidget(i['widget'])
        
    
    def itemClicked(self, fname, song, album, artist):
        def callback(self):
            subprocess.run([cmus_remote_cmd, '-C', 'view 1', 'filter', '/{} {} {}'.format(song, artist, album), 'win-activate'])
            
        return callback
    
    def contextMenu(self, btn):
        def callback(self):
            m = QMenu()
            play = m.addAction("Play")
            add_to_queue = m.addAction("Add to play queue")
            
            res = m.exec_(QCursor.pos())
            if res == play:
                subprocess.run([cmus_remote_cmd, '-C', 'player-play {}'.format(btn.toolTip())])
            elif res == add_to_queue:
                subprocess.run([cmus_remote_cmd, '-q', btn.toolTip()])
        
        return callback

