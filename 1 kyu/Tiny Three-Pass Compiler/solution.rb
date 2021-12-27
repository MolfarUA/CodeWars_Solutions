class Compiler
    
    @@OP_FUNC = {'+'=> ->(a,b){a+b}, '-'=> ->(a,b){a-b}, '*'=> ->(a,b){a*b}, '/'=> ->(a,b){a/b},}
    @@OP_CMD  = {'+'=> 'AD', '-'=> "SU", '*'=> 'MU', '/'=> "DI"}

    def compile(program) return pass3(pass2(pass1(program))) end
    
    
    def pass1(program)
        @tokens = program.scan(/[+*\/()\[\]-]|[A-Za-z]+|\d+/)
        @args   = {}
        ast = parseFunc()
        raise Exception.new("Tokens list should be empty: #{@tokens}") unless @tokens.empty?
        return ast
    end
    
    def taste(r=nil)
        return r.nil? ? "NOTHING" : @tokens[0] if @tokens.empty?
        return r.nil? ? false : @tokens[0].match?(r)
    end
    
    def eat(r=nil)
        raise Exception.new("Couldn't match #{taste()} with #{r}") if !r.nil? && !taste(r)
        return @tokens.shift
    end
    
    def parseFunc()
        if taste(/\[/)
            n = 0
            eat()
            while !taste(/\]/)
                @args[eat(/\w+/)] = n
                n+=1
            end
            eat(/\]/)
        end
        return parseAddSub()
    end
    
    def parseAddSub()
        node = parseMulDiv()
        while taste(/[+-]/)
            node = {'op'=> eat(), 'a'=> node, 'b'=>parseMulDiv()}
        end
        return node
    end
    
    def parseMulDiv()
        node = parseTerm()
        while taste(/[*\/]/)
            node = {'op'=> eat(), 'a'=> node, 'b'=>parseTerm()}
        end
        return node
    end
    
    def parseTerm()
        return {'op'=> "imm", 'n'=> eat().to_i}   if taste(/\d+/)
        return {'op'=> "arg", 'n'=> @args[eat()]} if taste(/\w+/)
        eat(/\(/)
        node = parseAddSub()
        eat(/\)/)
        return node
    end
    

    def pass2(node)
        return node if node.has_key?('n')
        
        node['a'] = pass2(node['a'])
        node['b'] = pass2(node['b'])
        
        if node['a']['op']=='imm' && node['b']['op']=='imm'
            node = {'op'=> "imm", 'n'=> @@OP_FUNC[node['op']].call(node['a']['n'], node['b']['n'])}
        end
        return node
    end
    

    def pass3(node)
        lst = []
        toAsm(node, lst)
        lst << 'PO'
        return lst
    end
    
    def toAsm(node, lst)
        if node.has_key?('n')
            lst << "#{ node['op'].upcase[0..1] } #{ node['n'] }"
        else
            toAsm(node['a'], lst)
            toAsm(node['b'], lst)
            lst.concat([ 'PO', 'SW', 'PO', @@OP_CMD[node['op']] ])
        end
        lst << 'PU'
    end
end

