53af2b8861023f1d88000832


export function areYouPlayingBanjo(name: string): string {
  return name.startsWith("r") || name.startsWith("R")? name+ " plays banjo": name+ " does not play banjo"
}
________________________________
export function areYouPlayingBanjo(name: string): string {
    return name.charAt(0).toUpperCase() === "R"
        ? `${name} plays banjo`
        : `${name} does not play banjo`;
}
________________________________
export function areYouPlayingBanjo(name: string): string {
  return name + (/^r/i.test(name) ? " plays banjo" : " does not play banjo");
}
