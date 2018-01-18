# _statusbar_funcs.py
# choose one of these for _prefs.statusbar_message

# Status bar message format
def statusbar_message_func_1(cmus):
    try:
        if cmus.vol_right != cmus.vol_left:
            volume = '{},{}'.format(cmus.vol_left, cmus.vol_right)
        else:
            volume = cmus.vol_left
        
        if cmus.repeat == 'false':
            repeat = 'false'
        elif cmus.repeat_current == 'true':
            repeat = 'current'
        else:
            repeat = 'true'
        
        msg = 'Status: {} | Repeat: {} | Shuffle: {} | Volume: {} | Continue: {} | Playing: {}'.format(
                cmus.status, repeat, cmus.shuffle, volume, cmus.continue_, cmus.aaa_mode)
    except:
        msg = ''
    
    return msg


def statusbar_message_func_2(cmus):
    try:
        if cmus.vol_right != cmus.vol_left:
            volume = '{},{}'.format(cmus.vol_left, cmus.vol_right)
        else:
            volume = cmus.vol_left
        
        if cmus.repeat_current == 'true':
            left = 'repeat current'
        else:
            left = '{} from {}library'.format(cmus.aaa_mode, 'sorted ' if cmus.play_sorted == 'true' else '')
        
        right = ''
        right += 'C' if cmus.continue_ == 'true' else ' '
        #right += 'F' if cmus.follow == 'true' else ' '
        right += 'R' if cmus.repeat == 'true' else ' '
        right += 'S' if cmus.shuffle == 'true' else ' '
        
        msg = '{} | {} | vol: {}'.format(left, right, volume)
    except:
        msg = ''
    
    return msg
