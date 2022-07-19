51c8e37cee245da6b40000bd


function solution(input, markers) {
  return input.split('\n').map(
    line => markers.reduce(
      (line, marker) => line.split(marker)[0].trim(), line
    )
  ).join('\n')
}
__________________________________
function solution(input, markers){
  return input.replace(new RegExp("\\s?[" + markers.join("") + "].*(\\n)?", "gi"), "$1");
}
__________________________________
function solution(input, markers){
  return input.replace(new RegExp(`\\s*[${markers.join('|')}].+`,'g'),'');
}
__________________________________
RegExp.escape = function (s) {
  return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
}

function solution (input, markers){
  markers_regexp = markers.map(function(marker) {
    return RegExp.escape(marker);
  }).join("|");
  pattern = new RegExp("\\s*(" + markers_regexp + ").*?\$", "gm");
  return input.replace(pattern, "");
}
