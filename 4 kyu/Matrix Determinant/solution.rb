require 'matrix'  
def determinant(matrix)
  Matrix[*matrix].det
end
_____________________________________________
def determinant(matrix)
  return matrix.flatten[0] if matrix.count == 1
  matrix.shift.each_with_index.reduce(0) do |res, (val, idx)|
    mat = matrix.transpose
    mat.delete_at(idx)
    res + val * determinant(mat) * (-1)**idx
  end
end
_____________________________________________
require 'matrix'

def determinant(matrix)
  Matrix[*matrix].determinant  
end
_____________________________________________
require 'matrix'

def determinant(m)
  Matrix[*m].determinant
end
_____________________________________________
def determinant(matrix)
  return matrix[0][0] if matrix.size == 1
  matrix[0].map.with_index do |v, i|
    minor = matrix[1..-1].map {|a| a.reject.with_index {|v,j| j==i}}
    (i%2==0?1:-1) * v * determinant(minor)
  end.reduce(&:+)
end
