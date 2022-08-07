5861487fdb20cff3ab000030


def boolfuck(code, input = "")
  cell = Cell.new
  input_bits = input.unpack("b*").first.chars.map(&:to_i)
  output_bits = []
  matching_brackets = matching_brackets_for(code)
  pointer = 0

  while pointer < code.size
    case code[pointer]
    when "+" then cell.flip!
    when "," then cell.value = input_bits.shift || 0
    when ";" then output_bits << cell.value
    when "<" then cell = cell.prev
    when ">" then cell = cell.succ
    when "[" then pointer = matching_brackets[pointer] if cell.zero?
    when "]" then pointer = matching_brackets[pointer] - 1
    end

    pointer += 1
  end

  [output_bits.join].pack("b*")
end

class Cell
  attr_accessor :value
  attr_writer :prev, :succ

  def initialize(value = 0, prev: nil, succ: nil)
    @value = value
    @prev = prev
    @succ = succ
  end

  def flip!
    @value ^= 1
  end

  def zero?
    @value.zero?
  end

  def prev
    @prev ||= Cell.new(succ: self)
  end

  def succ
    @succ ||= Cell.new(prev: self)
  end
end

def matching_brackets_for(code)
  stack = []
  (0..code.size).each_with_object({}) { |index, memo|
    case code[index]
    when "["
      stack << index
    when "]"
      last_index = stack.pop
      memo[last_index], memo[index] = index, last_index
    end
  }
end
_____________________________
class BrainFuck
  def initialize code
    @code = code
    @instr_pointer = 0
    @data = []
    def @data.[] i
      super || 0
    end
    @data_pointer = 0
  end
  
  def read_instruction
    return nil if @instr_pointer >= @code.size
    instr = @code[@instr_pointer]
    @instr_pointer += 1
    instr
  end

  def incr_data_pointer incr
    @data_pointer += incr
  end
  
  def incr_data op
    @data[@data_pointer] = @data[@data_pointer].send(op, 1) & 0xff
  end
  
  def run input
    output = ''
    while (instr = read_instruction) && instr != ']'
      case
      when instr == '['
        start_loop_pointer = @instr_pointer
        begin
          @instr_pointer = start_loop_pointer
          output << run(@data[@data_pointer] != 0 && input)
        end while @data[@data_pointer] != 0
      when input
        case instr
        when '>' then incr_data_pointer(1)
        when '<' then incr_data_pointer(-1)
        when '+', '-' then incr_data(instr)
        when '.' then output << @data[@data_pointer].chr
        when ',' then @data[@data_pointer] = input.slice!(0).ord
        end
      end
    end
    output
  end
end

class BoolFuck < BrainFuck
  def initialize code
    super code.gsub(/[.-]/, '').gsub(/;/, '.')
    @run_level = 0
  end

  def incr_data op
    super
    @data[@data_pointer] &= 1
  end

  def incr_data_pointer incr
    super
    @data_pointer, @data = 0, @data.unshift(0) if @data_pointer < 0
  end

  def run input
    @run_level += 1
    if @run_level == 1
      output = super input.chars.flat_map{|c| c.ord.to_s(2).reverse.ljust(8,"0").chars.map(&:to_i)}.pack("c" * 8 * input.size)
      output.unpack("c" * output.size).map{|i| i & 1}.each_slice(8).map{|a| a.reverse.join.to_i(2).chr}.join
    else
      super
    end
    ensure
    @run_level -= 1
  end
end

def boolfuck code, input = ''
  BoolFuck.new(code).run input
end
_____________________________
def boolfuck s,i=''
d=Hash.new c=0
i=i.chars.map{|c|c.ord.to_s(2).rjust(8,?0).reverse}*''
eval s.delete('^+,;<>[]').gsub(/.|/){{?]=>'end
',?[=>'until 1>d[c]
',?,=>'d[c]=i.slice!(0).to_i
',?;=>'s+="%d"%d[c]
',?+=>'d[c]^=1
'}[s=$&]||"c+=#{?=<=>s}
"}
s.gsub(/.{1,8}/){$&.reverse.to_i(2).chr}
end
