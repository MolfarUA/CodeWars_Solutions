515decfd9dcfc23bb6000006


function isValidIP(str) {
  return /^(([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])(\.(?!$)|$)){4}$/.test(str);
}
_____________________________
const net = require('net');
const isValidIP = (s) => net.isIP(s);
_____________________________
function isValidIP(str) {
  var p = str.split('.');
  return p.length == 4 && p.every(function(s) {
    return /^\d+$/.test(s) && s >= 0 && s <= 255;
  });
}
