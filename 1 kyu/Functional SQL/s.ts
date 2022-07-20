545434090294935e7d0010ab


type Table<R> = Iterable<R>;
type Selector<R, S = R> = (row: R) => S;
type Predicate<R> = (row: R) => boolean;
type GroupKey<R, K> = (row: R) => K;
type Group<R, K> = [K, Table<R>];
type Comparator<R> = (a: R, b: R) => number;
type Transform<A, B = A> = (table: Table<A>) => Table<B>;

interface Query<R> {
  select<S = R>(selector?: Selector<R, S>): Query<S>;
  from<T>(table: Table<T>): Query<T>;
  from<A, B>(tableA: Table<A>, tableB: Table<B>): Query<[A, B]>;
  from<A, B, C>(tableA: Table<A>, tableB: Table<B>, tableC: Table<C>): Query<[A, B, C]>;
  where(...predicates: Predicate<R>[]): Query<R>;
  orderBy(cmp: Comparator<R>): Query<R>;
  groupBy(...keys: GroupKey<R, any>[]): Query<Group<R, any>>;
  having(...predicates: Predicate<R>[]): Query<R>;
  execute(): R[];
}

interface Q<R = any, T = R, S = T> {
  SELECT?: Transform<T, S>,
  FROM?: Table<R>,
  WHERE?: Transform<R>,
  ORDERBY?: Transform<R>,
  GROUPBY?: Transform<R, any>,
  HAVING?: Transform<R, any>,
}

export function query(q: Q = {}): Query<any> {
  const { SELECT, FROM, WHERE, ORDERBY, GROUPBY, HAVING } = q;
  return {
    select(selector) {
      if (SELECT !== undefined) throw new Error('Duplicate SELECT');
      return query({ ...q, SELECT: map(selector) });
    },
    from(...tables: any[]) {
      if (FROM !== undefined) throw new Error('Duplicate FROM');
      return query({ ...q, FROM: tables.reduce(cross) });
    },
    where(...predicates) {
      const predicate = predicates.reduce(or);
      return query({ ...q, WHERE: compose(WHERE, filter(predicate)) });
    },
    orderBy(cmp) {
      if (ORDERBY !== undefined) throw new Error('Duplicate ORDERBY');
      return query({ ...q, ORDERBY: sort(cmp) });
    },
    groupBy(...keys) {
      if (GROUPBY !== undefined) throw new Error('Duplicate GROUPBY');
      return query({
        ...q,
        GROUPBY: groupBy(...keys),
      });
    },
    having(...predicates) {
      const predicate = predicates.reduce(or);
      return query({ ...q, HAVING: compose(HAVING, filter(predicate)) });
    },
    execute() {
      const transform = [
        WHERE,
        GROUPBY,
        HAVING,
        SELECT,
        ORDERBY,
      ].reduce(compose);
      return toArray(
        (
          transform || identity
        )(
          FROM || []
        )
      );
    },
  };
};

function cross<A, B>(tableA: Table<A>, tableB: Table<B>): Table<[A, B]> {
  return iter(function* (): Iterator<[A, B]> {
    for (const a of tableA) for (const b of tableB) yield [a, b];
  });
}

function filter<R>(predicate: Predicate<R>): Transform<R> {
  return (table) => iter(function* () {
    for (const row of table) if (predicate(row)) yield row;
  });
}

function map<R, S>(mapper: Selector<R, S> = identity): Transform<R, S> {
  return (table) => iter(function* () {
    for (const row of table) yield mapper(row);
  });
}

function groupBy<R>(...keys: GroupKey<R, any>[]): Transform<R, any> {
  if (keys.length === 0) return identity;
  const [key, ...rest] = keys;
  const groupByRest = groupBy(...rest);
  return compose(
    groupByKey(key),
    map(([k, group]) => [k, toArray(groupByRest(group))]),
  );
}

function groupByKey<R, K>(key: GroupKey<R, K>): Transform<R, Group<R, K>> {
  return (table) => {
    const result = new Map<K, R[]>();
    for (const row of table) {
      const k = key(row);
      const group = result.get(k) || [];
      result.set(k, [...group, row]);
    }
    return result.entries();
  };
}

