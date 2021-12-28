function maxSumPath(l1, l2) {
  let total = 0;
  let i = 0;
  let l1Index = 0,
    l2Index = 0;
  let l1Tot = 0,
    l2Tot = 0;
  let l1Contains;
  let l2Contains;

  const maximum = Math.max(l1.slice(-1), l2.slice(-1));
  while (i < maximum + 1) {
    l1Contains = false;
    l2Contains = false;
    if (l1[l1Index] === i) {
      l1Tot += l1[l1Index];
      l1Contains = true;
      l1Index++;
    }
    if (l2[l2Index] === i) {
      l2Tot += l2[l2Index];
      l2Contains = true;
      l2Index++;
    }
    if (l1Contains && l2Contains) {
      total += Math.max(l1Tot, l2Tot);
      l1Tot = 0;
      l2Tot = 0;
    }

    i++;
  }
  total += Math.max(l1Tot, l2Tot);
  return total;
}

_________________________________
function maxSumPath(a,b){
  let i=0, j=0, A=0, B=0
  while(i<a.length && j<b.length){
    let x=a[i], y=b[j]
    if(x===y) A=B=Math.max(A,B)
    if(x<=y){ i++; A+=x }
    if(x>=y){ j++; B+=y }
  }
  while(i<a.length) A+=a[i++]
  while(j<b.length) B+=b[j++]
  return Math.max(A,B)
}

_________________________________
function maxSumPath(arr1,arr2){
    let result = 0, sum1 = 0, sum2 = 0;
    let i = 0, j = 0;
    while(i < arr1.length && j < arr2.length){
        if(arr1[i] < arr2[j]){
            sum1 += arr1[i++];
        } else if (arr1[i] > arr2[j]){
            sum2 += arr2[j++];
        } else {
            result += Math.max(sum1, sum2) + arr1[i];
            sum1 = 0, sum2 = 0;
            i++, j++;
        }
    }
    while(i < arr1.length){ sum1 += arr1[i++] };
    while(j < arr2.length){ sum2 += arr2[j++] };
    return result += Math.max(sum1, sum2);
}

_________________________________
const maxSumPath=(a,b)=>{

  let i,j,p,q,s
  let m=a.length
  let n=b.length

  for ( i=j=p=q=s=0; i<m||j<n; )

    if(i>=m||a[i]>b[j]) q+=b[j++]; else
    if(j>=n||a[i]<b[j]) p+=a[i++]; else
    if(a[i]==b[j]) s+=(p>q?p:q)+a[i++],j++,p=q=0

  return s+(p>q?p:q)
}

_________________________________
function maxSumPath(l1,l2){
  
  var i=0, j=0;
  var acc1=0, acc2=0;
  var tot=0;
  
  /*
  walks both list same time
  accumulating until find a common number (where can change)
  and saves best value
  
  if one got to end accums the rest of the other and returns the best case
  */
  
  while(i<l1.length && j<l2.length){
    
    if(l1[i] === l2[j]){
      //keep the best acc
      if(acc1 > acc2){
        tot += acc1 + l1[i];
      }else{
        tot += acc2 + l1[i];
      }
      [acc1, acc2] = [0, 0];
      i++;
      j++;
    }else{
      if(l1[i] < l2[j]){
        acc1 += l1[i];
        i++;
      }else{
        acc2 += l2[j];
        j++;
      }
    }
    
  }
  
  while(i<l1.length){
    acc1 += l1[i++];
  }
  
  while(j<l2.length){
    acc2 += l2[j++];
  }
  
  return acc1 > acc2 ? tot+acc1 : tot+acc2;
  
}
