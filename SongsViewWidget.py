# SongsViewWidget.py

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import subprocess, mutagen, os

from _prefs import cmus_remote_cmd, songs_tab_show_full_name, songs_tab_cover_size, songs_tab_sort_by

class SongsViewWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.scroll = QScrollArea()
        self.scroll.setWidget(QWidget())
        self.scroll.setWidgetResizable(True)
        
        self.scroll.widget().setLayout(QVBoxLayout())
        self.scroll.widget().layout().setContentsMargins(0,0,0,0)
        self.scroll.widget().layout().setSpacing(0)
        self.scroll.widget().layout().setAlignment(Qt.AlignTop)
        
        self.search_layout = QHBoxLayout()
        self.search_layout.setContentsMargins(0,0,0,0)
        search_icon = QLabel()
        search_icon.setPixmap(QIcon.fromTheme('system-search').pixmap(40, 40))
        self.search_layout.addWidget(search_icon)
        self.search_layout.setAlignment(search_icon, Qt.AlignTop)
        self.searchbox = QLineEdit()
        self.searchbox.setPlaceholderText('Search')
        self.searchbox.textChanged.connect(self.searchAction)
        self.search_layout.addWidget(self.searchbox)
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().addLayout(self.search_layout)
        self.layout().addWidget(self.scroll)
        
        self.widgets = []
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
                
                w = QPushButton(text)
                w.setToolTip(s.fname)
                w.setFlat(True)
                w.clicked.connect(self.itemClicked(s.fname, s.title, a.album, a.artist))
                
                if songs_tab_cover_size > 0:
                    try:
                        w.setIcon(QIcon(pix))
                        w.setIconSize(QSize(songs_tab_cover_size, songs_tab_cover_size))
                    except:
                        pass
                
                w.setFixedSize(w.sizeHint())
                w.setFocusPolicy(Qt.NoFocus)
                w.setContextMenuPolicy(Qt.CustomContextMenu)
                w.customContextMenuRequested.connect(self.contextMenu(w))
                
                w.setProperty('artist', a.artist)
                w.setProperty('album', a.album)
                w.setProperty('title', s.title)
                self.widgets.append( w )
        
        if songs_tab_sort_by == "album":
            self.widgets.sort(key=lambda w : w.property('album'))
        elif songs_tab_sort_by == "artist":
            self.widgets.sort(key=lambda w : w.property('artist'))
        elif songs_tab_sort_by == "title":
            self.widgets.sort(key=lambda w : w.property('title'))
        elif songs_tab_sort_by == "filename":
            self.widgets.sort(key=lambda w : w.toolTip())
        
        for w in self.widgets:
            self.scroll.widget().layout().addWidget(w)
    
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
    
    def searchAction(self):
        needles = self.searchbox.text().lower().split()
        
        for w in self.widgets:
            haystack = '{}{}{}{}'.format(w.toolTip(), w.property('artist'), w.property('album'), w.property('title')).lower()
            hide = False
            for n in needles:
                if not n in haystack:
                    hide = True
            
            w.hide() if hide else w.show()
