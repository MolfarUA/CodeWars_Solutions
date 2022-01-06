def deriv(q)
  return 0.0 if q.is_a?(Numeric)
  return 1.0 if q == 'x'
  case q[0]
    when '+','-'
    return [q[0], deriv(q[1]), deriv(q[2])]
    when '*'
    return ['+', ['*', deriv(q[1]), q[2]], ['*', q[1], deriv(q[2])]]
    when '/'
    return ['/', ['-', ['*', deriv(q[1]), q[2]], ['*', q[1], deriv(q[2])]], ['^', q[2], 2]]
    when '^'
    return ['+', ['*', ['*', q[2], deriv(q[1])], ['^', q[1], ['-', q[2], 1]]], ['*', ['*', deriv(q[2]), ['ln', q[1]]], q]]
    when 'cos'
    return ['*', ['*', -1, deriv(q[1])], ['sin', q[1]]]
    when 'sin'
    return ['*', deriv(q[1]), ['cos', q[1]]]
    when 'tan'
    return ['*', deriv(q[1]), ['^', ['cos', q[1]], -2]]
    when 'exp'
    return ['*', deriv(q[1]), ['exp', q[1]]]
    when 'ln'
    return ['/', deriv(q[1]), q[1]]
  end
end

def simplify(q)
  return q if q.is_a?(String) || q.is_a?(Numeric)
  q[1..-1] = q[1..-1].map!{|w| simplify(w)}
  if /\+|-|\*|\/|\^/ =~ q[0] and q[1..2].all?(Numeric)
    return q[1..2].reduce({'^'=>'**'}[q[0]] || q[0])
  end
  case q[0]
    when '+'
    return q[1] if q[2] == 0
    return q[2] if q[1] == 0
    when '*'
    return 0 if q[1..2].include?(0)
    return q[1] if q[2] == 1
    return q[2] if q[1] == 1
    when '^'
    return 1 if q[2] == 0 || q[1] == 1
    return q[1] if q[2] == 1
  end
  q
end

def prx(q)
  return q if q.is_a? String
  return '%g'%q if q.is_a? Numeric
  '(' + ([q[0]]+(q[1..-1].map{|w| prx(w)})).join(' ') + ')'
end


def diff(s)
  q = eval(s.tr('(','[')
    .gsub(/\)/, '],')
    .gsub(/\+|-|\*|\/|\^|cos|sin|tan|exp|ln|x/, '"\0",')
    .gsub(/\d+/, '\0.0,')
    .gsub(/,\s*(\]|$)/,'\1'))
  w = deriv(q)
  r = simplify(w)
  t = prx(r)
end
______________________________________________
def d(q)
  return 0.0 if q.is_a?(Numeric)
  return 1.0 if q == 'x'
  case q[0]
    when '+','-'
    return [q[0], d(q[1]), d(q[2])]
    when '*'
    return ['+', ['*', d(q[1]), q[2]], ['*', q[1], d(q[2])]]
    when '/'
    return ['/', ['-', ['*', d(q[1]), q[2]], ['*', q[1], d(q[2])]], ['^', q[2], 2]]
    when '^'
    return ['+', ['*', ['*', q[2], d(q[1])], ['^', q[1], ['-', q[2], 1]]], ['*', ['*', d(q[2]), ['ln', q[1]]], q]]
    when 'cos'
    return ['*', ['*', -1, d(q[1])], ['sin', q[1]]]
    when 'sin'
    return ['*', d(q[1]), ['cos', q[1]]]
    when 'tan'
    return ['*', d(q[1]), ['^', ['cos', q[1]], -2]]
    when 'exp'
    return ['*', d(q[1]), ['exp', q[1]]]
    when 'ln'
    return ['/', d(q[1]), q[1]]
  end
end

def reduce(q)
  return q if q.is_a?(String) || q.is_a?(Numeric)
  q[1..-1] = q[1..-1].map!{|w| reduce(w)}
  if /\+|-|\*|\/|\^/ =~ q[0] and q[1..2].all?(Numeric)
    return q[1..2].reduce({'^'=>'**'}[q[0]] || q[0])
  end
  case q[0]
    when '+'
    return q[1] if q[2] == 0
    return q[2] if q[1] == 0
    when '*'
    return 0 if q[1..2].include?(0)
    return q[1] if q[2] == 1
    return q[2] if q[1] == 1
    when '^'
    return 1 if q[2] == 0
    return q[1] if q[2] == 1
  end
  q