________________________________
class Compiler

    def compile program
      ast = pass1 program
      ast = pass2 ast
      sub2 = pass3 ast
    end
  
    def pass1 program
      tok = tokenize program
      @par = process_signature! tok
      process_function! tok
    end
  
    def pass2 ast
      optimize! ast
    end
  
    def pass3 ast
      assemble ast
    end
  
    private
  
    def tokenize program
      program.scan(%r'[-+*/()\[\]]|[A-Za-z]+|\d+').map { |token| /^\d+$/.match(token) ? token.to_i : token }
    end
  
    def process_signature! tok
      tok.shift
      par = []
      while (t = tok.shift) != ']'
        compile_error 1 if t.nil?
        par.push t
      end
      par.each_with_index.to_h
    end
  
    def process_function! tok
      if tok.size == 1 
        tok = tok[0]
        if tok.is_a? Integer
          {'op' => 'imm', 'n' => tok}
        else
          {'op' => 'arg', 'n' => @par[tok]}
        end
      elsif tok.size == 3 
        b = process_function! [tok.pop]
        op = tok.pop
        a = process_function! [tok.pop]
        {'op' => op, 'a' => a, 'b' => b}
      elsif tok.last == ')' 
        tok.pop
        factor = []
        while (t = tok.pop) != '('
          factor.push t
        end
        factor.reverse!
        b = process_function! factor
        op = tok.pop
        if op
          if op =~ /[-+]/
            a = process_function! tok
            {'op' => op, 'a' => a, 'b' => b}
          else
            term = []
            term.push t until (t = tok.pop).nil? || (t =~ /[-+]/ && term.count('(') == term.count(')'))
            term.reverse!
            a = process_function! term
            b = {'op' => op, 'a' => a, 'b' => b}
            if t
              op = t
              a = process_function! tok
              {'op' => op, 'a' => a, 'b' => b}
            else
              b
            end
          end
        else
          b
        end
      elsif tok[-2] =~ /[-+]/ 
        b = process_function! [tok.pop]
        op = tok.pop
        a = process_function! tok
        {'op' => op, 'a' => a, 'b' => b}
      else 
        term = []
        term.push t until (t = tok.pop).nil? || (t =~ /[-+]/ && term.count('(') == term.count(')'))
        term.reverse!
        if t
          b = process_function! term
          op = t
          a = process_function! tok
        else
          b = process_function! [term.pop]
          op = term.pop
          a = process_function! term
        end
        {'op' => op, 'a' => a, 'b' => b}
      end
    end
  
    def optimize! ast
      if ast['op'] == 'imm' || ast['op'] == 'arg'
        ast
      else
        ast = {
          'op' => ast['op'],
          'a'  => optimize!(ast['a']),
          'b'  => optimize!(ast['b'])
        }
        if ast['a']['op'] == 'imm' && ast['b']['op'] == 'imm'
          n = ast['a']['n'].send ast['op'], ast['b']['n']
          {'op' => 'imm', 'n' => n}
        else
          ast
        end
      end
    end
  
    def assemble ast
      case ast['op']
      when 'imm'
        return "IM #{ast['n']}"
      when 'arg'
        return "AR #{ast['n']}"
      else
        op = {'+' => 'AD', '-' => 'SU', '*' => 'MU', '/' => 'DI'}[ast['op']]
      end
      a = assemble ast['a']
      b = assemble ast['b']
      [a, 'PU', b, 'SW', 'PO', op].flatten
    end
  end
  
  def simulate(sub2, argv)
      r0, r1 = 0, 0
      stack = []
      sub2.each do |ins|
          if ins[0..1] == 'IM' or ins[0..1] == 'AR'
              ins, n = ins[0..1], ins[2..-1].to_i
          end
          if ins == 'IM'    then r0 = n
          elsif ins == 'AR' then r0 = argv[n]
          elsif ins == 'SW' then r0, r1 = r1, r0
          elsif ins == 'PU' then stack.push(r0)
          elsif ins == 'PO' then r0 = stack.pop()
          elsif ins == 'AD' then r0 += r1
          elsif ins == 'SU' then r0 -= r1
          elsif ins == 'MU' then r0 *= r1
          elsif ins == 'DI' then r0 /= r1
          end
      end
      return r0
  end
  
  program = '[ a b c ] a + b * b + c - 6 * (5 + 3 * a)'
  arguments = [99, 103, 33]
  
  compiler = Compiler.new
  p simulate(compiler.compile(program), arguments)
            
