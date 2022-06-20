539a0e4d85e3425cb0000a88


class Adder
  def initialize(i)
    @value = i
  end
  
  def call(i)
    Adder.new(@value + i)
  end
  
  def to_int
    @value
  end
  alias_method :to_i, :to_int 
 
  def ==(other)
    Integer(other) == @value
  end
end

def add(n)
  Adder.new(n)
end
______________________
def add(n)
  n
end

class Fixnum
  def call(m=0)
    self + m
  end
end
______________________
def add(n)
  n.tap { Fixnum.class_eval { alias call + } }
end
