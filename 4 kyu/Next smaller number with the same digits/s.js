5659c6d896bc135c4c00021e


const nextSmaller = n => {
  let min = minify(n);
  while (--n >= min) if (minify(n) === min) return n;
  return -1;
};

const minify = n => [...`${n}`].sort().join``.replace(/^(0+)([1-9])/, '$2$1');
_______________________________
function nextSmaller(n) {
  var digits = ('' + n).split('');
  for (var ix = digits.length - 1; ix-- > 0;) {
    if (digits[ix + 1] < digits[ix]) {
      var tail = digits.slice(ix).sort((a, b) => b - a);
      var head = tail.splice(tail.findIndex(x => x < digits[ix]), 1);
      if (!ix && '0' == head[0]) {
        return -1;
      }
      return +digits.slice(0, ix).concat(head, tail).join('');
    }
  }
  return -1;
}
_______________________________
function nextSmaller(n) {
  var s=n.toString();
  var b='';
  var i=s.length-1;
  while (s[i]>=s[i-1])
    b=s[i--]+b;
  b=s[i]+b;
  if (b==s)
    return -1
  if (i!=0)
    b=s[--i]+b;
  var u='';
  for (var j=0; j<i; ++j)
    u+=s[j];
  var arr=[s];
  if (b.length==2)
  {
    var d=+(u+b[1]+b[0])+''
    if (d<s&&d.length==s.length)
      return +d;
    return -1;
  }
  if (b.length==3)
  {
    var d='';
    for (var i=0; i<3; ++i)
    for (var j=0; j<3; ++j)
    for (var k=0; k<3; ++k)
    if (i!=j&&i!=k&&j!=k)
    {
      d=Number(u+b[i]+b[j]+b[k])+''
      if (arr.indexOf(d)==-1&&d.length==s.length)
        arr.push(d);
    }
    arr.sort();
    if (arr.indexOf(s)==0)
      return -1;
    return +arr[arr.indexOf(s)-1];
  }
  if (b.length==4)
  {
    var d='';
    for (var a1=0; a1<4; ++a1)
    for (var a2=0; a2<4; ++a2)
    for (var a3=0; a3<4; ++a3)
    for (var a4=0; a4<4; ++a4)
    if (a1!=a2 && a1!=a3 && a1!=a4 &&
        a2!=a3 && a2!=a4 && 
        a3!=a4)
    {
      d=Number(u+b[a1]+b[a2]+b[a3]+b[a4])+''
      if (arr.indexOf(d)==-1 && d.length==s.length)
        arr.push(d);
    }
    arr.sort();
    if (arr.indexOf(s)==0)
      return -1;
    return +arr[arr.indexOf(s)-1];
  }
  if (b.length==5)
  {
    var d='';
    for (var a1=0; a1<5; ++a1)
    for (var a2=0; a2<5; ++a2)
    for (var a3=0; a3<5; ++a3)
    for (var a4=0; a4<5; ++a4)
    for (var a5=0; a5<5; ++a5)
    if (a1!=a2 && a1!=a3 && a1!=a4 && a1!=a5 &&
        a2!=a3 && a2!=a4 && a2!=a5 &&
        a3!=a4 && a3!=a5 &&
        a4!=a5)
    {
      d=Number(u+b[a1]+b[a2]+b[a3]+b[a4]+b[a5])+''
      if (arr.indexOf(d)==-1 && d.length==s.length)
        arr.push(d);
    }
    arr.sort();
    if (arr.indexOf(s)==0)
      return -1;
    return +arr[arr.indexOf(s)-1];
  }
  if (b.length==6)
  {
    var d='';
    for (var a1=0; a1<6; ++a1)
    for (var a2=0; a2<6; ++a2)
    for (var a3=0; a3<6; ++a3)
    for (var a4=0; a4<6; ++a4)
    for (var a5=0; a5<6; ++a5)
    for (var a6=0; a6<6; ++a6)
    if (a1!=a2 && a1!=a3 && a1!=a4 && a1!=a5 && a1!=a6 &&
        a2!=a3 && a2!=a4 && a2!=a5 && a2!=a6 &&
        a3!=a4 && a3!=a5 && a3!=a6 &&
        a4!=a5 && a4!=a6 &&
        a5!=a6)
    {
      d=Number(u+b[a1]+b[a2]+b[a3]+b[a4]+b[a5]+b[a6])+''
      if (arr.indexOf(d)==-1 && d.length==s.length)
        arr.push(d);
    }
    arr.sort();
    if (arr.indexOf(s)==0)
      return -1;
    return +arr[arr.indexOf(s)-1];
  }
  return -1;
}
