class TermStringifier
  attr_reader :f, :exp

  def initialize(f, exp)
    @f   = f
    @exp = exp
  end

  def var_str(var)
    return ""  if exp == 0
    return var if exp == 1

    "#{var}^#{exp}"
  end
  
  def f_num
    return exp == 0 ? '1'  : ''  if f == 1
    return exp == 0 ? '-1' : '-' if f == -1

    f.to_s
  end
  
  def f_str(first)
    return f_num if first

    f > 0 ? "+#{f_num}" : f_num
  end
  
  def stringify(var, first)
    return '' if f == 0

    "#{f_str(first)}#{var_str(var)}"
  end  
end

class Term
  attr_reader :f, :exp, :stringifier

  def initialize(f, exp)
    @f   = f
    @exp = exp
    
    @stringifier = TermStringifier.new(f, exp)
  end
  
  def to_s(var, first: false)
    stringifier.stringify(var, first)
  end
  
  def *(other)
    Term.new f * other.f, exp + other.exp
  end
  
  def +(other)
    raise unless exp == other.exp

    return Term.new(f + other.f, exp)
  end
end

  
def expand(expr)
  expr.scan(/\((-?)(\d*)(\w)(.-?\d+)\)\^(-?\d+)/) do |(a_sign, a_num, var, b, n)|
    return '1' if n == '0'

    a = "#{a_sign}#{a_num == "" ? 1 : a_num}"

    terms = [Term.new(a.to_i, 1), Term.new(b.to_i, 0)]
    base_terms = terms

    (n.to_i - 1).times do
      terms = terms.flat_map do |term1|
        base_terms.map { |term2| term1 * term2 }
      end
  
      terms = terms
        .group_by { |term| term.exp }
        .each_pair.map { |_, terms| terms.reduce(:+) }
    end
  
    return terms.map.with_index { |term, i| term.to_s(var, first: i == 0) }.join
  end
end

___________________________________________________
class Term

  attr_accessor :coef, :unknow, :degree

  def initialize(coef, unknow, degree)
    @coef = coef
    @unknow = unknow
    @degree = degree
  end

  def <=>(other)

    result =  other.degree <=> @degree

    if result == 0
      result = other.unknow <=> @unknow
    end

    return result
  end

  def get_degree_s
    if @degree == 1
      degree_s = '' 
    else
      degree_s = "^#{@degree}"
    end
  end

  def get_coef_s
    coef_s = ''
    if @coef == -1 and not unknow.empty?
      coef_s = '-'
    elsif @coef == 1 and not unknow.empty?
      coef_s = ''
    else
      coef_s = @coef.to_s
    end  
  end

  def key
    "#{@unknow}#{get_degree_s}"
  end

  def to_s   

    "#{get_coef_s}#{unknow}#{get_degree_s}"
  end

  def self.multy(term1, term2)

    coef = term1.coef * term2.coef

    d1 = term1.unknow.empty? ? 0 : term1.degree
    d2 = term2.unknow.empty? ? 0 : term2.degree

    degree = d1 + d2

    degree = 1 if degree == 0

    unknow = (term1.unknow.empty?? nil : term1.unknow) || (term2.unknow.empty?? nil : term2.unknow)    
    unknow ||= ''
  
    Term.new(coef, unknow, degree)
  
  end

end

def expand expr

  p expr
  array = expr.split('^')
  degree = array[1].to_i

  return '1' if degree == 0
  
  terms = extract_terms(array[0])
  accum_terms = terms.map {|t| t}

  1.upto(degree-1) do
      termsTemp = []
      accum_terms.each do |tl|
        terms.each do |tr|
          term = Term.multy(tl, tr)
          termsTemp << term if term.coef != 0
        end
      end
      accum_terms = sum_terms(termsTemp)
  end

  result = terms_to_s(accum_terms)

end

def terms_to_s(terms)
  result = ''
  terms.each_index do |i|
    t = terms[i]
    plus = '+' if t.coef > 0 and i > 0
    result += "#{plus}#{t.get_coef_s}#{t.unknow}#{t.get_degree_s}"
  end
  result
end


def sum_terms(terms)

  h = Hash.new(0)

  terms.each do |term|
    h[term.key] += term.coef    
  end

  terms = []
  h.each do |k, v|
    u = extract_unknown(k)
    d = extract_degree(k)
    terms << Term.new(v, u, d)
  end  

  terms.sort! {|a,b| a<=>b}

end

def extract_terms(expr)
  terms = expr.scan /-*\d*[a-z]*\^*\d*/ 
  terms.reject! {|t| t.empty?}

  terms.map do |t|

    coef = extract_coef(t)
    unknow = extract_unknown(t)
    degree = extract_degree(t)
    Term.new(coef, unknow, degree)
  end

end

def extract_degree(expr)

  unknow = extract_unknown(expr)


  array = expr.split('^') 

  return 1 unless array[1]

  array[1].to_i
end

def extract_coef(expr)

  coef_s = expr[/^-?[0-9]*/]
  if coef_s == '-'
    -1
  elsif coef_s.empty? 
    1
  else
    coef_s.to_i
  end 
