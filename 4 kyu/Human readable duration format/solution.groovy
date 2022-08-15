52742f58faf5485cae000b9a


class Kata {
  static String formatDuration(seconds){
    if (!seconds) return 'now'
    
    List strings = []
    Date date = new GregorianCalendar(0,0,0,0,0,seconds,0).time   
    
    int days  = (int)(seconds/60/60/24)
    int years = (int)(days/365)
   
    if (years)        { strings << getString(years,'year'); days%=365 }
    if (days)         { strings << getString(days,'day')}
    if (date.hours)   { strings << getString(date.hours, 'hour')  }    
    if (date.minutes) { strings << getString(date.minutes, 'minute') }
    if (date.seconds) { strings << getString(date.seconds, 'second') }
        
    String last = strings.pop()     
    (strings.size() ? strings.join(', ')+' and ' : '')+last
  }
  
  static String getString(int value, String string) { "$value ${string+(value>1?'s':'')}" }
}

__________________________________________________
class Kata {
  static String formatDuration(sec){
    if(sec == 0){
      return "now"
    }
    def (years, days, hours, minutes, seconds) = [0, 0, 0, 0, 0]   
  def (y, d, h, m, s) = [31536000, 86400 ,3600, 60, 1]
       if(sec >= y){
      years = (sec/y).toInteger()
      sec = sec - (years * y)
    }
    if(sec >= d){
      days = (sec/d).toInteger()
      sec = sec - (days * d)
    }
    if(sec >= h){
      hours = (sec/h).toInteger()
      sec = sec - (hours * h) 
    }
    if(sec >= m){
      minutes = (sec/m).toInteger()
      sec = sec - (minutes * m)
    }
    if(sec >= s){
      seconds = (sec/s).toInteger()
      sec = sec - (seconds * s)
    }
    List<String> result = []
    if(years){
      if(years > 1){
      result << "$years years"
      }else{
        result << "$years year"
      }
    }
    if(days){
      if(days > 1){
      result << "$days days"
      }else{
        result << "$days day"
      }
    }
    if(hours){
      if(hours > 1){
      result << "$hours hours"
      }else{
        result << "$hours hour"
      }
    }
    if(minutes){
      if(minutes > 1){
      result << "$minutes minutes"
      }else{
        result << "$minutes minute"
      }
    }
     if(seconds){
      if(seconds > 1){
      result << "$seconds seconds"
      }else{
        result << "$seconds second"
      }
    }
    def r = result.size()
     if(r < 2){
      return result[0]?.replaceAll("\\[|\\]", "")
    }else if(r == 2){
        result.add(1, "and")
         return result.join(" ")
    } else if(r > 2){
        result.add(r-1, "and");
        def last = result[-1]
      def an = result[-2]
        return result[0..(r - 2)].join(", ") + " $an" + " $last"     
    }    
  }
}

__________________________________________________
class Kata {
  static String formatDuration(seconds){
    if (seconds == 0)
      return "now"
    
    def res = ""
    
    if (seconds >= 31536000) {
      def counterYears = 0
      
      while (seconds >= 31536000) {
        seconds -= 31536000
        counterYears++
      }
      
      res += counterYears
      res += counterYears > 1 ? " years" : " year"
    }
    
    if (seconds >= 86400) {
      def counterDays = 0
      
      while (seconds >= 86400) {
        seconds -= 86400
        counterDays++
      }
      
      if (res != "")
        res += seconds > 0 ? ", " : " and "
      
      res += counterDays
      res += counterDays > 1 ? " days" : " day"
    }
    
    if (seconds >= 3600) {
      def counterHours = 0
      
      while (seconds >= 3600) {
        seconds -= 3600
        counterHours++
      }
      
      if (res != "")
        res += seconds > 0 ? ", " : " and "

      res += counterHours
      res += counterHours > 1 ? " hours" : " hour"
    }
    
    if (seconds >= 60) {
      def counterMinutes = 0
      
      while (seconds >= 60) {
        seconds -= 60
        counterMinutes++
      }
      
      if (res != "")
        res += seconds > 0 ? ", " : " and "
      
      res += counterMinutes
      res += counterMinutes > 1 ? " minutes" : " minute"
    }
    
    if (seconds > 0) {
      res += (res != "" ? " and " : "") + seconds + (seconds > 1 ? " seconds" : " second") 
    }
    
    return res
  }
}

__________________________________________________
class Kata {

    static String formatDuration(seconds) {
        if (!seconds) {
            return 'now'
        }
        def units = ['second': 1,
                     'minute': 60,
                     'hour': 60 * 60,
                     'day': 24 * 60 * 60,
                     'year': 365 * 24 * 60 * 60]
            .sort {-it.value}
            .collect {it ->
                if (seconds >= it.value) {
                    def unitCount = seconds.intdiv it.value
                    seconds -= it.value * unitCount
                    "${unitCount} ${it.key}${unitCount > 1 ? 's' : ''}"
                }
            }
            .findAll {it}
        def last = units.removeLast()
        units.isEmpty() ? last : "${units.join(', ')} and $last"
    }
}

__________________________________________________
class Kata {
  
    static String formatDuration(seconds) {
        if (seconds == 0) {
            return 'now'
        }
        def units = [1: 'second',
                     60: 'minute',
                     (60 * 60): 'hour',
                     (24 * 60 * 60): 'day',
                     (365 * 24 * 60 * 60): 'year']
            .sort {-it.key}
            .collect {it ->
                if (seconds >= it.key) {
                    def unitCount = seconds.intdiv it.key
                    seconds -= it.key * unitCount
                    "${unitCount} ${it.value}${unitCount > 1 ? 's' : ''}"
                }
            }
            .findAll {it}
        def last = units.removeLast()
        if (units.isEmpty()) {
            return last
        }
        def joiner = new StringJoiner(', ', '', " and ${last}")
        units.each {joiner.add(it)}
        joiner
    }
}
