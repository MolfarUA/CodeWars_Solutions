def stock_list(listOfArt, listOfCat)
    return "" if listOfArt.empty? || listOfCat.empty?
    listOfCat.map {|cat|
      cat = cat[0]
      n = listOfArt.select {|art|
        art[0] == cat
      }.map {|art|
        art.split[1].to_i
      }.sum
      
      "(#{cat} : #{n})"
    }.join(" - ")
end
________________________________________
def stock_list(listOfArt, listOfCat)
    if (listOfArt.size == 0) || (listOfCat.size == 0) 
      return "" 
    end
    result = ""
    listOfCat.each do |cat|
        total = 0
        listOfArt.each do |book|
            if (book[0] == cat[0])
              total += book.split(" ")[1].to_i 
            end
        end
        if (result.size != 0) 
          result += " - " 
        end
        result += "(" + cat.to_s + " : " + total.to_s + ")"
    end
    result
end
________________________________________
def stock_list(inventory, categories)
  return "" if inventory.empty?
  inventory = inventory.group_by(&.[0]).map {|category, items| 
    {category, items.map(&.split.last.to_i).sum}
  }.to_h
  categories.map {|category| "(#{category} : #{inventory[category[0]]? || 0})" }.join(" - ")
end
________________________________________
def stock_list(listOfArt, listOfCat)
 listOfArt.empty? || listOfCat.empty? ? "" : listOfCat.map{|x| "(#{x} : #{listOfArt.select{|a| a[0].to_s == x}.sum{|y| y.split[1].to_i}})"}.join(" - ")
end
________________________________________
def stock_list(listOfArt, listOfCat)
  return "" if listOfArt.empty? || listOfCat.empty?
  h = Hash(Char, Int32).new(0)
  listOfArt.each { |v| h[v[0]] += v.split.last.to_i }
  listOfCat.join(" - "){ |v| "(#{v} : #{h[v[0]]})" }
end
