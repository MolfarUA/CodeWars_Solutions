export function number(busStops:number[][]):number {
  return busStops.reduce((rem, [on, off]) => rem+(on-off), 0);
}
_____________________________________
export function number(busStops:number[][]):number {
  let result = 0;
  busStops.forEach((x) => {
    result += x[0] - x[1];
  });
  return result;
}
_____________________________________
export function number(busStops:number[][]):number {
   let people = 0;
    busStops.map(stop => {
      people += stop[0];
      people -= stop[1];
    });
    return people;
  }
_____________________________________
export function number( bS: [number, number][]): number {
  return bS.reduce((acc, [inBus, outBus]) => acc + inBus - outBus, 0)
}
_____________________________________
interface IPassengers {
  into: number;
  out: number;
}

export function number(busStops: [number, number][]): number {
  const passengers: IPassengers = { into: 0,  out: 0 };

  busStops.forEach(stop => {
    passengers.into += stop[0];
    passengers.out += stop[1];
  });
  
  const stillInBus: number = passengers.into - passengers.out;
  
  return stillInBus;
}
