def sort_array(source_array)
  odds = source_array.select(&:odd?).sort
  source_array.map { |n| n.even? ? n : odds.shift }
end
_______________________________________________
def sort_array(xs)
  odd = xs.select(&:odd?).sort.each
  xs.map{ |x| x.odd? ? odd.next : x }
end
_______________________________________________
def sort_array(source_array)
  odds = source_array.select(&:odd?).sort
  source_array.map { |e| e.odd? ? odds.shift : e }
end
_______________________________________________
def sort_array(source_array)
  odds = source_array.select{ |v| v.odd? }.sort
  source_array.map { |v| v.even? ? v : odds.shift }
end
_______________________________________________
def sort_array(source_array)
  mod = source_array.clone.delete_if {|el| el.even?}.sort
  source_array.map {|el| el.odd? ? nil : el}.map do |el|
    if el == nil
      el = mod[0]
      mod.slice!(0)
    else
      el
    end
  end
end