end

def extract_unknown(expr)
  u = expr[/[a-z]{1}/]
  u ||= ''
end

___________________________________________________
def expand expr
  pos = expr.rindex('^')
  p = expr[pos+1..].to_i
  return '1' if p.zero?
  expr = expr[1...pos-1]
  variable = expr[/[^+\-\d]/]
  expr.gsub!(Regexp.new('(?<!\d)'+variable), '1'+variable)
  first,last = expr.split(/([+-][^+-]+)/).filter(&''.method(:!=)).map(&:to_i)
  if last.zero?
    [[first ** p, p]]
  elsif first.zero?
    [[last ** p, 0]]
  else
    c = first ** p
    (0..p).map{|i|
      c = c * last / first * (p-i+1) / i unless i.zero?
      [c , p-i]
    }
  end
  .map{|(a,k)| (a==1 && k>0 ? '' : a == -1 && k>0 ? '-' : a.to_s)+(k.zero? ? '': variable + (k>1? '^'+k.to_s : ''))}.join('+').gsub('+-','-')
end

___________________________________________________
class PolynomePart
  attr_accessor :coef, :var, :degree

  def initialize(coef, var = '', degree = 0)
    @coef = coef
    @var = var
    @degree = degree
  end

  def *(obj)
    raise 'Failed to multiply polynomes with different indeterminates' if !@var.empty? && !obj.var.empty? && @var != obj.var
    PolynomePart.new(@coef * obj.coef, @var.empty? ? obj.var : @var, @degree + obj.degree)
  end  

  def +(obj)
    raise 'Failed to sum polynomes with different indeterminates' if @var != obj.var
    PolynomePart.new(@coef + obj.coef, @var || obj.var, @degree)
  end  

  def to_s
    return coef.to_s if coef == 0 || degree == 0
    (coef.abs == 1 ? coef.to_s[0..-2] : coef.to_s) + var + (degree == 1 ? '' : "^#{degree}")
  end
end

def expand expr
  _, coef, var, num, degree = /\(([-+]?[0-9]*)([a-z])([-+][0-9]+)\)\^([0-9]+)/.match(expr).to_a

  return '1' if degree == '0'

  coef += '1' if coef == '' || coef == '-'

  list = [PolynomePart.new(coef.to_i, var, 1), PolynomePart.new(num.to_i)]

  (degree.to_i - 1).times
                   .inject(list) { |product, n| multiply_polynomes(product, list) }
                   .map { |x| x.to_s }.join('+').gsub('+-', '-')
end

def multiply_polynomes(list1, list2)
  list1.product(list2)
       .map      { |x| x[0] * x[1] }
       .reject   { |x| x.coef == 0 }
       .group_by { |x| x.degree}
       .map      { |g| g[1].inject { |product, x| product.nil? ? x : product + x } }
end


___________________________________________________
class Chlen
  attr_accessor :coef, :var, :step

  def initialize(coef, var, step)
    @coef = coef
    @var = var
    @step = step
  end

  def to_s
    return '0' if coef == 0
    return coef.to_s if step == 0
    if var
      c = coef == 1 ? '' : (coef == -1 ? '-' : coef.to_s)
    else
      c = coef.to_s
    end
#     pp "<#{c} vs #{coef}>"
    return "#{c}#{var}" if step == 1
    "#{c}#{var}^#{step}"
  end

  def inspect
    to_s + '@'
  end
  
  def *(obj)
    Chlen.new(@coef * obj.coef, @var || obj.var, @step + obj.step)
  end  

  def +(obj)
    Chlen.new(@coef + obj.coef, @var || obj.var, @step)
  end  
end

def expand expr
  m = /\(([-+0-9]*)([a-z])([-+0-9]+)\)\^([0-9]+)/.match(expr)
  coef = m[1]

  coef = '-1' if coef == '-'
  coef = coef.empty? ? 1 : coef.to_i
  
  var = m[2]

  num = m[3]
  num = num.empty? ? 0 : num.to_i

  step = m[4]
  step = step.empty? ? 1 : step.to_i
  
  pp expr if step > 10 || step < -10

  return '1' if step == 0

  list = [Chlen.new(coef, var, 1), Chlen.new(num, var, 0)]
  s = list
  (1..step - 1).each do |x|
    s = mul(s, list)
  end
  to_sss(s)
end

def mul(list1, list2)
  r = []
  list1.each do |i1|
    list2.each do |i2|
      r << i1 * i2
    end
  end
  reduce r
  
#   reduce list1.product(list2).map { |x| x[0] * x[1] }
  ### 
end

def reduce(list)
  list.reject { |x| x.coef == 0 }.group_by { |x| x.step}.map { |g| summ(g[1]) }
end

def to_sss(list)
  pp 'to_sss:'

  ### .sort { |a, b| b.step <=> a.step }
  list.map { |x| x.to_s }.join('+').gsub('+-', '-')
end

def summ(list)
  coef = 0
  list.each { |item| coef += item.coef }
  list[0].coef = coef
#   pp "summ: #{list[0]}"
  return list[0]
end

