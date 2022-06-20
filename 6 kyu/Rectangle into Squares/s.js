55466989aeecab5aac00003e


function sqInRect(lng, wdth){
  let arr = []
  if(lng === wdth) return null
  while(lng > 0 && wdth > 0){
    arr.push(lng > wdth ? wdth : lng)
    lng > wdth ? lng -= wdth : wdth -= lng
  }
  return arr
}
______________________________
function sqInRect(lng, wdth){
  if(lng === wdth){
    return null;
  }
  var squares = [];
  
  while(lng !== wdth){
    if (lng > wdth) {
      squares.push(wdth);
      lng = lng - wdth;
    } else {
      squares.push(lng);
      wdth = wdth - lng;
    }
  }
  squares[squares.length] = squares[squares.length -1];
  
  return squares;
}
______________________________
function sqInRect(length, width) {
  if (length === width) {
    return null;
  }
  
  const result = [];
  
  while (length > 0 && width > 0) {
    result.push(Math.min(length, width));
    
    if (length > width) {
      length -= width;
    } else {
      width -= length;
    }
  }
  
  return result;
}
