def parse(data)
  val = 0
  out = []
  
  data.each_char { |cmd|
    case cmd
      when 'i' then val += 1
      when 'd' then val -= 1
      when 's' then val *= val
      when 'o' then out << val
    end
  }
  
  return out
end
__________________________________________
class Deadfish
  def initialize commands
    @current = 0
    @result = []
    @commands = commands.chars
  end
  
  def i; @current += 1 end
  def d; @current -= 1 end
  def s; @current = @current ** 2 end
  def o; @result << @current end
  
  def method_missing *; end
  
  def parse
    @commands.each { |cmd| send cmd }
    @result
  end
end

def parse(data)
  Deadfish.new(data).parse
end
__________________________________________
def parse commands
  value = 0
  outputs = []
  
  commands.chars.each do |command|
    case command
      when 'i' then value += 1
      when 'd' then value -= 1
      when 's' then value *= value
      when 'o' then outputs << value
    end
  end
  
  outputs
end
__________________________________________
def parse s
  values = []
  val = 0

  handlers = {
    'i' => Proc.new { val += 1 },
    'd' => Proc.new { val -= 1 },
    's' => Proc.new { val = val * val },
    'o' => Proc.new { values << val }
  }

  s.each_char { |c| handlers[c].call if handlers.key? c }

  values
end
