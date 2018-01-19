#! /usr/bin/python3
import sys, threading, time, subprocess

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QSlider,
        QHBoxLayout, QVBoxLayout, QApplication, QPushButton,
        QMainWindow, QAction)
from PyQt5.QtGui import QIcon, QPixmap, QFont
'''

from cmus import cmus
from AlbumViewWidget import AlbumViewWidget
from SongsViewWidget import SongsViewWidget
from PlayerViewWidget import PlayerViewWidget
from MiniPlayerViewWidget import MiniPlayerViewWidget
from Library import Library

from _prefs import cmus_remote_cmd, statusbar_message, statusbar_always_on, statusbar_font_size, statusbar_font, window_sizes, allow_resize, cmus_shortcuts_enabled, qcmus_exit_behaviour, cmus_autostart_if_dead

class qcmus(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # init controller
        self.cmus = cmus()
        self.library = Library()

        # now playing tab
        self.nowplaying_tab = PlayerViewWidget(self)
        
        # albums tab
        self.albums_tab = QWidget()
        self.albums_tab.setLayout(QVBoxLayout())
        self.albums_tab.layout().setContentsMargins(0,0,0,0)
        self.albums_tab.layout().addWidget(AlbumViewWidget(self))
        self.albums_tab_miniplayer = MiniPlayerViewWidget(self)
        self.albums_tab.layout().addWidget(self.albums_tab_miniplayer)
        
        # songs tab
        self.songs_tab = QWidget()
        self.songs_tab.setLayout(QVBoxLayout())
        self.songs_tab.layout().setContentsMargins(0,0,0,0)
        self.songs_tab.layout().addWidget(SongsViewWidget(self))
        self.songs_tab_miniplayer = MiniPlayerViewWidget(self)
        self.songs_tab.layout().addWidget(self.songs_tab_miniplayer)
        
        # central widget
        self.setCentralWidget(QTabWidget())
        self.centralWidget().addTab(self.nowplaying_tab, "Now Playing")
        self.centralWidget().addTab(self.albums_tab, "Albums")
        self.centralWidget().addTab(self.songs_tab, "Songs")
        
        self.centralWidget().setStyleSheet('QTabWidget::tab-bar { alignment: left; }')
        self.setWindowTitle(self.cmus.title + ' - ' + self.cmus.artist)
        
        # status bar font
        self.statusBar().setFont(QFont(statusbar_font, statusbar_font_size))
        statusbar_always_on or self.statusBar().hide()
        
        if allow_resize:
            self.resize(window_sizes['1'].width(), window_sizes['1'].height())
        else:
            self.is_maximized = False
            self.setFixedSize(window_sizes['1'])
        
        self.setWindowIcon(QIcon.fromTheme('audio-player'))
        self.show()
        
        def add_action(name, shortcut, call):
            act = QAction(name, self)
            act.setShortcut(shortcut)
            act.triggered.connect(call)
            self.addAction(act)
            
            return act
        
        # manual window refresh with F1
        def forceRefresh():
            self.refresh(True)
        
        add_action('Refresh', 'F1', forceRefresh)
        
        # quick jump to view
        add_action('Now Playing', 'Alt+1', self.jumpTo(self.nowplaying_tab))
        add_action('Albums', 'Alt+2', self.jumpTo(self.albums_tab))
        add_action('Songs', 'Alt+3', self.jumpTo(self.songs_tab))
        
        # resize
        add_action('maximize', 'Ctrl+`', self.toggleMaximized)
        for i, size in window_sizes.items():
            add_action('resize'+i, 'Ctrl+'+i, self.resizeTo(size.width(), size.height()))
        
        # cmus shortcuts
        def cmus_command(cmd):
            def call():
                subprocess.run([cmus_remote_cmd, '-C', cmd])
            
            return call
        
        if cmus_shortcuts_enabled:
            add_action('play/pause', 'c', cmus_command('player-pause'))
            add_action('stop', 'v', cmus_command('player-stop'))
            add_action('prev', 'z', cmus_command('player-prev'))
            add_action('next', 'b', cmus_command('player-next'))
            add_action('+1m', '.', cmus_command('seek +1m'))
            add_action('-1m', ',', cmus_command('seek -1m'))
            add_action('+5s', 'Right', cmus_command('seek +5'))
            add_action('+5s', 'l', cmus_command('seek +5'))
            add_action('+5s', 'Left', cmus_command('seek -5'))
            add_action('+5s', 'h', cmus_command('seek -5'))
            add_action('+10%', '+', cmus_command('vol +10%'))
            add_action('-10%', '-', cmus_command('vol -10%'))
            add_action('-1% left', '{', cmus_command('vol -1% -0'))
            add_action('-1% right', '}', cmus_command('vol -0 -1%'))
            add_action('+1% left', '[', cmus_command('vol +1% -0'))
            add_action('+1% right', ']', cmus_command('vol -0 +1%'))
            add_action('repeat', 'r', cmus_command('toggle repeat'))
            add_action('shuffle', 's', cmus_command('toggle shuffle'))
            add_action('r-current', 'Ctrl+r', cmus_command('toggle repeat_current'))
            add_action('continue', 'Alt+c', cmus_command('toggle continue'))
            add_action('sorted', 'o', cmus_command('toggle play_sorted'))
            add_action('aaa_mode', 'm', cmus_command('toggle aaa_mode'))
        
        # auto refresh player views
        refreshThread = threading.Thread(target = self.refreshScheduler)
        refreshThread.daemon = True
        refreshThread.start()
        
        # status bar
        self.statusbar_message = ''
        
    def refreshScheduler(self):
        while True:
            self.refresh()
            
            time.sleep(0.3)
    
    def refresh(self, force=False):
        self.cmus.refresh()
        
        if self.cmus.status == 'dead':
            self.setWindowTitle('cmus is not running') 
        else:
            self.statusbar_message = statusbar_message(self.cmus)
            self.statusBar().showMessage(self.statusbar_message)
            
            if self.cmus.has_changed or force:
                self.setWindowTitle(self.cmus.title + ' - ' + self.cmus.artist)
            
        self.nowplaying_tab.refresh(force)
        self.albums_tab_miniplayer.refresh(force)
        self.songs_tab_miniplayer.refresh(force)
    
    def jumpTo(self, tab):
        def callback():
            self.centralWidget().setCurrentWidget(tab)
        
        return callback
    
    def resizeTo(self, w, h):
        def callback():
            self.showNormal()
            if allow_resize:
                self.resize(w, h)
            else:
                self.setFixedSize(w, h)
                
                # if out of bounds, return inside if possible
                rect = QDesktopWidget().availableGeometry(self)
                new_x = self.x()
                new_y = self.y()
                if self.x() + w > rect.x() + rect.width():
                    new_x = max(0,rect.x() + rect.width() - w)
                if self.y() + h > rect.y() + rect.height():
                    new_y = max(0,rect.y() + rect.height() - h)
                
                self.move(new_x, new_y)
        
        return callback
    
    def toggleMaximized(self):
        if allow_resize:
            self.showNormal() if self.isMaximized() else self.showMaximized()
            return
        
        if not self.is_maximized:
            rect = QDesktopWidget().availableGeometry(self)
            
            self.move(QPoint(rect.x(), rect.y()))
            self.setFixedSize(QSize(rect.width(), rect.height()-self.statusBar().height()))
        else:
            self.setFixedSize(window_sizes['1'])
        
        self.is_maximized = not self.is_maximized
    
    def keyPressEvent(self, event):
        global statusbar_always_on
        if event.key() == 96:
            self.statusBar().showMessage(self.statusbar_message)
            statusbar_always_on or self.statusBar().show()
            
            # pressing alt-tilde toggles the status bar persistence
            if event.modifiers() == Qt.AltModifier:
                statusbar_always_on = not statusbar_always_on
    
    def keyReleaseEvent(self, event):
        if event.key() == 96:
            statusbar_always_on or self.statusBar().hide()
    
    def closeEvent(self, event):
        if qcmus_exit_behaviour == 'kill' or (qcmus_exit_behaviour == 'kill-if-owner' and self.cmus.is_owner == True):
            subprocess.run([cmus_remote_cmd, '-C', 'quit'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qcmus = qcmus()
    sys.exit(app.exec_())
