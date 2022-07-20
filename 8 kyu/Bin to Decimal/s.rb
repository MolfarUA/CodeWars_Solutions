57a5c31ce298a7e6b7000334


def bin_to_dec(str)
  str.to_i(2)
end
_________________________
def bin_to_dec(str)
  Integer("0b" + str)
end
_________________________
def bin_to_dec(str)
  str.chars.reverse.each.with_index.inject(0) {|dec, (n, i)| dec += (n.to_i)*(2**i)}
end
_________________________
def bin_to_dec(str)
  decimal = str.to_i(2)
  decimal
end
