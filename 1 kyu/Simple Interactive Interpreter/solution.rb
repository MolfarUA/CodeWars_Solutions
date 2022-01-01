module Operators
    def operator_for_multiplicatives
        operator_for(['*', '/', '%']) # multiplication, division, modulo
    end

    def operator_for_additives
        operator_for(['+', '-']) # addition, subtraction
    end

    def operator_for(symbols)
        symbols = Regexp.escape(symbols.join)
        lambda do |expr|
            regex = %r{(?<x>[\+-]?\w+\.?\d*)\s?(?<op>[#{symbols}])\s?(?<y>[\+-]?\w+\.?\d*)}

            bkup = expr.dup
            while expr.match(regex) do
                expr.sub!(regex) do |str|
                    m = str.match(regex)
                    x = try_variable(m[:x])
                    y = try_variable(m[:y])

                    r = to_num(x.send(m[:op], y))
                    ("%.15f" % r).sub(/\.?0+$/, '')
                end
            end
        end
    end

    def lookup
        regex = %r{\A[a-zA-Z]+\Z}
        lambda do |expr|
            expr.gsub!(regex) { |str| try_variable(str) }
        end
    end

    def try_variable(var)
        multipler = var.delete_prefix!('-').nil? ? 1 : -1

        regex = %r{\A[a-zA-Z]+\Z}
        if var =~ regex
            var = @variables[var] || raise("ERROR: Invalid identifier. No variable with name '#{var}' was found.")
        end

        var.to_f * multipler
    end

    def to_num(val) # int float thingy
        i, f = val.to_i, val.to_f
        i == f ? i : f
    end
end

class Fn
    include Operators

    def initialize(name, body, params)
        @name = name
        @body = body
        @params = params

        @variables = {}
        @operators = [
            operator_for_multiplicatives,
            operator_for_additives,
            lookup
        ]
    end

    def self.operator_from(match)
        params = []
        params = match[:args].split unless match[:args].nil?

        raise "Error: duplicate variables in function args: #{match[:args]}" if params.uniq.length != params.length

        body = match[:body]

        body.scan(/\b[a-zA-Z]\b/) do |var|
            raise "Error: unknown variable #{var} in function body: #{match.string}" unless params.include?(var)
        end

        new(match[:name], body, params)
    end

    def regex(available_vars)
        length = @params.length

        return %r{\b(#{@name})\b} unless length.positive?

        vars = ['\d+\.?\d*'] + available_vars
        args = "(?<!\\w)[\+-]?(#{vars.join('|')})(?!\\w) " * length
        %r{\b#{@name}\b\s#{args.strip}}
    end

    def call(args)
        args = args.split[1..-1] unless args.nil?
        args ||= []

        raise "Error: expected #{@params.length} arguments for func: #{@name} but got: #{args.length}" unless args.length == @params.length

        args.each_with_index { |arg, i| @variables[@params[i]] = arg.to_f }

        interpret(@body.dup)
    end

    def interpret(expression)
        regex = %r{-?\([^\(\)]+\)}
        while expression.match(regex) do
            expression.gsub!(regex) do |match|
                multiplier = match.delete_prefix!('-').nil? ? 1 : -1
                res = evaluate(match[1...-1])

                res.empty? ? res : multiplier * to_num(res)
            end # remove outer parentheses
        end

        res = evaluate(expression)
        expression.empty? ? '' : res
    end

    def evaluate(expression)
        @operators.each { |operator| operator.call(expression) }
        expression
    end
end

class Interpreter < Fn
    def initialize
        super('main', '', [])

        @functions = {}
        @operators += [assignments]

        @operators.prepend(evaluate_functions) # evaluate functions first
    end

    def interpret(expression)
        expression = expression.strip
        return register_function(expression) if expression.start_with?('fn')

        raise 'Error: function declared within expression' if expression =~ /\A.+fn\s.*\Z/

        is_function_call = @functions.has_key?(expression.split.first)

        invalid = %r{\A\d+[^%=\/\*\+-]\w+\Z}
        raise "Invalid expression: #{expression}" if !is_function_call && expression =~ invalid

        return '' if expression.empty?

        to_num(super(expression))
    end

    private

    def assignments
        regex = %r{(?<var>\w+)\s?=\s?(?<val>[\+-]?\w+\.?\d*)\Z}
        lambda do |expr|
            while expr.match(regex) do
                expr.sub!(regex) do |str|
                    m = str.match(regex)
                    var = m[:var]

                    raise "Error: variable name '#{var}' conflicts with function of same name" if @functions.has_key?(var)

                    @variables[var] = try_variable(m[:val])
                    to_num(@variables[var])
                end
            end
        end
    end

    def register_function(expr)
        regex = %r{\Afn\s(?<name>\w+)\s(?<args>[a-zA-Z\s]+)?\s*=>\s(?<body>.*)\Z}

        m = expr.match(regex)
        fname = m[:name]

        raise "Error: function name '#{fname}' conflicts with variable of same name" if @variables.has_key?(fname)

        @functions[fname] = Fn.operator_from(m)
        ''
    end

    def evaluate_functions
        regex = %r{(?!.+[=])[a-z]+}

        lambda do |expr|          
            available_vars = @variables.keys

            while !(expr.scan(regex) & @functions.keys).empty? do
                bkup = expr.dup

                @functions.each do |name, fn|
                    expr.gsub!(fn.regex(available_vars)) do |match|
                        available_vars.each { |var| match.gsub!(%r{\b#{var}\b}, ("%.15f" % @variables[var]).sub(/\.?0+$/, '')) }
                        fn.call(match)
                    end

                    # check invalid args
                    bkup.gsub(%r{\A#{name}\s[\d\s\.]+\Z}) { |match| fn.call(match) }
                end

                raise "Error: infinite loop detected in function call: #{bkup}" if expr == bkup
            end
        end
    end
end

@interpreter = Interpreter.new
def interpret(expression)
    @interpreter.interpret(expression)
end

___________________________________________________________________________

class Context
  attr_reader :variables

  def initialize(variables = {})
    @variables = variables
  end

  def self.main
    @@context ||= self.new
  end
  
  def define_fn(name:, params:, fn_body:)
    raise unless variables[name].nil? || variables[name].respond_to?(:call)

    raise if params.uniq.size < params.size

    fn_body.scan(/[a-zA-Z]+/) do |identifier|
      raise unless params.include?(identifier)
    end

    variables[name] = -> (args) do
      raise if args.size != params.size

      interpret(fn_body, Context.new(params.zip(args).to_h))
    end

    ""  
  end
  
  def assign_variable(name:, value:)
    variables[name] = value
  end
end

def float_or_integer(str)
  i = str.to_i
  f = str.to_f

  i - f == 0 ? i : f
end

def calc_expression(expression)
  while expression.match(/\(|\)/) do
    expression = expression.gsub(/(-?)\(([^()]+)\)/) do
      sign = ($1 == '' ? 1 : -1)

      sign * calc_expression($2)
    end
  end
  
  num_reg = '(-?\d+(\.\d+)?)'
  reg = -> (op) { Regexp.new("#{num_reg}\s*(\\#{op})\s*#{num_reg}") }  

  eval_op = -> (op) do
    while expression.match(reg.(op)) do
      expression = expression.sub(reg.(op)) { "%.20f" % float_or_integer($1.to_f.send($3, $4.to_f)) }
    end
  end

  eval_op.('/|\*|\%')
  eval_op.('-|\+')

  float_or_integer(expression)
end

def interpret(expression, context = Context.main)
  expression.split(/\n/).reduce("") do |last_line, line|
    line.strip!

    if line.match(/fn/)
      raise if line.match(/\(.*fn.*\)/)

      line.gsub!(/fn (?<name>[a-zA-Z]+)(?<params>[ \S+]+)\s*=> (?<fn_body>.+)/) do
        match = Regexp.last_match
        
        name    = match[:name]
        params  = match[:params].strip.split(' ')
        fn_body = match[:fn_body]
        
        context.define_fn(name: name, params: params, fn_body: fn_body)
      end
    end

    raise if line.match(/\d+[a-zA-Z]/)

    line.gsub!(/([a-zA-Z]+)\s*=\s*([^\(\)]*(\(.+\))?[^\(\)]*)/) do
      raise if context.variables[$1].respond_to?(:call)

      context.assign_variable(name: $1, value: "%.20f" % interpret($2, context))
    end

    line.gsub!(/(-?)([a-zA-Z]+)/) do
      sign  = ($1 == '' ? 1 : -1)
      name  = $2
      value = context.variables[name]

      raise unless value

      value.respond_to?(:call) ? $1 + $2 : sign * float_or_integer(value)
    end

    while line.match(/(-?)([a-zA-Z]+)(( (-?\d+(\.\d+)?))+)/) do
      line.gsub!(/(-?)([a-zA-Z]+)(( (-?\d+(\.\d+)?))+)/) do
        sign = ($1 == '' ? 1 : -1)
        name = $2
        args = ($3 || "").split(' ')

        sign * float_or_integer(context.variables[name].call(args))
      end
    end

    line.gsub!(/(-?)([a-zA-Z]+)/) do
      sign = ($1 == '' ? 1 : -1)

      sign * context.variables[$2].call([]).to_f
    end

    raise if line.match(/\d+\s+\d+/)

    line.strip == '' ? line.strip : calc_expression(line.strip)
  end
end

___________________________________________________________________________
require 'set'


Token = Struct.new :type, :value do
  def inspect
    "'#{value}'"
  end
end


class Tokenizer
  def initialize(string)
    @string = string
  end

  def tokens
    string = @string.dup.strip

    Enumerator.new do |yielder|
      while not string.empty?
        case string
        when /^\d+(?!\.)|\d*\.\d+/
          yielder.yield Token.new :number, $&
        when /^=>/
          yielder.yield Token.new :arrow, $&
        when /^\+/
          yielder.yield Token.new :plus, $&
        when /^-/
          yielder.yield Token.new :minus, $&
        when /^\*/
          yielder.yield Token.new :times, $&
        when %r{^/}
          yielder.yield Token.new :divide, $&
        when /^%/
          yielder.yield Token.new :modulo, $&
        when /^=/
          yielder.yield Token.new :assign, $&
        when /^\(/
          yielder.yield Token.new :lparen, $&
        when /^\)/
          yielder.yield Token.new :rparen, $&
        when /^fn/
          yielder.yield Token.new :function, $&
        when /^\d+[a-zA-Z_]+/
          raise "Invalid input #{$&}"
        when /^[a-zA-Z_]\w*/
          yielder.yield Token.new :identifier, $&
        else
          raise "Could not tokenize \"#{string}\""
        end

        string = $'.strip
      end
    end
  end
end

class BinaryOperation
  def initialize(left, right)
    @left = left
    @right = right
  end

  def free_vars
    @left.free_vars + @right.free_vars
  end

  def inspect
    "(#{@left.inspect} #{operator} #{@right.inspect})"
  end
end

class Addition < BinaryOperation
  def evaluate(environment)
    @left.evaluate(environment) + @right.evaluate(environment)
  end

  def operator
    '+'
  end
end

class Subtraction < BinaryOperation
  def evaluate(environment)
    @left.evaluate(environment) - @right.evaluate(environment)
  end

  def operator
    '-'
  end
end

class Multiplication < BinaryOperation
  def evaluate(environment)
    @left.evaluate(environment) * @right.evaluate(environment)
  end

  def operator
    '*'
  end
end

class Division < BinaryOperation
  def evaluate(environment)
    @left.evaluate(environment) / @right.evaluate(environment)
  end

  def operator
    '/'
  end
end

class Modulo < BinaryOperation
  def evaluate(environment)
    @left.evaluate(environment) % @right.evaluate(environment)
  end

  def operator
    '%'
  end
end

class Literal
  def initialize(value)
    @value = value
  end

  def evaluate(environment)
    @value
  end

  def free_vars
    [].to_set
  end

  def inspect
    @value.inspect
  end
end

class Variable
  def initialize(identifier)
    @identifier = identifier
  end

  def evaluate(environment)
    if environment.has_key? @identifier
      v = environment[@identifier]

      if Function === v
        raise 'Missing arguments' unless v.parameters.empty?
        v.body.evaluate(environment)
      else
        v
      end
    else
      raise "Unknown identifier #{@identifier}"
    end
  end

  def free_vars
    [ @identifier ].to_set
  end

  def inspect
    @identifier
  end
end

class FunctionCall
  def initialize(identifier, arguments)
    @identifier = identifier
    @arguments = arguments
  end

  def evaluate(environment)
    func = environment[@identifier]
    raise "#{@identifier} is not a function #{func.inspect}" unless Function === func
    raise "Wrong arity for #{@identifier}: expected #{func.parameters.size} arguments, got #{@arguments.size}" unless func.parameters.size == @arguments.size

    env = environment.dup

    func.parameters.zip(@arguments) do |p, a|
      env[p] = a.evaluate(environment)
    end

    func.body.evaluate(env)
  end

  def free_vars
    [].to_set
  end

  def inspect
    "#{@identifier}(#{arguments.map(&:inspect).join(',')})"
  end
end

class Assignment
  def initialize(identifier, operand)
    @identifier = identifier
    @operand = operand
  end

  def evaluate(environment)
    raise "Cannot redefine #{@identifier}" if environment.has_key? @identifier and Function === environment[@identifier]
    environment[@identifier] = @operand.evaluate(environment)
  end

  def free_vars
    @operand.free_vars
  end

  def inspect
    "#{@identifier} = #{@operand}"
  end
end

class Skip
  def evaluate(environment)
    ''
  end

  def free_vars
    [].to_set
  end

  def inspect
    "skip"
  end
end

class FunctionDefinition
  def initialize(identifier, parameters, body)
    @identifier = identifier
    @parameters = parameters
    @body = body
  end

  def evaluate(environment)
    raise "Cannot redefine #{@identifier}" if environment.has_key?(@identifier) and !(Function === environment[@identifier])
    environment[@identifier] = Function.new(@parameters, @body)
    ''
  end

  def inspect
    "fn #{@identifier}(#{@parameters.join(',')}) { #{@body} }"
  end
end

Function = Struct.new :parameters, :body

class Parser
  def initialize(environment, tokens)
    @environment = environment
    @tokens = tokens
    @index = 0
  end

  def parse
    if end_reached?
      Skip.new
    else
      if peek.type == :function
        consume
        identifier = consume
        parameters = []

        while peek.type == :identifier
          parameters << consume.value
        end

        raise 'Expected =>' unless consume.type == :arrow
        raise 'Duplicate parameter names' if parameters.size != parameters.uniq.size

        body = expression1

        raise 'Unbound variables' if body.free_vars != parameters.to_set

        FunctionDefinition.new(identifier.value, parameters, body)
      else
        result = expression1
        raise "Expected end of input: #{@tokens[@index..-1]} left, parsed #{result.inspect}" unless end_reached?
        result
      end
    end
  end

  def expression1
    result = expression2

    while not end_reached?
      case (token = peek).type
      when :plus
        consume
        result = Addition.new(result, expression2)
      when :minus
        consume
        result = Subtraction.new(result, expression2)
      else
        break
      end
    end

    result
  end

  def expression2
    result = expression3

    while not end_reached?
      case (token = peek).type
      when :times
        consume
        result = Multiplication.new(result, expression3)
      when :divide
        consume
        result = Division.new(result, expression3)
      when :modulo
        consume
        result = Modulo.new(result, expression3)
      else
        break
      end
    end

    result
  end

  def expression3
    case (token = consume).type
    when :minus
      Multiplication.new(Literal.new(-1), expression3)
    when :number
      Literal.new(token.value.to_f)
    when :identifier
      identifier = token.value

      case
      when !end_reached? && (nxt = peek).type == :assign
        consume
        expr = expression1
        Assignment.new(identifier, expr)
      when @environment.has_key?(identifier) && Function === (func = @environment[identifier])
        arity = func.parameters.size
        arguments = (1..arity).map { expression3 }
        FunctionCall.new(identifier, arguments)
      else
        Variable.new(identifier)
      end
    when :lparen
      expr = expression1
      raise 'Expected )' unless consume.type == :rparen
      expr
    end
  end

  def peek
    @tokens[@index]
  end

  def consume
    result = @tokens[@index]
    @index += 1
    result
  end

  def end_reached?
    @index == @tokens.size
  end
end


class Interpreter
  def initialize
    @environment = {}
  end

  def input(expr)
    tokens = Tokenizer.new(expr).tokens.to_a
    expr = Parser.new(@environment, tokens).parse

    expr&.evaluate(@environment) || ''
  end
end

$interpreter = Interpreter.new

def interpret(input)
  p input
  $interpreter.input(input)
end
