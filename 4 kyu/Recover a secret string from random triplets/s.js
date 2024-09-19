53f40dff5f9d31b813000774


var recoverSecret = function(triplets) {
  for(var [first] of triplets)
  {
    if (triplets.every(tuple => tuple.indexOf(first) <= 0))
    {
      triplets.filter(([item]) => item == first).forEach(tuple => tuple.shift());
      return first + recoverSecret(triplets.filter(tuple => tuple.length > 0));
    }
  }
  return '';
}
##########################
var recoverSecret = function(triplets) {
  var nodes = []
  var graph = {}
  var sortedlist = []

  function visit(node) {
    if (sortedlist.indexOf(node) < 0) {
      (graph[node] || []).forEach(function (node2) { visit(node2) })
      sortedlist.unshift(node)
    }
  }

  triplets.forEach(function (triplet) {
    triplet.forEach(function (node) {
      if (nodes.indexOf(node) < 0) nodes.push(node);
    })
    graph[triplet[0]] = (graph[triplet[0]] || []).concat(triplet[1])
    graph[triplet[1]] = (graph[triplet[1]] || []).concat(triplet[2])
  })

  while (nodes.length) visit(nodes.pop());
  return sortedlist.join('');
}

######################
var recoverSecret = function(triplets) {
  var charInfo = {};
  
  var registeredOrderedPair = function(ch1, ch2) {
    var ch1Info = charInfo[ch1] || {earlier: [], later: []};
    var ch2Info = charInfo[ch2] || {earlier: [], later: []};
    ch1Info.later.push(ch2);
    ch2Info.earlier.push(ch1);
    charInfo[ch1] = ch1Info;
    charInfo[ch2] = ch2Info;
  }
  
  var findEarliest = function() {
    // Earliest is the one that has no earlier characters
    for(var ch in charInfo) {
      if (charInfo[ch].earlier.length == 0) return ch;
    }
  }
  
  var removeChar = function(chToDelete) {
    delete charInfo[chToDelete];
    var isNotCh = function(ch) {return ch !== chToDelete;};
    for(var ch in charInfo) {
      charInfo[ch].earlier = charInfo[ch].earlier.filter(isNotCh);
      charInfo[ch].later = charInfo[ch].later.filter(isNotCh);
    }
  }
  
  triplets.forEach(function(triplet) {
     registeredOrderedPair(triplet[0], triplet[1]); 
     registeredOrderedPair(triplet[1], triplet[2]); 
  });
  
  var result = '';
  while(Object.keys(charInfo).length > 0) {
    var ch = findEarliest();
    result += ch;
    removeChar(ch);
  }
  
  return result;
}
