57037ed25a7263ac35000c80


function generateLink(user) {
  return `http://www.codewars.com/users/${encodeURIComponent(user)}`;
}
_______________________________________
const generateLink = user => `http://www.codewars.com/users/${encodeURIComponent(user)}`;
_______________________________________
function generateLink(user) {
  return 'http://www.codewars.com/users/' + encodeURIComponent(user);
}