end

def prx(q)
  return q if q.is_a? String
  return '%g'%q if q.is_a? Numeric
  '(' + ([q[0]]+(q[1..-1].map{|w| prx(w)})).join(' ') + ')'
end


def diff(s)
  q = eval(s.tr('(','[')
    .gsub(/\)/, '],')
    .gsub(/\+|-|\*|\/|\^|cos|sin|tan|exp|ln|x/, '"\0",')
    .gsub(/\d+/, '\0.0,')
    .gsub(/,\s*(\]|$)/,'\1'))
  w = d(q)
  r = reduce(w)
  t = prx(r)
end
______________________________________________
def diff(s)
  expr = parse(s)
  expr = deriv(expr)
  loop do
    simplified = simplify(expr)
    break if simplified == expr

    expr = simplified
  end
  stringify(expr)
end

def parse(str)
  if str[0] == '(' && str[-1] == ')'
    str[1..-2].scan(/\(.+\)|\S+/).map { |chunk| parse(chunk) }
  elsif str.to_i.to_s == str
    str.to_i
  else
    str.to_sym
  end
end

def deriv(expr)
  case expr
  when Symbol then 1
  when Numeric then 0
  else
    op, *operands = expr
    case op
    when :+, :- then [op, *operands.map { |o| deriv(o) }]
    when :*
      u, v = if operands.size >= 3
               [operands.first, [:*, *operands[1..-1]]]
             else
               operands
             end
      [:+, [:*, deriv(u), v], [:*, u, deriv(v)]]
    when :/
      u, v = operands
      [:/, [:-, [:*, deriv(u), v], [:*, u, deriv(v)]], [:^, v, 2]]
    when :^
      base, power = operands
      [:*, power, [:^, base, [:-, power, 1]], deriv(base)]
    when :sin then [:*, deriv(operands.first), [:cos, operands.first]]
    when :cos then [:*, -1, deriv(operands.first), [:sin, operands.first]]
    when :ln then [:/, deriv(operands.first), operands.first]
    when :tan then [:*, deriv(operands.first), [:^, [:cos, operands.first], -2]]
    when :exp then [:*, deriv(operands.first), [:exp, operands.first]]
    end
  end
end

def simplify(expr)
  return expr unless expr.is_a?(Array)

  op, *operands = expr
  operands = operands.map { |o| simplify(o) }
  case
  when %i[+ - * /].include?(op) && operands.all?(Numeric)
    operands.map(&:to_f).reduce(op)
  when op == :+ && operands.index(0) then [op, *operands.reject { |o| o == 0 }]
  when op == :* && operands.index(1) then [op, *operands.reject { |o| o == 1 }]
  when op == :* && operands.index(0) then 0
  when %i[+ *].include?(op) && operands.one? then operands.first
  when %i[+ *].include?(op)
    nums, rest = operands.partition { |o| o.is_a?(Numeric) }
    return [op, *operands] if nums.one?
    reduced = nums.reduce(op)
    [op, reduced, *rest]
  when op == :- && operands.last == 0 then operands.first
  when op == :- && operands.first == 0 then [:*, -1, operands.first]
  when op == :/ && operands.last == 1 then operands.first
  when op == :^ && operands.all?(Numeric) then operands.reduce(:**)
  when op == :^ && operands.last == 1 then operands.first
  when op == :^ && operands.last == 0 then 1
  else [op, *operands]
  end
end

def stringify(expr)
  stringified = stringify_term(expr)
  stringified.is_a?(Array) ? stringified.join('') : stringified
end

def stringify_term(term)
  case term
  when Array
    ['(',
     stringify_term(term.first),
     *term[1..-1].flat_map { |t| [' ', stringify_term(t)] },
     ')']
  when Float
    term = term.to_i if term.to_i == term
    term.to_s
  else
    term.to_s
  end
end

