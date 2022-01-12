def parse(expr)
  case expr 
    when /^\w+$/
    expr.strip
    when /->/
    "(#{$`[1..-1].split(?,).map(&:strip)*?,}){#{$'[0..-2].split.map{|p| p + ?;}*''}}"
    else
    "(){#{expr[1..-2].split.map{|p| p + ?;}*''}}"
  end
end

def transpile(expr)
  expr.gsub!(/\s+/,' ')
  expr.gsub!(/(?<=\W|^) | (?=\W|$)/,'')
  return '' unless /^(?<e>\w+|(?<l>{(\w+(,\w+)*->)?(\w+(\s+\w+)*)?}))(\((\g<e>(,\g<e>)*)?\)\g<l>?|\g<l>)$/ === expr
  return '' if /\b\d+[a-zA-Z_]/ === expr
  fun, *param = expr.gsub(/\n/,'').scan(/\w+|{.*?}/)
  parse(fun) + ?( + param.map{|p| parse(p)}*?, + ?)
end
_____________________________________________________
def transpile(expr)
  puts expr
  tokens = Lexer.new(expr).tokenize
  ast = Parser.new(tokens).parse
  Transpiler.new(ast).transpile
rescue Lexer::LexerError, Parser::ParserError
  ""
end

class Token
  attr_reader :type, :literal

  def initialize(type, literal = nil)
    @type = type
    @literal = literal
  end

  def inspect
    literal ? "[:#{type}, '#{literal}']" : "[:#{type}]"
  end
end

class Lexer
  class LexerError < StandardError; end

  def initialize(expr)
    @expr = expr
    @start = 0
    @current = 0
    @tokens = []
  end

  def tokenize
    while !is_at_end?
      @start = @current
      c = advance

      case c
      when "("
        add_simple_token(:left_paren)
      when ")"
        add_simple_token(:right_paren)
      when "{"
        add_simple_token(:left_brace)
      when "}"
        add_simple_token(:right_brace)
      when ","
        add_simple_token(:comma)
      when "-"
        add_simple_token(:arrow) if match?(">")
      when " ", "\n"
      else
        if is_digit?(c)
          number
        elsif is_letter?(c)
          identifier
        else
          raise LexerError
        end
      end
    end
    @tokens << Token.new(:eof)
    @tokens
  end

  def advance
    @current += 1
    @expr[@current - 1]
  end

  def peek
    return "\0" if is_at_end?
    @expr[@current]
  end

  def add_simple_token(type)
    @tokens << ::Token.new(type)
  end

  def add_compound_token(type, literal)
    @tokens << ::Token.new(type, literal)
  end

  def is_digit?(c)
    c =~ /[[:digit:]]/
  end

  def is_letter?(c)
    c =~ /[[:alnum:]]/ || c =~ /\_/
  end

  def match?(c)
    return false if is_at_end?
    return false if @expr[@current] != c

    @current += 1
    true
  end

  def is_at_end?
    @current >= @expr.length
  end

  def number
    advance while is_digit?(peek)
    value = @expr[@start...@current]
    add_compound_token(:number, value.to_i)
  end

  def identifier
    advance while is_letter?(peek)
    value = @expr[@start...@current]
    raise LexerError if value.start_with?(/[0-9]/)
    add_compound_token(:identifier, value)
  end
end

# function ::= expression "(" [parameters] ")" [lambda]
#            | expression lambda

# expression ::= nameOrNumber
#              | lambda

# parameters ::= expression ["," parameters]

# lambdaparam ::= nameOrNumber ["," lambdaparam]
# lambdastmt  ::= nameOrNumber [lambdastmt]

# lambda ::= "{" [lambdaparam "->"] [lambdastmt] "}"