_________________________________
class Compiler

  def compile program
    ast = pass1 program
    ast = pass2 ast
    asm = pass3 ast
  end

  def pass1 program
    tokens = tokenize program
    @args = process_signature! tokens
    process_function! tokens
  end

  def pass2 ast
    optimize! ast
  end

  def pass3 ast
    assemble ast
  end

  private

  def tokenize program
    program.scan(%r'[-+*/()\[\]]|[A-Za-z]+|\d+').map { |token| /^\d+$/.match(token) ? token.to_i : token }
  end

  def process_signature! tokens
    tokens.shift
    args = []
    while (t = tokens.shift) != ']'
      compile_error 1 if t.nil?
      args.push t
    end
    args.each_with_index.to_h
  end

  def process_function! tokens
    if tokens.size == 1 # simple factor
      tokens = tokens[0]
      if tokens.is_a? Integer
        {'op' => 'imm', 'n' => tokens}
      else
        {'op' => 'arg', 'n' => @args[tokens]}
      end
    elsif tokens.size == 3 # term | simple expression
      b = process_function! [tokens.pop]
      op = tokens.pop
      a = process_function! [tokens.pop]
      {'op' => op, 'a' => a, 'b' => b}
    elsif tokens.last == ')' # factor
      tokens.pop
      factor = []
      while (t = tokens.pop) != '('
        factor.push t
      end
      factor.reverse!
      b = process_function! factor
      op = tokens.pop
      if op
        if op =~ /[-+]/
          a = process_function! tokens
          {'op' => op, 'a' => a, 'b' => b}
        else
          term = []
          term.push t until (t = tokens.pop).nil? || (t =~ /[-+]/ && term.count('(') == term.count(')'))
          term.reverse!
          a = process_function! term
          b = {'op' => op, 'a' => a, 'b' => b}
          if t
            op = t
            a = process_function! tokens
            {'op' => op, 'a' => a, 'b' => b}
          else
            b
          end
        end
      else
        b
      end
    elsif tokens[-2] =~ /[-+]/ 
      b = process_function! [tokens.pop]
      op = tokens.pop
      a = process_function! tokens
      {'op' => op, 'a' => a, 'b' => b}
    else 
      term = []
      term.push t until (t = tokens.pop).nil? || (t =~ /[-+]/ && term.count('(') == term.count(')'))
      term.reverse!
      if t
        b = process_function! term
        op = t
        a = process_function! tokens
      else
        b = process_function! [term.pop]
        op = term.pop
        a = process_function! term
      end
      {'op' => op, 'a' => a, 'b' => b}
    end
  end

  def optimize! ast
    if ast['op'] == 'imm' || ast['op'] == 'arg'
      ast
    else
      ast = {
        'op' => ast['op'],
        'a'  => optimize!(ast['a']),
        'b'  => optimize!(ast['b'])
      }
      if ast['a']['op'] == 'imm' && ast['b']['op'] == 'imm'
        n = ast['a']['n'].send ast['op'], ast['b']['n']
        {'op' => 'imm', 'n' => n}
      else
        ast
      end
    end
  end

  def assemble ast
    case ast['op']
    when 'imm'
      return "IM #{ast['n']}"
    when 'arg'
      return "AR #{ast['n']}"
    else
      op = {'+' => 'AD', '-' => 'SU', '*' => 'MU', '/' => 'DI'}[ast['op']]
    end
    a = assemble ast['a']
    b = assemble ast['b']
    [a, 'PU', b, 'SW', 'PO', op].flatten
  end
end

def simulate(asm, argv)
    r0, r1 = 0, 0
    stack = []
    asm.each do |ins|
        if ins[0..1] == 'IM' or ins[0..1] == 'AR'
            ins, n = ins[0..1], ins[2..-1].to_i
        end
        if ins == 'IM'    then r0 = n
        elsif ins == 'AR' then r0 = argv[n]
        elsif ins == 'SW' then r0, r1 = r1, r0
        elsif ins == 'PU' then stack.push(r0)
        elsif ins == 'PO' then r0 = stack.pop()
        elsif ins == 'AD' then r0 += r1
        elsif ins == 'SU' then r0 -= r1
        elsif ins == 'MU' then r0 *= r1
        elsif ins == 'DI' then r0 /= r1
        end
    end
    return r0
end

program = '[ a b c ] a + b * b + c - 6 * (5 + 3 * a)'
arguments = [99, 103, 33]

compiler = Compiler.new
p simulate(compiler.compile(program), arguments)
          
__________________________________

      @tokens << LParenToken.new
    when /^[)]/
      @tokens << RParenToken.new
    when /^(\w+)/
      @tokens << IdentifierToken.new($1)
    else
      raise "Cannot tokenize #{@string}"
    end

    @string = $'
  end

  def tokenize
    tokenize_next while not @string.empty?
    @tokens
  end
end

def tokenize(string)
  Lexer.new(string).tokenize
