57eadb7ecd143f4c9c0000a3


def abbrev_name(name)
  name.split.map { |s| s[0]}.join('.').upcase
end
_________________________
def abbrev_name(name)

name.upcase.split.map(&:chr).join"."

end
_________________________
def abbrev_name(name)
    "#{name.split[0][0]}.#{name.split[1][0]}".upcase
end
