const ACTION = Symbol('ACTION');

const GLOBAL = (function () { return this; })();

class Scheduler {
  constructor (defaultReturnValue) {
    this.returnValue = defaultReturnValue;
  }
  
  apply (...args) {
    return this.action.apply(null, args);
  }
  
  isReady () {
    return typeof this.action === 'function';
  }
  
  plan (newAction, returnValue = this.returnValue) {
    this.action = newAction;
    return returnValue;
  }
  
  clear (returnValue = this.returnValue) {
    return this.plan(null, returnValue);
  }
  
  clearAfter (fn) {
    return this.clear(fn());
  }
}

const createSetter = () => {
  const values = [];
  const actualSetter = (thing) => {
    let result = thing;
    for (const key of values) {
      result = result[key];
    }
    return result;
  };
  
  const proxy = new Proxy(actualSetter, {
    get(target, name, receiver) {
      switch(name) {
        case ACTION:
          return ACTION;
        case 'and_the':
          return scheduler.plan((key) => scheduler.plan((value) => scheduler.clearAfter(() => {
            values.push('is_the', key, value);
          })));
      }
      
      if (scheduler.isReady()) {
        return scheduler.apply(name);
      }
      
      const result = target[name];
      return typeof result === 'function' ? result.bind(target) : result;
    }
  });
  
  const scheduler = new Scheduler(proxy);

  return proxy;
}

const being_the = new Proxy({}, {
    get(_, name) {
      const setter = createSetter();
      return setter.and_the[name];
    }
});

const having = (count) => {
  return new Proxy({}, {
    get(_, name) {
      const action = (thing) => {
        thing.having(count)[name];
      };
      
      action[ACTION] = ACTION;
      
      return action;
    }
  });
};

class Thing {
  constructor (thingName) {
    this.name = thingName;
    
    const customHandlers = {};
    
    const proxy = new Proxy(this, {
      get(target, name, receiver) {
        switch (name) {
          case 'can':
            return scheduler.plan((actionName) => scheduler.clear((...canArgs) => {
              if (typeof canArgs[0] === 'function') {
                const actionRule = canArgs[0];
                target[actionName] = target.expose(actionRule);
              } else {
                const [resultsName, actionRule] = canArgs;
                const results = [];
                const wrappedActionRule = target.expose(actionRule);
                
                target[actionName] = (...args) => {
                  const result = wrappedActionRule(...args);
                  results.push(result);
                  return result;
                };
                
                customHandlers[resultsName] = () => results;
              }
            }));

          case 'has':
          case 'having':
          {
            return (count) => {
              if (count <= 0) {
                return scheduler.plan((_arg) => scheduler.clear());
              }
              
              if (count === 1) {
                return scheduler.plan((name) => scheduler.clear(target[name] = Thing.createOne(name)));
              }
              
              return scheduler.plan((name) => scheduler.clear(target[name] = Thing.create(count, name)));
            };
          }
            
          case 'is_a':
            return scheduler.plan((name) => scheduler.clearAfter(() => {
              target[`is_a_${name}`] = true;
            }));
            
          case 'is_not_a':
            return scheduler.plan((name) => scheduler.clearAfter(() => {
              target[`is_a_${name}`] = false;
            }));
            
          case 'is_the':
            return scheduler.plan((key) => scheduler.plan((value) => scheduler.clearAfter(() => {
              target[key] = value;
            })));
        }
        
        if (scheduler.isReady()) {
          return scheduler.apply(name);
        }
        
        if (typeof customHandlers[name] === 'function') {
          return customHandlers[name]();
        }
        
        const result = target[name];
        return typeof result === 'function' ? result.bind(target) : result;
      }
    });
    
    const scheduler = new Scheduler(proxy);
    
    return proxy;
  }

  expose (fn) {
    return (...args) => {
      const prevName = GLOBAL.name;
      GLOBAL.name = this.name;
      const result = fn(...args);
      GLOBAL.name = prevName;
      return result;
    };
  }
  
  static createOne (pluralName) {
    return new Thing(pluralName.replace(/s$/, ''));
  }

  static create (count, pluralName) {
    const items = new Array(count).fill(0).map(_ => Thing.createOne(pluralName));
    items.each = (iteratorFn) => {
      for (const item of items) {
        const result = iteratorFn(item);
        if (result && result[ACTION] === ACTION) {
          result(item);
        }
      }
    };
    return items;
  }
}

