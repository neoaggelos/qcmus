# _prefs.py

from _statusbar_message_funcs import *
from PyQt5.QtCore import QSize

#########################################################################
### cmus settings
#########################################################################

# cmus-remote executable
cmus_remote_cmd = 'cmus-remote'


# cmus executable
cmus_cmd = 'cmus'


# path to cmus library (lib.pl) -- can contain environment variables
cmus_lib_path = '$HOME/.config/cmus/lib.pl'


# auto start cmus if needed
cmus_autostart_if_dead = True


# command to start cmus on terminal
cmus_autostart_cmd = ['gnome-terminal', '--', cmus_cmd]
#cmus_autostart_terminal_cmd = ['exo-open', '--launch', 'TerminalEmulator', cmus_cmd]


#########################################################################
### player settings
#########################################################################

# Keep only the first N characters for huge song names (-1 to keep the whole string)
songinfo_length_max = -1


# Album art size on player tab
player_coversize = 400


# Album art size on mini player
miniplayer_coversize = 50


#########################################################################
### qcmus settings
#########################################################################

# qcmus playlist name (used for playing other playlists)
qcmus_playlist_name = '_qcmus_playlist_'


# listen to default cmus keyboard shortcuts
cmus_shortcuts_enabled = True


#########################################################################
### albums tab settings
#########################################################################

# Album sort method
default_albums_sort = "album"
#default_albums_sort = "artist"


# Size of album image in albums tab
album_size = 150


# Spacing of albums in albums tab
spacing = 20


# Do not touch, calculate column width for albums tab
column_width = album_size  + 2.3*spacing


#########################################################################
### songs tab settings
#########################################################################

# Display full file name in songs tab
songs_tab_show_full_name = False


# Album art size for each file (0 == don't show album art)
songs_tab_cover_size = 0


# Sort method
#songs_tab_sort_by = "album"
songs_tab_sort_by = "artist"
#songs_tab_sort_by = "filename"
#songs_tab_sort_by = "title"


#########################################################################
### gui settings
#########################################################################

# Available window sizes (may add up to 9)
window_sizes = {
    '1' : QSize(player_coversize + spacing, player_coversize + 280),
    '2' : QSize(player_coversize * 2, player_coversize + 280),
    '3' : QSize(player_coversize * 2.5, player_coversize + 400),
    # '4' : QSize( custom_width, custom_height)
}

# Resizable window (if True, long song titles may resize the window)
allow_resize = True


# Status bar always on
statusbar_always_on = True


# See _statusbar_message_funcs.py
statusbar_message = statusbar_message_func_2


# Font size for status bar message
statusbar_font_size = 9


# Font used in status bar
statusbar_font = 'monospace'
#statusbar_font = 'Ubuntu Mono'


