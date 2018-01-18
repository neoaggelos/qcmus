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
        
        self.widgets = []
        for f in parent.cmus.files:
            data = mutagen.File(f).tags
            
            isFile = True
            try:
                song = data['TIT2'].text[0]
                album = data['TALB'].text[0]
                artist = data['TPE1'].text[0]
                
                try:
                    art = data['APIC:']
                except:
                    art = []
                
                isFile = False
            except:
                pass
            
            if songs_tab_show_full_name:
                text = f
            else:
                text = os.path.basename(f)
            
            btn = QPushButton(text)
            btn.setToolTip(f)
            '''
            if art != []:
                pix = QPixmap()
                pix.loadFromData(art.data, art.mime)
                btn.setIcon(QIcon(pix.scaled(80, 80)))
                btn.setIconSize(QSize(80, 80))
            '''
            btn.setFixedSize(btn.sizeHint())
            #btn.setStyleSheet('QPushButton { text-align:center }')
            btn.setFlat(True)
            btn.clicked.connect(self.itemClicked(isFile, f, song, album, artist))
            
            self.widgets.append(btn)
            
            self.widget().layout().addWidget(btn)
            #self.widget().layout().setAlignment(btn, Qt.AlignCenter)
    
    def itemClicked(self, isfile, f, song, album, artist):
        def callback(self):
            if not isfile:
                subprocess.run([cmus_remote_cmd, '-C', 'view 1', 'filter', '/{} {} {}'.format(song, artist, album), 'win-activate'])
            else:
                subprocess.run([cmus_remote_cmd, '-C', 'player-play {}'.format(f)])

        return callback
    
    def resizeEvent(self, event):
        self.widget().resize(event.size().width(), self.widget().height())
