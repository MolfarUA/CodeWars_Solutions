def calc expression
  expression.delete! ' '
  nil while expression.sub!(/\(([^()]+)\)/){ calc $1 }
  nil while expression.sub! /--/, ?+
  nil while expression.sub!(/(-?[.\d]+)([*\/])\+?(-?[.\d]+)/){ $1.to_f.send $2, $3.to_f }
  nil while expression.sub!(/(-?[.\d]+)([-+])\+?(-?[.\d]+)/){ $1.to_f.send $2, $3.to_f }
  expression.to_f
end
_____________________________
def exp tokens
  val = term tokens
  while tokens[0] =~ /[+-]/
    op = tokens.shift
    val = val.send op, (term tokens)
  end
  val
end

def term tokens
  val = factor tokens
  while tokens[0] =~ /[*\/]/
    op = tokens.shift
    val = val.send op, (factor tokens)
  end
  val
end

def factor tokens
  multiplier = 1
  if tokens[0] == '-'
    multiplier = -1
    tokens.shift
  end
  multiplier * (primary tokens)
end

def primary tokens
  if tokens[0] == '('
    tokens.shift
    val = exp tokens
    tokens.shift
  else
    val = Float tokens.shift
  end
  val
end

def calc expression
  exp expression.scan /\d+(?:\.\d+)?|[-+*\/()]/
end