function sort<R>(cmp: Comparator<R>): Transform<R> {
  return (table) => [...table].sort(cmp);
}

function iter<T>(generator: () => Iterator<T>): Iterable<T> {
  return ({
    [Symbol.iterator]: generator,
  })
}

function compose<A, B, C>(
  fnA: ((a: A) => B) = identity,
  fnB: ((b: B) => C) = identity,
): (a: A) => C {
  return (a: A) => fnB(fnA(a));
}

function identity(v: any) {
  return v;
}

function or<R>(a: Predicate<R>, b: Predicate<R>): Predicate<R> {
  return (row) => a(row) || b(row);
}

// XXX chai can not deeply compare lazy structures
function toArray<R>(table: Table<R>): R[] {
  return [...table];
}
__________________________________________
export function query() {
  return new Query()
};

type Predicate = (arg:any) => Boolean
type Selector = (arg:any) => any
type Orderer = (a:any, b:any) => number

class Query<T, Tresult> {
  private _hasSelect = false
  private _select : Selector = (v:T) => v
  private _hasData = false
  private _data : T[] | T[][]  = []
  private _where : Predicate[] = []
  private _groupBy : Selector[] = []
  private _orderBy? : Orderer = undefined
  private _having : any[] = []
  
  select(fieldsSelector? : Selector) {
    if (fieldsSelector) {
      this._select = fieldsSelector
    }
    if(this._hasSelect) throw new Error('Duplicate SELECT')
    this._hasSelect = true
    return this
  }
  
  from(...data: T[][]) {
    if(this._hasData) throw new Error('Duplicate FROM')
    this._hasData = true
    this._data = data.length === 1 ? [...data[0]] : join(data[0],data[1])
    return this
  }
  
  
  
  where(filter: Predicate, ...ors:Predicate[]) {
    let f = filter
    if (ors && ors.length) {
      f = (v:T) => filter(v) || ors.map(o => o(v)).reduce((acc,curr) => acc || curr, false)
    } 
    this._where.push(f)
    return this
  }
  
  groupBy(...fieldsSelectors : Selector[]) {
    for(const selector of fieldsSelectors) this._groupBy.push(selector)
    return this
  }
  
  having(haver:any) {
    this._having.push(haver)
    return this
  }
  
  orderBy(comparer:Orderer) {
    this._orderBy = comparer
    return this
  }
  
  execute() {
    if(!this._data) return []
    
    let result:any[] = this._data
    console.log('data',result)
    for (const where of this._where) {
      result = result.filter(where)
    }
    console.log('where',result)
    if(this._groupBy.length) {
      result = groupByRec(result, this._groupBy, 0)
    }
    for(const have of this._having) {
      result = result.filter(have)
    }
    if(this._orderBy) {
      result.sort(this._orderBy)
    }
    //console.log('sorted', result)
    result = result.map(this._select)
    return result
  }
}

function groupByRec(data:any[], groupers:Selector[], level:number):any[] {
  const grouper = groupers[level]
  const grouped = arrayify(data.reduce((acc,curr) => groupBy(acc, curr, grouper), new Map<any,any[]>()))
  //console.log('grouped',JSON.stringify(grouped,null,2))
  if(level+1===groupers.length) return grouped
  return grouped.map(([key, groupData]:[any,any[]]) => [key, groupByRec(groupData, groupers, level+1)])
}

function groupBy(acc:Map<any,any[]>, curr:any, grouper:Selector):any {
  const key = grouper(curr)
  const val = acc.get(key) || []
  val.push(curr)
  acc.set(key, val)
  return acc
}

function arrayify(acc:Map<any,any[]>):any{
  return Array.from(acc.keys()).map((k:any) => [k, acc.get(k)])
}

function join(as:any[], bs:any[]) {
  const result = []
  for(const a of as) {
    for(const b of bs) {
      result.push([a,b])
    }
  }
  return result
}
__________________________________________
class SQL {
    private _data: any[] = [];
    private _fromSet: boolean = false;
    private _select: any;
    private _selectSet: boolean = false;
    private _where: any[][] = [];
    private _groupBy: any[] = [];
    private _orderBy: any[] = [];
    private _having: any[][] = [];

