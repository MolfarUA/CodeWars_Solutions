58b1ae711fcffa34090000ea


function door(events) {

  const OPENED = 0;
  const CLOSED = 1;
  const OPENING = 2;
  const CLOSING = 3;
  const PAUSED_OPENING = 4;
  const PAUSED_CLOSING = 5;

  let state = 1;
  let pos = 0;
  let res = '';

  for (let event of events) {

    switch (state) {

      case OPENED: 
        if (event === 'P') state = CLOSING;
        break;

      case CLOSED:
        if (event === 'P') state = OPENING;
        break;

      case OPENING:
        if (event === 'P') state = PAUSED_OPENING;
        if (event === 'O') state = CLOSING;
        if (pos === 5) state = OPENED;
        break;
        
      case CLOSING: 
        if (event === 'P') state = PAUSED_CLOSING;
        if (event === 'O') state = OPENING;
        if (pos === 0) state = CLOSED;
        break;

      case PAUSED_OPENING: 
        if (event === 'P') state = OPENING;
        break;

      case PAUSED_CLOSING:
        if (event === 'P') state = CLOSING;
        break;

    }

    if (state === OPENING)
      pos += 1;

    if (state === CLOSING)
      pos -= 1;

    res = res + pos;

  }
  
  return res;

}
______________________________________
function door(events) {
  let dir = 0, paused = true, prev = 0
  return [...events].map(x => {
    if (x == '.') {
      if ((dir > 0 && prev == 5) || (dir < 0 && prev == 0)) paused = true
      if (paused) return prev
      return prev += dir
    }
    if (x == 'P') {
      if (paused) {
        if (prev == 5) dir = -1
        else if (prev == 0) dir = 1
        paused = false
        return prev += dir
      }
      paused = true
      return prev
    }
    // x == 'O'
    dir = -dir
    return prev += dir
  }).join``
}
______________________________________
door=(ev)=>{
  var d=0,i=0,p=-1,s='';
  for (var c in ev) {
    var e=ev[c];if(e=='P')if(i%5==0)d=1-(i==5?2:0);else p=-p; 
    s+=i=Math.max(0,Math.min(i+(p==1?0:(d=e=='O'?-d:d)),5));
  }
  return s;
}
