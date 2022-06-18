def find_needle(haystack)
  "found the needle at position #{haystack.index('needle')}"
end
________________________
def find_needle(haystack)
  haystack.each_with_index do |item,index|
    return "found the needle at position #{index}" if item == "needle" 
  end
end
________________________
def find_needle(haystack)
  @index = haystack.index("needle")
  return "found the needle at position #{@index}"
end
________________________
def find_needle(haystack)
  "found the needle at position #{haystack.find_index("needle").to_s}"
end
________________________
def find_needle(haystack)
  for i in 0..haystack.length-1
    if haystack[i]== "needle"; return "found the needle at position "+i.to_s; end
  end
end
