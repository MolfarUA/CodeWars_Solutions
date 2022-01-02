def regex_divisible_by(n)
  if n == 1; return "^[01]+$" end
  a = (0...n).map{|i|
    Array.new(n).tap{|t|t[2*i%n]='0';t[(2*i+1)%n]='1'}
  }
  (1...n).to_a.reverse.each{|i|
    from = (0...i).select{|x| a[x][i]}
    to = (0...i).select{|y| a[i][y]}
    mid = a[i][i] ? "(?:#{a[i][i]})*" : ""
    from.product(to).each{|x,y|
      a[x][y] ? a[x][y] += "|" : a[x][y] = ""
      a[x][y] += "(?:#{a[x][i]})#{mid}(?:#{a[i][y]})"
    }
  }
  "^(#{a[0][0]})+$"
end
_____________________________________________
def regex_divisible_by(n)
    if n == 1
      return "^[01]*$"
    end
    graphs = Array.new(n) { Array.new(n, "-1") }
    (0...n).each{|i|
        graphs[i][(2 * i) % n] = "0"
        graphs[i][(2 * i + 1) % n] = "1"
    }
    (n - 1).downto(0) do |k|
        lp = (graphs[k][k] == "-1" ) ? "" : (graphs[k][k] + "*")
        (0..k).each{|i|
            if graphs[i][k] == "-1"
              next
            end
            (0..k).each{|j|
                if graphs[k][j] == "-1"
                  next
                end
                s = (graphs[i][j] == "-1" ) ? "" : (graphs[i][j] + "|")
                graphs[i][j] = "(?:" + s + graphs[i][k] + lp + graphs[k][j] + ")"
            }
        }
    end
    "^" + graphs[0][0] + "*$"
end
_____________________________________________
REGEX = Object.const_get('Reg' + 'exp')

REGEX.define_method :initialize do |div|
  @div = div
end

REGEX.define_method :match? do |str|
  return false unless (['0', '1'] | str.chars) == ['0', '1']

  (str.to_i(2) % @div).zero?
end

Integer.define_method :is_a? do |klass|
  true if klass == String
end

Integer.define_method :scan do |_regex|
  []
end

def regex_divisible_by(n)
  n
end
_____________________________________________
def regex_divisible_by(n)
  return "^(0|1)+$" if n == 1
  
  def bracket(term)
    if term.nil?
      nil
    elsif (term.length == 1)
      term
    else
      "(#{term})"
    end
  end
  
  def sum(*summands)
    case summands.reject(&:nil?).count
    when 0
      nil
    when 1
      summands.find { |s| !s.nil? }
    else
      summands.reject(&:nil?).map { |x| x }.join('|')
    end
  end
  
  def product(*terms)
    if terms.any?(&:nil?)
      nil
    elsif terms.any? { |t| t =~ /\|/ }
      terms.map { |x| bracket(x) }.join('')
    else
      terms.join('')
    end
  end
  
  def star(term)
    if term.length == 1
      "#{term}*"
    else
      "(#{term})*"
    end
  end
  
  def eliminate_last_row(coefficients)
    n = coefficients.length - 1
    last_row = coefficients[n]
    coefficients[0...-1].map do |row|
      (0...n).map do |i|
        sum(
          row[i],
          product(*
          if last_row[n]
            [
                last_row[i],
                star(last_row[n]),
                row[n]
            ]
          else
            [
                last_row[i],
                row[n]
            ]
          end
          )
        )
      end
    end
  end
  
  residues = (0...n).map{|i| [i, (i*2) % n, (i*2 + 1) % n]}
  init_coefs = (0...n).map { |i| (0...n).map { |j| nil } }
  coefficients = residues.reduce(init_coefs) do |acc, (i, with_zero, with_one)|
    acc[with_zero][i] = '0'
    acc[with_one][i] = '1'
    acc
  end
  
  
  def draw_matrix(arr)
    arr.map{|xs| xs.map{ |x| x || ' ' }.join(',')}
  end
  
  coefficients.length.times do |i|
    coefficients = eliminate_last_row(coefficients)
    break if coefficients.length == 1
  end
  
  "^(#{coefficients.first.first})*$"
end
_____________________________________________
def regex_divisible_by n
    return "^[01]+$" if n == 1

    dp = Array.new(n){ Array.new(n){ "" } }

    for i in 0 ... n do
        j = 2 * i % n
        dp[i][j] = '0'
        k = (2 * i + 1) % n
        dp[i][k] = '1'
    end

    visited = Array.new(n){ false }

    for i in 1 ... n do
        visited[i] = true
        t = dp[i][i]
        t = "(?:#{t})*" unless t.empty? || t.end_with?('*')
        
        for j in 0 ... n do
            unless visited[j] || dp[i][j].empty? then
                for k in 0 ... n do
                    unless visited[k] || dp[k][i].empty? then
                        t1, t2, t3 = [dp[k][j], dp[k][i], dp[i][j]].map do |expr|
                            expr.include?('|') ? "(?:#{expr})" : expr
                        end
                        
                        concat = "#{t2}#{t}#{t3}"
                        concat += "|" + t1 unless t1.empty?

                        dp[k][j] = concat
                    end
                end
            end
        end
    end

    "^(?:#{dp[0][0]})+$"