    public query(): SQL {
        return this;
    }

    public from(...args: any[]): SQL {
        if (this._fromSet) {
            throw Error('Duplicate FROM');
        }
        this._fromSet = true;
        const data = cloneArray(args);
        if(data.length === 1){
            this._data = data[0];
        }
        else if(data.length > 1){
            this._data = this.join(data);
        }
        return this;
    }

    public select(select?: any): SQL {
        if (this._selectSet) {
            throw Error('Duplicate SELECT');
        }
        this._selectSet = true;
        this._select = select;
        return this;
    }

    public groupBy(...args: any[]): SQL {
        if (this._groupBy && this._groupBy.length > 0) {
            throw Error('Duplicate GROUPBY');
        }
        this._groupBy = args;
        return this;
    }

    public orderBy(...args: any[]): SQL {
        if (this._orderBy && this._orderBy.length > 0) {
            throw Error('Duplicate ORDERBY');
        }
        this._orderBy = args;
        return this;
    }

    public having(...args: any[]): SQL {
        this._having.push(args);
        return this;
    }

    public where(...args: any[]): SQL {
        this._where.push(args);
        return this;
    }

    public execute(): any[] {
        let data = this._data;
        data = this.whereFilter(data);
        data = this.groupByData(data);
        data = this.havingData(data);
        data = this.selectData(data);
        data = this.orderByData(data);
        return data;
    }

    private orderByData<T>(data: T[]): T[] {
        for (const order of this._orderBy) {
            data = data.sort((a: any, b: any) => order(a, b))
        }
        return data;
    }

    private selectData<T>(data: T[]): T[] {
        return this._select ? data.map((row: any) => this._select(row)) : data;
    }

    private whereFilter<T>(data: T[]): T[] {
        for (const where of this._where) {
            data = data.filter((data: any) => {
                let stay = false;
                for (const whereOr of where) {
                    if (whereOr(data)) {
                        stay = true;
                    }
                }
                return stay;
            });
        }
        return data;
    }

    private join(data: any[][]): any[][] {
        const result: any[][] = [];
        for(const row1 of data[0]){
            for (const row2 of data[1]){
                result.push([row1, row2]);
            }
        }
        return result;
    }

    private groupNextLevel(data: any[], group: Function) {
        if (Array.isArray(data) && Array.isArray(data[0])) {
            for (let i = 0; i < data.length; i++) {
                this.groupNextLevel(data[i], group);
            }
        } else if (Array.isArray(data[1]) && Array.isArray(data[1][0])) {
            this.groupNextLevel(data[1], group)
        } else {
            data[1] = this.groupByLevel(data[1], group, 0);
        }
    }

    private havingData<T>(data: T[]): T[] {
        for (const havings of this._having) {
            data = data.filter((row: any) => {
                let stay = false;
                for (const having of havings) {
                    if (having(row)) {
                        stay = true;
                    }
                }
                return stay;
            });
        }
        return data;
    }

    private groupByData(data: any[]): any[] {
        for (let level = 0; level < this._groupBy.length; level++) {
            const group = this._groupBy[level];
            data = this.groupByLevel(data, group, level)
        }
        return data;
    }

    private groupByLevel(data: any[], group: Function, level: number): any[] {
        if (level > 0) {
            this.groupNextLevel(data, group);
            return data;
        }
        if (data.length === 1) {
            const key = group(data[0]);
            return [[key, [data[0]]]]
        }
        return data.reduce((total: any, value: any, i: number) => {
            if (i === 1) {
                total = [[group(total), [total]]];
            }
            const key = group(value);

            for (let i = 0; i < total.length; i++) {
                if (total[i][0] && total[i][0] === key) {
                    total[i][1].push(value);
                    return total;
                }
            }
            total.push([key, [value]]);
            return total;
        })
    }
}

function cloneArray<T>(array: T[]): T[] {
    return JSON.parse(JSON.stringify(array));
}