class Parser
  class ParserError < StandardError; end

  def initialize(tokens)
    @tokens = tokens
    @current = 0
  end

  def parse
    function
  end

  def function
    expr = expression
    params = parameters
    lambda_expr = lambda

    raise ParserError unless is_at_end?

    ::Function.new(expr, params, lambda_expr)
  end

  def expression
    if check?(:identifier) || check?(:number) || check?(:left_brace)
      return ::Literal.new(previous.literal) if match?(:identifier, :number)

      lambda
    else
      raise ParserError
    end
  end

  def lambda
    if match?(:left_brace)
      params = lambda_params
      stmt = lambda_stmt
      consume(:right_brace)
      ::Lambda.new(params, stmt)
    end
  end

  def parameters
    if match?(:left_paren)
      params = []
      while !check?(:right_paren) &&
        params << expression
        consume(:comma) unless check?(:right_paren)
      end
      @current -= 1 if previous.type == :comma
      consume(:right_paren)
      params
    end
  end

  def lambda_params
    params = []
    return params if no_lambda_params

    while match?(:identifier, :number)
      params << ::Literal.new(previous.literal)
      consume(:comma) unless check?(:arrow)
    end

    consume(:arrow)
    raise ParserError if params.none?
    params
  end

  def no_lambda_params
    tmp = @current - 1
    while @tokens[tmp].type != :right_brace
      return false if @tokens[tmp].type == :arrow
      tmp += 1
    end
    true
  end

  def lambda_stmt
    identifiers = []
    while match?(:identifier, :number)
      identifiers << ::Literal.new(previous.literal)
    end

    ::LambdaStmt.new(identifiers)
  end

  def name_or_number
    return ::Literal.new(previous().literal) if match?(:identifier, :number)
  end

  def consume(*types)
    types.each do |t|
      if check?(t)
        return advance
      end
    end

    raise ParserError.new("#{types.map(&:to_s).join(' or ')} not present")
  end

  def advance
    @current += 1 unless is_at_end?
    previous
  end

  def check?(type)
    return if is_at_end?
    peek.type == type
  end

  def match?(*types)
    types.each do |t|
      if check?(t)
        advance
        return true
      end
    end

    false
  end

  def peek
    @tokens[@current]
  end

  def previous
    return nil if @current == 0
    @tokens[@current - 1]
  end

  def is_at_end?
    peek.type == :eof
  end
end

module Visitor
  def accept(visitor)
    visitor.send("visit#{self.class.name}Expr", self)
  end
end

class Function
  include Visitor

  attr_reader :expr, :params, :lambda

  def initialize(expr, params, lambda)
    @expr = expr
    @params = params
    @lambda = lambda
  end
end

class Lambda
  include Visitor

  attr_reader :params, :stmt

  def initialize(params, stmt)
    @params = params
    @stmt = stmt
  end
end

class Literal
  include Visitor

  attr_reader :value

  def initialize(value)
    @value = value
  end
end

class LambdaStmt
  include Visitor

  attr_reader :identifiers

  def initialize(identifiers)
    @identifiers = identifiers
  end
end

class Transpiler
  def initialize(expr)
    @expr = expr
  end

  def transpile
    @expr.accept(self)
  end

  def visitFunctionExpr(function_expr)
    expr = case function_expr.expr
           when Literal
             function_expr.expr.accept(self)
           when Lambda
             function_expr.expr.accept(self)
           end

    params = function_expr.params.map { |x| x.accept(self) }.join(",") if function_expr.params&.any?
    lambda = function_expr.lambda.accept(self) if function_expr.lambda

    content = [params, lambda].compact.join(",")

    expr ? expr + "(#{content})" : ""
  end

  def visitLambdaExpr(lambda_expr)
    str = "("
    if lambda_expr.params.any?
      str << lambda_expr.params.map { |x| x.accept(self) }.join(",")
    end
    str << ")"
    str << "{"
    if lambda_expr.stmt.identifiers.any?
      str << lambda_expr.stmt.identifiers.map { |x| x.accept(self) }.join(";")
      str << ";"
    end
    str << "}"
  end

  def visitLiteralExpr(literal_expr)
    literal_expr.value.to_s
  end
end

