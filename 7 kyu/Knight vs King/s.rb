564e1d90c41a8423230000bc


def knight_vs_king((nx, ny), (kx, ky))
  dx = nx - kx
  dy = ny.ord - ky.ord
  d = dx**2 + dy**2
  
  d == 5 ? "Knight" : d < 3 ? "King" : "None"
end
_______________________________________
C_TO_N = {'A' => 1, 'B' => 2, 'C' => 3, 'D' => 4, 'E' => 5, 'F' => 6, 'G' => 7, 'H' => 8}

ADDINGS = [ [1, 2], [ 2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]

def numeric_pos(chess_pos)
  [chess_pos[0], C_TO_N[chess_pos[1]]]  
end

def king_beats_knight?(king, knight)
  (king[0]-1..king[0]+1).include?(knight[0]) && (king[1]-1..king[1]+1).include?(knight[1])
end

def knight_beats_king?(knight, king)
  ADDINGS.map{ |e| [e[0] + king[0], e[1] + king[1]] }.include? knight
end

def knight_vs_king(knight_position, king_position)
  knight = numeric_pos knight_position
  king   = numeric_pos king_position
  return 'King' if king_beats_knight?(king, knight)
  return 'Knight' if knight_beats_king?(knight, king)
  'None'
end
_______________________________________
def knight_vs_king(knight_position, king_position)
  y = y_distance(knight_position, king_position)
  x = x_distance(knight_position, king_position)

  winner(y, x)
end

def winner(y, x)
  if knight_wins(y, x)
    "Knight"
  elsif king_wins(y, x)
    "King"
  else
    "None"
  end
end

def y_distance(knight, king)
  (king[0].ord - knight[0].ord).abs
end

def x_distance(knight, king)
  (king[1].ord - knight[1].ord).abs
end

def knight_wins(y, x)
  (y==2 && x==1) || (y==1 && x==2)
end

def king_wins(y, x)
  (y==1 && x==1) || (x==1 && y==0) || (x==0 && y==1)
end
