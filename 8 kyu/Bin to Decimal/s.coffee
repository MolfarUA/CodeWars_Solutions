57a5c31ce298a7e6b7000334


binToDec = (bin)->
  n=0
  for c in bin
    n=(n<<1)+(+c)
  n
_________________________
binToDec = (bin)->
  parseInt(bin, 2)
