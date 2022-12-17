5376b901424ed4f8c20002b7


function closestPair(a, cd) {
    let mf = function(a) {
        a = a.slice();
        if (a.length < 2) return [9999999, 0, 0];
        if (a.length == 2) return [cd(a[0], a[1]), a[0], a[1]];

        var q = Math.floor(a.length / 2);
        var a1 = a.slice(0, q);
        var a2 = a.slice(q);
        var [mi1, x1, y1] = mf(a1);
        var [mi2, x2, y2] = mf(a2);
        if (mi1 < mi2) {
            var [mi, x, y] = [mi1, x1, y1];
        } else {
            var [mi, x, y] = [mi2, x2, y2];
        }
        var b = a.filter(p => Math.abs(p[0] - a[q][0]) < mi);
        b.sort((a, b) => a[1] - b[1]);
        for (let i = 0; i < b.length - 1; i++) {
            for (let j = i + 1; j < b.length; j++) {
                if (b[j][1] - b[i][1] > mi) break;
                var mid = cd(b[i], b[j]);
                if (mid < mi) {
                    var [mi, x, y] = [mid, b[i], b[j]];
                }
            }
        }
        return [mi, x, y];
    }

    a = a.slice();
    a.sort((a, b) => a[0] - b[0]);

    var [_, x, y] = mf(a);

    return [x, y];
}
______________________________________
function closestPair(points) {
  const arr = points.sort((a,b)=>a[0]-b[0]);
  const n = arr.length;
  let l = Number.MAX_VALUE;
  let tolerance = Math.sqrt(l);
  let a = 0, b = 0;
  for (let i=0; i+1<n; i++) {
    for (let j=i+1; j<n; j++) {
      if (arr[j][0] >= arr[i][0] + tolerance) break;
      let ls = (arr[i][0]-arr[j][0])**2 + (arr[i][1]-arr[j][1])**2;
      if (ls < l) {
        l = ls;
        tolerance = l**0.5;
        a = i;
        b = j;
      }
    }
  }
  return [arr[a], arr[b]];
}
______________________________________
// Calculate a pair of closest points in linearithmic time
function closestPair(points) {
   
  // 1. sort by x
  points.sort(([x1],[x2]) => x1-x2);
  
  // 2. recursively devide two halves and find smalles distances
  return closest(points).points;
}

// distance helper
const distance = ([x1,y1],[x2,y2]) => Math.sqrt(Math.pow(x1-x2,2) + Math.pow(y1-y2,2));

// last 2/3 items compare all
const bruteForce = points => {
  const l = points.length;
  let min = null;
  let minDistance = undefined;
  
  for (let i=0; i < l; i++) {
    for (let j=i+1; j<l; j++) {
      let tmpDistance = distance(points[i], points[j]);
      if (!min || tmpDistance < minDistance) {
        min = [points[i], points[j]];
        minDistance = tmpDistance;
      }
    }
  }
  return { points: min, d: minDistance };
};

const closest = points => {
  if (points.length <= 3) return bruteForce(points);
  
  // split in halves and get smallest distance
  const mid = Math.floor(points.length/2);
  const midPoint = points[mid];

  const dl = closest(points.slice(0, mid));
  const dr = closest(points.slice(mid));
  const dMin = dl.d < dr.d ? dl : dr;
  
  // find points closer than dMin to middle-point (x)
  const strip = points.filter(p => Math.abs(p[0] - midPoint[0]) < dMin.d);
  const stripPoints = stripClosest(strip, dMin.d);

  return dMin.d < stripPoints.d ? dMin : stripPoints;
};

// find smallest distance to mid-stripe
const stripClosest = (points, minDistance) => {
  points.sort(([,y1],[,y2]) => y1-y2);

  let min = minDistance;
  let minPoints = null;
  const l = points.length;
  
  for (let i=0; i<l; i++) {
    for (let j=i+1; j<l && Math.abs(points[j][1] - points[i][1]) < min; j++) {
      const tempDist = distance(points[i], points[j]);
      if (tempDist < min) {
        min = tempDist;
        minPoints = [points[i], points[j]];
      }
    }
  }

  return minPoints ? { points: minPoints, d: min } : { d: Infinity };
};