___________________________________________________
const proxy = (fn) => new Proxy({}, { get: (_, prop) => fn(prop) });
class Thing {
  constructor(name) {
    this.name = name;
  }

  get is_a() {
    return proxy((prop) => (this[`is_a_${prop}`] = true));
  }

  get is_not_a() {
    return proxy((prop) => (this[`is_a_${prop}`] = false));
  }

  get is_the() {
    return proxy((p1) =>
      proxy((p2) => {
        this[p1] = p2;
        return this;
      })
    );
  }

  get being_the() {
    return this.is_the;
  }
  get and_the() {
    return this.is_the;
  }

  get can() {
    return proxy((prop) => {
      return (a1, a2) => {
        this[a1] = [];
        const fp = (a2 || a1).toString().split(" => ");
        const f = new Function(fp[0], "with(this) return " + fp[1]);
        this[prop] = function (arg) {
          const res = f.bind(this)(arg);
          this[a1].push(res);
          return res;
        };
      };
    });
  }

  has(number) {
    return proxy((prop) => {
      if (number === 1) {
        this[prop] = new Thing(prop);
      } else {
        const arr = new Array(number).fill(new Thing(prop.slice(0, -1)));
        arr.each = (fn) => {
          const fs = fn.toString().split(" => ");
          arr.forEach((t) => {
            const f = new Function(fs[0], "with(this) return " + fs[1]);
            f.bind(t)();
          });
        };
        this[prop] = arr;
      }
      return this[prop];
    });
  }

  having(number) {
    return this.has(number);
  }
}

___________________________________________________
class Thing {
  constructor(name) {
    this.name = name;
    const c = this;
    this.is_a = new Proxy({}, {
      get: function(target, property, receiver) {
        if (typeof property === 'string' && property!=='inspect')
          c[`is_a_${property}`] = true;
      }
    });
    this.is_not_a = new Proxy({}, {
      get: function(target, property, receiver) {
        if (typeof property === 'string' && property!=='inspect')
          c[`is_a_${property}`] = false;
      }
    });
    this.is_the = new Proxy({}, {
      get: function(target, property, receiver) {
        if (typeof property === 'string' && property!=='inspect') {
          const prop = property;
          return new Proxy({}, {
            get: function(target, property, receiver) {
              if (typeof property === 'string' && property!=='inspect')
                c[prop] = property;
              return c;
            }
          });
        } 
      }
    });
    this.being_the = this.is_the;
    this.and_the = this.is_the;
    
    this.can = new Proxy({}, {
      get: function(target, property, receiver) {
        if (typeof property === 'string' && property!=='inspect') {
          const fn = (a1,a2) => {
            let f = a1;
            if (a2) {
              c[a1] = [];
              f=a2;
            }
            const fp = f.toString().split(' => ');
            const f2 = new Function(fp[0], 'with(this) return '+fp[1]);
            c[property] = function(arg) {
              const str = f2.bind(this)(arg);
              if (c[a1]) c[a1].push(str);
              return str;
            }
          };
          return fn
        }
      }
    });
  }
  
  has(number) {
    const insertObj = (str, name) => {
      str = str.replace('having',name+'.having');
      str = str.replace('being_the',name+'.being_the');
      return str;
    }
    const c = this;
    return new Proxy({}, {
      get: function(target, property, receiver) {
        if (typeof property === 'string') {
          if (number === 1) {
            c[property] = new Thing(property);
          } else {
            const arr = new Array(number).fill(new Thing(property.slice(0,-1)));
            arr.each = (fn) => {
              const fs = fn.toString().split(' => ');
              const f = new Function(fs[0], 'return '+insertObj(fs[1],fs[0]));
              arr.forEach(t => {
                f(t)
              });
            }
            c[property] = arr;      
          }
        }
        return c[property];
      }
    });
  }
  
  having(number) {
    return this.has(number)
  }
}

___________________________________________________
class Thing {
  // TODO: Make the magic happen 
  constructor(name) {
    this.name = name
  }
  
  get is_a() {
    return new Proxy(this, {
      get(t, p) {
        t[`is_a_${p}`]=true
        return t
      }
    })
  }
  
