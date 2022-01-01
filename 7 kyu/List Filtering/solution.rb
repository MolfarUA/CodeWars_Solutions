def filter_list(l)
  l.reject { |x| x.is_a? String }
end

_____________________________________________
def filter_list(l)
l.select{|i| i.is_a?(Integer)}
end

_____________________________________________
def filter_list(l)
 l.grep(Numeric)
end

_____________________________________________
def filter_list(l)
  result = l.map do |el| 
    if el.class == Integer 
      el
    end
  end
  result.compact
end

_____________________________________________
def filter_list(l)
  new_list = l.select {|n| n.class == Integer && n >= 0}
end
