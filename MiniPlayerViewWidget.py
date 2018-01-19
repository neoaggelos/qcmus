# MiniPlayerViewWidget.py

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys, subprocess, time, threading, datetime, os, mutagen

from _prefs import miniplayer_coversize, cmus_remote_cmd, player_coversize

coversize = miniplayer_coversize

class MiniPlayerViewWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        
        # layout
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,20,0)
        self.layout().setSpacing(20)
        self.layout().setAlignment(Qt.AlignLeft)
        
        # album art
        self.albumart_label = QLabel()
        self.albumart_label.setAlignment(Qt.AlignCenter)
        self.albumart_label.setFixedSize(QSize(coversize, coversize))
        self.albumart_label.setStyleSheet('QLabel { border: 2px solid black; }')
        
        self.layout().addWidget(self.albumart_label)
        self.layout().setAlignment(self.albumart_label, Qt.AlignLeft)
        
        # song info
        #self.layout().addStretch(-1)

        songinfo_layout = QVBoxLayout()
        songinfo_layout.setSpacing(1)
        self.layout().addLayout(songinfo_layout)
        self.layout().setAlignment(songinfo_layout, Qt.AlignLeft)
        
        def create_label(text, bold, scale):
            if bold:
                text = '<b>{}</b>'.format(text)
            
            label = QLabel(text)
            font = label.font()
            font.setPointSize(font.pointSize() * scale)
            label.setFont(font)
            
            songinfo_layout.addWidget(label)
            #self.layout().setAlignment(label, Qt.AlignLeft)
            
            return label
        
        self.title_label = create_label('', True, 1.4)
        self.artist_label = create_label('', False, 1.0)
        
        # buttons
        self.layout().addStretch(1)
        buttons_layout = QHBoxLayout()
        self.layout().addLayout(buttons_layout)
        self.layout().setAlignment(buttons_layout, Qt.AlignRight)
        
        def create_button(icon, scale, callback):
            icon = QIcon.fromTheme(icon)
            
            button = QPushButton(icon, '')
            button.setFixedSize(button.sizeHint() * scale)
            button.clicked.connect(callback)
            
            buttons_layout.addWidget(button)
            return button
        
        self.prev_button = create_button('media-skip-backward', 1.0, self.prevButtonPressed)
        self.play_button = create_button(self.playButtonIcon(), 1.3, self.playButtonPressed)
        self.next_button = create_button('media-skip-forward',  1.0, self.nextButtonPressed)
        
        self.refresh(True)
        
    def refresh(self, force=False):
        self.play_button.setIcon(QIcon.fromTheme(self.playButtonIcon()))
        
        if self.parent.cmus.has_changed or force:
            self.title_label.setText(self.parent.cmus.title)
            self.artist_label.setText(self.parent.cmus.artist)
                        
            if self.parent.cmus.albumart != []:
                pix = QPixmap()
                pix.loadFromData(self.parent.cmus.albumart.data, self.parent.cmus.albumart.mime)
                self.albumart_label.setPixmap(pix.scaled(coversize, coversize))
            else:
                self.albumart_label.clear()
    
    def playButtonIcon(self):
        name = 'media-playback-start'
        if self.parent.cmus.status == 'playing':
            name = 'media-playback-pause'
        
        return name
    
    def playButtonPressed(self):
        subprocess.call([cmus_remote_cmd, "-u"])
        #self.refresh()
    
    def nextButtonPressed(self):
        subprocess.call([cmus_remote_cmd, "-n"])
        #self.refresh()
    
    def prevButtonPressed(self):
        subprocess.call([cmus_remote_cmd, "-r"])
        #self.refresh()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.centralWidget().setCurrentWidget(self.parent.nowplaying_tab)
        
        event.accept()
