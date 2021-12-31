times = [("year", 365 * 24 * 60 * 60), 
         ("day", 24 * 60 * 60),
         ("hour", 60 * 60),
         ("minute", 60),
         ("second", 1)]

def format_duration(seconds):

    if not seconds:
        return "now"

    chunks = []
    for name, secs in times:
        qty = seconds // secs
        if qty:
            if qty > 1:
                name += "s"
            chunks.append(str(qty) + " " + name)

        seconds = seconds % secs

    return ', '.join(chunks[:-1]) + ' and ' + chunks[-1] if len(chunks) > 1 else chunks[0]
  
___________________________________________________
def format_duration(seconds):
    if seconds == 0: return "now"
    units = ( (31536000, "year"  ), 
              (   86400, "day"   ),
              (    3600, "hour"  ),
              (      60, "minute"),
              (       1, "second") )
    ts, t = [], seconds
    for unit in units:
        u, t = divmod(t, unit[0])
        ts += ["{} {}{}".format(u, unit[1], "s" if u>1 else "")] if u != 0 else []
    return ", ".join([str(d)for d in ts[:-1]]) + (" and " if len(ts)>1 else "") + ts[-1]
  
___________________________________________________
def format_duration(total_sec):
    years = int(total_sec / 31536000)
    days = int(total_sec / 86400 % 365)
    hours = int(total_sec / 3600 % 24)
    minutes = int(total_sec / 60 % 60)
    seconds = int(total_sec % 60)
    date = ''
    if years >= 1:
        if years == 1:
            date += str(years) + ' year'
        else:
            date += str(years) + ' years'
    if days >= 1:
        if days == 1:
            if date == '':
                date += str(days) + ' day'
            elif hours == minutes == seconds ==0:
                date +=' and ' + str(days) + ' day'
            else:
                date +=', ' + str(days) + ' day'
        else:
            if date == '':
                date += str(days) + ' days'
            elif hours == minutes == seconds ==0:
                date +=' and ' + str(days) + ' days'
            else:
                date +=', ' + str(days) + ' days'
    if hours >= 1:
        if hours == 1:
            if date == '':
                date += str(hours) + ' hour'
            elif minutes == seconds ==0:
                date +=' and ' + str(hours) + ' hour'
            else:
                date +=', ' + str(hours) + ' hour'
        else:
            if date == '':
                date += str(hours) + ' hours'
            elif minutes == seconds ==0:
                date +=' and ' + str(hours) + ' hours'
            else:
                date +=', ' + str(hours) + ' hours'
    if minutes >= 1:
        if minutes == 1:
            if date == '':
                date += str(minutes) + ' minute'
            elif seconds ==0:
                date +=' and ' + str(minutes) + ' minute'
            else:
                date +=', ' + str(minutes) + ' minute'
        else:
            if date == '':
                date += str(minutes) + ' minutes'
            elif seconds ==0:
                date +=' and ' + str(minutes) + ' minutes'
            else:
                date += ', ' + str(minutes) + ' minutes'
    if seconds >= 1:
        if seconds == 1:
            if date == '':
                date += str(seconds) + ' second'
            else:
                date += ' and ' + str(seconds) + ' second'
        else:
            if date == '':
                date += str(seconds) + ' seconds'
            else:
                date += ' and ' + str(seconds) + ' seconds'
    if date == '':
        return ('now')
    else:
        return(date)
      
___________________________________________________
def format_duration(seconds):
    if seconds == 0:
        return 'now'
    years,rest = divmod(seconds, 3600*24*365)
    days, rest = divmod(rest, 3600*24)
    hours, rest = divmod(rest, 3600)
    minutes, seconds = divmod(rest, 60)
    final_arr = []
    if seconds > 0: 
        final_arr.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    if minutes > 0:
        minutes_string = final_arr.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if hours > 0:    
        final_arr.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if days > 0:
        final_arr.append(f"{days} day{'s' if days > 1 else ''}")
    if years > 0:
        final_arr.append(f"{years} year{'s' if years > 1 else ''}")
    if len(final_arr) == 1:
        return final_arr[0]
    elif len(final_arr) == 2:
        final_arr.reverse()
        return " and ".join(final_arr)
    elif len(final_arr) == 3:
        return f"{final_arr[2]}, {final_arr[1]} and {final_arr[0]}"
    elif len(final_arr) == 4:
        return f"{final_arr[3]}, {final_arr[2]}, {final_arr[1]} and {final_arr[0]}"
    else:
        return f"{final_arr[4]}, {final_arr[3]}, {final_arr[2]}, {final_arr[1]} and {final_arr[0]}"
        
___________________________________________________
def format_duration(seconds):
    if seconds == 0:
        return "now"
    
    divisors = [31_536_000, 86_400, 3600, 60, 1]
    unit_names = ['year', 'day', 'hour', 'minute', 'second']
    unit_quants = []
    
    for i in range(5):
        quant = seconds // divisors[i]
        seconds = seconds % divisors[i]
        if quant == 1:
            unit_quants.append(f'1 {unit_names[i]}')
        elif quant:
            unit_quants.append(f'{quant} {unit_names[i]}s')
        
    return (", ".join(unit_quants[:-1]) +
            (" and " if len(unit_quants) > 1 else "") + unit_quants[-1])
    
___________________________________________________
def format_duration(seconds):
    words = ["year", "day", "hour", "minute", "second"]
    if seconds == 0:
        return "now"
    else:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)
        human = [y, d, h, m, s]
        duration = []
        for x, i in enumerate(human):
            if i == 1:
                duration.append(f"{i} {words[x]}")
            elif i > 1:
                duration.append(f"{i} {words[x]}s")

        if len(duration) == 1:
            return duration[0]
        elif len(duration) == 2:
            return f"{duration[0]} and {duration[1]}"
        else:
            return ", ".join(duration[:-1]) + " and " + duration[-1]
