function ipsBetween(start, end){
  const num = ip => ip.split('.')
                      .map(x => parseInt(x))
                      .reduce((acc, e) => acc * 256 + e);  
  
  return num(end) - num(start);
}
__________________
function ipsBetween(start, end)
{
    let res = 0
    const arr1 = start.split(".")
    const arr2 = end.split(".")

    for (let i = 0; i < 4; i++)
        { res += (parseInt(arr2[i]) - parseInt(arr1[i])) * Math.pow(256, (3 - i)) }

    return res
}
_________________
function ipsBetween(start, end){
  var start=start.split(".")
  var end=end.split(".")
  var sum1=0
  var sum2=0
  var len=start.length-1
  for (let i of start){
    sum1+=(+i)*(256**len)
    len--
  }
  len=start.length-1
  for (let i of end){
    sum2+=(+i)*(256**len)
    len--
  }
  return Math.abs(sum1-sum2)
}
_________________
function ipsBetween(start, end){
  const startOctets = start.split('.').map(Number);
  const endOctets = end.split('.').map(Number);
  let addressCount = 0;
  for (let i = 0; i < 4; i++) {
    addressCount = addressCount * 256 + (endOctets[i] - startOctets[i]);
  }

  return addressCount;  
}

