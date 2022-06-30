53af2b8861023f1d88000832


def are_you_playing_banjo(name)
  name.downcase[0]=='r' ? name+" plays banjo" : name+" does not play banjo"
end
________________________________
def are_you_playing_banjo(name)
  letter = name[0].downcase
  return name + " plays banjo" if letter == 'r'
  name + " does not play banjo"
end
________________________________
def are_you_playing_banjo(name)
  "#{name} #{name.downcase.starts_with?('r') ? "plays" : "does not play"} banjo"
end
