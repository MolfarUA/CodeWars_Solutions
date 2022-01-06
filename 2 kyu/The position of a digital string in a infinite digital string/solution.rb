def find_position(str)
  x = (1..str.size).map{|s| [s]}.find{|as|
    s = as[0]
    a = (0...s).each_with_object([]){|o, a|
      next if str[o] == '0'
      t = [o + s, str.size].min
      nstr = ''
      nstr[0...t - o] = str[o...t]
      nstr[t - o...s] = (str[0...o].to_i + 1).to_s.rjust(s, '0')[t - o...s] if t - o < s
      n = nstr.to_i
     a << [n, o] if str == (n - 1..n + str.size / s).to_a.join[(n - 1).to_s.size - o, str.size]
    }.sort_by{|n, o| [n, -o]}
    ! a.empty? && as << a.first
  } || [str.size + 1, [10**str.size + str.to_i, -1]]
  x = x.last
  y = Math.log10(x[0]).to_i
  z = (1..y).reduce(0){|a, i| a + 9 * i * 10**(i - 1)}
  z += (x[0] - 10**y) * (y + 1) - x[1]
  z
end
___________________________________________________
def find_position(s)
  s += '1' if s.count('0') == s.size
  (1..s.size).each{|k|
    number, shift = (1..k).map{|r|
      part = 
        if (k == r)
          s[0...k] unless s[0] == '0'
        elsif s[r] != '0'  
          tail = s[0...r]
          if tail == '9' * r
            s[r...k] == '1' + '0' * (k-r-1) ? '9' * k : s[r...k].to_i.pred.to_s + tail
          else
            s[r...k] + tail
          end    
        end
      i = part.to_i if part
      [i, k-r] if part && (i..i+s.size/k+1).map(&:to_s).join[k-r, s.size] == s
    }.compact.min
    if number
      len = number.to_s.size
      return (1..len-1).sum{|i| 9*10**(i-1)*i} + (number-10**(len-1)) * len + shift
    end  
  }
end  
___________________________________________________
def find_position(str)
  i=1
  puts str
  min=1.0/0.0
  #puts ""
  #puts str
  while i<=str.length do
    sol=backtrack(str,i)
    if i==1
      min=sol if sol
    else
      if sol  
        min=sol if sol<min
      end
    end
    i+=1
  end
  return min
end

def backtrack(str,r)
  #puts "r "+r.to_s
  min=nil
  for i in 0..r-1
    compare=false
    done=false
    first_nine=true
    last=nil
    aux=""
    digit_counter=0
    aux_r=r.dup
    arr=[]
    nine_to_ten_count=0
    remaining=str.length
    #puts "##############################"
    #puts "i "+i.to_s
    for j in 0..str.length-1
      aux.concat str[j]
      digit_counter+=1
      remaining-=1
      if j==i
        last=aux
        arr.push last
        digit_counter=0
        aux=""
        last.chars.each do |ch|
          first_nine=false if ch!="9"
        end
      end
      if digit_counter==aux_r and last
        digit_counter=0
        compare=true
      end
      if j==str.length-1
        compare=true
        done=true
      end
      if compare
        #puts "l "+last
        #puts "a "+aux
        #puts "j "+j.to_s
        if comparison(last,aux,done,arr.length,remaining)
          last=aux
          aux=""
          arr.push last if last!=""
          if done
            arr.push aux if aux!=""
            a=get_ind(arr,r,first_nine)
            #puts "ind "+a.to_s
            if a
              if !min
                min=a
              else
                min=a if a<min
              end
            end
          end
        else
          if nine_to_ten_count<1
            flag=true
            last.chars.each do |ch|
              flag=false if ch!="9"
            end
            if flag
              aux_r+=1
              nine_to_ten_count+=1
            else
              break
            end
          else
            break
          end
        end
      end
    end
  end
  min
end
  