export function query(): SQL {
    return new SQL();
}
__________________________________________
class SQL {
    private _from: any[] = [];
    private _fromSet: boolean = false;
    private _select: any;
    private _selectSet: boolean = false;
    private _where: any[][] = [];
    private _groupBy: any[] = [];
    private _orderBy: any[] = [];
    private _having: any[][] = [];

    public query(): SQL {
        return this;
    }

    public from(...data: any[]): SQL {
        if (this._fromSet) {
            throw Error('Duplicate FROM');
        }
        this._fromSet = true;
        this._from = cloneArray(data);
        return this;
    }

    public select(select?: any): SQL {
        if (this._selectSet) {
            throw Error('Duplicate SELECT');
        }
        this._selectSet = true;
        this._select = select;
        return this;
    }

    public groupBy(...args: any[]): SQL {
        if (this._groupBy && this._groupBy.length > 0) {
            throw Error('Duplicate GROUPBY');
        }
        this._groupBy = args;
        return this;
    }

    public orderBy(...args: any[]): SQL {
        if (this._orderBy && this._orderBy.length > 0) {
            throw Error('Duplicate ORDERBY');
        }
        this._orderBy = args;
        return this;
    }

    public having(...args: any[]): SQL {
        this._having.push(args);
        return this;
    }

    public where(...args: any[]): SQL {
        this._where.push(args);
        return this;
    }

    public execute(): any[] {
        let data = [];

        if (this._from.length === 1) {
            data = this._from[0];
        } else if (this._from.length > 1
        ) {
            data = this.join();
        }

        data = this.whereFilter(data);

        data = this.groupByData(data);

        data = this.havingData(data);

        data = this.selectData(data);

        data = this.orderByData(data);

        return data;
    }

    private orderByData<T>(data: T[]): T[] {
        for (const order of this._orderBy) {
            data = data.sort((a: any, b: any) => order(a, b))
        }
        return data;
    }

    private selectData<T>(data: T[]): T[] {
        return this._select ? data.map((row: any) => this._select(row)) : data;
    }

    private whereFilter<T>(data: T[]): T[] {
        for (const where of this._where) {
            data = data.filter((data: any) => {
                let stay = false;
                for (const whereOr of where) {
                    if (whereOr(data)) {
                        stay = true;
                    }
                }
                return stay;
            });
        }
        return data;
    }

    private join(): any[][] {
        const result: any[][] = [];
        for(const row1 of this._from[0]){
            for (const row2 of this._from[1]){
                result.push([row1, row2]);
            }
        }
        return result;
    }

    private groupNextLevel(data: any[], group: Function) {
        if (Array.isArray(data) && Array.isArray(data[0])) {
            for (let i = 0; i < data.length; i++) {
                this.groupNextLevel(data[i], group);
            }
        } else if (Array.isArray(data[1]) && Array.isArray(data[1][0])) {
            this.groupNextLevel(data[1], group)
        } else {
            data[1] = this.groupByLevel(data[1], group, 0);
        }
    }

    private havingData<T>(data: T[]): T[] {
        for (const havings of this._having) {
            data = data.filter((row: any) => {
                let stay = false;
                for (const having of havings) {
                    if (having(row)) {
                        stay = true;
                    }
                }
                return stay;
            });
        }
        return data;
    }

    private groupByData(data: any[]): any[] {
        for (let level = 0; level < this._groupBy.length; level++) {
            const group = this._groupBy[level];
            data = this.groupByLevel(data, group, level)
        }
        return data;
    }

    private groupByLevel(data: any[], group: Function, level: number): any[] {
        if (level > 0) {
            this.groupNextLevel(data, group);
            return data;
        }
        if (data.length === 1) {
            const key = group(data[0]);
            return [[key, [data[0]]]]
        }
        return data.reduce((total: any, value: any, i: number) => {
            if (i === 1) {
                total = [[group(total), [total]]];
            }
            const key = group(value);

            for (let i = 0; i < total.length; i++) {
                if (total[i][0] && total[i][0] === key) {
                    total[i][1].push(value);
                    return total;
                }
            }
            total.push([key, [value]]);
            return total;
        })
    }
}

function cloneArray<T>(array: T[]): T[] {
    return JSON.parse(JSON.stringify(array));
}

export function query(): SQL {
    return new SQL();
}
