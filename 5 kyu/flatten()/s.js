513fa1d75e4297ba38000003


function flatten(){
  return [].slice.call(arguments).reduce(function(a,b){              
    return a.concat(Array.isArray(b) ? flatten.apply(null,b) : b);
  },[]);
}
______________________________
var flatten=function(...arr){
  return arr.toString().split(",");
}
______________________________
const flatten = (...args) =>
  args.reduce((pre, val) => pre.concat(Array.isArray(val) ? flatten(...val) : val), []);
