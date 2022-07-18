515decfd9dcfc23bb6000006


require 'ipaddr'

def is_valid_ip(s)
  IPAddr.new(s) rescue nil
end
_____________________________
def is_valid_ip(ip)
  tokens = ip.split(".")
  tokens.size == 4 && tokens.all? { |token| token.to_i.to_s == token && (0..255).include?(token.to_i) }
end
_____________________________
def is_valid_ip(ip)
  valid_octets = (0..255).map(&:to_s)
  
  /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/
    .match(ip)
    &.captures
    &.all? { |octet| valid_octets.include?(octet) } || false
end
