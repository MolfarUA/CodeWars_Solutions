def format_duration(total)
  if total == 0
    "now"
  else
    duration = {
      year:   total / (60 * 60 * 24 * 365),
      day:    total / (60 * 60 * 24) % 365,
      hour:   total / (60 * 60) % 24,
      minute: total / 60 % 60,
      second: total % 60
    }
  
    @output = []
  
    duration.each do |key, value|
      if value > 0
        @output << "#{value} #{key}"
        @output.last << "s" if value != 1
      end
    end
  
    @output.join(', ').gsub(/\,\s(?=\d+\s\w+$)/, " and ")
  end
end

__________________________________________________
def format_duration(seconds)
  return "now" if seconds == 0
  m,s = seconds.divmod(60)
  h,m = m.divmod(60)
  d,h = h.divmod(24)
  y,d = d.divmod(365)

  *f,l = {'year'=>y,'day'=>d,'hour'=>h,'minute'=>m,'second'=>s}.to_a.select{|i| i.last > 0}.map{|i| (i.last>1)? "#{i.last} #{i.first+'s'}": "#{i.last} #{i.first}"}
  (f.count > 0)? f.join(', ') + ' and '+l : l
end

__________________________________________________
def format_duration(seconds)
  return "now" if seconds.zero?

  durations = {
    years: 31_536_000,
    days:      86_400,
    hours:      3_600,
    minutes:       60,
    seconds:        1
  }

  singularize = ->((k, v)) { "#{v} #{v == 1 ? k[0..-2] : k}" }

  units = durations.each_with_object({}) do |(name, duration), units|
    units[name], seconds = seconds.divmod(duration)
  end.reject { |k, v| v.zero? }.map(&singularize)

  last = units.pop
  return last if units.empty?
  units.join(", ") << " and #{last}"
end
