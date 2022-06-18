55f9bca8ecaa9eac7100004a


def past(h, m, s)
  (h * 3600 + m * 60 + s) * 1000
end
__________________________
def past(h, m, s)
  hours_to_ms(h) + minutes_to_ms(m) + seconds_to_ms(s)
end

def seconds_to_ms(s)
  s * 1_000
end

def minutes_to_ms(m)
  seconds_to_ms(m * 60)
end

def hours_to_ms(h)
  minutes_to_ms(h * 60)  
end
__________________________
require 'time'

def past(h, m, s)
  (Time.parse("#{h}:#{m}:#{s}") - Time.parse("0:0:0")) * 1000
end
__________________________
def past(h, m, s)
  ((((h*60)+m)*60)+s)*1000
end
__________________________
def past(h, m, s)
  miliseconds_per_second = 1000
  miliseconds_per_minute = miliseconds_per_second * 60
  miliseconds_per_hour   = miliseconds_per_minute * 60
  
  h * miliseconds_per_hour + m * miliseconds_per_minute + s * miliseconds_per_second
end
__________________________
def past(*time)
  time.reduce { |s, t| s * 60 + t } * 1000
end
