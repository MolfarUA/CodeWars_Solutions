Array.prototype.findIndex = function(fn) {
  for (let i = 0; i < this.length; i++) if (fn(this[i])) return i;
  return -1;
};
function product(a, arr) {
  if (arr.length==0) return a;
  let b = arr[0], res = [];
  for (let x of a) for (let y of b) res.push(x.concat(y));
  return product(res, arr.slice(1));
}
function query() {
  let s = {  where: [], having: [] },
      q = {
        select: function(fn){
          if (s.select) throw new Error('Duplicate SELECT');
          s.select = fn || (x => x);
          return q;
        },
        from: function(a, ...arr){
          if (s.from) throw new Error('Duplicate FROM');
          s.from = () => arr.length == 0 ? a : product(a.map(x=>[x]), arr);
          return q;
        },
        where: function(...fns){
          s.where.push(x => fns.some(fn => fn(x)));
          return q;
        },
        orderBy: function(fn){
          if (s.orderBy) throw new Error('Duplicate ORDERBY');
          s.orderBy = fn;
          return q;
        },
        groupBy: function(...fns){
          if (s.groupBy) throw new Error('Duplicate GROUPBY');
          s.groupBy = a => a.reduce((res, row) => {
            let a = res, b;
            for(let fn of fns) {
              let group = fn(row);
              let i = a.findIndex(x => x[0] == group);
              if (i<0) a.push([group, a = []]); else a = a[i][1];
            }
            a.push(row);
            return res;
          }, []);
          return q;
        },
        having: function(...fns){
          s.having.push(x => fns.some(fn => fn(x)));
          return q;
        },
        execute: function(){
          let res = s.from ? s.from() : [];
          res = res.filter(x => s.where.every(fn => fn(x)));
          if (s.groupBy) res = s.groupBy(res);
          res = res.filter(x => s.having.every(fn => fn(x)));
          if (s.orderBy) res.sort(s.orderBy);
          return s.select ? res.map(s.select) : res;
        }
      };
  return q;
}

__________________________________________________
function query() {
  var data, selectfunc, orderbyfunc, groupbyfuncs, wherefuncs=[], havingfuncs=[];
  
  function* join(lists,i=0) {
    if(i===lists.length) yield [];
    else for(let e of lists[i]) for(let r of [...join(lists,i+1)]) yield [e,...r];
  }
  function* group(list,fs,i=0) {
    if(i===fs.length) yield list;
    else {
      var m=list.reduce((m,e)=>{var t=fs[i](e); if(!m.has(t)) m.set(t,[]); m.get(t).push(e); return m},new Map());
      yield [...m.entries()].map(([k,v])=>[k,...group(v,fs,i+1)]);
    }
  }
  var obj = {
    select: function(f=e=>e) {
      if(selectfunc) throw new Error('Duplicate SELECT');
      selectfunc = f;
      return obj;
    },
    from: function(...ds) {
      if(data) throw new Error('Duplicate FROM');
      data = [...ds.length===1?ds[0]:join(ds)];
      return obj;
    },
    where: function(...fs) {wherefuncs.push(fs); return obj;},
    orderBy: function(f) {
      if(orderbyfunc) throw new Error('Duplicate ORDERBY');
      orderbyfunc = f;
      return obj;
    },
    groupBy: function(...fs) {
      if(groupbyfuncs) throw new Error('Duplicate GROUPBY');
      groupbyfuncs = fs;
      return obj;
    },
    having: function(...fs) {havingfuncs.push(fs); return obj;},
    execute: function() {
      if(!data) return [];
      data=wherefuncs.reduce((d,fs)=>d.filter(r=>fs.some(f=>f(r))),data);
      var res = group(data,groupbyfuncs||[]).next().value;
      res=havingfuncs.reduce((d,fs)=>d.filter(r=>fs.some(f=>f(r))),res);
      if(selectfunc) res=res.map(selectfunc);
      if(orderbyfunc) res=res.sort(orderbyfunc);
      return res;
    }
  }
  return obj;
};

