def assembler_interpreter(program)
  # define variables
  $code, $stack, ptr, flag, calls, output = [], {}, 0, 0, [], []
  
  # define helper functions
  def parse(s) $stack[s] or s.to_i end
  def label(s) $code.index(s + ':') end
  def parse_msg(s)
    quote, out = 0, ''
      s.split(' ', 2)[1].chars.each { |char|
        if    char == "'" then  quote ^= 1; next
        elsif char == ','  and quote == 0 then  char = '#SEP#' end
        out << char }
    out.split('#SEP# ').map { |s| $stack[s] or s } .join
  end
  
  # sanitize input
  program.lines.each { |line|
    line = line.split(/ *;/)[0].strip
    $code << line unless line.empty? }
  
  # process code
  while ptr < $code.size
    # parse line
    line = $code[ptr]
    command, arg1, arg2 = (line.gsub(',', '') + ' 0 0').split.first(3)
    
    # execute command
    case command
      when  'mov'  then  $stack[arg1] = parse(arg2)
      when  'inc'  then  $stack[arg1] += 1
      when  'dec'  then  $stack[arg1] -= 1
      when  'add'  then  $stack[arg1] += parse(arg2)
      when  'sub'  then  $stack[arg1] -= parse(arg2)
      when  'mul'  then  $stack[arg1] *= parse(arg2)
      when  'div'  then  $stack[arg1] /= parse(arg2)
      when  'cmp'  then  flag = parse(arg1) <=> parse(arg2)
      when  'jmp'  then  ptr = label(arg1)
      when  'jne'  then  ptr = label(arg1) if flag != 0
      when  'je'   then  ptr = label(arg1) if flag == 0
      when  'jge'  then  ptr = label(arg1) if flag > -1
      when  'jg'   then  ptr = label(arg1) if flag == 1
      when  'jle'  then  ptr = label(arg1) if flag < 1
      when  'jl'   then  ptr = label(arg1) if flag == -1
      when  'call' then  calls << ptr; ptr = label(arg1)
      when  'ret'  then  ptr = calls.pop
      when  'msg'  then  output << parse_msg(line)
      when  'end'  then  return output.join('\n')
    end
    
    ptr += 1
  end
  
  -1
end
        
____________________________________________________
def assembler_interpreter(program)
  Assembly::Interpreter.interpret(program)
end

