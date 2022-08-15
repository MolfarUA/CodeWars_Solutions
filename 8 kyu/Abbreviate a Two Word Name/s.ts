57eadb7ecd143f4c9c0000a3


export function abbrevName(name: string): string {
    return name.split(" ").map((item)=> item[0].toUpperCase()).join('.')
}
_________________________
export function abbrevName(name: string): string {
    return name
      .split(" ")
      .map(n => n[0].toUpperCase())
      .join(".");
}
_________________________
export function abbrevName(name: string): string {
    let arr: string[] = name.split(" ");
    return arr[0][0].toUpperCase() + "." + arr[1][0].toUpperCase();
}
