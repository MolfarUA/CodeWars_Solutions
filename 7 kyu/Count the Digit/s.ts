566fc12495810954b1000030


export class G964 {
    public static nbDig(n: number, d: number): number {
        let count: number = 0;
        for (let k: number = 0; k <= n; k++) {
            count += (k * k).toString().split(d.toString()).length - 1;
        }
        return count;
    }
}
____________________________
export class G964 {
  public static nbDig(n: number, d: number): number {
    let count = '';
    for (let i = 0; i <= n; i++){
      count += i**2 
    }
    return [...count].filter(el => el === String(d)).length
  }
}
// Don't understand why RegExp doesn't work here?
____________________________
export class G964 {
    public static nbDig(n, d) {
        let str = '';
        for (let k = 0; k <= n; k++) {
            str += k ** 2;
        }
        return str.split(d).length - 1;
    }
}
