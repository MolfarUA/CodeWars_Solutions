55f9bca8ecaa9eac7100004a


const seconds = (s: number) => s * 1000;
const minutes = (m: number) => m * seconds(60);
const hours = (h: number) => h * minutes(60);

export function past(h: number, m: number, s: number): number {
  return hours(h) + minutes(m) + seconds(s);
}
__________________________
export function past(h: number, m: number, s: number): number {
  return (h*3600+m*60+s)*1000
}
__________________________
export function past(h: number, m: number, s: number): number {
  h = h * 60 * 60 * 1000
  m = m * 60 * 1000
  s = s * 1000
  return +(h + m + s)
}
__________________________
export const past = (h: number, m: number, s: number): number => {
    h ? h = h * 60 * 60 * 1000 : 0;
    m ? m = m * 60 * 1000 : 0;
    s ? s = s * 1000 : 0;    
    return h + s + m;
}
__________________________
export function past(h: number, m: number, s: number): number {
  const secondsToMs = s * 1000;
  const minutesToMs = m * 60000;
  const hoursToMs = h * 3600000;
  
  const result = hoursToMs + minutesToMs + secondsToMs
  
  return result
}
