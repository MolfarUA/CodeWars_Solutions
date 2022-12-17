55b42574ff091733d900002f


function friend(friends){
  return friends.filter(n => n.length === 4)
}
________________________________
const friend = friends => friends.filter(friend => friend.length == 4);
________________________________
function friend(friends){
  return friends.filter(value => value.length === 4);
}
________________________________
function friend(friends){
    return friends.filter(function (name){
        return name.length == 4;
    });
}
