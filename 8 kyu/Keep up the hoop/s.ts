55cb632c1a5d7b3ad0000145


export function hoopCount(n: number): string {
  return n<10?"Keep at it until you get it":"Great, now move on to tricks"  
}
_____________________________
export function hoopCount(n: number): string {
  return n >= 10 ? "Great, now move on to tricks": "Keep at it until you get it"
}
_____________________________
export function hoopCount(n: number): string {
  let result: string = "";

  if (n < 10) {
    result = "Keep at it until you get it";
  } else if (n >= 10) {
    result = "Great, now move on to tricks";
  }

  return result;
}
