576757b1df89ecf5bd00073b


function towerbuilder(n)
  [ join( n ∈ x-y+1:x+y-1 ? '*' : ' ' for x ∈ 1:2n-1 ) for y ∈ 1:n ]
end
_____________________________
function towerbuilder(n)
    [repeat(' ', n - i) * repeat('*', 2 * i - 1) * repeat(' ', n - i) for i in 1:n]
end
_____________________________
function towerbuilder(nfloors)
    ans = []
    N = 2 * nfloors - 1
    for i in 1:nfloors
        nstars = 2 * i - 1
        nspaces::Int = (N - nstars) / 2
        push!(ans, "$(' '^nspaces)$('*'^nstars)$(' '^nspaces)")
    end
    ans
end
_____________________________
function towerbuilder(n)
    [repeat(' ', n - i) * repeat('*', 2 * i - 1) * repeat(' ', n - i) for i in 1:n]
end
_____________________________
function towerbuilder(nfloors)
    ans = []
    N = 2 * nfloors - 1
    for i in 1:nfloors
        nstars = 2 * i - 1
        nspaces::Int = (N - nstars) / 2
        push!(ans, "$(' '^nspaces)$('*'^nstars)$(' '^nspaces)")
    end
    ans
end
_____________________________
function towerbuilder(nfloors)
  map(i-> 
    repeat(" ",nfloors-i) * repeat("*", 2i-1) * repeat(" ",nfloors-i),
    1:nfloors)
end
_____________________________
function towerbuilder(nfloors)
    numChars = 2 * nfloors - 1
    tower = Vector{String}()
    for i ∈ 1:nfloors
        numThings = 2 * i - 1
        padding = (numChars - numThings) ÷ 2
        floor = (" " ^ padding) * ("*" ^ numThings) * (" " ^ padding)
        push!(tower, floor)
    end
    return tower
end
