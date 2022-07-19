51c8e37cee245da6b40000bd


def solution(input, markers)
  input.gsub(/\s+[#{markers.join}].*/, "")
end
__________________________________
def solution(input, markers)
  input.gsub(/\s*#{Regexp.union(markers)}.*$/, '')
end
__________________________________
def solution(input, markers)
  input
    .split("\n")
    .map { |line|
      markers.each { |marker|
        line = line.split(marker)[0]
      }
      line.strip
    }
    .join("\n")
end
