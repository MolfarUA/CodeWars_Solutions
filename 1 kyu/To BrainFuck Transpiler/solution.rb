NUMBER_LITERALS = (('a'..'z').to_a + ('A'..'Z').to_a + ('0'..'9').to_a).map { |e| "'" + e + "'" } + (-100..300).to_a

COMMENT_PREFIX          = /\/\/|--|#/
COMMENT                 = /#{COMMENT_PREFIX}[^"\n]*$/
TAB                     = /\t/
CHAR_ELEMENT            = /[^\,\"\\]|\\\\|\\'|\\"|\\n|\\r|\\t/
CHAR_QUOTE              = /'/
CHAR                    = /#{CHAR_QUOTE}#{CHAR_ELEMENT}#{CHAR_QUOTE}/
NUMBER                  = /-\d+|\d+|#{CHAR}/
WHOLE_NUMBER            = /^#{NUMBER}$/
STRING_QUOTE            = /"/
STRING                  = /"#{CHAR_ELEMENT}*"/
SPACE                   = /\s/
OPEN_SQUARE             = /\[/
CLOSE_SQUARE            = /\]/

VAR_PREFIX              = /\$|_|[a-zA-Z]/
VAR_SUFFIX              = /#{VAR_PREFIX}|\d/
VAR_NAME                = /#{VAR_PREFIX}#{VAR_SUFFIX}*/
MATCH_VAR_NAME          = /^#{VAR_NAME}$/
VAR_NAME_OR_NUMBER      = /#{VAR_NAME}|#{NUMBER}/
VAR_NAME_OR_STRING      = /#{VAR_NAME}|#{STRING}/

BASIC_INSTRUCTION       = ['set', 'inc', 'dec', 'add', 'sub', 'mul', 'divmod', 'div', 'mod', 'cmp', 'a2b', 'b2a']
LIST_INSTRUCTION        = ['lset','lget']
CONTROL_INSTRUCTION     = ['ifeq','ifneq','wneq','proc','end']
CALL_INSTRUCTION        = ['call']
INTERACTIVE_INSTRUCTION = ['msg', 'read']

INSTRUCTION = /var|set|inc|dec|add|sub|mul|divmod|div|mod|cmp|a2b|b2a|lset|lget|ifeq|ifneq|wneq|proc|end|call|read|msg|rem/


EOL                     = "\n"
EOF                     = "#END#"
WORD                    = /[^ \n\[\]]+/
TOKEN                   = Regexp.union(COMMENT, TAB, NUMBER, VAR_NAME, CHAR_ELEMENT, STRING_QUOTE, SPACE, INSTRUCTION, OPEN_SQUARE, CLOSE_SQUARE, WORD, NUMBER, EOL, EOF)

BRAIN_FUCK_CHAR         = "<>+-[],.".split('')

NUMBER_COMPONENT_INS  = {
  'set'     => [1, 1, true  ],
  'inc'     => [1, 1, true  ],
  'dec'     => [1, 1, true  ],
  'add'     => [1, 2, false ],
  'sub'     => [1, 2, false ],
  'mul'     => [1, 2, false ],
  'div'     => [1, 2, false ],
  'mod'     => [1, 2, false ],
  'cmp'     => [1, 2, false ],
  'divmod'  => [2, 2, false ],
  'a2b'     => [1, 3, false ],
  'b2a'     => [3, 1, false ],
  'ifeq'    => [1, 1, true  ],
  'ifneq'   => [1, 1, true  ],
  'wneq'    => [1, 1, true  ]
}
$code = ''
$pointer = 0
$proc_tokens = []
$stack_ins = []
$string_mode = false
$var = {}
$procs = {}
$stack_context  = ['main']

class ParsingError < StandardError; end

class ExpectedEndOfLine           < ParsingError; end
class ExpectedIndex               < ParsingError; end
class ExpectedListName            < ParsingError; end
class ExpectedNumber              < ParsingError; end
class ExpectedVar                 < ParsingError; end
class ExpectedVariableInstance    < ParsingError; end
class ExpectedVarOrNumber         < ParsingError; end
class ExpectedVarSingle           < ParsingError; end
class InvalidNumberLiterals       < ParsingError; end
class InvalidVarName              < ParsingError; end
class MismatchedParenthesesError  < ParsingError; end
class MismatchedStringQuoteError  < ParsingError; end
class MismatchedCharQuoteError    < ParsingError; end
class MismatchNumberArgument      < ParsingError; end
class MissingArgument             < ParsingError; end
class NestedProcedure             < ParsingError; end
class UnclosedBlock               < ParsingError; end
class UnexpectedEndInstruction    < ParsingError; end
class UnexpectedEndOfLine         < ParsingError; end
class UnexpectedList              < ParsingError; end
class UnexpectedNumber            < ParsingError; end
class UnexpectedVar               < ParsingError; end
class UnexpectedParenthese        < ParsingError; end
class UnknownInstruction          < ParsingError; end
class DuplicateArgumentName       < ParsingError; end
class UndefinedProcedure          < ParsingError; end
class RecursiveCalling            < ParsingError; end
class DefineVariableInsideProc    < ParsingError; end
class CollapseArgument            < StandardError; end
class DeleteUntempVariable        < StandardError; end
class DuplicateVariableError      < StandardError; end
class DuplicateProcError          < StandardError; end
class InvalidTypeArgument         < StandardError; end
class NotEnoughSpaceForVariable   < StandardError; end
class OutOfRangeList              < StandardError; end
class UndefinedVariableError      < StandardError; end
class UnexpectedIndex             < StandardError; end
class UnmatchNumberArgument       < StandardError; end


def random
  NUMBER_LITERALS.sample
end

def truth_value val
  val =~ CHAR ? val[1].ord : val.to_i % 256
end

class String
  def add
    $code += self
  end
end

class Integer
  def _v
    self
  end

  def wrap
    self % 256
  end
end

class Array
  def shift_space
    while $string_mode == false and first == " "
      shift
    end
    shift
  end

  def first_space
    while $string_mode == false and self.first == " "
      shift
    end
    first
  end
end

class Variable
  @@count = 0
  @@memory = Array.new (300) { nil }
  attr_accessor :_name, :length, :type, :_address, :space, :data, :index1, :index2

  def initialize(raw: nil, at: nil, length: 1, tokens: nil)
    raise NotEnoughSpaceForVariable if at.nil? == false and @@memory[at,length].any?
    if raw.nil? or (raw.is_a? Integer)
      @_address = at ? at : self.class.emptyIndex(length)
      @_name = "temp_#{_address}"
      @@count += 1
      $var[@_name] = @@memory[@_address] = self
      @length, @type = nil, :single_var
      _set(self, raw) if (raw.is_a? Integer)
      return self
    end

    @_name, @length, @type, @_address = raw, 1, :single_var, at.nil? ? self.class.emptyIndex : at

    raise DuplicateVariableError, "Already has variable name: #{@_name}" if ($var.has_key? @_name)

    $var[@_name] = self
    @@memory[@_address] = self
    @@count += 1

    try_parse_list tokens if tokens
    self
  end

  def try_parse_list tokens
    return unless tokens.first_space =~ OPEN_SQUARE
    tokens.shift_space
    raise ExpectedNumber unless tokens.first_space =~ WHOLE_NUMBER
    @length = get_var_or_number tokens
    @@memory[@_address] = nil
    @_address = Variable.emptyIndex(@length + 4)
    @type = :list_var
    @space  = Variable.new(raw: "#{@_name}__space",   at: @_address)
    @index1 = Variable.new(raw: "#{@_name}__index1",  at: @_address + 1)
    @index2 = Variable.new(raw: "#{@_name}__index2",  at: @_address + 2)
    @data   = Variable.new(raw: "#{@_name}__data",    at: @_address + 3)
    @@memory[@_address + 4, @length] = Array.new(@length) { |i| Variable.new(raw: "#{@_name}__#{i}") }
    raise MismatchedParenthesesError unless tokens.shift_space =~ CLOSE_SQUARE
  end

  def self.emptyIndex(length = 1)
    @@memory.each_cons(length).find_index {|slice| slice.none?}
  end

  def address(index = nil)
    if type == :list_var
      raise ExpectedNumber if (index.is_a? (Integer)) == false
      raise OutOfRangeList unless (0...length) === index
      _address + index
    else
      raise UnexpectedIndex if index.nil? == false
      _address
    end
  end

  def self.count
    @@count
  end

  def self.memory
    @@memory
  end

  def self.clear
    @@count = 0
    @@memory = Array.new(300) { nil }
  end

  def delete
    return unless _name.start_with? "temp_"
    @@count -= 1
    @@memory[address] = nil
    $var.tap { |hs| hs.delete(_name) }
    _zero(self)
  end

  def value other
    _copy(other, self)
    self
  end
end

def printMemory
  (0..9).each {|i|
    print "[" + i.to_s.rjust(2,'0').center(9, ' ') + " ]"
  }
  print "\n"
  (0..9).each {|i|
    print "[" + (Variable.memory[i] ?  Variable.memory[i]._name.to_s.center(9, ' ') : " ".center(9,' ') ) + " ]"
  }
  print "\n"
end

def _to s
  raise InvalidTypeArgument unless s.is_a? Variable
  d = ($pointer - s.address).abs
  ($pointer > s.address ? '<' * d : $pointer < s.address ? '>' * d : '').add
  $pointer = s.address
end

def _to_address add
  d = ($pointer - add).abs
  ($pointer > add ? '<' * d : $pointer < add ? '>' * d : '').add
  $pointer = add
end

def _zero s
  raise InvalidTypeArgument unless s.is_a? Variable
  _to(s)
  "[-]".add
end

def _for s
  raise InvalidTypeArgument unless s.is_a? Variable
  _to(s)
  "[".add
end

def _next a
  raise InvalidTypeArgument unless a.is_a? Variable
  _to(a)
  "-]".add
end

def _move(from, to, zero_to = true)
  raise InvalidTypeArgument unless (from.is_a? Variable) and (to.is_a? Variable)
  return if from === to

  _zero(to) if zero_to
  _for(from)
  _to(to); "+".add
  _next(from)
end

def _move2(from, to1, to2)
  raise InvalidTypeArgument unless from.is_a? Variable
  raise InvalidTypeArgument unless to1.is_a? Variable
  raise InvalidTypeArgument unless to2.is_a? Variable
  return if from === to1 or from === to2 or to1 === to2

  _zero(to1)
  _zero(to2)
  _for(from)
  _to(to1); '+'.add
  _to(to2); '+'.add
  _next(from)
end

def _copy(from, to)
  raise InvalidTypeArgument unless to.is_a? Variable
  raise InvalidTypeArgument unless (from.is_a? Variable) or (from.is_a? Integer)
  return if from === to

  if (from.is_a? Integer)

    _from = Variable.new
    _to(_from)
    $code += from > 0 ? '+' * from : '-' * from.abs
    res = _copy(_from, to)
    _from.delete

    return
  end

  temp = Variable.new
  _move2(from, to, temp)
  _move(temp, from)
  temp.delete
end

def _set(res, value)
  _copy(value, res)
end

def _inc_dec(res, val, op)
  raise InvalidTypeArgument if (op.nil?) and (op != '+') and (op != '-')
  _res  = Variable.new.value(res)
  _val  = Variable.new.value(val)

  _for(_val)
  _to(_res); op.add;
  _next(_val)

  _set(res, _res)

  [_res, _val].each {|e| e.delete}
end

def _inc(res, val = 1)
  _inc_dec(res, val, '+')
end

def _dec(res, val = 1)
  _inc_dec(res, val, '-')
end

def _add_sub(res, a, b, op = nil)
  _res = Variable.new

  _set(_res, a)
  _inc_dec(_res, b, op)
  _set(res, _res)

  _res.delete
end

def _add(res, a, b)
  _add_sub(res, a, b, '+')
end

def _sub(res, a, b)
  _add_sub(res, a, b, '-')
end

def _mul(res, a, b)
  _a, _b, _res = Variable.new.value(a), Variable.new.value(b), Variable.new

  _for(_a)
  _inc(_res, _b)
  _next(_a)
  _set(res, _res)
  [_a, _b, _res].each {|e| e.delete}
end

def _divmod(div, mod, num, denom)
  one, isOne, greaterThanOne = Variable.new.value(1), Variable.new, Variable.new

  _equal(isOne, denom, one)
  _greater(greaterThanOne, denom, one)

  _if(isOne)
  _set(div, num)
  _set(mod, 0)
  _endif(isOne)

  x1 = Variable.new(length: 5).value(num)
  x2 = Variable.new(at: x1.address + 1).value(0)
  x3 = Variable.new(at: x1.address + 2).value(denom)
  x4 = Variable.new(at: x1.address + 3).value(0)
  x5 = Variable.new(at: x1.address + 4).value(0)

  _if(greaterThanOne)
  _to(x1)
  "[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]".add
  _set(div, x5)
  _set(mod, x4)
  _endif(greaterThanOne)

  [x1, x2, x3, x4, x5, one, isOne, greaterThanOne].each {|e| e.delete}
end

def _div_or_mod(res, num, denom, calc_div)
  temp0, temp1 = Variable.new, Variable.new

  _divmod(temp0, temp1, num, denom)
  _set(res, (calc_div ? temp0 : temp1))

  [temp0, temp1].each {|e| e.delete}
end

def _div(res, num, denom)
  _div_or_mod(res, num, denom, true)
end

def _mod(res, num, denom)
  _div_or_mod(res, num, denom, false)
end

def _if a
  _to(a); '['.add
end

def _endif a
  _zero(a); ']'.add
end

def _or(res, a, b)
  _add(res, a, b)
end

def _and(res, a, b)
  _a, _b, _res = Variable.new.value(a), Variable.new.value(b), Variable.new

  _if(_a)
  _move(_b, _res)
  _endif(_a)
  _set(res, _res)

  [_a, _b, _res].each { |e| e.delete }
end

def _subtract_minimum(a, b, na, nb)
  _set(na, a); _set(nb, b)
  t1, t2, t3 = Variable.new, Variable.new, Variable.new

  _set(t1, na); _set(t2, nb); _and(t3, t1, t2)
  _to(t3); '['.add
  _zero(t3)
  _dec(na); _dec(nb)
  _set(t1, na); _set(t2, nb); _and(t3, t1, t2)
  _to(t3); ']'.add

  [t1, t2, t3].each { |e| e.delete  }
end

def _not(res, a)
  _a = Variable.new.value(a)

  _set(res, 1)
  _if(_a)
  _dec(res)
  _endif(_a)

  _a.delete
end

def _not_equal(res, a, b)
  na, nb = Variable.new, Variable.new

  _subtract_minimum(a, b, na, nb)
  _or(res, na, nb)

  [na, nb].each {|e| e.delete}
end

def _equal(res, a, b)
  _res = Variable.new

  _not_equal(_res, a, b)
  _not(res, _res)

  _res.delete
end

def _greater(res, a, b)
  na, nb = Variable.new, Variable.new

  _subtract_minimum(a, b, na, nb)
  _move(na, res)

  [na, nb].each { |e| e.delete }
end

def _less(res, a, b)
  na, nb = Variable.new, Variable.new

  _subtract_minimum(a, b, na, nb)
  _move(nb, res)

  [na, nb].each { |e| e.delete }
end

def _cmp(res, a, b)
  _zero(res)

  greater, less = Variable.new, Variable.new

  _greater(greater, a, b)
  _less(less, a, b)

  _if(greater)
  _inc(res)
  _endif(greater)

  _if(less)
  _dec(res)
  _endif(less)

  [greater, less].each { |e| e.delete }
end

def _a2b(res, a, b, c)
  _a, _b, _c = Variable.new, Variable.new, Variable.new

  _sub(_a, a, 48)
  _mul(_a, _a, 100)

  _sub(_b, b, 48)
  _mul(_b, _b, 10)

  _sub(_c, c, 48)
  _zero(res)
  _add(res, _a, _b)
  _add(res, res, _c)
  [_a, _b, _c].each { |e| e.delete }
end

def _b2a(b, c, d, a)
  _b, _c, _d = Variable.new, Variable.new, Variable.new

  _div(_b, a, 100)
  _inc(_b, 48)

  _div(_c, a, 10)
  _mod(_c, _c, 10)
  _inc(_c, 48)

  _mod(_d, a, 10)
  _inc(_d, 48)

  _set(b,_b)
  _set(c, _c)
  _set(d, _d)

  [_b, _c, _d].each { |e| e.delete }
end

def _read a
  _to(a)
  ','.add
end

def _msg tokens
  if $string_mode == false
    a = get_var(tokens)

    raise ExpectedVar unless a.type == :single_var
    _to(a)
    '.'.add
  else

    a = tokens.shift_space.gsub(/\\n/, "\n").gsub(/\\t/, "\t")
    a.chars.each {|c|
      x = Variable.new.value(c.ord)
      _to(x)
      '.'.add
      x.delete
    }
  end
end

def get_var tokens, context = nil
  context = $stack_context.last if context.nil?
  val = tokens.shift_space.downcase
  if context == 'main'
    raise MissingArgument if val == EOL
    raise InvalidVarName, "got #{val}" unless val =~ MATCH_VAR_NAME
    raise UndefinedVariableError, "got #{val}" unless $var.has_key? val
    raise UnexpectedList if $var[val].type == :list_var
    $var[val]
  else
    pr = $procs[context]
    if pr.args.include? val
      pr.params[pr.args.index(val)]
    else
      raise InvalidVarName, "got #{val}" unless val =~ MATCH_VAR_NAME
      raise UndefinedVariableError, "got #{val}" unless $var.has_key? val
      raise UnexpectedList if $var[val].type == :list_var
      $var[val]
    end
  end
end

def get_char tokens
  tokens.shift
  raise InvalidNumberLiterals if tokens.first.size != 1
  val = tokens.shift.ord
  raise MismatchedCharQuoteError if tokens.shift != "'"
  val
end

def get_var_or_number tokens
  raise MissingArgument if tokens.first_space == EOL
  return get_char tokens if tokens.first_space == "'"
  raise ExpectedVarOrNumber, "but got #{val}" unless tokens.first_space =~ VAR_NAME_OR_NUMBER
  return truth_value(tokens.shift_space) if tokens.first_space =~ WHOLE_NUMBER
  get_var tokens
end

def get_argument(tokens, *arg)
  n_var, n_number, var_first = arg
  vars = []
  numbers = []

  if var_first
    n_var   .times {vars  <<= get_var tokens  }
    n_number.times {numbers <<= get_var_or_number tokens  }
  else
    n_number.times {numbers <<= get_var_or_number tokens  }
    n_var   .times {vars  <<= get_var tokens  }
  end
  vars + numbers
end

def get_list tokens
  val = tokens.shift_space.downcase
  raise MissingArgument if val == EOL
  raise ExpectedListName, "but got #{val}" unless val =~ MATCH_VAR_NAME
  raise UndefinedVariableError, "got #{val}" unless $var.has_key? val
  raise UnexpectedVar unless $var[val].type == :list_var
  $var[val]
end

def var_instruction tokens
  tokens.shift_space
  raise DefineVariableInsideProc if $stack_context.last != 'main'
  raise UnexpectedNumber if tokens.first_space =~ WHOLE_NUMBER
  raise InvalidVarName if tokens.first_space =~ COMMENT
  while tokens.first_space != EOL
    next tokens.shift_space if tokens.first_space =~ COMMENT or tokens.first_space =~ TAB or tokens.first_space =~ SPACE
    raise MismatchedParenthesesError if tokens.first_space =~ CLOSE_SQUARE or tokens.first_space =~ OPEN_SQUARE
    raise UnexpectedNumber, "when parsing #{tokens.first_space}" if tokens.first_space =~ WHOLE_NUMBER
    raise InvalidVarName, "got #{tokens.first_space}" unless tokens.first_space =~ MATCH_VAR_NAME
    Variable.new(raw: tokens.shift_space.downcase, tokens: tokens)
  end
  raise ExpectedEndOfLine if tokens.shift_space != EOL
end

class Procedure
  attr_accessor :name, :args, :body, :params
  def initialize(name)
    raise DuplicateProcError, "program has already proc name #{name}" if $procs.has_key? name
    @name = name
    @args = []
    @params = []
    @body = []
    $procs[name] = self
    self
  end

  def add_arg arg_name
    raise DuplicateArgumentName if @args.include? arg_name
    @args <<= arg_name
  end

  def run_proc
    raise MismatchNumberArgument unless params.size == args.size
    raise RecursiveCalling if $stack_context.include? @name
    $stack_context.push @name
    _run @body.clone
    $stack_context.pop
  end
end

def proc_instruction tokens
  tokens.shift_space
  pr = Procedure.new(tokens.shift_space.downcase)
  raise UnexpectedNumber if tokens.first_space =~ WHOLE_NUMBER
  raise InvalidVarName if tokens.first_space =~ COMMENT
  while tokens.first_space != EOL
    next tokens.shift_space if tokens.first_space =~ COMMENT or tokens.first_space =~ TAB or tokens.first_space =~ SPACE
    raise UnexpectedEndInstruction if tokens.first_space =~ CLOSE_SQUARE or tokens.first_space =~ OPEN_SQUARE
    raise UnexpectedNumber, "when parsing #{tokens.first_space}" if tokens.first_space =~ WHOLE_NUMBER
    raise InvalidVarName, "got #{tokens.first_space} #{tokens}" unless tokens.first_space =~ MATCH_VAR_NAME
    pr.add_arg tokens.shift_space.downcase
  end
  raise DefineVariableInsideProc if tokens.map(&:downcase).include? "var"
  pr.body = tokens[0...tokens.rindex {|t| t.downcase == 'end'}]
end

def basic_instruction tokens
  ins = tokens.shift_space
  args = get_argument(tokens, *NUMBER_COMPONENT_INS[ins])
  raise ExpectedEndOfLine if tokens.shift_space != EOL
  send("_#{ins}", *args)
end

def _lset(list, ind, val)
  y, z = Variable.new.value(ind), Variable.new.value(val)
  space, data, index1, index2 = list.space, list.data, list.index1, list.index2
  [space, data, index1, index2].each {|x| _zero(x)}
  eval "z[-space+data+z]space[-z+space]
        y[-space+index1+y]space[-y+space]
        y[-space+index2+y]space[-y+space]
        >[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]
        >>>[-]<[->+<]<
        [[-<+>]<<<[->>>>+<<<<]>>-]<<"
        .gsub(/\w+/) { |m| m == "add" ? m : "_to(#{m}); "}
        .gsub(/[\<\>\[\]\+\-]+/) { |m| "\"#{m}\".add; "}
  $pointer = space._address
  [y, z].each {|x| x.delete}
end

def _lget(list, ind, val)
  x, y, z = val, list, Variable.new.value(ind)
  space, data, index1, index2 = list.space, list.data, list.index1, list.index2
  [space, data, index1, index2].each {|e| _zero(e)}
  eval "z[-space+index1+z]space[-z+space]
        z[-space+index2+z]space[-z+space]
        >[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]
        >>>[-<+<<+>>>]<<<[->>>+<<<]>
        [[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<
        x[-]
        data[-x+data]"
        .gsub(/\w+/) { |m| m == "add" ? m : "_to(#{m}); "}
        .gsub(/[\<\>\[\]\+\-]+/) { |m| "\"#{m}\".add; "}
  $pointer = data._address
  z.delete
end

def lset_instruction tokens
  tokens.shift_space
  list = get_list tokens
  ind = get_var_or_number tokens
  val = get_var_or_number tokens
  _lset(list, ind, val)
end

def lget_instruction tokens
  tokens.shift_space
  list = get_list tokens
  ind = get_var_or_number tokens
  val = get_var tokens
  _lget(list, ind, val)
end

def rem_instruction tokens
  nil while tokens.shift_space != EOL
end

def read_instruction tokens
  tokens.shift_space
  _read get_var tokens
end

def msg_instruction tokens
  tokens.shift_space
  while tokens.first_space != EOL
    tokens.first_space
    next tokens.shift_space if tokens.first_space =~ COMMENT and $string_mode == false
    if tokens.first_space =~ STRING_QUOTE
      $string_mode = !$string_mode
      next tokens.shift_space
    end
    _msg(tokens)
  end
  raise MismatchedStringQuoteError if $string_mode
end

def _ifeq a, b
  _equal(c = Variable.new, a, b)
  _to(c); "[".add
  $stack_ins <<= [c, __method__.to_sym]
  c.delete
end

def _ifneq a, b
  _not_equal(c = Variable.new, a, b)
  _to(c); "[".add
  $stack_ins <<= [c, __method__.to_sym]
end

def _wneq a, b
  c = Variable.new
  _not_equal(c, a, b)
  _to(c); "[".add
  $stack_ins <<= [c, a, b, __method__.to_sym]
end

def _end tokens
  tokens.shift_space
  raise UnexpectedEndInstruction if $stack_ins.empty?
  val, *args, type = $stack_ins.pop
  if type == :_ifeq or type == :_ifneq
    _to(val)
    _zero(val)
  elsif type == :_wneq
    _not_equal(val,*args)
    _to(val)
  end
  "]".add
end

def call_instruction tokens
  tokens.shift_space
  pr_name = tokens.shift_space.downcase

  raise UndefinedProcedure, "got #{pr_name}" unless $procs.has_key? pr_name
  pr = $procs[pr_name]
  pr.params.clear
  while tokens.first_space != EOL
    next tokens.shift_space if tokens.first_space =~ COMMENT or tokens.first_space =~ TAB or tokens.first_space =~ SPACE
    raise InvalidVarName, "got #{tokens.first_space}" unless tokens.first_space =~ MATCH_VAR_NAME
    pr.params <<= get_var tokens
  end
  pr.run_proc
end

def control_instruciton tokens
  ins = tokens.shift_space
  return (_end tokens) if ins == 'end'
  args = get_argument(tokens, *NUMBER_COMPONENT_INS[ins])
  raise ExpectedEndOfLine if tokens.shift_space != EOL
  send("_#{ins}", *args)
end

def get_proc tokens
  proc_mode = false
  deep = 0
  will_del = []
  tokens.each.with_index {|t,i|
    if t.downcase == 'proc'
      raise NestedProcedure if proc_mode
      proc_mode = true
      $proc_tokens <<= [t]
      will_del <<= i
      deep += 1
      next
    end

    if proc_mode
      $proc_tokens.last.push t
      will_del <<= i
    end

    if t.downcase == 'end'
      deep -= 1
      raise UnexpectedEndInstruction if deep < 0
      proc_mode = false if proc_mode and deep == 0
      next
    end

    deep += 1if CONTROL_INSTRUCTION.include?(t.downcase) and t != 'call'
  }
  will_del.reverse.each {|i| tokens.delete_at(i)}
  $proc_tokens.each {|pr| proc_instruction pr}
end

def run plain_code
  $var = {}
  $pointer = 0
  $code = ''
  $procs = {}
  $proc_tokens = []
  $stack_ins = []
  $string_mode = false
  $stack_context  = ['main']

  Variable.clear
  tokens = plain_code.scan(TOKEN)
  tokens <<= EOL if tokens.last != EOL
  tokens <<= EOF
  get_proc tokens
  _run tokens
end

def _run tokens
  while tokens.first_space != EOF
    return if tokens.empty?
    tokens.first_space.downcase!
    next tokens.shift_space if tokens.first_space == EOL or tokens.first_space =~ TAB or tokens.first_space =~ COMMENT or tokens.first_space =~ SPACE
    raise UnknownInstruction, "unknown #{tokens.first_space} instruction" unless tokens.first_space =~ INSTRUCTION
    next basic_instruction tokens if BASIC_INSTRUCTION.include? tokens.first_space
    next control_instruciton tokens if CONTROL_INSTRUCTION.include? tokens.first_space
    send("#{tokens.first_space}_instruction", tokens)
  end
  raise UnclosedBlock unless $stack_ins.empty?
  $code
end

def kcuf plain_code
  run plain_code
end
2 similar code variations are grouped with this one
Show Variations
Best Practices0Clever0
0ForkLink
Glyxerine
# require 'rspec'
# require_relative 'brainruby.rb'
# require 'ruby-prof'



NUMBER_LITERALS = (('a'..'z').to_a + ('A'..'Z').to_a + ('0'..'9').to_a).map { |e| "'" + e + "'" } + (-100..300).to_a

COMMENT_PREFIX          = /\/\/|--|#/
COMMENT                 = /#{COMMENT_PREFIX}[^"\n]*$/
TAB                     = /\t/
CHAR_ELEMENT            = /[^\,\"\\]|\\\\|\\'|\\"|\\n|\\r|\\t/
CHAR_QUOTE              = /'/
CHAR                    = /#{CHAR_QUOTE}#{CHAR_ELEMENT}#{CHAR_QUOTE}/
NUMBER                  = /-\d+|\d+|#{CHAR}/
WHOLE_NUMBER            = /^#{NUMBER}$/
STRING_QUOTE            = /"/
STRING                  = /"#{CHAR_ELEMENT}*"/
SPACE                   = /\s/
OPEN_SQUARE             = /\[/
CLOSE_SQUARE            = /\]/

VAR_PREFIX              = /\$|_|[a-zA-Z]/
VAR_SUFFIX              = /#{VAR_PREFIX}|\d/
VAR_NAME                = /#{VAR_PREFIX}#{VAR_SUFFIX}*/
MATCH_VAR_NAME          = /^#{VAR_NAME}$/
VAR_NAME_OR_NUMBER      = /#{VAR_NAME}|#{NUMBER}/
VAR_NAME_OR_STRING      = /#{VAR_NAME}|#{STRING}/

BASIC_INSTRUCTION       = ['set', 'inc', 'dec', 'add', 'sub', 'mul', 'divmod', 'div', 'mod', 'cmp', 'a2b', 'b2a']
LIST_INSTRUCTION        = ['lset','lget']
CONTROL_INSTRUCTION     = ['ifeq','ifneq','wneq','proc','end']
CALL_INSTRUCTION        = ['call']
INTERACTIVE_INSTRUCTION = ['msg', 'read']

INSTRUCTION = /var|set|inc|dec|add|sub|mul|divmod|div|mod|cmp|a2b|b2a|lset|lget|ifeq|ifneq|wneq|proc|end|call|read|msg|rem/


EOL                     = "\n"
EOF                     = "#END#"
WORD                    = /[^ \n\[\]]+/
TOKEN                   = Regexp.union(COMMENT, TAB, NUMBER, VAR_NAME, CHAR_ELEMENT, STRING_QUOTE, SPACE, INSTRUCTION, OPEN_SQUARE, CLOSE_SQUARE, WORD, NUMBER, EOL, EOF)

BRAIN_FUCK_CHAR         = "<>+-[],.".split('')

NUMBER_COMPONENT_INS  = {
  'set'     => [1, 1, true  ],
  'inc'     => [1, 1, true  ],
  'dec'     => [1, 1, true  ],
  'add'     => [1, 2, false ],
  'sub'     => [1, 2, false ],
  'mul'     => [1, 2, false ],
  'div'     => [1, 2, false ],
  'mod'     => [1, 2, false ],
  'cmp'     => [1, 2, false ],
  'divmod'  => [2, 2, false ],
  'a2b'     => [1, 3, false ],
  'b2a'     => [3, 1, false ],
  'ifeq'    => [1, 1, true  ],
  'ifneq'   => [1, 1, true  ],
  'wneq'    => [1, 1, true  ]
}
$code = ''
$pointer = 0
$proc_tokens = []
$stack_ins = []
$string_mode = false
$var = {}
$procs = {}
$stack_context  = ['main']

puts "Finish initialize"

class ParsingError < StandardError; end

class ExpectedEndOfLine           < ParsingError; end
class ExpectedIndex               < ParsingError; end
class ExpectedListName            < ParsingError; end
class ExpectedNumber              < ParsingError; end
class ExpectedVar                 < ParsingError; end
class ExpectedVariableInstance    < ParsingError; end
class ExpectedVarOrNumber         < ParsingError; end
class ExpectedVarSingle           < ParsingError; end
class InvalidNumberLiterals       < ParsingError; end
class InvalidVarName              < ParsingError; end
class MismatchedParenthesesError  < ParsingError; end
class MismatchedStringQuoteError  < ParsingError; end
class MismatchedCharQuoteError    < ParsingError; end
class MismatchNumberArgument      < ParsingError; end
class MissingArgument             < ParsingError; end
class NestedProcedure             < ParsingError; end
class UnclosedBlock               < ParsingError; end
class UnexpectedEndInstruction    < ParsingError; end
class UnexpectedEndOfLine         < ParsingError; end
class UnexpectedList              < ParsingError; end
class UnexpectedNumber            < ParsingError; end
class UnexpectedVar               < ParsingError; end
class UnexpectedParenthese        < ParsingError; end
class UnknownInstruction          < ParsingError; end
class DuplicateArgumentName       < ParsingError; end
class UndefinedProcedure          < ParsingError; end
class RecursiveCalling            < ParsingError; end
class DefineVariableInsideProc    < ParsingError; end
class CollapseArgument            < StandardError; end
class DeleteUntempVariable        < StandardError; end
class DuplicateVariableError      < StandardError; end
class DuplicateProcError          < StandardError; end
class InvalidTypeArgument         < StandardError; end
class NotEnoughSpaceForVariable   < StandardError; end
class OutOfRangeList              < StandardError; end
class UndefinedVariableError      < StandardError; end
class UnexpectedIndex             < StandardError; end
class UnmatchNumberArgument       < StandardError; end


def random
  NUMBER_LITERALS.sample
end

def truth_value val
  val =~ CHAR ? val[1].ord : val.to_i % 256
end

class String
  def add
    $code += self
  end
end

class Integer
  def _v
    self
  end

  def wrap
    self % 256
  end
end

class Array
  def shift_space
    while $string_mode == false and first == " "
      # p first
      shift
    end
    shift
  end

  def first_space
    while $string_mode == false and self.first == " "
      shift
    end
    first
  end
end

class Variable
  @@count = 0
  @@memory = Array.new (300) { nil }
  attr_accessor :_name, :length, :type, :_address, :space, :data, :index1, :index2

  def initialize(raw: nil, at: nil, length: 1, tokens: nil)
    raise NotEnoughSpaceForVariable if at.nil? == false and @@memory[at,length].any?
    if raw.nil? or (raw.is_a? Integer)
      @_address = at ? at : self.class.emptyIndex(length)
      @_name = "temp_#{_address}"
      @@count += 1
      $var[@_name] = @@memory[@_address] = self
      @length, @type = nil, :single_var
      _set(self, raw) if (raw.is_a? Integer)
      return self
    end

    @_name, @length, @type, @_address = raw, 1, :single_var, at.nil? ? self.class.emptyIndex : at

    raise DuplicateVariableError, "Already has variable name: #{@_name}" if ($var.has_key? @_name)

    $var[@_name] = self
    @@memory[@_address] = self
    @@count += 1

    try_parse_list tokens if tokens
    self
  end

  def try_parse_list tokens
    return unless tokens.first_space =~ OPEN_SQUARE
    tokens.shift_space
    raise ExpectedNumber unless tokens.first_space =~ WHOLE_NUMBER
    @length = get_var_or_number tokens
    @@memory[@_address] = nil
    @_address = Variable.emptyIndex(@length + 4)
    @type = :list_var
    @space  = Variable.new(raw: "#{@_name}__space",   at: @_address)
    @index1 = Variable.new(raw: "#{@_name}__index1",  at: @_address + 1)
    @index2 = Variable.new(raw: "#{@_name}__index2",  at: @_address + 2)
    @data   = Variable.new(raw: "#{@_name}__data",    at: @_address + 3)
    @@memory[@_address + 4, @length] = Array.new(@length) { |i| Variable.new(raw: "#{@_name}__#{i}") }
    raise MismatchedParenthesesError unless tokens.shift_space =~ CLOSE_SQUARE
  end

  def self.emptyIndex(length = 1)
    @@memory.each_cons(length).find_index {|slice| slice.none?}
  end

  def address(index = nil)
    if type == :list_var
      raise ExpectedNumber if (index.is_a? (Integer)) == false
      raise OutOfRangeList unless (0...length) === index
      _address + index
    else
      raise UnexpectedIndex if index.nil? == false
      _address
    end
  end

  def self.count
    @@count
  end

  def self.memory
    @@memory
  end

  def self.clear
    @@count = 0
    @@memory = Array.new(300) { nil }
  end

  def delete
    return unless _name.start_with? "temp_"
    @@count -= 1
    @@memory[address] = nil
    $var.tap { |hs| hs.delete(_name) }
    _zero(self)
  end

  def value other
    _copy(other, self)
    self
  end
end

def printMemory
  (0..9).each {|i|
    print "[" + i.to_s.rjust(2,'0').center(9, ' ') + " ]"
  }
  print "\n"
  (0..9).each {|i|
    print "[" + (Variable.memory[i] ?  Variable.memory[i]._name.to_s.center(9, ' ') : " ".center(9,' ') ) + " ]"
  }
  print "\n"
end

def _to s
  raise InvalidTypeArgument unless s.is_a? Variable
  d = ($pointer - s.address).abs
  ($pointer > s.address ? '<' * d : $pointer < s.address ? '>' * d : '').add
  $pointer = s.address
end

def _to_address add
  d = ($pointer - add).abs
  ($pointer > add ? '<' * d : $pointer < add ? '>' * d : '').add
  $pointer = add
end

def _zero s
  raise InvalidTypeArgument unless s.is_a? Variable
  _to(s)
  "[-]".add
end

def _for s
  raise InvalidTypeArgument unless s.is_a? Variable
  _to(s)
  "[".add
end

def _next a
  raise InvalidTypeArgument unless a.is_a? Variable
  _to(a)
  "-]".add
end

def _move(from, to, zero_to = true)
  # pos: from = 0; to = old_from + (to if zero_to == false)
  raise InvalidTypeArgument unless (from.is_a? Variable) and (to.is_a? Variable)
  return if from === to

  _zero(to) if zero_to
  _for(from)
  _to(to); "+".add
  _next(from)
end

def _move2(from, to1, to2)
  # pos: from = 0; to1 = to2 = old_from
  raise InvalidTypeArgument unless from.is_a? Variable
  raise InvalidTypeArgument unless to1.is_a? Variable
  raise InvalidTypeArgument unless to2.is_a? Variable
  return if from === to1 or from === to2 or to1 === to2

  _zero(to1)
  _zero(to2)
  _for(from)
  _to(to1); '+'.add
  _to(to2); '+'.add
  _next(from)

  # to1._v = to2._v = from._v
  # from._v = 0
end

def _copy(from, to)
  # pos: to = value_at_from if from === Variable or
  #      to = form          if from === Integer
  raise InvalidTypeArgument unless to.is_a? Variable
  raise InvalidTypeArgument unless (from.is_a? Variable) or (from.is_a? Integer)
  return if from === to

  if (from.is_a? Integer)

    _from = Variable.new
    _to(_from)
    $code += from > 0 ? '+' * from : '-' * from.abs
    res = _copy(_from, to)
    _from.delete

    return
  end

  temp = Variable.new
  _move2(from, to, temp)
  _move(temp, from)
  temp.delete
end

def _set(res, value)
  _copy(value, res)
end

def _inc_dec(res, val, op)
  raise InvalidTypeArgument if (op.nil?) and (op != '+') and (op != '-')
  _res  = Variable.new.value(res)
  _val  = Variable.new.value(val)

  _for(_val)
  _to(_res); op.add;
  _next(_val)

  _set(res, _res)

  [_res, _val].each {|e| e.delete}
end

def _inc(res, val = 1)
  _inc_dec(res, val, '+')
end

def _dec(res, val = 1)
  _inc_dec(res, val, '-')
end

def _add_sub(res, a, b, op = nil)
  _res = Variable.new

  _set(_res, a)
  _inc_dec(_res, b, op)
  _set(res, _res)

  _res.delete
end

def _add(res, a, b)
  _add_sub(res, a, b, '+')
end

def _sub(res, a, b)
  _add_sub(res, a, b, '-')
end

def _mul(res, a, b)

  # res._v = (a._v * b._v).wrap
  _a, _b, _res = Variable.new.value(a), Variable.new.value(b), Variable.new

  _for(_a)
  _inc(_res, _b)
  _next(_a)
  _set(res, _res)
  [_a, _b, _res].each {|e| e.delete}
end

def _divmod(div, mod, num, denom)
  # p [div, mod, num, denom]
  one, isOne, greaterThanOne = Variable.new.value(1), Variable.new, Variable.new

  _equal(isOne, denom, one)
  _greater(greaterThanOne, denom, one)

  _if(isOne)
  _set(div, num)
  _set(mod, 0)
  _endif(isOne)

  x1 = Variable.new(length: 5).value(num)
  x2 = Variable.new(at: x1.address + 1).value(0)
  x3 = Variable.new(at: x1.address + 2).value(denom)
  x4 = Variable.new(at: x1.address + 3).value(0)
  x5 = Variable.new(at: x1.address + 4).value(0)

  _if(greaterThanOne)
  _to(x1)
  "[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]".add
  _set(div, x5)
  _set(mod, x4)
  _endif(greaterThanOne)

  [x1, x2, x3, x4, x5, one, isOne, greaterThanOne].each {|e| e.delete}
end

def _div_or_mod(res, num, denom, calc_div)
  temp0, temp1 = Variable.new, Variable.new

  _divmod(temp0, temp1, num, denom)
  _set(res, (calc_div ? temp0 : temp1))

  [temp0, temp1].each {|e| e.delete}
end

def _div(res, num, denom)
  _div_or_mod(res, num, denom, true)
end

def _mod(res, num, denom)
  _div_or_mod(res, num, denom, false)
end

def _if a
  _to(a); '['.add
end

def _endif a
  _zero(a); ']'.add
end

def _or(res, a, b)
  _add(res, a, b)
end

def _and(res, a, b)
  _a, _b, _res = Variable.new.value(a), Variable.new.value(b), Variable.new

  _if(_a)
  _move(_b, _res)
  _endif(_a)
  _set(res, _res)

  [_a, _b, _res].each { |e| e.delete }
end

def _subtract_minimum(a, b, na, nb)
  _set(na, a); _set(nb, b)
  t1, t2, t3 = Variable.new, Variable.new, Variable.new

  _set(t1, na); _set(t2, nb); _and(t3, t1, t2)
  _to(t3); '['.add
  _zero(t3)
  _dec(na); _dec(nb)
  _set(t1, na); _set(t2, nb); _and(t3, t1, t2)
  _to(t3); ']'.add

  [t1, t2, t3].each { |e| e.delete  }
end

def _not(res, a)
  _a = Variable.new.value(a)

  _set(res, 1)
  _if(_a)
  _dec(res)
  _endif(_a)

  _a.delete
end

def _not_equal(res, a, b)
  na, nb = Variable.new, Variable.new

  _subtract_minimum(a, b, na, nb)
  _or(res, na, nb)

  [na, nb].each {|e| e.delete}
end

def _equal(res, a, b)
  _res = Variable.new

  _not_equal(_res, a, b)
  _not(res, _res)

  _res.delete
end

def _greater(res, a, b)
  na, nb = Variable.new, Variable.new

  _subtract_minimum(a, b, na, nb)
  _move(na, res)

  [na, nb].each { |e| e.delete }
end

def _less(res, a, b)
  na, nb = Variable.new, Variable.new

  _subtract_minimum(a, b, na, nb)
  _move(nb, res)

  [na, nb].each { |e| e.delete }
end

def _cmp(res, a, b)
  _zero(res)

  greater, less = Variable.new, Variable.new

  _greater(greater, a, b)
  _less(less, a, b)

  _if(greater)
  _inc(res)
  _endif(greater)

  _if(less)
  _dec(res)
  _endif(less)

  [greater, less].each { |e| e.delete }

  # res._v = [0, 1, 255][a._v <=> b._v]
end

def _a2b(res, a, b, c)
  _a, _b, _c = Variable.new, Variable.new, Variable.new

  _sub(_a, a, 48)
  _mul(_a, _a, 100)

  _sub(_b, b, 48)
  _mul(_b, _b, 10)

  _sub(_c, c, 48)
  _zero(res)
  _add(res, _a, _b)
  _add(res, res, _c)
  [_a, _b, _c].each { |e| e.delete }
end

def _b2a(b, c, d, a)
  _b, _c, _d = Variable.new, Variable.new, Variable.new

  _div(_b, a, 100)
  _inc(_b, 48)

  _div(_c, a, 10)
  _mod(_c, _c, 10)
  _inc(_c, 48)

  _mod(_d, a, 10)
  _inc(_d, 48)

  _set(b,_b)
  _set(c, _c)
  _set(d, _d)

  [_b, _c, _d].each { |e| e.delete }
  # t = a._v
  # b._v = 48 + (t / 100)
  # c._v = 48 + (t / 10 % 10)
  # d._v = 48 + (t % 10)
  # [b, c, d].each {|e| e._v = e._v.wrap}
end

def _read a
  _to(a)
  ','.add
end

def _msg tokens
  # p tokens

  if $string_mode == false
    a = get_var(tokens)

    raise ExpectedVar unless a.type == :single_var
    _to(a)
    '.'.add
  else

    a = tokens.shift_space.gsub(/\\n/, "\n").gsub(/\\t/, "\t")
    # p "--->", a
    # p [a, a.ord]
    a.chars.each {|c|
      x = Variable.new.value(c.ord)
      _to(x)
      '.'.add
      x.delete
    }
  end
end

def get_var tokens, context = nil
  # p "get_var #{tokens}"
  context = $stack_context.last if context.nil?
  val = tokens.shift_space.downcase
  if context == 'main'
    raise MissingArgument if val == EOL
    raise InvalidVarName, "got #{val}" unless val =~ MATCH_VAR_NAME
    raise UndefinedVariableError, "got #{val}" unless $var.has_key? val
    raise UnexpectedList if $var[val].type == :list_var
    $var[val]
  else
    pr = $procs[context]
    if pr.args.include? val
      pr.params[pr.args.index(val)]
    else
      raise InvalidVarName, "got #{val}" unless val =~ MATCH_VAR_NAME
      raise UndefinedVariableError, "got #{val}" unless $var.has_key? val
      raise UnexpectedList if $var[val].type == :list_var
      $var[val]
    end
  end
end

def get_char tokens
  tokens.shift
  raise InvalidNumberLiterals if tokens.first.size != 1
  val = tokens.shift.ord
  raise MismatchedCharQuoteError if tokens.shift != "'"
  val
end

def get_var_or_number tokens
  raise MissingArgument if tokens.first_space == EOL
  return get_char tokens if tokens.first_space == "'"
  raise ExpectedVarOrNumber, "but got #{val}" unless tokens.first_space =~ VAR_NAME_OR_NUMBER
  return truth_value(tokens.shift_space) if tokens.first_space =~ WHOLE_NUMBER
  get_var tokens
end

def get_argument(tokens, *arg)
  # p "get_argument #{tokens[0..tokens.index(EOL)]} context #{$stack_context.last}"
  n_var, n_number, var_first = arg
  vars = []
  numbers = []

  if var_first
    n_var   .times {vars  <<= get_var tokens  }
    n_number.times {numbers <<= get_var_or_number tokens  }
  else
    n_number.times {numbers <<= get_var_or_number tokens  }
    n_var   .times {vars  <<= get_var tokens  }
  end
  vars + numbers
end

def get_list tokens
  val = tokens.shift_space.downcase
  raise MissingArgument if val == EOL
  raise ExpectedListName, "but got #{val}" unless val =~ MATCH_VAR_NAME
  raise UndefinedVariableError, "got #{val}" unless $var.has_key? val
  raise UnexpectedVar unless $var[val].type == :list_var
  $var[val]
end

def var_instruction tokens
  tokens.shift_space
  raise DefineVariableInsideProc if $stack_context.last != 'main'
  raise UnexpectedNumber if tokens.first_space =~ WHOLE_NUMBER
  raise InvalidVarName if tokens.first_space =~ COMMENT
  while tokens.first_space != EOL
    next tokens.shift_space if tokens.first_space =~ COMMENT or tokens.first_space =~ TAB or tokens.first_space =~ SPACE
    raise MismatchedParenthesesError if tokens.first_space =~ CLOSE_SQUARE or tokens.first_space =~ OPEN_SQUARE
    raise UnexpectedNumber, "when parsing #{tokens.first_space}" if tokens.first_space =~ WHOLE_NUMBER
    raise InvalidVarName, "got #{tokens.first_space}" unless tokens.first_space =~ MATCH_VAR_NAME
    Variable.new(raw: tokens.shift_space.downcase, tokens: tokens)
  end
  raise ExpectedEndOfLine if tokens.shift_space != EOL
end

class Procedure
  attr_accessor :name, :args, :body, :params
  def initialize(name)
    raise DuplicateProcError, "program has already proc name #{name}" if $procs.has_key? name
    @name = name
    @args = []
    @params = []
    @body = []
    $procs[name] = self
    self
  end

  def add_arg arg_name
    raise DuplicateArgumentName if @args.include? arg_name
    @args <<= arg_name
  end

  def run_proc
    raise MismatchNumberArgument unless params.size == args.size
    raise RecursiveCalling if $stack_context.include? @name
    $stack_context.push @name
    _run @body.clone
    $stack_context.pop
  end
end

def proc_instruction tokens
  tokens.shift_space
  pr = Procedure.new(tokens.shift_space.downcase)
  raise UnexpectedNumber if tokens.first_space =~ WHOLE_NUMBER
  raise InvalidVarName if tokens.first_space =~ COMMENT
  while tokens.first_space != EOL
    next tokens.shift_space if tokens.first_space =~ COMMENT or tokens.first_space =~ TAB or tokens.first_space =~ SPACE
    raise UnexpectedEndInstruction if tokens.first_space =~ CLOSE_SQUARE or tokens.first_space =~ OPEN_SQUARE
    raise UnexpectedNumber, "when parsing #{tokens.first_space}" if tokens.first_space =~ WHOLE_NUMBER
    raise InvalidVarName, "got #{tokens.first_space} #{tokens}" unless tokens.first_space =~ MATCH_VAR_NAME
    pr.add_arg tokens.shift_space.downcase
  end
  raise DefineVariableInsideProc if tokens.map(&:downcase).include? "var"
  pr.body = tokens[0...tokens.rindex {|t| t.downcase == 'end'}]
end

def basic_instruction tokens
  # puts "Running: #{tokens[0...tokens.index(EOL)].join} in #{$stack_context.last} context "
  ins = tokens.shift_space
  args = get_argument(tokens, *NUMBER_COMPONENT_INS[ins])
  raise ExpectedEndOfLine if tokens.shift_space != EOL
  send("_#{ins}", *args)
end

def _lset(list, ind, val)
  y, z = Variable.new.value(ind), Variable.new.value(val)
  space, data, index1, index2 = list.space, list.data, list.index1, list.index2
  [space, data, index1, index2].each {|x| _zero(x)}
  eval "z[-space+data+z]space[-z+space]
        y[-space+index1+y]space[-y+space]
        y[-space+index2+y]space[-y+space]
        >[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]
        >>>[-]<[->+<]<
        [[-<+>]<<<[->>>>+<<<<]>>-]<<"
        .gsub(/\w+/) { |m| m == "add" ? m : "_to(#{m}); "}
        .gsub(/[\<\>\[\]\+\-]+/) { |m| "\"#{m}\".add; "}
  $pointer = space._address
  [y, z].each {|x| x.delete}
end

def _lget(list, ind, val)
  x, y, z = val, list, Variable.new.value(ind)
  space, data, index1, index2 = list.space, list.data, list.index1, list.index2
  [space, data, index1, index2].each {|e| _zero(e)}
  eval "z[-space+index1+z]space[-z+space]
        z[-space+index2+z]space[-z+space]
        >[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]
        >>>[-<+<<+>>>]<<<[->>>+<<<]>
        [[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<
        x[-]
        data[-x+data]"
        .gsub(/\w+/) { |m| m == "add" ? m : "_to(#{m}); "}
        .gsub(/[\<\>\[\]\+\-]+/) { |m| "\"#{m}\".add; "}
  $pointer = data._address
  z.delete
end

def lset_instruction tokens
  tokens.shift_space
  list = get_list tokens
  ind = get_var_or_number tokens
  val = get_var_or_number tokens
  _lset(list, ind, val)
end

def lget_instruction tokens
  tokens.shift_space
  list = get_list tokens
  ind = get_var_or_number tokens
  val = get_var tokens
  _lget(list, ind, val)
end

def rem_instruction tokens
  # p tokens[0..tokens.index(EOL)]
  nil while tokens.shift_space != EOL
end

def read_instruction tokens
  # p tokens[0..tokens.index(EOL)]
  tokens.shift_space
  _read get_var tokens
end

def msg_instruction tokens
  # puts "Running: #{tokens[0...tokens.index(EOL)].join} in #{$stack_context.last} context "
  tokens.shift_space
  while tokens.first_space != EOL
    tokens.first_space
    next tokens.shift_space if tokens.first_space =~ COMMENT and $string_mode == false
    if tokens.first_space =~ STRING_QUOTE
      $string_mode = !$string_mode
      next tokens.shift_space
    end
    # p tokens
    _msg(tokens)
  end
  raise MismatchedStringQuoteError if $string_mode
end

def _ifeq a, b
  _equal(c = Variable.new, a, b)
  _to(c); "[".add
  $stack_ins <<= [c, __method__.to_sym]
  c.delete
end

def _ifneq a, b
  _not_equal(c = Variable.new, a, b)
  _to(c); "[".add
  $stack_ins <<= [c, __method__.to_sym]
end

def _wneq a, b
  c = Variable.new
  _not_equal(c, a, b)
  _to(c); "[".add
  $stack_ins <<= [c, a, b, __method__.to_sym]
end

def _end tokens
  tokens.shift_space
  raise UnexpectedEndInstruction if $stack_ins.empty?
  val, *args, type = $stack_ins.pop
  if type == :_ifeq or type == :_ifneq
    _to(val)
    _zero(val)
  elsif type == :_wneq
    _not_equal(val,*args)
    _to(val)
  end
  "]".add
end

def call_instruction tokens
  tokens.shift_space
  pr_name = tokens.shift_space.downcase

  raise UndefinedProcedure, "got #{pr_name}" unless $procs.has_key? pr_name
  pr = $procs[pr_name]
  pr.params.clear
  while tokens.first_space != EOL
    next tokens.shift_space if tokens.first_space =~ COMMENT or tokens.first_space =~ TAB or tokens.first_space =~ SPACE
    raise InvalidVarName, "got #{tokens.first_space}" unless tokens.first_space =~ MATCH_VAR_NAME
    pr.params <<= get_var tokens
  end

  # puts "Calling proc #{pr.name} with params #{pr.params.map {|param| param._name}}"
  pr.run_proc
end

def control_instruciton tokens
  # puts "Running: #{tokens[0...tokens.index(EOL)].join} in #{$stack_context.last} context "
  ins = tokens.shift_space
  return (_end tokens) if ins == 'end'
  args = get_argument(tokens, *NUMBER_COMPONENT_INS[ins])
  raise ExpectedEndOfLine if tokens.shift_space != EOL
  send("_#{ins}", *args)
end

def get_proc tokens
  proc_mode = false
  deep = 0
  will_del = []
  puts "Getting procs"
  tokens.each.with_index {|t,i|
    if t.downcase == 'proc'
      raise NestedProcedure if proc_mode
      proc_mode = true
      $proc_tokens <<= [t]
      will_del <<= i
      deep += 1
      next
    end

    if proc_mode
      $proc_tokens.last.push t
      will_del <<= i
    end

    if t.downcase == 'end'
      deep -= 1
      raise UnexpectedEndInstruction if deep < 0
      proc_mode = false if proc_mode and deep == 0
      next
    end

    deep += 1if CONTROL_INSTRUCTION.include?(t.downcase) and t != 'call'
  }
  will_del.reverse.each {|i| tokens.delete_at(i)}
  puts "Parsing proc..."
  $proc_tokens.each {|pr| proc_instruction pr}
  # puts $procs
end

def run plain_code
  $var = {}
  $pointer = 0
  $code = ''
  $procs = {}
  $proc_tokens = []
  $stack_ins = []
  $string_mode = false
  $stack_context  = ['main']

  Variable.clear
  puts "Scaning tokens..."
  tokens = plain_code.scan(TOKEN)
  tokens <<= EOL if tokens.last != EOL
  tokens <<= EOF
  # p tokens
  puts "Getting procs..."
  get_proc tokens
  puts "Running main..."
  _run tokens
end

def _run tokens
  while tokens.first_space != EOF
    return if tokens.empty?
    tokens.first_space.downcase!
    next tokens.shift_space if tokens.first_space == EOL or tokens.first_space =~ TAB or tokens.first_space =~ COMMENT or tokens.first_space =~ SPACE
    raise UnknownInstruction, "unknown #{tokens.first_space} instruction" unless tokens.first_space =~ INSTRUCTION
    next basic_instruction tokens if BASIC_INSTRUCTION.include? tokens.first_space
    next control_instruciton tokens if CONTROL_INSTRUCTION.include? tokens.first_space
    send("#{tokens.first_space}_instruction", tokens)
  end
  raise UnclosedBlock unless $stack_ins.empty?
  $code
end

def kcuf plain_code
  run plain_code
end
  
##########################################
def kcuf xCode
  xCodeAt = 0
  xOutput = ''
  xPreserve = 9
  xPreserveMax = -1
  xStack = [0] * xPreserve
  xStackAt = xPreserve
  xPreserve -= 1
  xVar = {}
  xAST = []
  xASTStack = []
  xCurrentAST = xAST
  xProc = {}
  xCurrentProc = nil
  xCurrentProcVar = nil

  xLine = 0
  xLastCol = 0
  xCaseSensetive = ->q{q.upcase}
  xClamp = ->q{q.to_i % 256}

  xIsNumber = ->q{q.is_a? Numeric}
  xIsArray = ->q{q.is_a? Array}

  xBad = ->q,j = false{->*a{raise "#{q % a}\n\tat #{xLine}:#{j ? 1 + xLastCol : 1 + xCodeAt} `#{xCode}`"}}
  xBadTransform = ->q{->*a{raise q % a}}
  xErrorNumberExpected = xBad.call 'A number is expected but got %s'
  xErrorNameExpected = xBad.call 'A variable name / command is expected but got %s'
  xErrorCommand = xBad.call 'Unexpected command %s',true
  xErrorCommandEnd = xBad.call 'Expected end of line but got %s'
  xErrorDefineInProc = xBad.call 'Cannot define variables in procedures'
  xErrorVarUndefined = xBad.call 'Undefined variable %s',true
  xErrorVarRedeclare = xBad.call 'Re-defined variable %s',true
  xErrorVarButList = xBad.call 'Expected a variable but %s is a list',true
  xErrorListButVar = xBad.call 'Expected a list but %s is a variable',true
  xErrorUnEOL = xBad.call 'Unexpected end of line'
  xErrorUnclosed = xBad.call 'Unclosed %s, expected %s but got %s'
  xErrorBadEscape = xBad.call 'Unexpected char escape \\%s'
  xErrorStringExpect = xBad.call 'A string is expected but got %s'
  xErrorStringUnclose = xBad.call 'String is not closed'
  xErrorProcNested = xBad.call 'Procedures should not be nested',true
  xErrorProcUsed = xBad.call 'Procedure re-defined %s'
  xErrorDupParam = xBad.call 'Duplicate parameter name %s',true
  xErrorEndNothing = xBad.call 'Nothing to end'
  xErrorEndUnclose = xBad.call 'Unclosed block (ifeq / ifneq / ueq / proc)'
  xErrorNoProc = xBadTransform.call 'Undefined procedure %s%s'
  xErrorProcLength = xBadTransform.call 'Procedure %s expects %s argument(s) but got %s%s'
  xErrorRecursive = xBadTransform.call 'Recursive call %s'

  xTaste = ->q = 0{xCode[xCodeAt + q]}
  xTasteEOL = ->{xTaste.call || 'EOL'}
  xEat = ->{xCodeAt += 1}
  xSave = ->{xLastCol = xCodeAt}
  xWalk = ->q{
    while q =~ xTaste.call
      xEat.call()
    end
  }
  xDiscard = ->{xCodeAt = xCode.length}
  xWhite = ->{
    xWalk.call /\s/
    if '/' == xTaste.call && '/' == (xTaste.call 1) ||
      '-' == xTaste.call && '-' == (xTaste.call 1) ||
      '#' == xTaste.call
      xDiscard.call
    end
  }
  xWord = ->{
    r = xCodeAt
    xSave.call
    (/[^$_a-z]/i =~ xTaste.call) && (xErrorNameExpected.call xTasteEOL.call)
    xEat.call
    xWalk.call /[$\w]/
    r = xCaseSensetive.call xCode[r,xCodeAt - r]
    xWhite.call
    r
  }
  xVarName = ->{
    r = xWord.call
    '' == r && (xErrorNameExpected.call xTasteEOL.call)
    if !xCurrentProcVar || !(xCurrentProcVar.index r)
      xVar[r] || xErrorVarUndefined.call(r)
      (xIsNumber.call xVar[r]) || (xErrorVarButList.call r)
    end
    r
  }
  xListName = ->{
    r = xWord.call
    xVar[r] || (xErrorVarUndefined.call r)
    (xIsNumber.call xVar[r]) && (xErrorListButVar.call r)
    r
  }
  xNumber = ->{
    r = xCodeAt
    '-' == xTaste.call && xEat.call
    xWalk.call /\d/
    r = xCode[r,xCodeAt - r]
    '' != r && '-' != r || (xErrorNumberExpected.call xTasteEOL.call)
    xWhite.call
    xClamp.call r.to_i
  }
  xCharEscape = {"\\" => "\\",'"' => '"',"'" => "'",'n' => "\n",'r' => "\r",'t' => "\t"}
  xChar = ->{
    r = xTaste.call
    xEat.call
    if '\\' == r
      r = xCharEscape[xTaste.call]
      r || (xErrorBadEscape.call xTasteEOL.call)
      xEat.call
    end
    r
  }
  xNumberOrChar = ->{
    if "'" == xTaste.call
      xEat.call
      r = xChar.call.ord
      "'" == xTaste.call || (xErrorUnclosed.call "'","'",xTasteEOL.call)
      xEat.call
      xWhite.call
      r
    else
      xNumber.call
    end
  }
  xVarNameOrNumber = ->{(/[-\d']/ =~ xTaste.call) ? xNumberOrChar.call : xVarName.call}
  xString = ->{
    r = ''
    '"' == xTaste.call || (xErrorStringExpect.call xTasteEOL.call)
    xEat.call
    while xTaste.call && '"' != xTaste.call
      r += xChar.call
    end
    '"' == xTaste.call || xErrorStringUnclose.call
    xEat.call
    xWhite.call
    r
  }
  xVarNameOrString = ->{'"' == xTaste.call ? [0,xString.call] : [1,xVarName.call]}

  xMsgList = [->{
    r = [xVarNameOrString.call]
    while xTaste.call
      r.push xVarNameOrString.call
    end
    r
  }]

  xBegin = ->{xASTStack.push xCurrentAST.length}
  xMachine =
  {
    'VAR' => ->{
      xCurrentProc && xErrorDefineInProc.call
      xTaste.call || xErrorUnEOL.call
      while '' != (v = xWord.call)
        xVar[v] && (xErrorVarRedeclare.call v)
        if '[' == xTaste.call
          xEat.call
          xWhite.call
          n = xNumber.call
          ']' == xTaste.call || (xErrorUnclosed.call '[',']',xTasteEOL.call)
          xEat.call
          xWhite.call
          xVar[v] = [xStackAt,n]
          xStackAt += 4 + n
        else
          xVar[v] = xStackAt
          xStackAt += 1
        end
      end
    },

    'SET' => [xVarName,xVarNameOrNumber],

    'INC' => [xVarName,xVarNameOrNumber],
    'DEC' => [xVarName,xVarNameOrNumber],
    'ADD' => [xVarNameOrNumber,xVarNameOrNumber,xVarName],
    'SUB' => [xVarNameOrNumber,xVarNameOrNumber,xVarName],
    'MUL' => [xVarNameOrNumber,xVarNameOrNumber,xVarName],
    'DIVMOD' => [xVarNameOrNumber,xVarNameOrNumber,xVarName,xVarName],
    'DIV' => [xVarNameOrNumber,xVarNameOrNumber,xVarName],
    'MOD' => [xVarNameOrNumber,xVarNameOrNumber,xVarName],

    'CMP' => [xVarNameOrNumber,xVarNameOrNumber,xVarName],

    'A2B' => [xVarNameOrNumber,xVarNameOrNumber,xVarNameOrNumber,xVarName],
    'B2A' => [xVarNameOrNumber,xVarName,xVarName,xVarName],

    'LSET' => [xListName,xVarNameOrNumber,xVarNameOrNumber],
    'LGET' => [xListName,xVarNameOrNumber,xVarName],

    'IFEQ' => [xVarName,xVarNameOrNumber,xBegin],
    'IFNEQ' => [xVarName,xVarNameOrNumber,xBegin],
    'WEQ' => [xVarName,xVarNameOrNumber,xBegin],
    'WNEQ' => [xVarName,xVarNameOrNumber,xBegin],
    'PROC' => ->{
      xCurrentProc && xErrorProcNested.call
      n = xWord.call
      xProc[n] && (xErrorProcUsed.call n)
      xCurrentProcVar = []
      while xTaste.call
        t = xWord.call
        (xCurrentProcVar.index t) && (xErrorDupParam.call t)
        xCurrentProcVar.push t
      end
      xProc[n] = xCurrentProc = [xCurrentProcVar,xCurrentAST = []]
    },
    'END' => [->{
      if 0 < xASTStack.length
        xASTStack.pop
      elsif xCurrentProc
        xCurrentAST = xAST
        xCurrentProc = nil
      else
        xErrorEndNothing.call
      end
    }],
    'CALL' => [->{
      n = xWord.call
      a = []
      while xTaste.call
        a.push xWord.call
      end
      [n,a]
    }],

    'READ' => [xVarName],
    'MSG' => xMsgList,
    'LN' => xMsgList,

    'REM' => xDiscard,

    'DEBUG' => [xDiscard],
    'STOP' => [xDiscard]
  }

  xOpGotoCell = ->q{
    xOutput += q < xStackAt ?
      '<' * (xStackAt - q) :
      '>' * (q - xStackAt)
    xStackAt = q
  }
  xOpAdd = ->q{
    q = xClamp.call q
    xOutput += 128 < q ?
      '-' * (256 - q) :
      '+' * q
  }
  xOpSolvePreserve = ->q{
    xPreserveMax = [q,xPreserveMax].max
    xPreserve - q
  }
  xOpFly = ->q{xStackAt = xOpSolvePreserve.call q}
  xOpGotoPreserve = ->q{xOpGotoCell.call xOpSolvePreserve.call q}
  xOpGetPreserve = ->q{xStack[xOpSolvePreserve.call q]}
  xOpSetPreserve = ->q,s{xStack[xOpSolvePreserve.call q] = s}
  xOpModifyPreserve = ->q,s{
    xOpGotoPreserve.call q
    xOpAdd.call s - (xOpGetPreserve.call q)
    xOpSetPreserve.call q,s
  }
  xOpClearPreserve = ->q,j = false{
    if j || 0 != (xOpGetPreserve.call q)
      xOpGotoPreserve.call q
      xOutput += '[-]'
      xOpSetPreserve.call q,0
    end
  }
  xOpMsgList = ->q{
    for f in 0..q.length - 1
      t = q[f].ord
      xOpModifyPreserve.call 0,t
      xOutput += '.'
    end
  }

  xGenerate = ->xAST,xCallArg = ({}),xCallStack = [],xCallStackMessage = ''{
    xOpSolveVar = ->q{xCallArg[q] || q}
    xOpGoto = ->q,s = 0{
      if xIsNumber.call q
        if q < 0
          xOpGotoCell.call -q
        else
          xOpGotoPreserve.call q
        end
      elsif xIsNumber.call q = xVar[xOpSolveVar.call q]
        xOpGotoCell.call q
      else
        xOpGotoCell.call s + q[0]
      end
    }
    xOpClear = ->q,j = false{
      if xIsNumber.call q
        xOpClearPreserve.call q,j
      elsif xIsArray.call q
        q.each{|v| xOpClear.call v,j}
      else
        xOpGoto.call q
        xOutput += '[-]'
      end
    }
    xOpBegin = ->q,s = 0{
      xOpGoto.call q,s
      xOutput += '[-'
    }
    xOpEnd = ->q,s = 0{
      xOpGoto.call q,s
      xOutput += ']'
    }
    xOpMove = ->q,s,i = 0{
      xOpBegin.call q,i
      if xIsArray.call s
        s.each{|v|
          xOpGoto.call v
          xOutput += '+'
        }
      else
        xOpGoto.call s
        xOutput += '+'
      end
      xOpEnd.call q,i
    }
    xOpMoveReverse = ->q,s,i = 0{
      xOpBegin.call q,i
      if xIsArray.call s
        s.each{|v|
          xOpGoto.call v
          xOutput += '-'
        }
      else
        xOpGoto.call s
        xOutput += '-'
      end
      xOpEnd.call q,i
    }
    xOpCopy = ->q,s,t,j = true{
      j && (xOpClear.call t)
      xOpMove.call q,(xIsArray.call s) ? (s.concat [t]) : [s,t]
      xOpMove.call t,q
    }
    xOpPrepare = ->q,s,t{
      xOpClear.call s
      if xIsNumber.call q
        if xIsArray.call s
          xOpGoto.call t
          xOpAdd.call q
          xOpMove.call t,s
        else
          xOpGoto.call s
          xOpAdd.call q
        end
      else
        xOpCopy.call q,s,t
      end
    }
    xOpPrepare01 = ->q,w = 0,a = 1,t = 2{
      xOpPrepare.call q[0],w,t
      xOpPrepare.call q[1],a,t
    }
    xOpSet = ->q,s{
      xOpClear.call q
      xOpMove.call s,q
    }
    xOpDivMod = ->xArg{
      xOpPrepare01.call xArg,5,4,0
      xOpCopy.call 4,8,7
      xOpGoto.call 7
      xOutput += '+<-' +
        '[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>' +
        '[->>[->>>+<<<]<]'
      xOpFly.call 6
      xOpClear.call 8,true
      xOpClear.call 4,true
      xArg[2] ? (xOpSet.call xArg[2],2) : (xOpClear.call 2,true)
      xArg[3] ? (xOpSet.call xArg[3],3) : (xOpClear.call 3,true)
    }
    xOpIFWhile = ->xArg,xNot = false{
      if xIsNumber.call xArg[1]
        xOpClear.call 0
        xOpCopy.call xArg[0],0,1
        xOpGoto.call 0
        xOpAdd.call -xArg[1]
      else
        xOpPrepare01.call xArg
        xOpMoveReverse.call 1,0
      end
      if xNot
        xOpGoto.call 1
        xOutput += '+>[[-]<-]<[>+<-<]'
        xOpFly.call 2
      end
      xOpGoto.call 0
    }

    for v in xAST
      xCommand = v[0]
      xArg = v[1]
      xLine = v[2]
      case xCommand
        when 'SET'
          xOpGoto.call xArg[0]
          xOutput += '[-]'
          if xIsNumber.call xArg[1]
            xOpAdd.call xArg[1]
          else
            xOpCopy.call xArg[1],xArg[0],0
          end
        when 'INC'
          if xIsNumber.call xArg[1]
            xOpGoto.call xArg[0]
            xOpAdd.call xArg[1]
          elsif (xOpSolveVar.call xArg[0]) == (xOpSolveVar.call xArg[1])
            xOpClear.call 0
            xOpMove.call xArg[0],0
            xOpBegin.call 0
            xOpGoto.call xArg[0]
            xOutput += '++'
            xOpEnd.call 0
          else
            xOpCopy.call xArg[1],xArg[0],0
          end
        when 'DEC'
          if xIsNumber.call xArg[1]
            xOpGoto.call xArg[0]
            xOpAdd.call -xArg[1]
          else
            xOpCopy.call xArg[1],0,1
            xOpMoveReverse.call 0,xArg[0]
          end
        when 'ADD'
          xOpPrepare01.call xArg
          xOpMove.call 1,0
          xOpSet.call xArg[2],0
        when 'SUB'
          xOpPrepare01.call xArg
          xOpMoveReverse.call 1,0
          xOpSet.call xArg[2],0
        when 'MUL'
          xOpPrepare01.call xArg
          xOpBegin.call 0
          xOpCopy.call 1,2,3
          xOpEnd.call 0
          xOpClear.call 1,true
          xOpSet.call xArg[2],2
        when 'DIVMOD','DIV'
          xOpDivMod.call xArg
        when 'MOD'
          xOpDivMod.call [xArg[0],xArg[1],nil,xArg[2]]
        when 'CMP'
          x = 4
          t0 = 3
          t1 = 2
          xOpPrepare01.call xArg,[t0,x],[t1,1 + x],0
          xOpMoveReverse.call 1 + x,x

          xOpGoto.call 1 + x
          xOutput += '+>[[-]'
          xOpFly.call x

          xOpGoto.call t1 - 1
          xOutput += '+<[>-]>['
          xOpFly.call t1 - 1
          xOpGoto.call x
          xOutput += '+'
          xOpGoto.call t0
          xOutput += '[-]'
          xOpGoto.call t1 - 1
          xOutput += '->]<+'
          xOpGoto.call t0
          xOutput += '['
          xOpGoto.call t1
          xOutput += '-[>-]>['
          xOpFly.call t1 - 1
          xOpGoto.call x
          xOutput += '+'
          xOpGoto.call t0
          xOutput += '[-]+'
          xOpGoto.call t1 - 1
          xOutput += '->]<+'
          xOpGoto.call t0
          xOutput += '-]'

          xOpGoto.call x
          xOutput += '[<-]<[>-<-<]'
          xOpFly.call 2 + x

          xOpGoto.call 1 + x
          xOutput += ']<[-<]>'

          xOpClear.call 3,true
          xOpClear.call 2,true
          xOpClear.call 1,true

          xOpSet.call xArg[2],x
        when 'A2B'
          a = xArg[0]
          b = xArg[1]
          c = xArg[2]
          r = xArg[3]
          if xIsNumber.call a
            if a = (xClamp.call 10 * (a - 48))
              xOpGoto.call 1
              xOpAdd.call a
            end
          else
            xOpCopy.call a,2,0
            xOpGoto.call 2
            xOpAdd.call -48
            xOpBegin.call 2
            xOpGoto.call 1
            xOpAdd.call 10
            xOpEnd.call 2
          end
          if xIsNumber.call b
            xOpGoto.call 1
            xOpAdd.call b - 48
          else
            xOpCopy.call b,1,0
            xOpGoto.call 1
            xOpAdd.call -48
          end
          xOpBegin.call 1
          xOpGoto.call 0
          xOpAdd.call 10
          xOpEnd.call 1
          if xIsNumber.call c
            xOpGoto.call 0
            xOpAdd.call c - 48
          else
            xOpCopy.call c,0,1
            xOpGoto.call 0
            xOpAdd.call -48
          end
          xOpSet.call r,0
        when 'B2A'
          r = xArg[0]
          a = xArg[1]
          b = xArg[2]
          c = xArg[3]
          if xIsNumber.call r
            xOpClear.call a
            xOpAdd.call r / 100
            xOpClear.call b
            xOpAdd.call r / 10 % 10
            xOpClear.call c
            xOpAdd.call r % 10
          else
            xOpDivMod.call [r,10,b,c]
            xOpDivMod.call [b,10,a,b]
          end
          xOpGoto.call 0
          xOpAdd.call 48
          xOpMove.call 0,xArg[1,xArg.length - 1]
        when 'LSET'
          if xIsNumber.call xArg[1]
            xOpGoto.call xArg[0]
            xOpAdd.call xArg[1]
            xOutput += '[->+>+<<]'
          else
            xOpCopy.call xArg[1],[-1 - xVar[xArg[0]][0],-2 - xVar[xArg[0]][0]],xArg[0],false
          end
          if xIsNumber.call xArg[2]
            xOpGoto.call xArg[0],3
            xOpAdd.call xArg[2]
          else
            xOpCopy.call xArg[2],-3 - xVar[xArg[0]][0],xArg[0],false
          end
          xOpGoto.call xArg[0]
          xOutput += '>[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]' +
            '>>>[-]<[->+<]<' +
            '[[-<+>]<<<[->>>>+<<<<]>>-]<<'
        when 'LGET'
          if xIsNumber.call xArg[1]
            xOpGoto.call xArg[0]
            xOpAdd.call xArg[1]
            xOutput += '[->+>+<<]'
          else
            xOpCopy.call xArg[1],[-1 - xVar[xArg[0]][0],-2 - xVar[xArg[0]][0]],xArg[0],false
          end
          xOpGoto.call xArg[0]
          xOutput += '>[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]' +
            '>>>[-<+<<+>>>]<<<[->>>+<<<]>' +
            '[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<'
          xOpClear.call xArg[2]
          xOpMove.call xArg[0],xArg[2],3
        when 'IFEQ'
          xOpIFWhile.call xArg,true
          xOutput += '['
          xOpClear.call 0,true
        when 'IFNEQ'
          xOpIFWhile.call xArg
          xOutput += '['
          xOpClear.call 0,true
        when 'WEQ'
          xOpIFWhile.call xArg,true
          xOutput += '['
          xOpClear.call 0,true
        when 'WNEQ'
          xOpIFWhile.call xArg
          xOutput += '['
          xOpClear.call 0,true
        when 'END'
          if xArg[0]
            xCommand = xAST[xArg[0]][0]
            xArg = xAST[xArg[0]][1]
            if 'WEQ' == xCommand
              xOpIFWhile.call xArg,true
            elsif 'WNEQ' == xCommand
              xOpIFWhile.call xArg
            else
              xOpClear.call 0
            end
            xOpGoto.call 0
            xOutput += ']'
          end
        when 'CALL'
          xArg = xArg[0]
          t = xCallStackMessage + "\n\tat line:#{xLine} #{xArg[0]}"
          f = xProc[xArg[0]]
          xProc[xArg[0]] || (xErrorNoProc.call xArg[0],t)
          f[0].length == xArg[1].length || (xErrorProcLength.call xArg[0],F[0].length,xArg[1].length,t)
          (xCallStack.index xArg[0]) && (xErrorRecursive.call t)
          xCallStack.push xArg[0]
          r = {}
          f[0].each_with_index{|v,f| r[v] = xOpSolveVar.call xArg[1][f]}
          xGenerate.call f[1],r,xCallStack,t
          xCallStack.pop
        when 'READ'
          xOpGoto.call xArg[0]
          xOutput += ','
        when 'MSG','LN'
          for v in xArg[0]
            if 0 == v[0]
              xOpMsgList.call v[1]
            else
              xOpGoto.call v[1]
              xOutput += '.'
            end
          end
          if 'LN' == xCommand
            xOpMsgList.call "\n"
          end
        when 'DEBUG'
          xOutput += '_'
        when 'STOP'
          xOutput += '!'
      end
    end
  }

  for v in xCode.split "\n"
    xLine += 1
    xCode = v
    xCodeAt = 0
    xWhite.call
    if xTaste.call
      v = xWord.call
      xMachine[v] || (xErrorCommand.call v)
      if xIsArray.call xMachine[v]
        xCurrentAST.push [v,xMachine[v].map{|v| v.call},xLine]
      else
        xMachine[v].call
      end
      xTaste.call && (xErrorCommandEnd.call xTaste.call)
    end
  end
  0 < xASTStack.length && xErrorEndUnclose.call

  xStackAt = 0
  xGenerate.call xAST
  t = xPreserve - xPreserveMax
  xOutput[t,xOutput.length - t]
end