______________________________________________
class Fun
    attr_accessor :op, :a
    def initialize(op,a=nil) @op = op; @a = a&.simplify end
    def self.[](*a) new(*a) end
    def to_s() "(#{op} #{a})" end
    def derivate()
        d = case op
        when "ln"  then Op['/', Const[1], a] # ln(x) => 1/x
        when "sin" then Fun["cos", a] # sin(x) => cos(x)
        when "cos" then Op['*', Const[-1], Fun["sin", a]] # cos(x) => -sin(x)
        when "tan" then Op['/', Const[1], Op['^', Fun["cos", a], Const[2]]] # tan(x) => 1/cos(x)^2
        when "exp" then self # e^x => e^x
        end
        Op['*', d, a.derivate] # derivative chain rule -- f(g(x))' = f'(g(x)) * g'(x)
    end
    def simplify()
        @a.is_a?(Const) ? Const[Math.send(@op.sub("ln", "log"), @a.v)] : self
    end
    def zero?() false end
    def one?() false end
end

class Op
    attr_accessor :op, :a, :b
    def initialize(op,*a) @op = op; @a, @b = a.map(&:simplify) end
    def self.[](*a) new(*a) end
    def to_s()
        @a,@b = @b,@a if b.is_a?(Const) && op == '*'
        "(#{op} #{a} #{b})"
    end
    def derivate()
        case op
        when '^'
            if a.is_a?(Const)
                unless b.is_a?(Const) then Op['*', self, Fun["ln", a]] # a^x => a^x*ln(a)
                else self end
            else Op['*', b, Op['^', a, Op['-', b, Const[1]]]] # x^a => a*x^(a-1)
            end
        when '*' # derviative product rule -- (f(x)*g(x))' = f'(x)*g(x) + f(x)*g'(x)
            Op['+', Op['*', a.derivate, b], Op['*', a, b.derivate]]
        when '/' # derivative quotient rule -- (f(x)/g(x))' = (f'(x)*g(x) - f(x)*g'(x)) / g^2(x)
            Op['/', Op['-', Op['*', @a.derivate, b], Op['*', a, b.derivate]], Op['^', b, Const[2]]]
        else # derivative sum rule -- (a*f(x) + b*g(x))' = a*f'(x) + b*g'(x)
            Op[op, a.derivate, b.derivate]
        end
    end
    def simplify()
        case
        when a.is_a?(Const) && b.is_a?(Const) then Const[a.v.send(op.sub('^', "**"), b.v)]
        when "+-".include?(op) ? b.zero? : b.one? then a
        when op == '+' && a.zero? || op == '*' && a.one? then b
        when op == '*' && (a.zero? || b.zero?) || op == '^' && a.zero? then Const[0]
        when op == '^' && (a.one? || b.zero?) then Const[1]
        when op == '/' && a.one? && b.is_a?(Op) && b.op == '^' then Op[b.op, b.a, Op['*', Const[-1], b.b]] # 1/(e^n) => e^(-n)
        else self
        end
    end
    def zero?() false end
    def one?() false end
end

class Const
    attr_accessor :v
    def initialize(v) @v = v end
    def self.[](v) new(v) end
    def to_s() format("%g", v) end
    def derivate() Const[0] end
    def simplify() self end
    def zero?() v == 0 end
    def one?() v == 1 end
end

class Symbol
    def derivate() Const[1] end
    def simplify() self end
    def zero?() false end
    def one?() false end
end


def diff expr
    tokens = expr.scan(/cos|sin|tan|exp|ln|[()+\-*\/\^]|-?\d+(?:\.\d+)?|x/)
    ptr = 0

    parse = -> do
        ops = []
        stack = []
        while ptr < tokens.size do
            t = tokens[ptr]
            case t
            when '('
                ptr += 1
                stack << parse.()
            when ')' then break
            when 'x' then stack << :x
            when '+','-','*','/','^' then ops << Op[t]
            when "cos","sin","tan","exp","ln" then ops << Fun[t]
            else stack << Const[tokens[ptr].to_f]
            end
            if ops.last.is_a?(Fun) && !stack.empty? then
                f = ops.pop
                f.a = stack.pop
                stack << f
            end
            if ops.last.is_a?(Op) && stack.size > 1 then
                o = ops.pop
                o.a, o.b = stack.pop(2)
                stack << o
            end
            ptr += 1
        end
        stack.pop
    end

    parse.().simplify.derivate.simplify.to_s
end