module Assembly
  module Interpreter
    class << self
      def interpret(raw_program)
        program = setup_program(raw_program)

        until program.finished?
          program.current_instruction.execute(program)
        end

        program.output
      rescue Assembly::Errors::Error
        -1
      end

      private

      def setup_program(raw_program)
        instruction_set = InstructionSet.new(raw_program)
        registry = Registry.new
        Program.new(instruction_set, registry)
      end
    end
  end

  class Registry
    REGISTERS = (:a..:z).to_a.freeze

    def initialize
      @values = {}
    end

    def insert(value, at:)
      register = at
      validate_register(register)
      values[register] = value
    end

    def read(register)
      validate_register(register)
      values[register] || (raise Errors::EmptyRegister)
    end

    private

    attr_reader :values

    def validate_register(register)
      unless REGISTERS.include?(register)
        raise Errors::InvalidRegister, "Specified register is invalid; it must be one of the following: #{REGISTERS}"
      end
    end
  end

  class Program
    attr_reader :instruction_pointer, :registry, :ret_targets
    attr_accessor :output, :last_cmp

    def initialize(instruction_set, registry)
      @instruction_set = instruction_set
      @registry = registry

      @instruction_pointer = 0
      @ret_targets = []
      @last_cmp = NilComparison.new
      @output = nil
      @finished = false
    end

    def get_register(value_or_variable)
      return value_or_variable if value_or_variable.is_a? Integer

      registry.read(value_or_variable)
    end

    def set_register(variable, value)
      registry.insert(value, at: variable)
    end

    def proceed
      @instruction_pointer += 1
    end

    def call_subprogram(subprogram)
      ret_targets.push(instruction_pointer)
      jump_to_subprogram(subprogram)
    end

    def jump_to_subprogram(subprogram)
      @instruction_pointer = instruction_set.line_number(label: subprogram)
    end

    def return_to_last_target
      @instruction_pointer = ret_targets.pop || (raise Errors::EmptyReturnTarget)
    end

    def current_instruction
      instruction_set.get(instruction_pointer)
    end

    def finished?
      @finished
    end

    def finish
      @finished = true
      freeze
    end

    private

    attr_reader :instruction_set
  end

  class InstructionSet
    attr_reader :instructions, :labels

    def initialize(raw_instructions)
      @instructions = create_instructions(raw_instructions)
      @labels = {}
      scan_labels
    end

    def get(line_number)
      instructions[line_number] || (raise Errors::InstructionOutOfBounds)
    end

    def line_number(label:)
      labels.fetch(label) { raise Errors::InvalidIdentifier }
    end

    private

    def create_instructions(raw_instructions)
      Instructions::Parser.parse_instructions(raw_instructions)
        .map(&method(:create_instruction))
    end

    def create_instruction(parsed_instruction)
      Instructions::Factory.create(*parsed_instruction)
    end

    def scan_labels
      instructions.each_with_index do |instruction, index|
        add_label(instruction, index) if label?(instruction)
      end

      labels.freeze
    end

    def label?(instruction)
      instruction.is_a? Instructions::Label
    end

    def add_label(label, label_index)
      labels[label.identifier] = label_index
    end
  end

  class Comparison
    def initialize(x, y)
      validate(x, y)
      @x = x
      @y = y
    end

    def greater?
      x > y
    end

    def greater_or_equal?
      x >= y
    end

    def equality?
      x == y
    end

    def less_or_equal?
      x <= y
    end

    def less?
      x < y
    end

    def inequality?
      x != y
    end

    def ==(other)
      x == other.x && y == other.y
    end

    protected

    attr_reader :x, :y

    private

    def validate(x, y)
      unless x.is_a?(Integer) && y.is_a?(Integer)
        raise Errors::InvalidValue, 'x and y must be integers.'
      end
    end
  end

  class NilComparison
    def nil?; true end

    def greater?; false end
    def greater_or_equal?; false end
    def equality?; false end
    def less_or_equal?; false end
    def less?; false end
    def inequality?; false end

    def ==(other)
      other.nil?
    end
  end

  module Instructions
    module Factory
      class << self
        INSTRUCTIONS = %i[mov inc dec add sub mul div jmp cmp
                        jne je jge jg jle jl call ret msg end].freeze

        def create(instruction, *arguments)
          return create_label(instruction.to_s) if Parser.label?(instruction)

          validate!(instruction)
          instruction_klass(instruction).new(*arguments)
        end

        private

        def create_label(raw_label)
          Label.new(raw_label.strip.delete_suffix(':').to_sym)
        end

        def validate!(instruction)
          unless INSTRUCTIONS.include?(instruction)
            raise Errors::InvalidInstruction, "#{instruction} is an invalid instruction"
          end
        end

        def instruction_klass(instruction)
          Instructions.const_get(instruction.to_s.capitalize)
        end
      end
    end

    class Instruction
      def ==(other)
        self.class == other.class
      end

      def to_s
        arguments =
          instance_variables
            .map { |v| instance_variable_get(v) }
            .map { |arg| arg.is_a?(String) ? "'#{arg}'" : arg }

        instruction_name =
          self.class
            .name
            .delete_prefix('Assembly::Instructions::')
            .downcase

        "#{instruction_name}  #{arguments.join(', ')}"
      end
    end

    class ArithmeticInstruction < Instruction
      def initialize(target_register, source_register)
        @target_register = target_register
        @source_register = source_register
      end

      def execute(program)
        x_value = program.get_register(target_register)
        y_value = program.get_register(source_register)
        value = compute(x_value, y_value)

        program.set_register(target_register, value)
        program.proceed
      end

      def ==(other)
        super &&
          target_register == other.target_register &&
          source_register == other.source_register
      end

      protected

      attr_reader :target_register, :source_register

      private

      def compute(_x_value, _y_value)
        raise NotImplementedError
      end
    end

    class Add < ArithmeticInstruction
      def compute(x_value, y_value)
        x_value + y_value
      end
    end

    class Sub < ArithmeticInstruction
      def compute(x_value, y_value)
        x_value - y_value
      end
    end

    class Mul < ArithmeticInstruction
      def compute(x_value, y_value)
        x_value * y_value
      end
    end

    class Div < ArithmeticInstruction
      def compute(x_value, y_value)
        x_value / y_value
      end
    end

    class Call < Instruction
      def initialize(label)
        @label = label
      end

      def execute(program)
        program.call_subprogram(label)
        program.proceed
      end

      def ==(other)
        super && label == other.label
      end

      protected

      attr_reader :label
    end

    class Cmp < Instruction
      def initialize(x, y)
        @x = x
        @y = y
      end

      def execute(program)
        x_val = program.get_register(x)
        y_val = program.get_register(y)
        program.last_cmp = Comparison.new(x_val, y_val)
        program.proceed
      end

      def ==(other)
        super &&
          x == other.x &&
          y == other.y
      end

      protected

      attr_reader :x, :y
    end

    class Dec < Instruction
      def initialize(register)
        @register = register
      end

      def execute(program)
        value = program.get_register(register)
        program.set_register(register, value - 1)
        program.proceed
      end

      def ==(other)
        super && register == other.register
      end

      protected

      attr_reader :register
    end

    class Inc < Instruction
      def initialize(register)
        @register = register
      end

      def execute(program)
        value = program.get_register(register)
        program.set_register(register, value + 1)
        program.proceed
      end

      def ==(other)
        super && register == other.register
      end

      private

      attr_reader :register
    end

    class Jmp < Instruction
      def initialize(label)
        @label = label
      end

      def execute(program)
        desired_last_cmp?(program) && program.jump_to_subprogram(label)
        program.proceed
      end

      def ==(other)
        super && label == other.label
      end

      protected

      attr_reader :label

      private

      def desired_last_cmp?(_program)
        true
      end
    end

    class Je < Jmp
      private

      def desired_last_cmp?(program)
        program.last_cmp.equality?
      end
    end

    class Jg < Jmp
      private

      def desired_last_cmp?(program)
        program.last_cmp.greater?
      end
    end

    class Jge < Jmp
      private

      def desired_last_cmp?(program)
        program.last_cmp.greater_or_equal?
      end
    end

    class Jl < Jmp
      private

      def desired_last_cmp?(program)
        program.last_cmp.less?
      end
    end

    class Jle < Jmp
      private

      def desired_last_cmp?(program)
        program.last_cmp.less_or_equal?
      end
    end

    class Jne < Jmp
      private

      def desired_last_cmp?(program)
        program.last_cmp.inequality?
      end
    end

    class End < Instruction
      def execute(program)
        program.finish
      end
    end

    class Mov < Instruction
      def initialize(register, value)
        @register = register
        @value = value
      end

      def execute(program)
        val = program.get_register(value)
        program.set_register(register, val)
        program.proceed
      end

      def ==(other)
        super &&
          register == other.register
          value == other.value
      end

      protected

      attr_reader :register, :value
    end

    class Msg < Instruction
      def initialize(*arguments)
        @arguments = arguments
      end

      def execute(program)
        program.output = concoct_message(program)
        program.proceed
      end

      def ==(other)
        super && arguments == other.arguments
      end

      protected

      attr_reader :arguments

      private

      def concoct_message(program)
        arguments.map do |argument|
          argument.is_a?(Symbol) ? program.get_register(argument) : argument
        end.join
      end
    end

    class Ret < Instruction
      def execute(program)
        program.return_to_last_target
        program.proceed
      end
    end

    Label = Struct.new(:identifier) do
      def to_s
        "label: #{identifier}"
      end

      def execute(program)
        program.proceed
      end
    end

    module Parser
      class << self
        MATCHERS = {
          comment: /;.*$/,
          instruction: /\A([a-z0-9_]+)(?:\s+|\z)/,
          arguments: /\A[a-z0-9_]+\s+(.+)/,
          argument: /'[^']*'|[^,\s]+/,
          register: /\A[a-z]+\z/,
          integer: /\A-?\d+\z/,
          string: /\A'(.*)'\z/,
          label: /\A[a-z0-9_]+:\z/,
          subprogram: /\A[a-z0-9_]+\z/
        }.freeze

        def parse_instructions(raw_program)
          remove_comments(raw_program)
            .lines
            .map(&:strip)
            .reject(&:empty?)
            .map(&method(:parse_line))
        end

        def label?(raw_line)
          raw_line.match? MATCHERS[:label]
        end

        private

        def remove_comments(raw_program)
          raw_program.gsub(MATCHERS[:comment], '')
        end

        def parse_line(raw_line)
          return [raw_line.strip.to_sym] if label?(raw_line)

          instruction = parse_instruction(raw_line)
          args = parse_arguments(raw_line) if has_arguments?(raw_line)

          [instruction, *args]
        end

        def parse_instruction(raw_line)
          extract(raw_line, :instruction).to_sym
        end

        def extract(raw_line, matcher_type)
          match = raw_line.match(MATCHERS[matcher_type])
          unless match
            raise Errors::InvalidInstruction,
              "Could not extract #{matcher_type} from '#{raw_line}'"
          end
          match.captures.first
        end

        def has_arguments?(raw_line)
          raw_line.match?(MATCHERS[:arguments])
        end

        def parse_arguments(raw_line)
          extract(raw_line, :arguments)
            .yield_self(&method(:split_args))
            .map(&method(:parse_arg))
        end

        def split_args(raw_args)
          raw_args.scan(MATCHERS[:argument])
        end

        def parse_arg(arg)
          case arg
          when MATCHERS[:register] then arg.to_sym
          when MATCHERS[:integer] then arg.to_i
          when MATCHERS[:string] then arg.delete_prefix("'").delete_suffix("'")
          when MATCHERS[:subprogram] then arg.to_sym
          else
            raise Errors::InvalidInstruction, "\"#{arg}\" is an invalid argument."
          end
        end
      end
    end
  end

  module Errors
    Error = Class.new(StandardError)

    InvalidValue = Class.new(Error)
    EmptyRegister = Class.new(Error)
    InvalidRegister = Class.new(Error)
    EmptyReturnTarget = Class.new(Error)
    InvalidIdentifier = Class.new(Error)
    InvalidInstruction = Class.new(Error)
    InstructionOutOfBounds = Class.new(Error)
  end
