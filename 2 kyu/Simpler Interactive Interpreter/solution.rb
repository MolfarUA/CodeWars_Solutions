class Interpreter
  def initialize
    @variables = {}
  end

  def input(expression)
    evaluate(expression.gsub(%r{[^\w\*/\+-\.\(\)%=]}, ''))
  end

  private

  def evaluate(expression)
    expression.empty? && '' ||
      number(expression) ||
      variable(expression) ||
      assignment(expression) ||
      sum(expression) ||
      multiplication(expression) ||
      expression =~ /^\(.+\)$/ && evaluate(expression[1..-2])
  end

  def number(expression)
    expression.to_f if expression =~ /^[\+-]?\d+(\.\d+)?$/
  end

  def variable(expression)
    return unless expression =~ /^\w+$/
    @variables[expression] || raise("ERROR: Invalid identifier. No variable "\
                                    "with name '#{expression}' was found.")
  end

  def sum(expression)
    expression.gsub!('--', '+')
    operation_at = last_operation_at(expression, /\+|-/)
    return unless operation_at
    operation = expression[operation_at]
    expr1 = operation_at > 0 ? evaluate(expression[0..operation_at - 1]) : 0
    expr2 = evaluate(expression[operation_at + 1..-1])
    operation == '-' ? expr1 - expr2 : expr1 + expr2
  end

  def multiplication(expression)
    operation_at = last_operation_at(expression, %r{\*|\/|%})
    return unless operation_at
    operation = expression[operation_at]
    expr1 = evaluate(expression[0..operation_at - 1])
    expr2 = evaluate(expression[operation_at + 1..-1])
    operation == '*' && expr1 * expr2 ||
      operation == '%' && expr1 % expr2 || expr1 / expr2
  end

  def assignment(expression)
    match = expression.match(/^(?<variable>\w+)=(?<expression>.+)$/)
    return unless match
    @variables[match[:variable]] = evaluate(match[:expression])
  end

  def last_operation_at(expression, pattern)
    stack_size = 0
    (expression.size - 1).downto(0) do |i|
      case expression[i]
      when pattern
        return i if stack_size.zero? && expression[i - 1] !~ %r{\*|/}
      when ')'
        stack_size += 1
      when '('
        stack_size -= 1
      end
    end
    nil
  end
end

________________________________________________________
class Interpreter
  def input expr
    return "" if expr.empty?
    print expr
    Kernel::eval expr
  end
end

________________________________________________________
class Interpreter
  def initialize
    @instructions = []
  end
  
  def compile_and_eval
    RubyVM::InstructionSequence.compile(@instructions.join(';')).eval || ''
  end
  
  def input(expression)
    @instructions << expression
    begin
      compile_and_eval
    rescue => e
      @instructions.pop
      raise
    end
  end
end

________________________________________________________
class Interpreter
  def initialize
    @vars = []
    @b = binding
  end

  def input(expr)
    if expr.match?(/([a-zA-Z]+.=.\d+)/)
      varible_name = expr.scan(/[a-zA-Z]+/).first
      varible_value = expr.scan(/\d+/).first
      
      @vars << { name: varible_name.to_sym, value: varible_value.to_i } 
    end
    
    @vars.each do |var|
      @b.local_variable_set var[:name], var[:value]
    end

    Kernel.eval(expr, @b) || ""
  end
end