__________________________________________________
class Query {
  constructor() {
    this.q = {
      where: [],
      having: []
    };
  }

  select(fn) {
    if ('select' in this.q) {
      throw new Error('Duplicate SELECT');
    }
    this.q.select = fn;
    return this;
  }

  from(...ts) {
    if ('from' in this.q) {
      throw new Error('Duplicate FROM');
    }
    this.q.from = ts;
    return this;
  }

  where(...fns) {
    this.q.where.push(fns);
    return this;
  }

  groupBy(...fns) {
    if ('groupBy' in this.q) {
      throw new Error('Duplicate GROUPBY');
    }
    this.q.groupBy = fns;
    return this;
  }

  orderBy(fn) {
    if ('orderBy' in this.q) {
      throw new Error('Duplicate ORDERBY');
    }
    this.q.orderBy = fn;
    return this;
  }

  having(...fns) {
    this.q.having.push(fns);
    return this;
  }

  _group(t, fns) {
    var fn, g, gt, i, k, len, results, v, x;
    [fn, ...fns] = fns;
    gt = new Map;
    for (i = k = 0, len = t.length; k < len; i = ++k) {
      v = t[i];
      g = fn(v);
      if (!gt.has(g)) {
        gt.set(g, []);
      }
      gt.get(g).push(t[i]);
    }
    results = [];
    for (x of gt) {
      [g, t] = x;
      if (fns.length) {
        t = this._group(t, fns);
      }
      results.push([g, t]);
    }
    return results;
  }

  _join(ts) {
    var j, k, l, len, len1, len2, m, o, r, t, v;
    [t, ...ts] = ts;
    o = (function() {
      var k, len, results;
      results = [];
      for (k = 0, len = t.length; k < len; k++) {
        r = t[k];
        results.push([r]);
      }
      return results;
    })();
    for (k = 0, len = ts.length; k < len; k++) {
      t = ts[k];
      j = o;
      o = [];
      for (l = 0, len1 = j.length; l < len1; l++) {
        r = j[l];
        for (m = 0, len2 = t.length; m < len2; m++) {
          v = t[m];
          o.push(r.concat([v]));
        }
      }
    }
    return o;
  }

  execute() {
    var fr, hv, k, l, len, len1, o, ref, ref1, ref2, wh;
    fr = (ref = this.q.from) != null ? ref : [];
    o = fr.length === 0 ? [] : fr.length === 1 ? fr[0] : this._join(fr);
    ref1 = this.q.where;
    for (k = 0, len = ref1.length; k < len; k++) {
      wh = ref1[k];
      o = o.filter((v) => {
        var fn, l, len1;
        for (l = 0, len1 = wh.length; l < len1; l++) {
          fn = wh[l];
          if (fn(v)) {
            return true;
          }
        }
        return false;
      });
    }
    if (this.q.groupBy != null) {
      o = this._group(o, this.q.groupBy);
    }
    ref2 = this.q.having;
    for (l = 0, len1 = ref2.length; l < len1; l++) {
      hv = ref2[l];
      o = o.filter((v) => {
        var fn, len2, m;
        for (m = 0, len2 = hv.length; m < len2; m++) {
          fn = hv[m];
          if (fn(v)) {
            return true;
          }
        }
        return false;
      });
    }
    if (this.q.orderBy != null) {
      o = o.slice(0).sort(this.q.orderBy);
    }
    if (this.q.select != null) {
      o = o.map(this.q.select);
    }
    return o;
  }

};

function query() {
  return new Query;
};

