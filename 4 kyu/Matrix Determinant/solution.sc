object Matrix {
  
  def det2x2(matrix: Array[Array[Int]]): Int = {
    matrix(0)(0) * matrix(1)(1) - matrix(0)(1) * matrix(1)(0)
  }
  
  def getMinor(column: Int, matrix: Array[Array[Int]]): Array[Array[Int]] = {
    val rows = matrix.drop(1) // eliminate first row
    rows.map(x => x.zipWithIndex.filter(_._2 != column).map(_._1))
  }
  
  def sig(n: Int): Int = {
    if (n % 2 == 0) 1 else -1
  }
  
  def determinant(matrix: Array[Array[Int]]): Int = {
    
    matrix.size match {
      case 0 => throw new Exception("Empty matrix")
      case 1 => matrix(0)(0)
      case 2 => det2x2(matrix)
      case _ => (0 until matrix.size).map(
        c => sig(c) * matrix(0)(c) * determinant(getMinor(c, matrix))).sum
    }
    
  }
}
_____________________________________________
object Matrix {

  def determinant(matrix: Array[Array[Int]]): Int =
    matrix match {
      case Array(Array(a)) => a
      case _ =>
        matrix
          .head.zipWithIndex
          .map { case (x, i) => math.pow(-1, i).toInt * x * determinant(matrix.drop(1).map(_.patch(i, Nil, 1))) }
          .sum
    }
}
_____________________________________________
object Matrix {

  def dropRowColumn(row: Int, col: Int, array: Array[Array[Int]]): Array[Array[Int]] =
    (array.take(row) ++ array.drop(row + 1))
      .map(row => row.take(col) ++ row.drop(col + 1))

  def determinant(matrix: Array[Array[Int]]): Int = matrix.length match {
    case 1 => matrix(0)(0)
    case 2 => matrix(0)(0) * matrix(1)(1) - matrix(0)(1) * matrix(1)(0)
    case _ =>
      matrix.indices.map(
        i => (if (i % 2 == 0) 1 else -1) * matrix(0)(i) * determinant(dropRowColumn(0, i, matrix))
      ).sum
  }
}
_____________________________________________
object Matrix {

  def determinant(matrix: Array[Array[Int]]): Int = new Mat(matrix).det
  
  class Mat(data: Array[Array[Int]], rowIdx: Array[Int], colIdx: Array[Int]) {
    def this(data: Array[Array[Int]]) = this(data, Array.range(0, data.size), Array.range(0, data.size))
    def apply(row: Int, col: Int): Int = data(rowIdx(row))(colIdx(col))
    def size: Int = rowIdx.size
    def minor(row: Int, col: Int): Mat = new Mat(data, rowIdx.take(row) ++ rowIdx.drop(row+1), colIdx.take(col) ++ colIdx.drop(col+1))
    def det: Int = size match {
      case 1 => this(0, 0)
      case n => (0 until n).map(col => (if(col%2 == 0) 1 else -1) * this(0, col) * minor(0, col).det).sum
    }
  }
}
