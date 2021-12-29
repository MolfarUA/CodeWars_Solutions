#!/bin/bash
mix () {
  res=( )
  s1=( $( echo {a..z} {a..z} $1|tr -cd 'a-z'|grep -o .|sort|tr -d '\n'|grep -oE '([a-z])\1+' ) )
  s2=( $( echo {a..z} {a..z} $2|tr -cd 'a-z'|grep -o .|sort|tr -d '\n'|grep -oE '([a-z])\1+' ) )
  
  for (( c=0; c<26; ++c )); do
    (( ${#s1[$c]}==${#s2[$c]} ))  && val="3:${s1[$c]:2}"
    (( ${#s1[$c]} < ${#s2[$c]} )) && val="2:${s2[$c]:2}"
    (( ${#s1[$c]} > ${#s2[$c]} )) && val="1:${s1[$c]:2}"
    (( ${#val} >= 4 )) && res+=( $val )
    done
  
  for x in ${res[@]}; do
    echo ${#x} ${x:0:1} ${x:1}
    done|sort -t ' ' --key=1,1r --key=2,1n |cut -d ' ' -f2-3|tr -d ' '|tr '3' '='|tr '\n' "/"|sed -E 's:/$::'
}
mix "$1" "$2"

_____________________________________________________
#!/bin/bash

getOrderedList () {
  echo "$1" | grep -o . | sed "s/[^[:lower:].-]//g" | sort | sed -r '/^\s*$/d' | uniq -cd | tr -d ' ' | tr '\n' ' '
}

mix () {
  s1=($(getOrderedList "$1"))
  s2=($(getOrderedList "$2"))
  
  declare -A dict1 dict2
  
  first=true
  res=""

  for c in "${s1[@]}"; do
    dict1["${c: -1}"]="${c::-1}"
  done
  
  for c in "${s2[@]}"; do
    dict2["${c: -1}"]="${c::-1}"
  done
  
  for c in {a..z}; do
    val1="${dict1[$c]}"
    val2="${dict2[$c]}"

    [[ ! -v dict1["$c"] ]] && val1=0
    [[ ! -v dict2["$c"] ]] && val2=0
    
    [[ $val1 -le 1 && $val2 -le 1 ]] && continue
    
    [ "$first" = true ] && first=false || res+="/"

    max=$val1
    if [ $val1 -gt $val2 ]; then
      res+="1:"
    elif [ $val2 -gt $val1 ]; then
      res+="2:"
      max=$val2
    else
      res+="=:"
    fi
    
    res+=$(printf "%${max}s" | sed "s/ /$c/g")
  done
  
  res=$(echo "$res" | tr '/' '\n' | awk '{print length, $0}' | sort -k 1nr -k 2d | cut -d" " -f2- | tr '\n' '/' | sed 's/.$//g')
  echo $res
  
}
mix "$1" "$2"

_____________________________________________________
#!/bin/bash
mix () {
  for i in $(echo $1$2 | grep -o . | grep [a-z] | sort -u); do
    s1=${1//[^$i]} s2=${2//[^$i]}
    
    [ ${#s1} -eq 0 -a ${#s2} -eq 0 ] && continue
    [ ${#s1} -le 1 -a ${#s2} -le 1 ] && continue
    
    [ ${#s1} -lt ${#s2} ] && { echo "${#s2}@2:$s2" ; continue ; }
    [ ${#s1} -eq ${#s2} ] && { echo "${#s2}@=:$s2" ; continue ; }
    echo "${#s1}@1:$s1"
  done | sort -k 1r,2h -t @ | tr "\n" "/" | sed s/"[0-9]*@"/""/g | sed s/"\/$"//g
}
mix "$1" "$2"

_____________________________________________________
#! /bin/bash

counter()
{
    # Count lowercase letters in string.

    string=$1
    array=$2

    declare -n stats=$array

    for ((i = 0; i < ${#string}; i++)); do
        c=${string[*]:$i:1}
        [[ $c =~ [[:lower:]] ]] && stats[$c]=$((${stats[$c]:-0} + 1))
    done
}

max()
{
    # Return maximum of two numbers.

    [ $1 -gt $2 ] && echo $1 || echo $2
}

which()
{
    # Return symbol indicating which number is greater.

    diff=$(($1 - $2))
    [ $diff -eq 0 ] && echo 3 && return
    [ $diff -gt 0 ] && echo 1 || echo 2
}

repeat()
{
    # Repeat character count times.

    char=$1
    count=$2

    out=
    for ((i = 0; i < $count; i++)); do out+=$char; done
    echo $out
}

mix()
{
    # Visualize how two strings differ based on letter frequency.

    string1=$1
    string2=$2

    declare -A count1 count2
    counter "$string1" count1
    counter "$string2" count2
    letters=$(echo ${!count1[*]} ${!count2[*]} | xargs -n1 | sort -u)

    stats=()
    for char in ${letters[*]}; do
        a=${count1[$char]:-0}
        b=${count2[$char]:-0}
        [ $a -lt 2 -a $b -lt 2 ] && continue
        c=$(which $a $b),$(repeat $char $(max $a $b))
        stats+=(${#c},$c)
    done
    [ ${#stats[*]} -eq 0 ] && return
    stats=($(echo "${stats[*]}" | xargs -n1 | \
             sed 's/,/ /g' | sort -k1nr -k2n -k3 | \
             awk '{sub("3", "=", $2); print $2":"$3}'))
    echo "${stats[*]}" | sed 's# #/#g'
}

mix "$1" "$2"
