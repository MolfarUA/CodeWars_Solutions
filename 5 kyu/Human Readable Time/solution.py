def make_readable(s):
    return '{:02}:{:02}:{:02}'.format(s / 3600, s / 60 % 60, s % 60)
  
_____________________________________
def make_readable(seconds):
    hours, seconds = divmod(seconds, 60 ** 2)
    minutes, seconds = divmod(seconds, 60)
    return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
  
_____________________________________
def make_readable(seconds):
    h= seconds/60**2
    m= (seconds%60**2)/60
    s= (seconds%60**2%60)
    return "%02d:%02d:%02d" % (h, m, s)
  
_____________________________________
def make_readable(seconds):
    
    sec = seconds % 60
    min = seconds//60 % 60
    hrs = seconds//60//60%100
    
    return f"{str(hrs).zfill(2)}:{str(min).zfill(2)}:{str(sec).zfill(2)}" 
      
_____________________________________
def make_readable(seconds):
    hours = seconds // (60 * 60)
    minutes = (seconds - hours * 60 * 60) // 60
    seconds = seconds % 60
    
    hours = str(hours)
    minutes = str(minutes)
    seconds = str(seconds)
    
    time = "0" * (2-len(hours)) + hours + ":" + "0" * (2-len(minutes)) + minutes + ":" + "0" * (2-len(seconds)) + seconds
    
    return time
  
_____________________________________
def make_readable(seconds):
    h = seconds/60/60
    m = h %1*60
    s = m %1*60
    return f'{int(h):02}:{int(m):02}:{round(s):02}'
      
_____________________________________
def make_readable(seconds):
    
    m = seconds // 60 #Calculate minutes
    seconds %= 60 #Calculate remaining seconds
    h = m // 60 #Calculate hours
    m %= 60 #Calculate remaining minutes
    
    if h < 10:
        HH = '0' + str(h)
    else:
        HH = str(h)
        
    if m < 10:
        MM = '0' + str(m)
    else:
        MM = str(m)
        
    if seconds < 10:
        SS = '0' + str(seconds)
    else:
        SS = str(seconds)
        
    return HH + ':' + MM + ':' + SS
    
