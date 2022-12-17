57873ab5e55533a2890000c7


export function timeCorrect(ts: String): String {
  if(ts === "") return ""; 
  if(ts === null || !ts.match(/^[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]$/)) return null;
  let [h, m, s] = ts.split(':').map(v => parseInt(v));
  let temp: number = 0;
  [s, temp] = convToUp(s);
  [m, temp] = convToUp(m + temp);
  h = (h + temp) % 24;
  return [h, m, s].map(v => (`0${v}`).substr(v.toString().length - 1)).join(':');
}

function convToUp(num): number[] {
  let s: number = num % 60;
  let temp: number = (num - s) / 60;
  return [s, temp];
}
_________________________________
function prependZeros(str: string): string {
  let result = str;
  while(result.length < 2) {
    result = "0" + result;
  }
  return result
}

export function timeCorrect(timestring: string | null): string | null {
  if(!timestring) return timestring;
  
  const arrayTimestring = timestring.split(":").map(el => +el);
  if(arrayTimestring.filter(el => !Number.isNaN(el)).length !== 3) return null;
  
  let [hours, minutes, seconds] = arrayTimestring;
  if(seconds >= 60) {
    minutes += Math.floor(seconds / 60);
    seconds = seconds - Math.floor(seconds / 60) * 60
  }
  
  if(minutes >= 60) {
    hours += Math.floor(minutes / 60);
    minutes = minutes - Math.floor(minutes / 60) * 60
  }
  
  if (hours >= 24) {
    hours = hours - Math.floor(hours / 24) * 24
  }
  
  return prependZeros(hours + "") + ":" + prependZeros(minutes + "") + ":" + prependZeros(seconds + "");
}
_________________________________
export function timeCorrect(timestring: string | null): string | null {
  if (timestring === null) return null;
  if (timestring === "") return "";
  
  const regex = /^\d{2}:\d{2}:\d{2}$/
  if (!regex.test(timestring)) {
    return null
  }
  
  

  let hr: string | number = parseInt(timestring.split(":")[0]);
  let min: string | number = parseInt(timestring.split(":")[1]);
  let sec: string | number = parseInt(timestring.split(":")[2]);

  if (sec >= 60) {
    sec = sec % 60;  
    min += 1
  }
  
  if (min >= 60) {
    min = min % 60;
    hr += 1
  }
  
  if (hr >= 24) {
    hr = hr % 24;
  }
  
  if (sec < 10) {
    sec = "0" + sec.toString()
  } else {
    sec = sec.toString()
  }
  
  if (min < 10) {
    min = "0" + min.toString()
  } else {
    min = min.toString()
  }
  
  if (hr < 10) {
    hr = "0" + hr.toString()
  } else {
    hr = hr.toString()
  }
  
  return `${hr}:${min}:${sec}`
}
