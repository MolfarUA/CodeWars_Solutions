function dnatorna(dna::String)::String
  replace(dna, 'T' => 'U')
end

_____________________________
function dnatorna(dna::String)
  replace(dna,"T"=>"U")
end

_____________________________
function dnatorna(dna::String)
  return replace(dna, "T" => "U")
end

_____________________________
function dnatorna(dna::String)
  replace(dna::String, "T" => "U")
end

_____________________________
function dnatorna(dna::String)
  join([l != 'T' ? l : 'U' for l in dna])
end
