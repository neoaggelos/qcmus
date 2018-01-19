# PlayerView.py

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import subprocess, datetime

from _prefs import player_coversize, cmus_remote_cmd

from _Slider import _Slider
coversize = player_coversize

class PlayerViewWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        
        # layout
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        
        # album art
        self.layout().addStretch(-1)
        self.albumart_label = QLabel()
        self.albumart_label.setAlignment(Qt.AlignCenter)
        self.albumart_label.setFixedSize(QSize(coversize, coversize))
        self.albumart_label.setStyleSheet('QLabel { border: 2px solid black; }')
        
        self.layout().addWidget(self.albumart_label)
        self.layout().setAlignment(self.albumart_label, Qt.AlignCenter)
        self.layout().addStretch(1)
        
        def create_label(text, scale, layout=self.layout(), align=Qt.AlignCenter):
            label = QLabel(text)
            font = label.font()
            font.setPointSize(font.pointSize() * scale)
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            
            layout.addWidget(label)
            layout.setAlignment(label, align)
            
            return label
        
        # song info
        self.title_label = create_label('', 1.8)
        self.artist_label = create_label('', 1.5)
        self.album_label = create_label('', 1)
        
        # time slider
        self.time_slider = _Slider(Qt.Horizontal)
        self.time_slider.valueChanged.connect(self.seekTo)
        self.layout().addWidget(self.time_slider)
        
        # current and total time
        time_layout = QHBoxLayout()
        self.position_label = create_label('', 0.8, time_layout, Qt.AlignLeft)
        self.duration_label = create_label('', 0.8, time_layout, Qt.AlignRight)
        time_layout.setContentsMargins(10, 0, 10, 0)
        self.layout().addLayout(time_layout)
        
        # play/pause, next, previous buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        self.layout().addLayout(buttons_layout)
        self.layout().setAlignment(buttons_layout, Qt.AlignCenter)
        
        def create_button(iconName, scale, callback):
            icon = QIcon.fromTheme(iconName)
            
            button = QPushButton(icon, '')
            button.setFixedSize(button.sizeHint() * scale)
            button.clicked.connect(callback)
            
            buttons_layout.addWidget(button)
            
            return button
        
        self.prev_button = create_button('media-skip-backward', 1.2, self.prevButtonPressed)
        self.play_button = create_button(self.playButtonIcon(), 1.8, self.playButtonPressed)
        self.next_button = create_button('media-skip-forward', 1.2, self.nextButtonPressed)
        
        self.refresh(force=True)
    
    
    def refresh(self, force=False):
        self.play_button.setIcon(QIcon.fromTheme(self.playButtonIcon()))
        
        # TODO: what about > 1 hour?
        position = int(self.parent.cmus.position)
        duration = int(self.parent.cmus.duration)
        self.position_label.setText(str(datetime.timedelta(seconds=position))[-5:])
        self.duration_label.setText(str(datetime.timedelta(seconds=duration))[-5:])
        
        self.time_slider.blockSignals(True)
        self.time_slider.setRange(0, duration)
        self.time_slider.setValue(position)
        self.time_slider.blockSignals(False)
        
        if self.parent.cmus.has_changed or force:
            self.artist_label.setText(self.parent.cmus.artist)
            self.album_label.setText(self.parent.cmus.album)
            self.title_label.setText(self.parent.cmus.title)
            
            if self.parent.cmus.albumart == []:
                self.albumart_label.setText('No album art')
            else:
                pix = QPixmap()
                pix.loadFromData(self.parent.cmus.albumart.data, self.parent.cmus.albumart.mime)
                self.albumart_label.setText('')
                self.albumart_label.setPixmap(pix.scaled(coversize, coversize))
    
    def playButtonIcon(self):
        name = 'media-playback-start'
        if self.parent.cmus.status == 'playing':
            name = 'media-playback-pause'
        
        return name
    
    def playButtonPressed(self):
        subprocess.call([cmus_remote_cmd, "-u"])
    
    def nextButtonPressed(self):
        subprocess.call([cmus_remote_cmd, "-n"])
    
    def prevButtonPressed(self):
        subprocess.call([cmus_remote_cmd, "-r"])
        
    def seekTo(self):
        subprocess.call([cmus_remote_cmd, "-C", "seek {}".format(self.time_slider.value())])
