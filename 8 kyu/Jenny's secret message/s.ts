55225023e1be1ec8bc000390


export function greet(name: string): string {
  if (name === "Johnny") {
    return "Hello, my love!";
    }
  return "Hello, " + name + "!";
  
}
__________________________________
export const greet = (name : string) : string => `Hello, ${name === "Johnny" ? "my love!" : name}!`;
__________________________________
export function greet(name: string): string {
  if(name === "Johnny") {
    name = "my love";
  }
  return "Hello, " + name + "!";
}
__________________________________
export const greet = (name: string): string => `Hello, ${name === 'Johnny' ? 'my love!' : `${name}!`}`;
__________________________________
export const greet = (name: string): string => `Hello, ${name === 'Johnny' ? 'my love' : name}!`;