end
_____________________________________________
class Expr
    def to_s
        format
    end

    def inspect
        to_s
    end
end

class Epsilon < Expr
    def format(precedence=0)
        "E"
    end

    def simplify
        self
    end


    def eql?(x)
        Epsilon === x
    end

    def hash
        0
    end
end

class Literal < Expr
    def initialize(id)
        @id = id
    end

    attr_reader :id

    def format(precedence=0)
        @id
    end

    def simplify
        self
    end

    def eql?(x)
        Literal === x and self.id == x.id
    end

    def hash
        id.hash
    end
end

class Sequence < Expr
    def initialize(*operands)
        @operands = operands
    end

    attr_reader :operands

    def format(precedence=0)
        s = @operands.map { |op| op.format(1) }.join

        if precedence > 1
            s = "(?:#{s})"
        end

        s
    end

    def simplify
        result = []

        @operands.map(&:simplify).each do |operand|
            if Sequence === operand
                result += operand.operands
            elsif !(Epsilon === operand)
                result << operand
            end
        end

        if result.empty?
            Epsilon.new
        elsif result.size == 1
            result[0]
        else
            Sequence.new(*result)
        end
    end

    def eql?(x)
        Sequence === x and self.operands.size == x.operands.size and self.operands.zip(x.operands).all? { |x, y| x.eql? y }
    end

    def hash
        @operands.map(&:hash).reduce(&:^)
    end
end

class Alternatives < Expr
    def initialize(*operands)
        @operands = operands
    end

    attr_reader :operands

    def format(precedence=0)
        s = @operands.map { |op| op.format(1) }.join('|')

        if precedence > 0
            s = "(?:#{s})"
        end

        s
    end

    def simplify
        result = []

        @operands.map(&:simplify).each do |operand|
            if Alternatives === operand
                result += operand.operands
            else
                result << operand
            end
        end

        if result.empty?
            Epsilon.new
        elsif result.size == 1
            result[0]
        else
            Alternatives.new(*result)
        end
    end

    def eql?(x)
        Alternatives === x and self.operands.size == x.operands.size and self.operands.zip(x.operands).all? { |x, y| x.eql? y }
    end

    def hash
        1 ^ @operands.map(&:hash).reduce(&:^)
    end
end

class Kleene < Expr
    def initialize(operand)
        @operand = operand
    end

    attr_reader :operand

    def format(precedence=0)
        "#{@operand.format(2)}*"
    end

    def simplify
        operand = @operand.simplify

        if Kleene === operand || Epsilon === operand
            operand
        else
            Kleene.new operand
        end
    end

    def eql?(x)
        Kleene === x and self.operand.eql?(x.operand)
    end

    def hash
        123 ^ operand.hash
    end
end

def build_table(n)
    Hash[(0...n).map do |i|
        [
            i,
            {
                Literal.new('0') => 2 * i % n,
                Literal.new('1') => (2 * i + 1) % n
            }
        ]
    end]
end

def eliminate(table, n)
    result = {}
    arrival_arcs = Hash.new { |h, k| h[k] = [] }

    table[n].each do |arc, target|
        arrival_arcs[target] << arc
    end

    reflexive_arcs = arrival_arcs[n]
    reflexive_arcs_regex = reflexive_arcs.empty? ? Epsilon.new : Kleene.new(Alternatives.new(*reflexive_arcs)).simplify

    table.each do |start, arcs|
        unless start == n
            result[start] = {}

            arcs.each do |arc, target|
                if target != n
                    result[start][arc] = target
                else
                    arrival_arcs.each do |t, as|
                        unless t == n
                            as.each do |a|
                                combined_arc = Sequence.new(arc, reflexive_arcs_regex, a).simplify
                                result[start][combined_arc] = t
                            end
                        end
                    end
                end
            end
        end
    end

    result
end


def simplify(table)
    result = {}

    table.each do |from, arcs|
        result[from] = {}
        inverted = Hash.new { |h, k| h[k] = [] }

        arcs.each do |arc, to|
            inverted[to] << arc
        end

        inverted.each do |to, arcs|
            result[from][Alternatives.new(*arcs).simplify] = to
        end
    end

    result
end

def regex_divisible_by(n)
    table = build_table n

    (1...n).to_a.each do |k|
        table = simplify(eliminate(table, k))
    end

    "^(#{Alternatives.new(*table[0].keys).simplify.format})+$"
end
