56a1c63f3bc6827e13000006


function node(value) {
    return {
        value: value,
        left: null,
        right: null,
        lcount: 0,
        scount: 1
    };
}
function Bst() {
    this.root = null;
}
Bst.prototype.insert = function (value) {
    var count = 0;
    if (this.root === null) {
        this.root = node(value);
        return count;
    }
    var current = this.root;
    while (true) {
        if (value < current.value) {
            current.lcount++;
            if (current.left === null) {
                current.left = node(value);
                return count;
            }
            current = current.left;
        }
        else if (value > current.value) {
            count += current.scount + current.lcount;
            if (current.right === null) {
                current.right = node(value);
                return count;
            }
            current = current.right;
        }
        else if (value === current.value) {
            count += current.lcount;
            current.scount++;
            return count;
        }
    }
}

function smaller(arr) {
    var tmp = [];
    var b = new Bst();
    for (var i = arr.length - 1; i >= 0; i--)
        tmp[i] = (b.insert(arr[i]));
    return tmp;
}
______________________________________
function smaller(arr) {
  const n = arr.length;
  if (n == 0) return [];
  const sorted = Array.from(new Set(arr)).sort((a, b) => a - b);
  const u = sorted.length;
  const ords = sorted.reduce((h, x, i) => (h[x] = i, h), {});
  const tree = new Uint16Array(u + 1); // Binary Indexed Tree
  const xs = arr.slice();
  for (let i = n - 1; i >= 0; --i) {
    const k = ords[arr[i]];
    xs[i] = _count(tree, k); // count of visited values ordered before arr[i]
    _incr(tree, k + 1, u);
  }
  return xs;
}

function _count(tree, index) {
  var i = index + 1;
  var sum = 0;
  while (i > 0) sum += tree[i], i -= (i & -i);
  return sum;
}

function _incr(tree, index, n) {
  var i = index + 1;
  while (i <= n) ++tree[i], i += (i & -i);
}
