514a3996d22ce03198000003

class MrFreeze
  self.freeze
end
_________________________
MrFreeze.freeze
_________________________
MrFreeze.freeze unless MrFreeze.frozen?
_________________________
class MrFreeze
  def is_frozen?
    true
  end
  def freeze
    puts "PRETENDING TO BE FROZEN"
  end
end
MrFreeze.freeze
_________________________
def MrFreeze.frozen?
  return true
end
_________________________
MrFreeze::freeze
