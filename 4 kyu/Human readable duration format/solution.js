function formatDuration (seconds) {
  var time = { year: 31536000, day: 86400, hour: 3600, minute: 60, second: 1 },
      res = [];

  if (seconds === 0) return 'now';
  
  for (var key in time) {
    if (seconds >= time[key]) {
      var val = Math.floor(seconds/time[key]);
      res.push(val += val > 1 ? ' ' + key + 's' : ' ' + key);
      seconds = seconds % time[key];
    }
  }
 
  return res.length > 1 ? res.join(', ').replace(/,([^,]*)$/,' and'+'$1') : res[0]
}

__________________________________________________
function formatDuration (seconds) {
  if(!seconds)return "now";
  var strout = "";
  var s = seconds%60;
  seconds = (seconds-s)/60;
  var m = seconds%60;
  seconds = (seconds-m)/60;
  var h = seconds%24;
  seconds = (seconds-h)/24;
  var d = seconds%365;
  seconds = (seconds-d)/365;
  var y = seconds;
  
  var english=[];
  if(y)english.push(y+" year"+(y>1?'s':''));
  if(d)english.push(d+" day"+(d>1?'s':''));
  if(h)english.push(h+" hour"+(h>1?'s':''));
  if(m)english.push(m+" minute"+(m>1?'s':''));
  if(s)english.push(s+" second"+(s>1?'s':''));
  
  return english.join(", ").replace(/,([^,]*)$/," and$1");
  
}

__________________________________________________
var formatDuration = (function () {

  return function formatDuration (seconds) {
    return [{name: 'year',   size: 365 * 24 * 60 * 60 * 1},
            {name: 'day',    size:       24 * 60 * 60 * 1},
            {name: 'hour',   size:            60 * 60 * 1},
            {name: 'minute', size:                 60 * 1},
            {name: 'second', size:                      1}].
            reduce(parse, { parts: [], seconds: seconds }).
            parts.
            reduce(join, 'now');
  };
  
  function parse (result, part) {
    var quantity = Math.floor(result.seconds / part.size);
    if (quantity > 0) {
      result.seconds -= quantity * part.size;
      result.parts.push(quantity + ' ' + part.name + (quantity == 1 ? '' : 's'));
    }
    return result;
  }
  
  function join (result, part, index, arr) {
    switch (index) {
      case 0: return part;
      case arr.length - 1: return result + ' and ' + part;
      default: return result + ', ' + part;
    }
  }
  
}());

__________________________________________________
function formatDuration (seconds){
  if(seconds == 0) return "now";
  var s = {
    "year" : (60 * 60 * 24 * 365),
    "day" : (60 * 60 * 24),
    "hour" : (60 * 60),
    "minute" : 60
  }
  var output = new Array();
  var years = Math.floor(seconds / s.year);
  if(years > 0){
    output.push(years + " year" + (years == 1 ? "" : "s"));
    seconds = seconds % s.year;
  }
  var days = Math.floor(seconds / s.day);
  if(days > 0){
    output.push(days + " day" + (days == 1 ? "" : "s"));
    seconds = seconds % s.day;
  }
  var hours = Math.floor(seconds / s.hour);
  if(hours > 0){
    output.push(hours + " hour" + (hours == 1 ? "" : "s"));
    seconds = seconds % s.hour;
  }
  var minutes = Math.floor(seconds / s.minute);
  if(minutes > 0){
    output.push(minutes + " minute" + (minutes == 1 ? "" : "s"));
    seconds = seconds % s.minute;
  }
  if(seconds > 0){
    output.push(seconds + " second" + (seconds == 1 ? "" : "s"));
  }
  if(output.length > 1){
    var last = output.pop();
    return output.join(", ") + " and " + last;
  } else {
    return output[0];
  }
}

__________________________________________________
const delegates = [
  { s: 'year', v: 60 * 60 * 24 * 365 },
  { s: 'day', v: 60 * 60 * 24 },
  { s: 'hour', v: 60 * 60 },
  { s: 'minute', v: 60 },
  { s: 'second', v: 1 }
];

function formatDuration (seconds) {
  if (!seconds) return 'now';
  
  return delegates.reduce((ret, dg, idx) => {
    const val = Math.floor(seconds / dg.v);
    if (!val) return ret;
    seconds -= dg.v * val;
    const str = val > 1 ? dg.s + 's' : dg.s;
    const add = !ret ? '' : (seconds > 0 ? ', ' : ' and ');
    return ret + add + `${val} ${str}`;
  }, '');
}