__________________________________________________
var query = function() {
  var tables = [];
  var select = function(row) { return row; };
  var where = function(row) { return true; };
  var groupBys = [];
  var orderBy = function(row1, row2) { return 0; };
  var having = function(group) { return true; };
  
  var self = {
    select: function(f) {
      select = f || select;
      return self;
    },
    
    from: function() {
      tables = Array.prototype.slice.call(arguments);
      return self;
    },
    
    _or: function (fs) {
      return function(row) {
        return fs.some(function (f) {
          return f(row);
        });
      };
    },
    
    _and: function(f, g) {
      return function(row) {
        return f(row) && g(row);
      };
    },
    
    where: function() {
      where = this._and(
        where,
        this._or(Array.prototype.slice.call(arguments))
      );
      return self;
    },
        
    having: function() {
      having = this._and(
        having,
        this._or(Array.prototype.slice.call(arguments))
      );
      return self;
    },
    
    groupBy: function() {
      groupBys = Array.prototype.slice.call(arguments);
      return self;
    },
    
    _group: function(rows, by) {
      if (by.length === 0) {
        return rows;
      }
      
      var groups = [];
      rows.forEach(function (row) {
        var key = by[0](row);
        var found = false;
        groups.forEach(function (group) {
          if (group[0] === key) {
            found = true;
            group[1].push(row);
          }
        });
        if (!found) {
          groups.push([key, [row]]);
        }
      });
      
      var that = this;
      return groups.map(function (group) {
        return [group[0], that._group(group[1], by.slice(1))];
      });
    },
    
    orderBy: function(f) {
      orderBy = f;
      return self;
    },
    
    _cross: function(tables) {
      switch (tables.length) {
        case 0: return tables;
        case 1: return tables[0];
        case 2:
          var result = [];
          tables[0].forEach(function (row0) {
            tables[1].forEach(function (row1) {
              result.push([row0, row1]);
            });
          });
          return result;
      }
    },

    execute: function() {
      return this._group(
          this._cross(tables)
              .filter(where),
          groupBys)
        .filter(having)
        .map(select)
        .sort(orderBy);
    }
  };
  
  var _once = function(f, error) {
    var called = false;
    var self = this;
    return function() {
      if (called) {
        throw new Error(error);
      }
      called = true;
      return f.apply(self, arguments);
    };
  };
  
  self.select = _once(self.select, 'Duplicate SELECT');
  self.from = _once(self.from, 'Duplicate FROM');
  self.orderBy = _once(self.orderBy, 'Duplicate ORDERBY');
  self.groupBy = _once(self.groupBy, 'Duplicate GROUPBY');
  return self;
};

__________________________________________________
const query = () => {
  let q = {}, p = new Proxy({}, {
    get(_, method) {
      if (method === 'execute') { return execute; }
      if (method in q && !['where', 'having'].includes(method)) {
        throw new Error('Duplicate ' + method.toUpperCase());
      }
      q[method] = q[method] || [];
      return (...a) => {
        if (['where', 'having'].includes(method)) {
          let b = a;
          a = [x => b.some(m => m(x))];
        }
        q[method] = [...q[method], ...a];
        return p;
      };
    }
  });
  function execute() {
    (!q.select || q.select.length < 1) && (q.select = [x => x]);
    let r = (q.from || [[]]), t = [];
    r.length > 1 && r[0].forEach(x => r[1].forEach(y => t.push([x, y])));
    r = t.length ? t : r[0];
    let actions = 'where groupBy having orderBy select'.split(' ');
    for (let a of actions) {
      if (!q[a]) { continue; }
      a === 'select' && (r = r.map(...q[a]));
      a === 'orderBy' && (r = r.slice().sort(...q[a]));
      while ((a === 'where' || a === 'having') && q[a].length) {
        r = r.filter(q[a].shift());
      }
      if (a === 'groupBy') {
        r = groupBy(r, q[a]);
      }
    }
    return r;
  }
  // group by is actually rather different from sql ;)
  function groupBy(r, f, co = 0) {
    let m = f[co];
    if (!m) { return r; }
    let t = [...new Set(r.map(m))].map(x => [x, []]);
    let s = r.map(x => [m(x), x]);
    s.forEach(x => {
      y = t.find(([g]) => g === x[0]);
      y[1] = [...y[1], x[1]];
    });
    for (let i of t) {
      i[1] = groupBy(i[1], f, co + 1)
    }
    return t;
  }
  return p;
}

