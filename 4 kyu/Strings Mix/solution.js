const alphabet = 'abcdefghijklmnopqrstuvwxyz'.split('');

function mix(s1, s2) {
  return alphabet
    .map(char => {
      const s1Count = s1.split('').filter(x => x === char).length,
            s2Count = s2.split('').filter(x => x === char).length,
            maxCount = Math.max(s1Count, s2Count);

      return {
        char: char,
        count: maxCount,
        src: maxCount > s1Count ? '2' : maxCount > s2Count ? '1' : '='
      };
    })
    .filter(c => c.count > 1)
    .sort((objA, objB) => objB.count - objA.count || (objA.src + objA.char > objB.src + objB.char ? 1 : -1))
    .map(c => `${c.src}:${c.char.repeat(c.count)}`)
    .join('/');
}

__________________________________________________
function mix(s1, s2) {
  var counter = s => s.replace(/[^a-z]/g,'').split('').sort().reduce((x,y)=> (x[y] = 1 + (x[y]||0), x),{});
  s1 = counter(s1); s2 = counter(s2);
  var res = [], keys = new Set(Object.keys(s1).concat(Object.keys(s2)));
  keys.forEach(key => {
    var c1 = s1[key]||0, c2 = s2[key]||0, count = Math.max(c1, c2);
    if (count>1) {
      var from = [1, '=', 2][Math.sign(c2-c1)+1];
      var str = [...Array(count)].map(_=>key).join('');
      res.push(from+':'+str);
    }
  });
  return res.sort((x, y) => y.length - x.length || (x < y ? -1 : 1)).join('/');
}

__________________________________________________
const sanitise = string => {
  return string
          .split('')
          .filter(Boolean)
          .filter(c => 'abcdefghijklmnopqrstuvwxyz'.indexOf(c) > -1)
          .filter(c => string.match(new RegExp(c, 'g')).length > 1)
          .join('');
}

const group = string => {
  return string.split('').sort().reduce((acc, c, i, arr) => {
    if (!acc[c]) acc[c] = arr.slice(arr.indexOf(c), arr.lastIndexOf(c) + 1).length;
    return acc;
  }, {});
}

const alphaSort = (a, b) => {
  if (a > b) return -1;
  if (a < b) return 1;
  return 0;
}

const sort = (a, b) => {
  const comparator = a.split(':')[1].length - b.split(':')[1].length;
  return comparator !== 0 ? comparator : alphaSort(a, b);
}

const repeat = (c, n) => {
  return Array(n + 1).join(c)
}

function mix(s1, s2) {
  const group1 = group(sanitise(s1));
  const group2 = group(sanitise(s2));
  const keys = [...Object.keys(group1), ...Object.keys(group2)];

  return keys
    .filter((c, i, arr) => arr.indexOf(c) === i)
    .reduce((output, k) => {
      const len1 = group1[k] || 0;
      const len2 = group2[k] || 0;

      if (len1 === len2) {
        return [...output, `=:${repeat(k, len1)}`];
      }
      else if (len1 > len2) {
        return [...output, `1:${repeat(k, len1)}`];
      }
      else {
        return [...output, `2:${repeat(k, len2)}`];
      }
      return output;
    }, [])
    .sort(sort)
    .reverse()
    .join('/');
}

__________________________________________________
const group = (a) => a.reduce((g, v) => Object.assign(g, { [v]: ++g[v] || 1 }), {})

const mix = (s1, s2) => {
  const s1_values = group(s1.match(/[a-z]/g))
  const s2_values = group(s2.match(/[a-z]/g))

  return Object.keys(Object.assign({}, s1_values, s2_values))
    .map((key) => {
      const s1len = s1_values[key] || 0
      const s2len = s2_values[key] || 0
      const l = Math.max(s1len, s2len)

      return l > 1 && `${s1len === s2len ? '=' : s1len > s2len && '1' || '2'}:${key.repeat(l)}`
    })
    .filter(Boolean)
    .sort((a, b) => a.length < b.length
      ? 1
      : a.length > b.length
        ? -1
        : a > b ? 1 : a < b ? -1 : 0
    )
    .join('/')
}
