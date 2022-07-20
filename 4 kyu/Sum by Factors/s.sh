54d496788776e49e6b00052f


#!/bin/bash
sumOfDivided() {
  declare -A sum
  
  for nb in $1; do
    factor=$(cut -d ":" -f2 <<< $(factor $(tr -d "-" <<< $nb)))
    factors="$factors $factor"
    for j in $(tr " " "\n" <<< $factor | sort -u); do
      sum[$j]=$(expr ${sum[$j]} + $nb)
    done
  done
  
  for i in $(tr " " "\n" <<< $factors | sort -nu); do
    echo -n "($i ${sum[$i]}) "
  done
}
sumOfDivided "$1"
________________________________________________
#!/bin/bash
sumOfDivided() {
  declare -A primes

  for n in $@; do
    factors=($(factor ${n#-} | cut -d: -f2))  # create array
    factors=($(printf '%s\n' "${factors[@]}"|sort -u -n))  # and sort it
    
    for p in "${factors[@]}"; do
      ((primes[$p]+=n))
    done
  done

  keys=($(printf '%s\n' "${!primes[@]}"|sort -n))  # sort damn keys
  for key in ${keys[@]}; do
    printf "(%s %s) " "$key" "${primes[$key]}"
  done
}

sumOfDivided "$1"
________________________________________________
#!/bin/bash
abs () { echo -E "${1#-}" ;}

sumOfDivided() {
  s=$1
  for uu in $s
  do
    uu=$(abs $uu)
    res="${res}$uu "
  done
  res=$(echo $res | tr ' ' '\n' | sort -nu)  
  for r in $res
  do
    fcts=$(echo $(factor $r) | cut -f1 -d " " --complement)
    lfct="${lfct}$fcts "
  done
  lfct=$(echo $lfct | tr ' ' '\n' | sort -nu)  
  for f in $lfct
  do
    sum=0
    for uu in $s
    do
      rem=$(($uu % $f))
      if [ $rem -eq 0 ]
      then
        sum=$(($sum+$uu))
      fi
    done
    result="${result} ($f $sum) "
  done
  echo $result
}
sumOfDivided "$1"
