55225023e1be1ec8bc000390


function greet(name){
  return "Hello, " + (name == "Johnny" ? "my love" : name) + "!";
}
__________________________________
function greet(name){  
  if(name === "Johnny")
    return "Hello, my love!";
  return "Hello, " + name + "!";
}
__________________________________
function greet(name){
  if(name === "Johnny")
    return "Hello, my love!";
  else
    return "Hello, " + name + "!";
}
__________________________________
let greet = name => `Hello, ${name == "Johnny" ? "my love" : name}!`;
__________________________________
function greet(name){
  return name === "Johnny" ? "Hello, my love!" : "Hello, " + name + "!";
}
