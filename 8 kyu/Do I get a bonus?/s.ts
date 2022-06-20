56f6ad906b88de513f000d96


export class Kata {
    public static bonusTime(salary:number, bonus:boolean):string {
      return `£${salary * (bonus ? 10 : 1)}`;
    }
}
__________________________
export class Kata {
    public static bonusTime(salary:number, bonus:boolean):string {
      return `£${bonus ? 10 * salary : salary}`;
    }
}
__________________________
export class Kata {
    public static bonusTime(salary:number, bonus:boolean):string {
      return bonus ? '£' + salary * 10 : '£' + salary;
    }
}
__________________________
export class Kata {
  public static bonusTime = (salary: number, bonus: boolean): string =>
    `£${salary * (bonus ? 10 : 1)}`;
}
