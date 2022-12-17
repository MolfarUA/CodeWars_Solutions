57873ab5e55533a2890000c7


timeCorrect = (timestring) ->
  return timestring if !timestring || timestring == ""
  return null if !/^\d\d:\d\d:\d\d$/.test(timestring)
  [h, m, s] = timestring.split(":").map((x) -> +x)
  m += Math.floor(s / 60)
  h += Math.floor(m / 60)
  [h % 24, m % 60, s % 60].map((x) -> (""+x).padStart(2, '0')).join(":")
_________________________________
timeCorrect = (timestring) ->
  if ((timestring == null) ||(timestring == ""))
    return timestring;  
  
  parts = timestring.split(':');
  if(parts.length != 3)
    return null;  
  
  if(parts.some((i) -> parseInt(i) == NaN || padLeft(parseInt(i).toString(), 2) != i))  
    return null;  
  
  hour = parseInt(parts[0]);
  minute = parseInt(parts[1]);
  second = parseInt(parts[2]);
  
  minute += Math.floor(second / 60);
  second = second % 60;      

  hour += Math.floor(minute / 60);
  minute = minute % 60;
    
  hour = hour % 24; 
  
  return padLeft(hour.toString(), 2) + ":" + padLeft(minute.toString(), 2) + ":" + padLeft(second.toString(), 2);

padLeft = (nr, n) ->
    return Array(n-String(nr).length+1).join('0')+nr;    
_________________________________
timeCorrect = (timestring) ->
  if ((timestring == null) ||(timestring == ""))
    return timestring;  
  
  parts = timestring.split(':');
  if(parts.length != 3)
    return null;  
  
  if(parts.some((i) -> parseInt(i) == NaN || padLeft(parseInt(i).toString(), 2) != i))  
    return null;  
  
  hour = parseInt(parts[0]);
  minute = parseInt(parts[1]);
  second = parseInt(parts[2]);
  
  minute += Math.floor(second / 60);
  second = second % 60;      

  hour += Math.floor(minute / 60);
  minute = minute % 60;
    
  hour = hour % 24; 
  
  return padLeft(hour.toString(), 2) + ":" + padLeft(minute.toString(), 2) + ":" + padLeft(second.toString(), 2);

padLeft = (nr, n) ->
    return Array(n-String(nr).length+1).join('0')+nr;    
