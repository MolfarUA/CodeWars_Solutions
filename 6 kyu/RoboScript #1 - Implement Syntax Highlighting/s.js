58708934a44cfccca60000c4


function highlight(code) {
  return code.replace(/(F+)/g,'<span style="color: pink">$1</span>').
    replace(/(L+)/g,'<span style="color: red">$1</span>').
    replace(/(R+)/g,'<span style="color: green">$1</span>').
    replace(/(\d+)/g,'<span style="color: orange">$1</span>');
}
__________________________
const color = char => {
  return { F: 'pink', L: 'red', R: 'green' }[char] || 'orange';
};

const highlight = code =>
  code.replace(/([FRL]|\d+)\1*/g, m => 
    '<span style="color: ' + color(m[0]) + '">' + m + '</span>');
__________________________
function highlight(code) {
  const style = color => `<span style="color: ${color}">$&</span>`;
  
  code = code.replace(/F+/g, style('pink'));
  code = code.replace(/L+/g, style('red'));
  code = code.replace(/R+/g, style('green'));
  code = code.replace(/[0-9]+/g, style('orange'));
  
  return code;
}