__________________________________________________
"use strict";
// The reason that this code looks horrendous is because I originally wrote it in TypeScript.
// However, the version of TypeScript used by this kata did not allow the use of v8.serialize/deserialize
// which were key components of my solution. Hence I have compiled the TypeScript in order to
// use these functions. I have uploaded my TypeScript code to a **secret** gist here:
// https://gist.github.com/sportshead/009f3d5e938d04927943b036dd4f88e8/

var v8_1 = require("v8");
var structuredClone = function (o) { return (0, v8_1.deserialize)((0, v8_1.serialize)(o)); };
var SQL = /** @class */ (function () {
    function SQL() {
        this.commands = [];
    }
    SQL.prototype.select = function (field) {
        // check if select is already called
        if (this.commands.find(function (command) { return command.command === 0 /* select */; })) {
            throw new Error("Duplicate SELECT");
        }
        this.commands.push({ command: 0 /* select */, field: field });
        return this;
    };
    SQL.prototype.from = function (target, target2) {
        // check if from is already called
        if (this.commands.find(function (command) { return command.command === 1 /* from */; })) {
            throw new Error("Duplicate FROM");
        }
        // deepclone all inputs to prevent side effects
        var _t1 = structuredClone(target);
        var _t2 = structuredClone(target2);
        var _t = [];
        // join
        if (_t2) {
            _t1.forEach(function (c1) {
                _t2.forEach(function (c2) {
                    _t.push([c1, c2]);
                });
            });
        }
        else {
            _t = _t1;
        }
        this.target = _t;
        this.commands.push({ command: 1 /* from */, target: _t });
        return this;
    };
    SQL.prototype.where = function () {
        var filter = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            filter[_i] = arguments[_i];
        }
        this.commands.push({ command: 2 /* where */, filter: filter });
        return this;
    };
    SQL.prototype.orderBy = function (compare) {
        // check if orderBy is already called
        if (this.commands.find(function (command) { return command.command === 3 /* orderBy */; })) {
            throw new Error("Duplicate ORDERBY");
        }
        this.commands.push({ command: 3 /* orderBy */, compare: compare });
        return this;
    };
    SQL.prototype.groupBy = function () {
        var field = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            field[_i] = arguments[_i];
        }
        // check if groupBy is already called
        if (this.commands.find(function (command) { return command.command === 4 /* groupBy */; })) {
            throw new Error("Duplicate GROUPBY");
        }
        this.commands.push({ command: 4 /* groupBy */, functions: field });
        return this;
    };
    SQL.prototype.having = function () {
        var filter = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            filter[_i] = arguments[_i];
        }
        this.commands.push({ command: 5 /* having */, filter: filter });
        return this;
    };
    // recurse through each group by function
    SQL.prototype.executeGroupBy = function (result, functions) {
        var _this = this;
        if (functions.length === 0) {
            return result;
        }
        var fieldSelector = functions.shift();
        var nums = [];
        var grouped = result.reduce(function (a, i) {
            var key = fieldSelector(i);
            if (typeof key === "number") {
                nums.push(key);
            }
            if (!a[key]) {
                a[key] = [];
            }
            a[key].push(i);
            return a;
        }, {});
        return Object.keys(grouped).map(function (key) {
            return [
                nums.includes(+key) ? +key : key,
                _this.executeGroupBy(grouped[nums.includes(+key) ? +key : key], functions.slice()),
            ];
        });
    };
    SQL.prototype.execute = function () {
        if (!this.target || !this.commands.length) {
            return [];
        }
        var result = this.target;
        this.commands.forEach(function (command) {
            if (command.command === 2 /* where */) {
                result = result.filter(function (entry) {
                    return command.filter.some(function (filter) { return filter(entry); });
                });
            }
        });
        var groupByCommand = (this.commands.find(function (command) { return command.command === 4 /* groupBy */; }));
        if (groupByCommand && groupByCommand.functions.length) {
            result = this.executeGroupBy(result, groupByCommand.functions);
        }
        this.commands.forEach(function (command) {
            if (command.command === 5 /* having */) {
                result = result.filter(function (group) {
                    return command.filter.some(function (filter) { return filter(group); });
                });
            }
        });
        var orderByCommand = (this.commands.find(function (command) { return command.command === 3 /* orderBy */; }));
        if (orderByCommand) {
            result = result.sort(orderByCommand.compare);
        }
        var selectCommand = (this.commands.find(function (command) { return command.command === 0 /* select */; }));
        if (selectCommand && selectCommand.field) {
            result = result.map(selectCommand.field);
        }
        return result;
    };
    return SQL;
}());
function query() {
    return new SQL();
}

