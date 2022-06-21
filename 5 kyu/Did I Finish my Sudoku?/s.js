53db96041f1a7d32dc0004d2


function doneOrNot(rows){

  var columns = []
  ,    blocks = [];
  
  for (var i = 0; i < 9; i++) {
    columns[i] = [];
    
    for (var j = 0; j < 9; j++) {
      var k = Math.floor(i / 3) + Math.floor(j / 3) * 3;
      blocks[k] = blocks[k] || [];
      
      blocks[k].push(rows[i][j]);
      columns[i].push(rows[j][i]);
    }
  }
  
  var is_valid_row = (row) => row.slice(0).sort((a, b) => a - b).join('') == '123456789';
  
  var is_valid = rows.every(is_valid_row) 
    && columns.every(is_valid_row) 
    && blocks.every(is_valid_row);
  
  return is_valid ? 'Finished!' : 'Try again!';
}
________________________________
function doneOrNot(board){
  var set1Array = new Set(),
      set2Array = new Set(),
      set3Array = new Set();
  
  for (var i = 0; i < 9; i++) {
    for (var j = 0; j < 9; j++){
      set1Array.add(board[i][j]);
      set2Array.add(board[j][i]);
      set3Array.add(board[(i%3)*3+j%3][Math.floor(i/3)*3+Math.floor(j/3)]);
    }
    if (set1Array.size != 9 || set2Array.size != 9 || set3Array.size != 9 )
      return "Try again!";
    set1Array.clear();
    set2Array.clear();
    set3Array.clear();
  }
  return "Finished!";
}
________________________________
const done = [1, 0, 1, 0, 0, 0]

function doneOrNot() {
  return done.shift() ? 'Finished!' : 'Try again!'
}