def get_ind(arr,r,bool)
  #puts "length "+arr.length.to_s
  aux_zero=arr[0]
  if arr[1]
    if arr[1][0]=="0"
      aux3="1"+arr[1].dup
    else
      aux3=arr[1].dup
    end
  end
  if arr.length>1
   
    ##puts "aux "+aux.to_s
    ##puts arr[1].to_i/10**(aux)*10**(arr[1].length)
    if arr[0].length>aux3.length
      aux=arr[0].dup
      aux2=add_one(aux)
      #puts "aux2 "+aux2
      sol=nil
      flag=true
      for i in 0..aux3.length-1
        flag=true
        for j in 0..aux3.length-1
          if aux3.length-1-i-j>=0
            if aux2[aux3.length-1-i-j]!=aux3[-1-j]
              flag=false
              break
            end
          end
        end
        if flag
          sol=i
          break
        end
      end
      nines_bool=true
      nine_flag=false
      nine_count=0
      zero_count=0
      for i in 0..arr[0].length-1
        if !nine_flag
          if arr[0][i]!="0"
            nines_bool=false
            break
          else
            zero_count+=1
            if i==1
              nines_bool=false
            else
              if arr[0][i+1]=="9"
                nine_flag=true
              end
            end
          end
        else
          if arr[0][i]!="9"
            nines_bool=false
            break
          else
            nine_count+=1
          end
        end
      end
      #puts "bool "+nines_bool.to_s
      #puts "nines "+nine_count.to_s
      #puts "sol "+sol.to_s
      
      if sol
        for i in 0..aux3.length-1
          aux2.prepend(aux3[-1-i]) if aux3.length-1-sol-i<0
        end
      else
        for i in 0..aux3.length-1
          aux2.prepend(aux3[-1-i])
        end
      end
      aux2=aux3+aux2 if nines_bool and arr[0].length>1 and aux2.length==arr[0].length
      #puts "aux2 "+aux2
      n=aux2.to_i
      n-=1
    elsif arr[0].length==aux3.length
      aux=arr[0].dup
      aux2=add_one(aux)
      #puts "aux2 "+aux2
      sol=nil
      flag=true
      for i in 0..aux2.length-1
        flag=true
        for j in 0..aux3.length-1
          if aux2.length-1-i-j>=0
            if aux2[-1-i-j]!=aux3[-1-j] or (aux2=="1" and aux3=="1")
              flag=false 
              break
            end
          end
        end
        if flag
          sol=i
          break
        end
      end
      nines_bool=true
      nine_flag=false
      nine_count=0
      zero_count=0
      for i in 0..arr[0].length-1
        if !nine_flag
          if arr[0][i]!="0"
            nines_bool=false
            break
          else
            zero_count+=1
            if i==1
              nines_bool=false
            else
              if arr[0][i+1]=="9"
                nine_flag=true
              end
            end
          end
        else
          if arr[0][i]!="9"
            nines_bool=false
            break
          else
            nine_count+=1
          end
        end
      end
      #puts "bool "+nines_bool.to_s
      #puts "nines "+nine_count.to_s
      #puts "sol "+sol.to_s
      if sol
        for i in 0..aux3.length-1
          aux2.prepend(aux3[-1-i]) if aux2.length-1-sol-i<0
        end
      else
        for i in 0..aux3.length-1
          aux2.prepend(aux3[-1-i])
        end
      end
      aux2=aux3+aux2 if nines_bool and arr[0].length>1 and aux2.length==arr[0].length
      #puts "aux2 "+aux2
      n=aux2.to_i
      n-=1
    elsif arr[0].length<aux3.length
      aux=arr[0].dup
      aux2=add_one(aux)
      #puts "aux2 "+aux2
      sol=nil
      flag=true
      for i in 0..aux2.length-1
        flag=true
        for j in 0..aux3.length-1
          if aux2.length-1-i-j>=0
            if aux2[-1-i-j]!=aux3[-1-j]
              flag=false
              break
            end
          end
        end
        if flag
          sol=i
          break
        end
      end
      nines_bool=true
      nine_flag=false
      nine_count=0
      zero_count=0
      for i in 0..arr[0].length-1
        if !nine_flag
          if arr[0][i]!="0"
            nines_bool=false
            break
          else
            zero_count+=1
            if i==1
              nines_bool=false
            else
              if arr[0][i+1]=="9"
                nine_flag=true
              end
            end
          end
        else
          if arr[0][i]!="9"
            nines_bool=false
            break
          else
            nine_count+=1
          end
        end
      end
      #puts "bool "+nines_bool.to_s
      #puts "nines "+nine_count.to_s
      #puts "sol "+sol.to_s
      if sol
        for i in 0..aux3.length-1
          aux2.prepend(aux3[-1-i]) if aux2.length-1-sol-i<0
        end
      else
        for i in 0..aux3.length-1
          aux2.prepend(aux3[-1-i])
        end
      end
      aux2=aux3+aux2 if nines_bool and arr[0].length>1 and aux2.length==arr[0].length
      #puts "aux2 "+aux2
      n=aux2.to_i
      n-=1
    end
    
    #puts "b "+bool.to_s
    
  else
    #puts "entroooooooo"
    if arr[0][0]!="0"
      n=arr[0].to_i
    else
      n=arr[0].dup.prepend("1")
      n=n.to_i
    end
  end
  #puts "n "+n.to_s
  x=0
  ch=0
  aux=0
  for i in 0..n.to_s.length-1
    aux=10**i
    x=aux
    aux-=10**(i-1) if i>=2
    #puts "x "+x.to_s
    ch+=aux*i
    ch-=1 if i==1
    #puts "ch "+ch.to_s
  end
  ind=ch+(n-x)*n.to_s.length
  
  ind+=n.to_s.length-aux_zero.length
  return ind
end
  
def comparison(first,second,done,size,remain)
  return true if second==""
  ##puts "f "+first.to_s
  ##puts "s "+second.to_s
  #puts "l "+size.to_s
  #puts "d "+done.to_s
  return false if first[0]=="0" and second[0]=="0"
  if size<2 and remain==0
    return false if first[0]!="0" and second[0]=="0"
    return true
  else
    nines=true
    first.chars.map {|m| nines=false if m!="9"}
