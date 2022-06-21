58708934a44cfccca60000c4


highlight = (code) ->
  code
    .replace(/(F+)/g, '<span style="color: pink">$1</span>')
    .replace(/(L+)/g, '<span style="color: red">$1</span>')
    .replace(/(R+)/g, '<span style="color: green">$1</span>')
    .replace(/(\d+)/g, '<span style="color: orange">$1</span>')
__________________________
highlight = (code) =>
  code
  .replace(/(F+)/g, '<span style="color: pink">$1</span>')
  .replace(/(L+)/g, '<span style="color: red">$1</span>')
  .replace(/(R+)/g, '<span style="color: green">$1</span>')
  .replace(/([0-9]+)/g, '<span style="color: orange">$1</span>')
__________________________
C = {F:'pink',L:'red',R:'green','\\d':'orange'}

highlight = (s) ->
  for k,v of C
    s = s.replace(new RegExp(k + '+', 'g'), "<span style=\"color: #{v}\">$&</span>")
  s