__________________________________________________
const query = () => new SQL()

class SQL {
  constructor() {
    this.data = []
    this.mapOutput = x => x
    this.preFilters = false
    this.groupingByList = false
    this.orderingBy = false
    this.havingFilter = () => true
    this.clauseChain = []
    this.returnThisUponExecute = false
  }
  checkRepeatedClause(clause) {
    if (this.clauseChain.includes(clause)) {
      this.returnThisUponExecute = 'Duplicate ' + clause
    }
    this.clauseChain.push(clause)
  }
  select(mapOutput) {
    this.checkRepeatedClause('SELECT')
    if (typeof mapOutput != "function") return this
    this.mapOutput = mapOutput
    return this
  }
  from(...data) {
    this.checkRepeatedClause('FROM')
    if (data.length === 1) {
      data = data[0]
    } else {
      if (typeof data[0][0] == "number") {
        let newData = []
        for (let i = 0; i < data[0].length; i ++) {
          for (let j = 0; j < data[1].length; j ++) {
            newData.push([data[0][i], data[1][j]])
          }
        }
        data = newData
      } else {
        // Zip arrays together https://stackoverflow.com/questions/22015684/how-do-i-zip-two-arrays-in-javascript
        data = data[0].map((e, i) => {
          return [e, data[1][i]];
        })
      }
    }
    this.data = data
    return this
  }
  where(...filters) {
    this.preFilters = filters
    return this
  }
  orderBy(orderingBy) {
    this.checkRepeatedClause('ORDERBY')
    this.orderingBy = orderingBy
    return this
  }
  groupBy(...groupBy) {
    this.checkRepeatedClause('GROUPBY')
    this.groupingByList = groupBy
    return this
  }
  having(hav) {
    this.havingFilter = hav
    return this
  }
  execute() {
    
    // Detect errors
    console.log("\n\n\n"+this.clauseChain+"\n----------------")
    this.checkRepeatedClause('EXECUTE')
    if (this.returnThisUponExecute) {
      throw new Error(this.returnThisUponExecute)
    }
    
    // WHERE
    if (this.preFilters) {
      this.data = this.data.filter(d => this.preFilters.some(f => f(d)))
      
    }

    // Recursively compartmentalize into groups
    if (this.groupingByList.length) {
      let groupArray = function(array, criteriaChain) {
        let newArray = []
        console.log(criteriaChain)
        let myCriteria = criteriaChain.shift()
        for (let item of array) {
          let category = myCriteria(item)
          let point = newArray.find(c => c[0] == category)
          if (point) {
            point[1].push(item)
          } else {
            newArray.push([category, [item]])
          }
        }
        if (criteriaChain.length) {
          for (let i = 0; i < newArray.length; i ++) {
            newArray[i][1] = groupArray(newArray[i][1], [...criteriaChain])
          }
        }
        return newArray
      }
      this.data = groupArray(this.data, this.groupingByList)
    }
    
    // HAVING
    if (this.havingFilter) {
      this.data = this.data.filter(this.havingFilter)
    }

    // ORDER
    if (this.orderingBy) {
      this.data.sort(this.orderingBy)
    }
    
    // SELECT - final mapping
    this.data = this.data.map(this.mapOutput)
    
    // Return data
    console.log("== OUTPUT ==")
    console.log(this.data)
    return this.data
  }
}