=begin
    if nines and second.to_i%10**(second.length-1)==0 and second.to_i%10**(second.to_i)
      puts "cchau"
      return true if second.to_i!=0
      return false if second.to_i==0
    end
=end
    if first.length==second.length
      aux=add_one1(first)
      if aux.length>first.length
        aux=aux[0..-2]
        puts "noooo"
        puts aux
      end
      puts "hola"
      if aux==second
        return true
      else
        return false
      end
    elsif first.length<second.length
      aux=add_one(first)
      return false if first[0]!="0" and second[0]=="0"
      for i in 0..aux.length-1
        if aux[-1-i]!=second[-1-i]
          return false
        end
      end
      return true
    elsif first.length>second.length
      aux=add_one(first)
      for i in 0..second.length-1
        if second[-1-i]!=first[second.length-1-i]
          return false
        end
      end
      return true
    end
  end
end
  
def add_one(first)
  zero_bool=true
  first.chars.each do |ch|
    zero_bool=false if ch!="0"
  end
  if zero_bool
    aux="1"+("0"*(first.length-1))+"1"
  else
    aux=(first.to_i+1).to_s
  end
  #puts "add "+aux
  dif=first.length-aux.length
  if dif<0
    aux=aux.chars.drop(1).join("")
  else
    for i in 1..dif
      aux.prepend("0")
    end
  end
  return aux
end

def add_one1(first)
  zero_bool=true
  first.chars.each do |ch|
    zero_bool=false if ch!="0"
  end
  if zero_bool
    aux="1"+("0"*(first.length-1))+"1"
  else
    aux=(first.to_i+1).to_s
  end
  #puts "add "+aux
  dif=first.length-aux.length
  if dif<0
    aux=aux[0..-2]
  else
    for i in 1..dif
      aux.prepend("0")
    end
  end
  return aux
end
  

def zeros_and_nines(str)
  nines_bool=true
  nine_flag=false
  nine_count=0
  zero_count=0
  for i in 0..str.length-1
    if !nine_flag
      if str[i]!="0"
        nines_bool=false
        break
      else
        zero_count+=1
        if i==1
          nines_bool=false
        else
          if str[i+1]=="9"
            nine_flag=true
          end
        end
      end
    else
      if str[i]!="9"
        nines_bool=false
        break
      else
        nine_count+=1
      end
    end
  end
  nines_bool
end
  
___________________________________________________
def successor?(a,b)
  return false if b =~ /^0/

  if a =~ /x/ && b =~ /x/
    an = a.gsub('x','')
    am = ("0" * an.size + (an.to_i + 1).to_s)[-an.size..-1]
    at = ("x" * a.size + am)[-a.size..-1]
    aa = ""
    bb = ""
    at.size.times { |i| if at[i] != 'x' && b[i] != 'x'; aa += at[i]; bb += b[i]; end }
    return aa==bb
  end

  if a =~ /^\d+$/ && b =~ /^\d+$/
    return ("0"*a.size + (a.to_i + 1).to_s)[-a.size..-1] == b
  end

  if a =~ /x/
    bb = (("1" + b).to_i - 1).to_s[-b.size..-1]
    return a.chars.zip(bb.chars).all? { |x,y| x == 'x' || x == y }
  end

  if b =~ /x/
    aa = ("0"*a.size + (a.to_i + 1).to_s)[-a.size..-1]
    return aa.chars.zip(b.chars).all? { |x,y| y == 'x' || x == y }
  end
end

def position(n)
  (1...n.size).map { |e| e*9*10**(e-1) }.sum + (n.to_i - 10**(n.size-1))*n.size
end

S = (1..1010).map {|n| n.to_s }.join

def find_position(str)
  i = S.index(str)
  return i if !i.nil?
  
  (3..str.size).each do |n|
    results = []
    # find options for string length n
    n.times do |offset|
      options = []
      options << 'x' * (n-offset) + str[0...offset] if offset > 0
      options += str[offset..-1].scan(/.{1,#{n}}/)
      options[-1] = (options[-1] + 'x' * n)[0...n]

      if options.size == 1
        num = options[0][0] == "0" ? "1" + options[0] : options[0]
        results << position(num) + (options[0][0] == "0" ? 1 : 0)
      elsif options.each_cons(2).map {|a,b| successor?(a,b) }.all?
        a, b = options
        if a =~ /x/ && b =~ /x/
          r = ""
          a.size.times do |i| 
            if a[i] == 'x' && b[i] != 'x'
              r[i] = b[i]
            elsif a[i] == 'x' && b[i] == 'x'
              r[i] = 1
            else
              r[i] = a[i]
            end       
          end
          r = '1' + r if r[0] == "0"

          # compensate for ending 9's
          chars = a.gsub('x','').chars
          if chars.uniq == ['9'] 
            r = (r.to_i - 10**chars.size).to_s
          end
          
          results << position(r)+a.count('x')
        elsif a =~ /x/
          a = '1' + a if a[0] == "0"
          results << position(b)-a.size+a.count('x')
        else
          a = '1' + a if a[0] == "0"
          results << position(a)
        end
      end
    end
    
    # take best result
    return results.min if results.size > 0
  end
end
