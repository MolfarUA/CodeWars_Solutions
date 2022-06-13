function sayHello( name, city, state ) {
return `Hello, ${name.join(' ')}! Welcome to ${city}, ${state}!`
}
_______________________________________
function sayHello( name, city, state ) {
  return 'Hello, ' + name.join(' ') + '! Welcome to ' + city + ', ' + state + '!';
}
_______________________________________
var sayHello = (n, c, s) => `Hello, ${n.join(' ')}! Welcome to ${c}, ${s}!`;
_______________________________________
const sayHello = ( name, city, state ) => `Hello, ${name.join(' ')}! Welcome to ${city}, ${state}!`
_______________________________________
function sayHello( a, b, c) {
  return 'Hello, ' + a.join(' ') + '! Welcome to ' + [b,c].join(', ') + '!';
}