_____________________________________________________
class Transpiler
    def initialize expr
        @tokens = expr.scan(/->|[,(){}]|[_a-zA-Z]\w*|\d+|\S+?/).reverse
    end

    def exec
        begin
            result = fun
            fail unless @tokens.empty?
            result
        rescue
            String.new
        end
    end

    def name_or_number
        /[_a-zA-Z]\w*|\d+/ =~ @tokens.last && @tokens.pop
    end
    def fun
        f_prefix = expr
        fail unless f_prefix
        if @tokens.last == '(' then
            @tokens.pop
            f_params = params
            fail unless @tokens.pop == ')'
            f_suffix = _lambda
            f_params.push(f_suffix) if f_suffix
            "#{f_prefix}(#{f_params.join(',')})"
        else
            "#{f_prefix}(#{_lambda})"
        end
    end
    def expr
        name_or_number || _lambda
    end
    def params expect = false
        elem = expr
        arr = []
        if elem then
            if @tokens.last == ',' then
                @tokens.pop
                return [elem, *params(true)]
            end
            arr.push(elem)
        else fail if expect
        end
        arr
    end
    def lambda_params expect = false
        elem = name_or_number
        if elem then
            case @tokens.last
            when ','
                @tokens.pop
                return [elem, *lambda_params(true)]
            when '->'
                @tokens.pop
                return [elem]
            else
                fail if expect
                @tokens.push(elem)
            end
        else fail if expect
        end
        []
    end
    def lambda_stmt
        elem = name_or_number
        elem ? [elem, *lambda_stmt] : []
    end
    def _lambda
        return unless @tokens.last == '{'
        @tokens.pop
        l_params = lambda_params
        l_stmt = lambda_stmt
        fail unless @tokens.pop == '}'
        "(#{l_params.join(',')}){#{l_stmt.map{|s| s + ';'}.join}}"
    end
end

def transpile expression
    Transpiler.new(expression).exec
end
_____________________________________________________
require 'strscan'

DEBUG = true

def transpile(s)
  scanner = StringScanner.new s.strip.gsub(/\n/, '')
  puts "In: `#{s}`" if DEBUG
  res = _function(scanner)
  puts "Res: #{res.inspect}", "remainder: #{scanner.inspect}", "" if DEBUG
  return res || "" if scanner.eos?
  ""
end

def _function(scanner)
  expression = _expression(scanner)
  return if expression&.empty?
  if scanner.scan(/ *\( */)
    parameters = _parameters(scanner)
    return unless parameters
    return unless scanner.scan(/ *\) */)
    return unless (lambda = _lambda(scanner))
    parameters << lambda unless lambda.empty?
    "#{expression}(#{parameters.join(',')})"
  else
    return unless (lambda = _lambda(scanner))
    "#{expression}(#{lambda})"
  end
end

def _name_or_number(scanner)
  scanner.scan(/ *(\d+(?=[^_a-zA-Z])|[_a-zA-Z][_a-zA-Z0-9]*) */)&.strip
end

def _expression(scanner)
  _name_or_number(scanner) || _lambda(scanner)
end

def _lambda(scanner)
  return "" unless scanner.scan(/ *{ */)
  reading_params = true
  has_arrow = false
  params = []
  stmts = []
  until scanner.scan(/ *} */)
    if reading_params && !params.empty? && scanner.scan(/ *, */) # params
      return unless (non = _name_or_number(scanner))
      params << non
    elsif !has_arrow && !params.empty? && scanner.scan(/ *-> */) # ->
      has_arrow = true
      reading_params = false
    else
      return unless (non = _name_or_number(scanner))
      if reading_params # we are reading params; could be first param, or stmt
        if params.empty? # first param
          params << non
        else # we were actually reading stmts
          return if params.length > 1
          reading_params = false
          stmts, params = params, []
          stmts << non
        end
      else
        stmts << non
      end
    end
  end
  stmts, params = params, [] if !has_arrow && params.length == 1
  "(#{params.join(',')}){#{stmts.join ';'}#{stmts.empty? ? "" : ";"}}"
end

def _parameters(scanner)
  return unless (expression = _expression(scanner))
  return [] if expression.empty?
  params = [expression]
  while scanner.scan(/ *, */)
    return if (expression = _expression(scanner))&.empty?
    params << expression
  end
  params
end
