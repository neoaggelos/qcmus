# SongsViewWidget.py

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import subprocess, mutagen, os

from _prefs import cmus_remote_cmd, songs_tab_show_full_name

class SongsViewWidget(QScrollArea):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.setWidget(QWidget())
        self.setWidgetResizable(True)
        
        self.widget().setLayout(QVBoxLayout())
        self.widget().layout().setContentsMargins(0,0,0,0)
        self.widget().layout().setSpacing(0)
        
        for a in parent.library.albums:
            for s in a.songs:
                if songs_tab_show_full_name:
                    text = s.fname
                else:
                    text = os.path.basename(s.fname)
                
                btn = QPushButton(text)
                btn.setToolTip(s.fname)
                btn.setFixedSize(btn.sizeHint())
                btn.setFlat(True)
                btn.clicked.connect(self.itemClicked(s.fname, s.title, a.album, a.artist))
                
                self.widget().layout().addWidget(btn)
                

    def itemClicked(self, fname, song, album, artist):
        def callback(self):
            subprocess.run([cmus_remote_cmd, '-C', 'view 1', 'filter', '/{} {} {}'.format(song, artist, album), 'win-activate'])
            
        return callback
    '''
    def resizeEvent(self, event):
        self.widget().resize(event.size().width(), self.widget().height())
    '''