end

LiteralAst = Struct.new :value do
  def substitute(parameters)
    self
  end

  def json
    { "op" => 'imm', "n" => value }
  end

  def simplify
    self
  end

  def compile
    [ "IM #{value}" ]
  end

  def to_s
    value.to_s
  end
end

OperationAst = Struct.new :operator, :left, :right do
  def substitute(parameters)
    l = left.substitute(parameters)
    r = right.substitute(parameters)
    OperationAst.new(operator, l, r)
  end

  def to_s
    "(#{operator} #{left} #{right})"
  end

  def json
    { "op" => operator.to_s, 'a' => left.json, 'b' => right.json }
  end

  def simplify
    l = left.simplify
    r = right.simplify

    case
    when LiteralAst === l && LiteralAst === r
      value = l.value.send(operator, r.value)
      LiteralAst.new value
    when operator == :+ && LiteralAst === l && l.value == 0
      r
    when operator == :+ && LiteralAst === r && r.value == 0
      l
    when operator == :- && LiteralAst === r && r.value == 0
      l
    when operator == :* && LiteralAst === l && l.value == 1
      r
    when operator == :* && LiteralAst === r && r.value == 1
      l
    when operator == :/ && LiteralAst === r && r.value == 1
      l
    else
      OperationAst.new(operator, l, r)
    end
  end

  def compile
    [
      *left.compile,
      "PU",
      *right.compile,
      "SW",
      "PO",
      assembly_instruction
    ]
  end

  def assembly_instruction
    case operator
    when :+
      "AD"
    when :-
      "SU"
    when :*
      "MU"
    when :/
      "DI"
    end
  end
end

VariableAst = Struct.new :identifier do
  def substitute(parameters)
    index = parameters.index(identifier)
    ArgumentAst.new index
  end

  def simplify
    self
  end
end

FunctionAst = Struct.new :parameters, :body do
  def json
    body.json
  end

  def simplify
    FunctionAst.new(parameters, body.simplify)
  end
end

ArgumentAst = Struct.new :index do
  def json
    { op: 'arg', n: index }
  end

  def simplify
    self
  end

  def compile
    [ "AR #{index}" ]
  end

  def to_s
    "##{index}"
  end
end

class Parser
  def initialize(tokens)
    @tokens = tokens
    @index = 0
  end

  def consume
    @index += 1
  end

  def current
    @tokens[@index]
  end

  def end_reached?
    @index == @tokens.size
  end

  def parse
    parse_function
  end

  def parse_function
    if LBracketToken === current
      consume
      parameters = []
      while not (RBracketToken === current)
        parameters << current.name
        consume
      end
      consume
      body = parse_expression.substitute(parameters)
      FunctionAst.new(parameters, body)
    end
  end

  def parse_expression
    if result = parse_term
      while (PlusToken === current && op = :+) || (MinusToken === current && op = :-)
        consume
        term = parse_term
        result = OperationAst.new(op, result, term)
      end

      result
    end
  end

  def parse_term
    if result = parse_atom
      while (TimesToken === current && op = :*) || (DivideToken === current && op = :/)
        consume
        atom = parse_atom
        result = OperationAst.new(op, result, atom)
      end

      result
    end
  end

  def parse_atom
    case current
    when LiteralToken
      result = LiteralAst.new(current.value)
      consume
    when IdentifierToken
      result = VariableAst.new(current.name)
      consume
    when LParenToken
      consume
      result = parse_expression
      raise "Expected )" unless RParenToken === current
      consume
    else
      result = nil
    end

    result
  end
end

def parse(tokens)
  Parser.new(tokens).parse
end

def from_json(obj)
  case obj['op'] || obj[:op]
  when '+'
    left = from_json(obj['a'] || obj[:a])
    right = from_json(obj['b'] || obj[:b])
    OperationAst.new(:+, left, right)
  when '-'
    left = from_json(obj['a'] || obj[:a])
    right = from_json(obj['b'] || obj[:b])
    OperationAst.new(:-, left, right)
  when '*'
    left = from_json(obj['a'] || obj[:a])
    right = from_json(obj['b'] || obj[:b])
    OperationAst.new(:*, left, right)
  when '/'
    left = from_json(obj['a'] || obj[:a])
    right = from_json(obj['b'] || obj[:b])
    OperationAst.new(:/, left, right)
  when 'arg'
    ArgumentAst.new(obj['n'] || obj[:n])
  when 'imm'
    LiteralAst.new(obj['n'] || obj[:n])
  else
    raise "Unknown #{obj}"
  end