  get is_not_a() {
    return new Proxy(this, {
      get(t, p) {
        t[`is_a_${p}`]=false
        return t
      }
    })
  }
  
  has(n) {
    return new Proxy(this, {
      get(t, p) {
        const name = p.match(/s$/) ? p.substr(0, p.length - 1) : p
        const children = n > 1 ? Array(n).fill().map(() => new Thing(name)) : new Thing(name)
        if (n > 1) {
          children.each = function(fn) {
            children.forEach(child => {
              global.having = child.having.bind(child)
              global.being_the = child.is_the
              fn(child)
            })
          }
        }
        t[p] = children
        return children
      }
    })
  }
  
  having(n) {
    return this.has(n)
  }
  
  get is_the() {
    return new Proxy(this, {
      get(t, p1) {
        return new Proxy(t, {
          get(t, p2) {
            t[p1] = p2
            return t
          }
        })
      }
    })
  }
  
  get and_the() {
    return this.is_the
  }
  
  get can() {
    return new Proxy(this, {
      get(t, p) {
        return function(pt, fn) {
          global.name = t.name
          if (typeof pt === 'function') {
            fn = pt
            t[p] = fn
            return t
          }
          t[pt] = t[pt] || []
          t[p] = function() {
            t[pt].push(fn(...arguments))
          }
          return t
        }
      }
    })
  }
}

___________________________________________________
class Thing {
    constructor(name) {
        this.name = name;
        if (!global.name) global.name = name;
        let self = this;
        this.is_a = new Proxy(self, {
            get: (obj, prop) => {
                obj[`is_a_${prop}`] = true;
            }
        });
        this.is_not_a = new Proxy(self, {
            get: (obj, prop) => {
                obj[`is_a_${prop}`] = false;
            }
        });
        this.is_the = new Proxy(self, {
            get: (obj, prop) => {
                return new Proxy({}, {
                    get: (childObj, childProp) => {
                        obj[prop] = childProp;
                    }
                })
            }
        });
        this.has = this.having = this.with = function (count) {
            return new Proxy(self, {
                get: (obj, prop) => {
                    let things = obj.setThing(prop, count);
                    return new Proxy({}, {
                        get: (obj, prop) => {
                            if (prop === 'each') {
                                return new Proxy(function(){}, {
                                    apply: (target, thisArg, argumentsList) => {
                                        let cb = self.getRightCallback(argumentsList[0]);
                                        things.map(thing => cb.apply(thing, [thing]));
                                    }
                                })
                            }
                            else if (prop === 'having') {
                                return new Proxy(function(){}, {
                                    apply: (target, thisArg, argumentsList) => {
                                        return things[0].having(argumentsList[0]);
                                    }
                                });
                            }
                            else if (prop === 'being_the') {
                                return things[0].being_the;
                            }
                        }
                    })
                }
            })
        };
        this.setThing = function(thing, count) {
            if (count === 1) {
                self[thing] = new Thing(thing);
                return [ self[thing] ];
            }
            else {
                self[thing] = [];
                for (let i = 1; i <= count; i++) {
                    self[thing].push(new Thing(thing.slice(0, -1)));
                }
                return self[thing];
            }
        };

        this.getRightCallback = function(cb) {
            let parts = cb.toString().split('=>').map(p => p.trim());
            parts[1] = `${parts[0]}.${parts[1]}`;
            return new Function(parts[0], `return ${parts[1]}`);
        };

        this.being_the = this.and_the = new Proxy(self, {
            get: (obj, prop) => {
                return new Proxy({}, {
                    get: (childObj, childProp) => {
                        obj[prop] = childProp;
                        return self;
                    }
                });
            }
        }); 

        this.can = new Proxy(self, {
            get (target, property) {
                return new Proxy(function() {}, {
                    apply: function(target, thisArg, argumentsList) {
                        let past, action;
                        if (argumentsList.length > 1) {
                            past = argumentsList[0];
                            action = argumentsList[1];
                        }
                        else action = argumentsList[0];
                        if (past) { self[past] = []; }
                        thisArg[property] = function(text) {
                            if (past) { self[past].push(action(text)); }
                            return action(text);
                        }
                    }
                })
            },
        });
    }    
}
