514a3996d22ce03198000003


function deepFreeze (o) {
  var prop, propKey;
  
  Object.freeze( o );
  for ( propKey in o ) {
    prop = o[ propKey ];
    
    if ( !o.hasOwnProperty( propKey ) || !(typeof prop === "object") || Object.isFrozen( prop ) ) {
      continue;
    }

    deepFreeze(prop);
  }
}

deepFreeze(MrFreeze);
_________________________
Object.freeze(MrFreeze)
_________________________
var MyFreeze = {};
(Object.freeze || object)(MrFreeze);
_________________________
function freezeObj(obj) {
  Object.freeze(obj);
}

freezeObj(MrFreeze);
