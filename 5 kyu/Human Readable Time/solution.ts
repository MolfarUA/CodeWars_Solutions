export function humanReadable(seconds:number):string {
  const minutes = Math.floor(seconds / 60)

  const onlySeconds = seconds % 60
  const onlyMinutes = minutes % 60
  const onlyHours = Math.floor(minutes / 60)
  
  return [onlyHours, onlyMinutes, onlySeconds].map(formatTime).join(':')
}

const formatTime = (time: number) :string => time >= 10 ? time.toString() : `0${time}`

_____________________________________
const format = (n: number) => String(Math.floor(n)).padStart(2, "00");

export function humanReadable(seconds: number): string {
  const h = seconds / 3600;
  const m = seconds % 3600 / 60;
  const s = seconds % 3600 % 60;
  
  return [h, m, s].map(format).join(":");
}

_____________________________________
export function humanReadable(seconds:number):string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor(seconds / 60) % 60;
  const pad = (n: number) => `${n}`.padStart(2, '0');
  return `${pad(hours)}:${pad(minutes)}:${pad(seconds % 60)}`;
}

_____________________________________
const formatTime = (sec: number) => (sec > 9 ? `${sec}` : `0${sec}`);

export function humanReadable(seconds: number): string {
  const hh = Math.floor(seconds / 3600);
  const mm = Math.floor(seconds / 60) % 60;
  const ss = seconds % 60;

  return [hh, mm, ss].map(formatTime).join(":");
}

_____________________________________
export function humanReadable(seconds:number):string {
  return [Math.floor((seconds/60)/60), Math.floor(seconds/60)%60, seconds%60].map(part=>(("0"+part).substr(-2))).join(":");
}
