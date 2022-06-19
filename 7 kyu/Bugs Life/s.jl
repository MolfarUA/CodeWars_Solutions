5b71af678adeae41df00008c


function shortestdistance(a::Real, b::Real, c::Real)::Real
    sqrt(a^2 + b^2 + c^2 + 2 * prod(sort([a,b,c])[1:2]))
end
____________________________
function shortestdistance(a::Real, b::Real, c::Real)::Real
    (x, y, z) = sort([a, b, c])
    sqrt((x+y)^2 + z^2)
end
____________________________
function shortestdistance(a::Real, b::Real, c::Real)::Real
  edges = [a,b,c]
  longest_edge = findmax(edges)
  deleteat!(edges, longest_edge[2])
  step1 = sqrt((longest_edge[1] * edges[1]/sum(edges))^2 + edges[1]^2)
  step2 = sqrt((longest_edge[1] * edges[2]/sum(edges))^2 + edges[2]^2)
  return step1 + step2
end
____________________________
function shortestdistance(a::Real, b::Real, c::Real)::Real
    minimum([sqrt(c^2 + (a + b)^2), sqrt(a^2 + (c + b)^2), sqrt(b^2 + (a + c)^2)])
end
