515decfd9dcfc23bb6000006


isValidIP = (str) ->
  str.split(".").filter((v) ->
    v is Number(v).toString() and Number(v) < 256
  ).length is 4
_____________________________
isValidIP = (ip) ->
  /^((\d|([1-9]\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))\.){4}$/.test(ip + '.')
_____________________________
isValidIP = (ip) ->
  /^(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$/.test(ip)
_____________________________
isValidIP = (ip) -> require('net').isIPv4(ip)
