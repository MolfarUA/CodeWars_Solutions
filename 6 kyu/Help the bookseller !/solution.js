function stockList(listOfArt, listOfCat) {
  var qs = {};
  if (!listOfArt.length) return '';

  listOfArt.forEach(function(art) {
    var cat = art[0];
    qs[cat] = (qs[cat] | 0) + +art.split(' ')[1];
  });

  return listOfCat.map(function(c) {
    return '(' + c + ' : ' + (qs[c] | 0) + ')';  
  }).join(' - ');  
}
________________________________________
function stockList(listOfArt, listOfCat) {
  if (!listOfArt.length || !listOfCat.length) return ''
  return listOfCat.map(w => {
    const s = listOfArt.reduce((a, b) => a + (b.charAt(0) === w ? +b.split(' ')[1] : 0), 0)
    return `(${w} : ${s})`
  }).join(' - ')
}
________________________________________
function stockList(listOfArt, listOfCat) {
  return (! listOfArt.length || ! listOfCat.length) ? "" : listOfCat.map(cat => {
    let needs = listOfArt.filter(el => el.charAt(0) === cat);
    let count = needs.reduce((a, b) => {
      return Number(a) + Number(b.split(" ")[1]);
    }, 0);
    
    return "(" + cat + " : " + count + ")";
  }).join(" - ");
}
________________________________________
function stockList(listOfArt, listOfCat) {
  if (listOfArt.length === 0 || listOfCat === 0) {
    return ''
  }
  
  const catCounts = {}
  
  listOfArt.forEach(entry => {
    const [code, count] = entry.split(' ')
    const category = code[0]
    catCounts[category] = catCounts[category] || 0
    catCounts[category] += Number(count)
  })
  
  
  const catDescription = listOfCat.map(category => {
    return `(${category} : ${catCounts[category] || 0})` 
  })
  
  return catDescription.join(' - ')
}
________________________________________
const stockList = (listOfArt, listOfCat) =>
  listOfArt.length ? listOfCat.map(val => `(${val} : ${listOfArt.reduce((pre, v) => pre + (v[0] === val) * v.split(` `)[1], 0)})`).join(` - `) : ``;
________________________________________
function stockList(listOfArt, listOfCat){
  if( !listOfArt.length || !listOfCat.length ) return ""
  var count = listOfArt.reduce(function(cat,art){
    cat[art[0]]=~~cat[art[0]]+ +art.split(" ")[1];
    return cat
  },{});
  return listOfCat.map(function(cat){ return "("+cat+" : "+(count[cat]||0)+")"}).join(" - ")
}
________________________________________
stockList=(a,b,c=a.map(a=>a.split` `))=>a.length?b.map(i=>[i,c.reduce((a,[b,c])=>a+(b[0]==i?+c:0),0)]).map(([a,b])=>`(${a} : ${b})`).join` - `:''