_________________________________________
def calc(expression)
    operators = ["*","+","/","-"] # It is important that the + and - are at indeces 1 & -1.
    
    # This flag only exists because the creator of this kata forgot Ruby does integer division between integers...
    float_flag = (expression.include?(".")) ? true : false
    
    expression.strip!
    
    return nil if operators.include?(expression[expression.length - 1]) # Return nil if the last char is an operator
    return nil if operators.include?(expression[0]) and (expression[0] != "+" and expression[0] != "-") # Return nil if the first char is an operator other than - or +
    
    return expression.to_i if expression.length == 1 # 0 - 9
    
    if expression.split('')[1...expression.length].none? {|ele| operators.include?(ele)} # ex: -5001
        if (expression.include?("(") or expression.include?(")"))
            expression.delete!("(")
            expression.delete!(")")
            
            return  float_flag ? expression.to_f : expression.to_i
        else
            return  float_flag ? expression.to_f : expression.to_i
        end
    end

    # Dirty because all digits occupy their own element, even if they compose a single number. (100 would be ["1", "0", "0"] instead of ["100"])
    expression_arr_dirty = expression.gsub(/\s+/, "").split('') # Remove whitespace.
    
    expression_arr_dirty.each_with_index {|ele, index|
        if (index != expression_arr_dirty.length - 1 and (["*", "/"].include?(ele) and ["*", "/"].include?(expression_arr_dirty[index + 1])))
            return nil # Return nil if there is a "*" or "/" next to another operator
        end
    }
    
    
    paranthesis_index_start = -1
    paranthesis_index_end = -1
    
    
    expression_arr_dirty.insert(0, "0") if operators.include?(expression_arr_dirty[0]) # Insert a 0 at the beginning if the first element is "-" or "+"

    
    # Transform situation like this (-(-(-(-4)))) into this: (0-(0-(0-(0-4)))) so that it is compatible with this algorithm.
    if (expression_arr_dirty.include?("("))
        insert_indeces = []
        
        expression_arr_dirty.each_with_index {|ele, index|
            if (ele == "(" and expression_arr_dirty[index + 1] == "-")
                insert_indeces.push(index + 1)
            end
        }
        
        insert_indeces.reverse! # It's important to add to the array from the back, so that none of the targeted indeces get displaced during the insertion process below ;)
        
        insert_indeces.each {|index|
            expression_arr_dirty.insert(index, "0")
        }
    end
    
    
    expression_arr_dirty.map! {|ele| (operators.include?(ele)) ? ele.to_sym : ele} # Convert all operators to symbols (for use with the 'reduce' method)
    
    operators.map! {|ele| ele.to_sym} # Change all elements in operators to symbols.

    # The following chunk of code handles the reassembly of multi-digit numbers.
    expression_arr = []
    exp_index = 0
    
    expression_arr_dirty.each {|ele|
        if (expression_arr.length == 0 or ele.class == Symbol or expression_arr.last.class == Symbol or ["(", ")"].include?(ele) or ["(", ")"].include?(expression_arr.last))
            
            expression_arr.push(ele)
        elsif (ele.class == String and !["(", ")"].include?(ele) and expression_arr.last.class == String and !["(", ")"].include?(expression_arr.last))
            
            expression_arr[expression_arr.length - 1] = expression_arr[expression_arr.length - 1] + ele
        end
    }
    # expression_arr_dirty is not used past this point. Going forward, expression_arr is what is used.
    
    
    # Handle parantheticals
    while expression_arr.include?(")") do
        expression_arr.each_with_index {|ele, index|
            case ele
            when "("
                paranthesis_index_start = index
            when ")"
                paranthesis_index_end = index
                
                evaluated_paranthetical = calc(expression_arr[(paranthesis_index_start + 1)..(paranthesis_index_end - 1)].join).to_s
                return nil if evaluated_paranthetical.nil?
                
                expression_arr[paranthesis_index_start] = evaluated_paranthetical
                
                (paranthesis_index_end - (paranthesis_index_start)).times {
                    expression_arr.delete_at(paranthesis_index_start + 1)
                }
              
                break
            end
        }
    end
    
    
    
    # peMDas
    while (operators.any? {|op| expression_arr.include?(op) and (op == :* or op == :/)}) do
        expression_arr.each_with_index {|ele, index|
            if (ele == :* or ele == :/)
                if (expression_arr[index + 1].class == Symbol) # Example scenario:  ":*", ":-", "number"     Mulpiplying by a negative.
                    operator_index = operators.index(expression_arr[index + 1]) # 1 for :+     -1 for :-
                    expression_arr.delete_at(index + 1)
                    
                    # If there are situations like - + - + + - - - 3, it simplifies it. ("-3" will be the result and it will be one element)
                    while (operators.include?(expression_arr[index + 1])) do # If the NEXT next element is :- or :+
                        operator_index *= -1 if (expression_arr[index + 1] == :-)
                        expression_arr.delete_at(index + 1)
                    end
                    
                    next_value = (float_flag) ? expression_arr[index + 1].to_f : expression_arr[index + 1].to_i
                    
                    expression_arr[index + 1] = [0, next_value].reduce(operators[operator_index]).to_s
                end
                
                previous_value = (float_flag) ? expression_arr[index - 1].to_f : expression_arr[index - 1].to_i
                next_value = (float_flag) ? expression_arr[index + 1].to_f : expression_arr[index + 1].to_i
                
                sub_result = [previous_value, next_value].reduce(expression_arr[index]) # Calculate
            
                expression_arr[index - 1] = nil
                expression_arr[index] = nil
                expression_arr[index + 1] = sub_result
                
                # print expression_arr
                # print "         working*/"
                # puts
            end
        }
    end
    
    
    expression_arr.compact! # Get rid of the nil values that were inserted
    
    
    # pemdAS
    while (operators.any? {|op| expression_arr.include?(op) and (op == :+ or op == :-)}) do
        expression_arr.each_with_index {|ele, index|
            if (ele == :+ or ele == :-)
                if (expression_arr[index + 1].class == Symbol) # Example scenario:  ":*", ":-", "number"     Mulpiplying by a negative.
                    operator_index = operators.index(expression_arr[index + 1]) # 1 for :+     -1 for :-
                    expression_arr.delete_at(index + 1)
                    
                    # If there are situations like - + - + + - - - 3, it simplifies it. ("-3" will be the result and it will be one element)
                    while (operators.include?(expression_arr[index + 1])) do # If the NEXT next element is :- or :+
                        operator_index *= -1 if (expression_arr[index + 1] == :-)
                        expression_arr.delete_at(index + 1)
                    end
                    
                    next_value = (float_flag) ? expression_arr[index + 1].to_f : expression_arr[index + 1].to_i
                    
                    expression_arr[index + 1] = [0, next_value].reduce(operators[operator_index]).to_s
                end
                
                previous_value = (float_flag) ? expression_arr[index - 1].to_f : expression_arr[index - 1].to_i
                next_value = (float_flag) ? expression_arr[index + 1].to_f : expression_arr[index + 1].to_i
                
                sub_result = [previous_value, next_value].reduce(expression_arr[index]) # Calculate
            
                expression_arr[index - 1] = nil
                expression_arr[index] = nil
                expression_arr[index + 1] = sub_result
            end
        }
    end
    

    expression_arr.compact! # Get rid of the nil values that were inserted
    

    float_flag ? expression_arr[0].to_f : expression_arr[0].to_i
end
________________________________________________
def calc(expression)
  `echo 'console.log(#{expression})' | node`.to_f
end
_______________________________
def calc(expression)
  RubyVM::InstructionSequence.compile("1.0*" + expression).eval
end
