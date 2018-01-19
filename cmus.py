import subprocess, mutagen, os

## TODO
## faster way to get info

from _prefs import cmus_remote_cmd, cmus_autostart_if_dead, cmus_cmd, cmus_autostart_cmd, cmus_lib_path, songinfo_length_max

class cmus:
    
    def __init__(self):
        #super.__init__()
        
        # "cmus-remote -Q" output
        self.data = ''
        
        # does GUI need to refresh
        self.has_changed = True
        
        # cmus state
        self.status = ''
        self.vol = 0
        self.vol_right = ''
        self.vol_left = ''
        self.repeat = ''
        self.repeat_current = ''
        self.shuffle = ''
        self.continue_ = ''
        self.aaa_mode = ''
        self.play_sorted = ''
        self.follow = ''
        
        # now playing
        self.fname = ''
        self.title = ''
        self.album = ''
        self.tracknumber = ''
        self.duration = ''
        self.position = ''
        self.artist = ''
        self.albumart = []
        
        # did we start cmus?
        self.is_owner = False
        
        self.refresh()
        
    def refresh(self):
        self.data = subprocess.run([cmus_remote_cmd, "-Q"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        
        if len(self.data) < 3:
            self.status = 'dead'
            
            global cmus_autostart_if_dead
            if cmus_autostart_if_dead:
                subprocess.run(cmus_autostart_cmd)
                self.is_owner = True
        
        elif self.data.startswith('status playing'):
            self.status = 'playing'
        else:
            self.status = 'stopped'
        
        self.duration = self.recoverField('duration', '0')
        self.position = self.recoverField('position', '0')
        
        self.repeat = self.recoverField('set repeat', '')
        self.shuffle = self.recoverField('set shuffle', '')
        self.repeat_current = self.recoverField('set repeat_current', '')
        self.continue_ = self.recoverField('set continue', '')
        self.aaa_mode = self.recoverField('set aaa_mode', '')
        self.play_sorted = self.recoverField('set play_sorted', '')
        
        self.vol_right = self.recoverField('set vol_right', '0')
        self.vol_left = self.recoverField('set vol_left', '0')
        self.vol = max(int(self.vol_right), int(self.vol_left))
        
        newfile = self.recoverField('file', '')
        self.has_changed = newfile == '' or self.fname == '' or newfile != self.fname

        if self.has_changed:
            self.fname = newfile
            self.title = self.recoverField('tag title', '-')
            self.album = self.recoverField('tag album', '-')
            self.artist = self.recoverField('tag artist', '-')
            self.tracknumber = self.recoverField('tag tracknumber', '0')
            
            if songinfo_length_max > 0:
                if len(self.title) > songinfo_length_max:
                    self.title = self.title[:songinfo_length_max]
                if len(self.artist) > songinfo_length_max:
                    self.artist = self.artist[:songinfo_length_max]
                if len(self.album) > songinfo_length_max:
                    self.album = self.album[:songinfo_length_max]
            
            try:
                mfile = mutagen.File(self.fname)
                self.albumart = mfile.tags["APIC:"]
            except:
                self.albumart = []

    def recoverField(self, field, default):
        begin = self.data.find('\n{}'.format(field))
        length = self.data[begin+1:].find('\n')
        
        if begin != -1:
            return self.data[begin+len(field)+2:begin+length+1]
        else:
            return default
    
