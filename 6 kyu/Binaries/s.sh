#!/bin/bash
C=( 10 11 0110 0111 001100 001101 001110 001111 00011000 00011001 )
s=I$1                                  #`echo $1 | sed -e "s/^/I/g"`
while true
do 
  for i in "${!C[@]}"
  do 
    s=${s/I${C[i]}/$i\I}               #`echo $s | sed -e "s/I${C[i]}/$i\I/g"`  WAS WAY TOO SLOW
  done
  if [[ $s == *"I" ]]
  then
    s=${s/I/}                          #`echo $s | sed -e "s/I//g"`
    echo $s
    exit 
  fi
done
__________________________
#!/bin/bash
function decode {
    local r=$1
    declare -A dic=( ["10"]="0" ["11"]="1" ["0110"]="2" ["0111"]="3" ["001100"]="4" ["001101"]="5" ["001110"]="6" ["001111"]="7" ["00011000"]="8" ["00011001"]="9")
    local temp="" res="" ss testa
    while [ -n "$r" ]; do
        testa=$(expr index "$r" 1)        
        temp=${r:0:$(($testa + $testa))}
        ss=${dic["$temp"]}
        if [ -n "${ss}" ]; then
            res=$res$ss
            r="${r/$temp/}"
        fi
    done
    echo $res
}
decode $1
__________________________
#!/bin/bash
function decode {
    STRING=$1
    codes=("10" "11" "0110" "0111" "001100" "001101" "001110" "001111" "00011000" "00011001")
    while [[ "$STRING" != "" ]]
    do
      for number in ${!codes[@]}
      do
        if [[ "${STRING}" == "${codes[$number]}"* ]]
        then
            echo -n $number
            STRING=$(echo "$STRING" | sed "s/${codes[$number]}//")
        fi
      done
    done
}

decode $1
__________________________
#!/bin/bash
function decode {
  i=0;
  arr=$1;
  detected=false
  int=""
  final="";
  obj="";
  count=0;

  if [[ ${arr:0:1} == "1" ]]
  then
    final=$((2#"${arr:1:1}"))
    i=2;
  fi  
  while [[ $i -lt "${#arr}" ]]
  do
    val=${arr:i:1};
    if [[ $val == "0"  && $detected == "false" ]]
    then
      count=$((count + 1));
    elif [[ $val == "1"  && $detected == "false" ]]
    then
        detected=true
        count=$((count + 1));
    elif [[ ($count -gt 0)  && ($detected=="true") ]]
    then
      obj+=$val;
      count=$((count-1));
      if [[ $count -eq 0 ]]
      then
        final+=$((2#$obj))
        detected=false;
        obj="";
      fi
    fi
  i=$((i+1));
  done
  echo $final;



}
decode $1
__________________________
#!/bin/bash

function decode {
    # your code
  local strng="$1"
  local len="${#1}"
  local result=""
  for ((i = 0; i < len; i++)); do
    local d="${strng:i:1}"
    if ((d == 0)); then
      local counter=1
      while ((d == 0 && i < len)); do
        ((i += 1))
        d="${strng:i:1}"
        ((counter+=1))
      done
      if ((d != 1 || (len - counter) < counter )); then
        echo 'Unexpected EOF:' $i >&2
        exit 1
      fi
      result="${result}$((2#"${strng:i+1:counter}"))"
      ((i += counter))
    elif ((d == 1)); then
      ((i += 1))
      if ((i >= len)); then
        echo 'Unexpected EOF:' $((i - 1)) >&2
        exit 1
      fi
      d="${strng:i:1}"
      result="${result}$((2#$d))"
    else
      echo 'Illegal digit:' $d >&2
      exit 1
    fi
  done
  echo "$result"
}
decode $1