end

____________________________________________________
class String
  def is_integer?
    self.to_i.to_s == self
  end
end

$commands=["mov","inc","dec","add","sub","mul","div","jmp","cmp","jne","je","jge","jg","jle","jl","call","ret","msg","end"]

def assembler_interpreter(program)
  $program_array=program.gsub(/;.*/,"").split
  $variable_hash={}
  $cmp=nil
  $msg=nil
  a=travel_through_program(0,true)
  if a==1
    return -1
  else
    return $msg
  end
end

def travel_through_program(ind,main)
  i=ind
  while i<$program_array.length
    case $program_array[i]
    when "mov"
      mov($program_array[i+1][0..-2],$program_array[i+2])
      i+=3
    when "inc"
      inc($program_array[i+1])
      i+=2
    when "dec"
      dec($program_array[i+1])
      i+=2
    when "add"
      add($program_array[i+1][0..-2],$program_array[i+2])
      i+=3
    when "sub"
      sub($program_array[i+1][0..-2],$program_array[i+2])
      i+=3
    when "mul"
      mul($program_array[i+1][0..-2],$program_array[i+2])
      i+=3
    when "div"
      div($program_array[i+1][0..-2],$program_array[i+2])
      i+=3
    when "call"
      a=call($program_array[i+1],i)
      if a==1
        break
      end
      i+=2
    when "cmp"
      $cmp=cmp($program_array[i+1][0..-2],$program_array[i+2])
      i+=3
    when "jne"
      a=jne($cmp,$program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "je"
      a=je($cmp,$program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "jge"
      a=jge($cmp,$program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "jg"
      a=jg($cmp,$program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "jle"
      a=jle($cmp,$program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "jl"
      a=jl($cmp,$program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "jmp"
      a=jmp($program_array[i+1],i)
      if a
        i=a+1
      else
        i+=2
      end
    when "msg"
      a=msg(i+1)
      $msg=a[0]
      i=a[1]
      if i==$program_array.length
        return 1
      end
    when "end"
      return 2
    when "ret"
      return 2
    end
    if $program_array[i][-1]==":"
      i+=1
    end
  end
  return 1
end

def mov(x,y)
  if !y.is_integer?
    $variable_hash[x.to_sym]=$variable_hash[y.to_sym]
  else
    $variable_hash[x.to_sym]=y.to_i
  end
end

def dec(x)
  $variable_hash[x.to_sym]-=1
end

def inc(x)
  $variable_hash[x.to_sym]+=1
end

def add(x,y)
  if !y.is_integer?
    $variable_hash[x.to_sym]+=$variable_hash[y.to_sym]
  else
    $variable_hash[x.to_sym]+=y.to_i
  end  
end

def sub(x,y)
  if !y.is_integer?
    $variable_hash[x.to_sym]-=$variable_hash[y.to_sym]
  else
    $variable_hash[x.to_sym]-=y.to_i
  end  
end

def mul(x,y)
  if !y.is_integer?
    $variable_hash[x.to_sym]*=$variable_hash[y.to_sym]
  else
    $variable_hash[x.to_sym]*=y.to_i
  end
end

def div(x,y)
  if !y.is_integer?
    $variable_hash[x.to_sym]/=$variable_hash[y.to_sym]
  else
    $variable_hash[x.to_sym]/=y.to_i
  end
end

def call(lbl,ind)
  beginning=0
  for i in 0..$program_array.length-1
    if $program_array[i]==lbl+":"
      return travel_through_program(i+1,false)
    end
  end
end

def cmp(x,y)
  if $variable_hash[x.to_sym]
    if $variable_hash[y.to_sym]
      return compare($variable_hash[x.to_sym],$variable_hash[y.to_sym])
    else
      return compare($variable_hash[x.to_sym],y.to_i)
    end
  else
    if $variable_hash[y.to_sym]
      return compare(x.to_i,$variable_hash[y.to_sym])
    else
      return compare(x.to_i,y.to_i)
    end
  end
end
    
def compare(x,y)
  if x==y
    return "eq"
  elsif x>y
    return "gr"
  else
    return "le"
  end
end
  
def jne(res,lbl,ind)
  if res=="gr"or res=="le"
    return jmp(lbl,ind)
  end
  return nil
end
  
def je(res,lbl,ind)
  if res=="eq"
    return jmp(lbl,ind)
  end
  return nil
end
  
def jge(res,lbl,ind)
  if res=="gr"or res=="eq"
    return jmp(lbl,ind)
  end
  return nil
end

def jg(res,lbl,ind)
  if res=="gr"
    return jmp(lbl,ind)
  end
  return nil
end

def jle(res,lbl,ind)
  if res=="eq"or res=="le"
    return jmp(lbl,ind)
  end
  return nil
end
  
def jl(res,lbl,ind)
  if res=="le"
    return jmp(lbl,ind)
  end
  return nil
end

def jmp(lbl,ind)
  for i in 0..$program_array.length-1
    if $program_array[i]==lbl+":"
      return i
    end
  end
end
  
def msg(ind)
  flag=false
  str=""
  count=0
  count_false=0
  ending=0
  for i in ind..$program_array.length-1
    if ($program_array[i][-1]==":" or $commands.include?($program_array[i])) and !flag
      ending=i
      break
    end
    if i==$program_array.length-1
      ending=i+1
    end
    if $program_array[i].scan(/(?=')/).count==2
      str=str+$program_array[i][1..-3]
    else
      if $program_array[i][0]=="'" or $program_array[i][-1]=="'"
        if !flag
          flag=true
          count_false=0
        else
          flag=false
          count=0
        end
      end
      if !flag
        var=$program_array[i] =~ /'/
        if !var
          comma_ind=$program_array[i]=~/,/
            if comma_ind
              str=str+$variable_hash[$program_array[i][0..-2].to_sym].to_s
            else
              str=str+$variable_hash[$program_array[i].to_sym].to_s
            end
        else
          if i==$program_array.length-1
            str=str+$program_array[i][0..-2]
          else
            if($program_array[i+1][-1]==":" or $commands.include?($program_array[i+1]))
              str=str+$program_array[i][0..-2]
            else
              str=str+$program_array[i][0..-3]
            end
          end
        end
      else
        if $program_array[i].length==1 and count==0
          str=str+" "
        elsif $program_array[i].length>1 and count==0
          str=str+$program_array[i][1..-1]+" "
        elsif count>0
          str=str+$program_array[i]+" "
        end

        count+=1
      end
    end
  end
  return [str,ending]
end

____________________________________________________
class InvalidSubroutineExitException < StandardError; end

INSTRUCTIONS = {
    'mov' => -> (register, args) { register[args[0]] = lookup(register, args[1]) },
    'inc' => -> (register, args) { register[args[0]] += 1 },
    'dec' => -> (register, args) { register[args[0]] -= 1 },
    'add' => -> (register, args) { register[args[0]] += lookup(register, args[1]) },
    'sub' => -> (register, args) { register[args[0]] -= lookup(register, args[1]) },
    'mul' => -> (register, args) { register[args[0]] *= lookup(register, args[1]) },
    'div' => -> (register, args) { register[args[0]] /= lookup(register, args[1]) },
    'cmp' => -> (register, args) { $compared = { x: lookup(register, args[0]), y: lookup(register, args[1]) } },
    'msg' => -> (register, args ) { $output = args.join(',').split(/('[^']+',)/).map {|arg|
        next if arg.empty?
        arg.tap{|x| x.sub!(/,\s*\Z/, '')}
           .start_with?("'") ? arg[1..-2] : lookup(register, arg) # remove surrounding quotes
        }.compact.join
    }
}

JUMPS = {
    'ret' => -> (register, arg, subroutines) { true },
    'end' => -> (register, arg, subroutines) { true },
    'jmp' => -> (register, arg, subroutines) { run(arg, subroutines, register) },
    'je' => -> (register, arg, subroutines) {
        return false unless $compared[:x].eql? $compared[:y]
        run(arg, subroutines, register)
     },
    'jne' => -> (register, arg, subroutines) {
        return false if $compared[:x].eql? $compared[:y]
        run(arg, subroutines, register)
     },
    'jge' => -> (register, arg, subroutines) {
        return false unless $compared[:x] >= $compared[:y]
        run(arg, subroutines, register)
     },
    'jg' => -> (register, arg, subroutines) {
        return false unless $compared[:x] > $compared[:y]
        run(arg, subroutines, register)
     },
    'jle' => -> (register, arg, subroutines) {
        return false unless $compared[:x] <= $compared[:y]
        run(arg, subroutines, register)
     },
    'jl' => -> (register, arg, subroutines) {
        return false unless $compared[:x] < $compared[:y]
        run(arg, subroutines, register)
     }
}

def lookup(register, arg)
    arg = arg.strip
    register[arg] || arg.to_i
end

def args_from(param)
    param.split(',')
end

def ensure_correct_exit!(name, last_instruction)
    exception = InvalidSubroutineExitException.new("Found routine: #{name} with final instruction: #{last_instruction}")
    if name.eql?('main')
        raise exception unless last_instruction.eql? 'end'
    end

    raise raise exception unless %w{ret call}.include? last_instruction
end

def run(name, subroutines, register = {})
    # assume subroutine name will always exist in subroutines hash
    last_instruction = ''
    subroutines[name].each do |command|
        cmd, params = command.match(/(?<cmd>\w+)\s+(?<params>.+)/)&.named_captures&.values
        cmd = command if cmd.nil?
        last_instruction = cmd
      
        instruction = INSTRUCTIONS[cmd]
        if !instruction.nil?
            instruction.call(register, args_from(params))
            next
        end

        if cmd == 'call'
            run(params, subroutines, register)
            next
        end

        # here we are probably dealing with a jmp
        jump = JUMPS[cmd]
        if !jump.nil?
            # if a jump returns true; return
            return true if jump.call(register, params, subroutines)
            next
        end
    end

    ensure_correct_exit!(name, last_instruction)

    true # useful to notify jumps that run finished
end

def parse(program)
    subroutine = 'main' # start with main routine
    subroutines = { subroutine => [] }

    program.split("\n").each do |line|
        line = line.sub(/;.+/, '').strip
        case
        when line =~ /.+:$/
            subroutine = line.sub(':', '')
            subroutines[subroutine] = []
        when line == ""
            subroutine = 'main'
        else
            subroutines[subroutine] << line
        end
    end

    subroutines
end

def assembler_interpreter(program)
    $compared = {}
    $output = ''
    
    subroutines = parse(program)

    # start main subroutine
    run('main', subroutines)
    return $output
rescue InvalidSubroutineExitException
    return -1
end