end


class Compiler
  def compile(program)
    return pass3(pass2(pass1(program)))
  end

  def pass1(program)
    tokens = tokenize(program)
    parse(tokens).json
  end

  def pass2(ast)
    from_json(ast).simplify.json
  end

  def pass3(ast)
    from_json(ast).compile
  end
end
  
_____________________________________
class Compiler

  def compile(program)
    return pass3(pass2(pass1(program)))
  end

  def tokenize(program)
    # Turn a program string into an array of tokens.  Each token
    # is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
    # name or a number (as a string)
    return program.scan(%r'[-+*/()\[\]]|[A-Za-z]+|\d+').map { |token| /^\d+$/.match(token) ? token.to_i : token }
  end

  IMM = 'imm'
  ARG = 'arg'

  PREC = {
    '+' => 1,
    '-' => 1,
    '*' => 2,
    '/' => 2,
    '^' => 3,
  }

  DUALS = PREC.keys

  def op(type, *values)
    DUALS.include?(type) ?
    { op: type, a: values.first, b: values.last } :
      { op: type, n: values.first }
  end

  def pass1(program)
    # Returns an un-optimized AST
    tokens = tokenize(program)
    params = {}
    if params_end_index = tokens.index(']')
      tokens[1...params_end_index].each_with_index { |label, index| params[label] = index }
      tokens = tokens[(params_end_index + 1)..-1]
    end
    output = []
    stack = []
    loop do
      break if tokens.empty?
      token = tokens.shift
      if token.is_a?(Integer)
        output << op(IMM, token)
      elsif params[token]
        output << op(ARG, params[token])
      elsif token == '('
        stack << token
      elsif token == ')'
        loop do
          token = stack.pop
          break if token == '('
          b, a = 2.times.map { output.pop }
          output << op(token, a, b)
        end
      else
        if PREC[token] > PREC[stack.last].to_i
          stack << token
        else
          loop do
            break if PREC[token] > PREC[stack.last].to_i
            b, a = 2.times.map { output.pop }
            output << op(stack.pop, a, b)
          end
          stack << token
        end
      end
    end
    stack.reverse.each do |token|
      b, a = 2.times.map { output.pop }
      output << op(token, a, b)
    end
    output.last
  end

  def pass2(ast)
    # Returns an AST with constant expressions reduced
    loop { break unless reduce!(ast) }
      ast
    end

    def reduce!(ast)
      reduced = false
      nodes = [ast]
      loop do
        break if nodes.empty?
        candidates = []
        nodes.each do |node|
          if DUALS.include?(node[:op])
            if node[:a][:op] == IMM && node[:b][:op] == IMM
              a, b = %i(a b).map { |k| node[k][:n] }
              op = node[:op]
              op = '**' if node == '^'
              node[:n] = a.send(op, b)
              node.delete(:a)
              node.delete(:b)
              node[:op] = IMM
              reduced = true
            else
              candidates << node[:a] unless [IMM, ARG].include?(node[:a][:op])
              candidates << node[:b] unless [IMM, ARG].include?(node[:b][:op])
            end
          end
        end
        nodes = candidates
      end
      reduced
    end

    OPS = { '+' => 'AD', '-' => 'SU', '*' => 'MU', '/' => 'DI' }
    
    def pass3(ast)
      # Returns assembly instructions
      op = ast[:op]
      if op == IMM
        ["IM #{ast[:n]}"]
      elsif op == ARG
        ["AR #{ast[:n]}"]
      else
        raise 'Unimplemented (^)' if op == '^'
        a, b = [pass3(ast[:a]), pass3(ast[:b])]
        result = %w(SW PU SW) + b + ['SW'] + a + [OPS[op]] + %w(SW PO SW)
        warn result.inspect
        result
      end
    end
  end
