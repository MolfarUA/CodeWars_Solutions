package kata

import (
  "fmt"
  "sort"
)

var (
  // key1:正向层数;key2:反向层数;value:数组
  clueListMap = map[int]map[int][][]int{}
)

const (
  N = 7
)

// 自定义规则节点(记录非0规则正向和反向层数以及索引)
type SelfClueNode struct {
  Index        int
  Forward, Rev int
}

/*
  更换思路:

  1、递归规则,直接填一列或一行,若没法填下一个规则,则返回上一个规则,当规则填完时,就返回
  2、规则填完后再填充为0的格子,若为0的格子不能正确填写,则继续返回1的递归中
*/

func init() {
  // 生成全排列列表
  data := make([]int, N)
  for i := 0; i < N; i++ {
    clueListMap[i+1] = make(map[int][][]int)
    data[i] = i + 1
  }
  result := PermutationConcurrency(data)

  for _, items := range result {
    // 统计正向反向数出的层数
    count := calcCount(items)
    reCount := calcCount(reverse(items))

    // 组装规则字符串字典
    clueListMap[count][reCount] = append(clueListMap[count][reCount], items)
    clueListMap[count][0] = append(clueListMap[count][0], items)
  }
}

func SolvePuzzle(clues []int) [][]int {
  result := make([][]int, N)
  for i := 0; i < N; i++ {
    result[i] = make([]int, N)
  }

  selfClueNodeList := make([]*SelfClueNode, 0)
  existMap := make(map[int]interface{})
  for i := 0; i < len(clues); i++ {
    if clues[i] == 0 {
      continue
    }

    // 组装有限制的规则列表
    if i < N {
      selfClueNodeList = append(selfClueNodeList, &SelfClueNode{i, clues[i], clues[3*N-1-i]})

      if clues[3*N-1-i] != 0 {
        existMap[3*N-1-i] = struct{}{}
      }
    } else if i < 2*N {
      selfClueNodeList = append(selfClueNodeList, &SelfClueNode{i, clues[i], clues[5*N-1-i]})

      if clues[5*N-1-i] != 0 {
        existMap[5*N-1-i] = struct{}{}
      }
    } else {
      // 需要去掉已经在双向列表中的规则
      if _, exists := existMap[i]; exists {
        continue
      }

      selfClueNodeList = append(selfClueNodeList, &SelfClueNode{i, clues[i], 0})
    }
  }

  sort.Slice(selfClueNodeList, func(i, j int) bool {
    // 排序规则
    // 1、forward和rev都不为0的排前面
    // 2、两个clue中forward, rev最大的排前面
    maxNum := 0
    if selfClueNodeList[j].Forward > maxNum {
      maxNum = selfClueNodeList[j].Forward
    }

    if selfClueNodeList[j].Rev > maxNum {
      maxNum = selfClueNodeList[j].Rev
    }

    if selfClueNodeList[i].Rev == 0 && selfClueNodeList[j].Rev != 0 {
      return false
    }

    if selfClueNodeList[j].Rev == 0 && selfClueNodeList[i].Rev != 0 {
      return true
    }

    return selfClueNodeList[i].Forward > maxNum || selfClueNodeList[i].Rev > maxNum
  })

  clueIndexList := make([]int, len(selfClueNodeList))
  if dfs(0, result, selfClueNodeList, clueIndexList) == false {
    fmt.Println("failed!")
  }

  return result
}

func dfs(level int, result [][]int, cluesList []*SelfClueNode, clueIndexList []int) bool {
  if level > len(cluesList)-1 {
    // 规则填完后,还需要校验为0的格子

    // 统计结果中为0的格子
    zeroNodeList := make([][2]int, 0)
    for i := 0; i < N; i++ {
      for j := 0; j < N; j++ {
        if result[i][j] == 0 {
          zeroNodeList = append(zeroNodeList, [2]int{i, j})
        }
      }
    }

    if len(zeroNodeList) == 0 {
      return true
    }

    return dfs1(0, result, zeroNodeList)
  }

  clues := cluesList[level]
  cluesNodeList := clueListMap[clues.Forward][clues.Rev]
  var isRow bool
  var curIndex int
  var ifReverse bool
  nowData := make([]int, N)

  if clues.Index < N {
    // 从上到下,列
    ifReverse = false
    isRow = false
    curIndex = clues.Index
    for i := 0; i < N; i++ {
      nowData[i] = result[i][curIndex]
    }
  } else if clues.Index < 2*N {
    // 反向,行,需要将数据倒转然后从左到右
    ifReverse = true
    isRow = true
    curIndex = clues.Index - N
    for j := 0; j < N; j++ {
      nowData[j] = result[curIndex][j]
    }
  } else if clues.Index < 3*N {
    // 反向,列,需要将数据倒转然后从上到下
    ifReverse = true
    isRow = false
    curIndex = 3*N - 1 - clues.Index
    for i := 0; i < N; i++ {
      nowData[i] = result[i][curIndex]
    }
  } else {
    // 从左到右,行
    ifReverse = false
    isRow = true
    curIndex = 4*N - 1 - clues.Index
    for j := 0; j < N; j++ {
      nowData[j] = result[curIndex][j]
    }
  }

  for cluesListIndex := clueIndexList[level]; cluesListIndex < len(cluesNodeList); cluesListIndex++ {
    data := cluesNodeList[cluesListIndex]
    if ifReverse {
      data = reverse(data)
    }
    if isMatch(data, nowData, result, isRow, curIndex) {
      clueIndexList[level] = cluesListIndex + 1
      fillData(result, data, curIndex, isRow)
      if dfs(level+1, result, cluesList, clueIndexList) {
        return true
      }
      clueIndexList[level] = 0
      fillData(result, nowData, curIndex, isRow)
    }
  }

  return false
}

func dfs1(level int, result [][]int, zeroNodeList [][2]int) bool {
  if level > len(zeroNodeList)-1 {
    return true
  }

  i, j := zeroNodeList[level][0], zeroNodeList[level][1]
  for num := 1; num <= N; num++ {
    if isValid(result, i, j, num) {
      result[i][j] = num
      if dfs1(level+1, result, zeroNodeList) {
        return true
      }
      result[i][j] = 0
    }
  }

  return false
}

// 校验行列是否重复
func isValid(result [][]int, i, j, num int) bool {
  for k := 0; k < N; k++ {
    if k != j && result[i][k] != 0 && result[i][k] == num {
      return false
    }
  }
  for k := 0; k < N; k++ {
    if k != i && result[k][j] != 0 && result[k][j] == num {
      return false
    }
  }

  return true
}

// 填充数据
func fillData(result [][]int, data []int, index int, isRow bool) {
  if isRow {
    for j := 0; j < N; j++ {
      result[index][j] = data[j]
    }
  } else {
    for i := 0; i < N; i++ {
      result[i][index] = data[i]
    }
  }
}

func reverse(data []int) []int {
  result := make([]int, len(data))
  copy(result, data)

  for i, j := 0, len(result)-1; i < j; i, j = i+1, j-1 {
    result[i], result[j] = result[j], result[i]
  }

  return result
}

func calcCount(data []int) int {
  max, count := data[0], 1
  for _, cur := range data[1:] {
    if cur > max {
      count++
      max = cur
    }
  }

  return count
}

func isMatch(data []int, existsNum []int, result [][]int, isRow bool, index int) bool {
  for i := 0; i < N; i++ {
    if existsNum[i] == 0 {
      continue
    }

    if existsNum[i] != data[i] {
      return false
    }
  }

  if isRow {
    // 行需要判断每一列是否有重复
    for j := 0; j < N; j++ {
      if existsNum[j] != 0 {
        continue
      }

      for i := 0; i < N; i++ {
        if i == index {
          continue
        }

        if result[i][j] != 0 && result[i][j] == data[j] {
          return false
        }
      }
    }
  } else {
    // 列需要判断每一行是否有重复
    for i := 0; i < N; i++ {
      if existsNum[i] != 0 {
        continue
      }

      for j := 0; j < N; j++ {
        if j == index {
          continue
        }

        if result[i][j] != 0 && result[i][j] == data[i] {
          return false
        }
      }
    }
  }

  return true
}

func prefixIncrement(in []int, s []int, next chan []int) {
  for _, c := range s {
    exist := false
    for _, e := range in {
      if e == c {
        exist = true
        break
      }
    }
    if exist {
      continue
    }

    temp := make([]int, 0)
    temp = append(temp, in...)
    temp = append(temp, c)
    next <- temp
  }
}

func permutaionConImpl(req chan []int, out chan []int, s []int) {
  go func() {
    //递归退出条件: len(v) == len(s)-1
    v, ok := <-req
    if !ok {
      return
    }

    next := out
    if len(v) != len(s)-1 {
      next = make(chan []int)
      permutaionConImpl(next, out, s)
    }

    prefixIncrement(v, s, next)
    for in := range req {
      prefixIncrement(in, s, next)
    }
    close(next)
  }()
}

// PermutationConcurrency  并发计算全排列
func PermutationConcurrency(s []int) [][]int {
  req, out := make(chan []int), make(chan []int)

  //开启goroutine计算
  permutaionConImpl(req, out, s)

  over := make(chan [][]int)

  //要开goroutine读取out，如果放在主函数中，会导致死锁。
  go func() {
    result := make([][]int, 0)

    for res := range out {
      result = append(result, res)
    }

    over <- result
  }()

  for _, c := range s {
    sl := []int{c}
    req <- sl
  }
  close(req)

  return <-over
}
___________________________________________________________
package kata








import (
  "fmt"
  "time"
  //"github.com/pkg/profile"
)

func main() {
  //defer profile.Start().Stop()

  clues := []int{0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3}
  fmt.Println(SolvePuzzle(clues))

  clues = []int{6, 4, 0, 2, 0, 0, 3, 0, 3, 3, 3, 0, 0, 4, 0, 5, 0, 5, 0, 2, 0, 0, 0, 0, 4, 0, 0, 3}
  fmt.Println(SolvePuzzle(clues))

  clues = []int{0, 0, 0, 5, 0, 0, 3, 0, 6, 3, 4, 0, 0, 0, 3, 0, 0, 0, 2, 4, 0, 2, 6, 2, 2, 2, 0, 0}
  fmt.Println(SolvePuzzle(clues))

  clues = []int{0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1}
  fmt.Println(SolvePuzzle(clues))

  clues7 := []int{7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4}
  fmt.Println(SolvePuzzle(clues7))

  //fmt.Println(SolvePuzzle(clues))
}

const SIZE = 7
const FACTORIAL = 5040

var INITIAL = []uint16{1, 2, 3, 4, 5, 6, 7}

var permutations [FACTORIAL][SIZE]uint16 = sortedPermutations(INITIAL)
var leftVizibility, rightVizibility [FACTORIAL]uint16 = computeVizibility(permutations)

var possibleLines = &[SIZE][FACTORIAL]bool{}
var possibleColumns = &[SIZE][FACTORIAL]bool{}

func SolvePuzzle(clues []int) [][]int {
  start := time.Now()

  //fmt.Println(clues)
  //permutations = sortedPermutations(INITIAL)
  //leftVizibility, rightVizibility = computeVizibility(permutations)

  updatePossibleLines(clues, possibleLines, possibleColumns)
  updatePossibleColumns(clues, possibleLines, possibleColumns)

  updateLinesBasedOnColumns(clues, possibleLines, possibleColumns)
  updateColumnsBasedOnLines(clues, possibleLines, possibleColumns)

  //printPossible(possibleLines, possibleColumns)

  possibleLinesShort, possibleColumnsShort := computeShort(possibleLines, possibleColumns)
  validLinesCount, validColsCount := validCOunts(possibleLinesShort, possibleColumnsShort)

  //printPossible(possibleLinesShort, possibleColumnsShort)
  ColumnOrder = columnOrder(validColsCount)
  fmt.Println("ColumnOrder", ColumnOrder)

  solution, found := computeSolution(&[]uint16{}, possibleLinesShort, possibleColumnsShort, validLinesCount, validColsCount)

  elapsed := time.Since(start)
  fmt.Println("elapsed", elapsed)
  //fmt.Println("count", count)

  if found {
    return convertSolutionToMatrix(solution)
  }

  return nil

}

var ColumnOrder [SIZE]int

// TODO: find a order for columns: least possib to highest
func columnOrder(possibleColumnsShortCount *[SIZE]int) [SIZE]int {
  //fmt.Println("possibleColumnsShortCount", possibleColumnsShortCount)
  clone := [SIZE]int{}
  for i := 0; i < SIZE; i++ {
    clone[i] = possibleColumnsShortCount[i]
  }
  //fmt.Println("clone", clone)

  result := [SIZE]int{}

  for index := 0; index < SIZE; index++ {
    min, val := -1, 9999
    for i := 0; i < SIZE; i++ {
      if clone[i] < val {
        min = i
        val = possibleColumnsShortCount[i]
      }
    }

    clone[min] = 9999
    result[index] = min
  }

  return result
}

func validCOunts(l, c [][]uint16) (*[SIZE]int, *[SIZE]int) {
  countL, countC := [SIZE]int{}, [SIZE]int{}

  for i := 0; i < SIZE; i++ {
    countL[i] = len(l[i])
    countC[i] = len(c[i])
  }

  return &countL, &countC
}

// EMPTY is larger than the max possbile poermutation of 7! = 5040
const EMPTY = uint16(6000)

func computeSolution(columnsSoFar *[]uint16, possibleLines, possibleColumns [][]uint16, validLinesCount, validColsCount *[SIZE]int) (*[]uint16, bool) {
  if len(*columnsSoFar) == SIZE {
    //fmt.Println("len(*columnsSoFar)", len(*columnsSoFar))

    return columnsSoFar, true
  }

  // ColumnOrder[columnIndex] == actual column
  for i := 0; i < len(possibleColumns[ColumnOrder[len(*columnsSoFar)]]); i++ {
    if possibleColumns[ColumnOrder[len(*columnsSoFar)]][i] != EMPTY {
      val := possibleColumns[ColumnOrder[len(*columnsSoFar)]][i]

      *columnsSoFar = append(*columnsSoFar, val)

      validLinesCountFiltered, validColsCountFiltered := copyValidCounts(validLinesCount, validColsCount)
      filteredPossibleLines, filteredPossibleColumns := copyLinesAndColumns(possibleLines, possibleColumns, validLinesCountFiltered, validColsCountFiltered)
      isEmpty := eliminateColumn(len(*columnsSoFar)-1, val, filteredPossibleLines, filteredPossibleColumns, validLinesCountFiltered, validColsCountFiltered)
      if isEmpty {
        *columnsSoFar = (*columnsSoFar)[:len(*columnsSoFar)-1]
        continue
        //  return columnsSoFar, false
      }

      computeSolution(columnsSoFar, filteredPossibleLines, filteredPossibleColumns, validLinesCountFiltered, validColsCountFiltered)

      if len(*columnsSoFar) >= SIZE {
        return columnsSoFar, true
      }

      *columnsSoFar = (*columnsSoFar)[:len(*columnsSoFar)-1]
    }
  }

  return columnsSoFar, false
}

func copyValidCounts(validLinesCount, validColsCount *[SIZE]int) (*[SIZE]int, *[SIZE]int) {
  l, c := &[SIZE]int{}, &[SIZE]int{}

  for i := 0; i < SIZE; i++ {
    l[i] = validLinesCount[i]
    c[i] = validColsCount[i]
  }

  return l, c
}

func eliminateColumn(columnIndex int, perm uint16, filteredPossibleLines, filteredPossibleColumns [][]uint16, validLinesCountFiltered, validColsCountFiltered *[SIZE]int) bool {
  //fmt.Println("before", columnIndex)
  //printPossible(filteredPossibleLines, filteredPossibleColumns)

  result := false

  for i := 0; i < SIZE; i++ {
    emptyLines := removeLinesNotStarting(permutations[perm][i], filteredPossibleLines, i, columnIndex, validLinesCountFiltered)
    if emptyLines {
      result = true
    }
  }

  emptyCols := removesColumnsMimicking(permutations[perm], filteredPossibleColumns, columnIndex, validColsCountFiltered)
  if emptyCols {
    result = true
  }

  //fmt.Println("after", columnIndex, permutations[perm])
  //printPossible(filteredPossibleLines, filteredPossibleColumns)

  return result
}

// ColumnOrder[columnIndex] == actual column
func removesColumnsMimicking(val [SIZE]uint16, columns [][]uint16, columnIndex int, validColsCOunt *[SIZE]int) bool {
  result := false

  for col := 0; col < SIZE; col++ {
    if col != ColumnOrder[columnIndex] {
      empty := true

      for i := 0; i < len(columns[col]); i++ {
        // columns[col][i] != EMPTY <=> columns[col][i] is a valid perm for columns[col]
        if columns[col][i] != EMPTY {
          if permutations[columns[col][i]][0] == val[0] ||
            permutations[columns[col][i]][1] == val[1] ||
            permutations[columns[col][i]][2] == val[2] ||
            permutations[columns[col][i]][3] == val[3] ||
            permutations[columns[col][i]][4] == val[4] ||
            permutations[columns[col][i]][5] == val[5] ||
            permutations[columns[col][i]][6] == val[6] {
            columns[col][i] = EMPTY
            validColsCOunt[col]--
          } else {
            empty = false
          }
        }
      }

      if empty {
        result = true
      }
    }
  }

  return result
}

func removeLinesNotStarting(val uint16, lines [][]uint16, lineIndex, columnIndex int, validLinesCOunt *[SIZE]int) bool {
  empty := true

  for i := 0; i < len(lines[lineIndex]); i++ {
    if lines[lineIndex][i] != EMPTY {
      if permutations[lines[lineIndex][i]][ColumnOrder[columnIndex]] != val {
        lines[lineIndex][i] = EMPTY
        validLinesCOunt[lineIndex]--
      } else {
        empty = false
      }
    }
  }

  return empty
}

func computeShort(lines, cols *[SIZE][FACTORIAL]bool) ([][]uint16, [][]uint16) {
  linesShort := make([][]uint16, SIZE)
  for l := 0; l < SIZE; l++ {
    linesShort[l] = make([]uint16, countTrueBool(lines[l]))

    index := 0
    for i := uint16(0); i < uint16(FACTORIAL); i++ {
      if lines[l][i] {
        linesShort[l][index] = i

        index++
      }
    }
  }

  colsShort := make([][]uint16, SIZE)
  for c := 0; c < SIZE; c++ {
    colsShort[c] = make([]uint16, countTrueBool(cols[c]))

    index := 0
    for i := uint16(0); i < uint16(FACTORIAL); i++ {
      if cols[c][i] {
        colsShort[c][index] = i

        index++
      }
    }
  }

  return linesShort, colsShort
}

func printPossible(possibleLines, possibleColumns [][]uint16) {
  for i := 0; i < len(possibleLines); i++ {
    fmt.Println("column:", i, countTrue(possibleColumns[i]))
  }

  for i := 0; i < len(possibleLines); i++ {
    fmt.Println("line:", i, countTrue(possibleLines[i]))
  }
}

func copyLinesAndColumns(possibleLines, possibleColumns [][]uint16, validLinesCount, validColsCount *[SIZE]int) ([][]uint16, [][]uint16) {
  filteredLines := make([][]uint16, SIZE)

  for i := 0; i < SIZE; i++ {
    filteredLines[i] = make([]uint16, validLinesCount[i])

    index := 0
    for j := 0; j < len(possibleLines[i]); j++ {
      if possibleLines[i][j] != EMPTY {
        filteredLines[i][index] = possibleLines[i][j]
        index++
      }
    }
  }

  filteredColumns := make([][]uint16, SIZE)
  for i := 0; i < SIZE; i++ {
    filteredColumns[i] = make([]uint16, validColsCount[i])

    index := 0
    for j := 0; j < len(possibleColumns[i]); j++ {
      if possibleColumns[i][j] != EMPTY {
        filteredColumns[i][index] = possibleColumns[i][j]
        index++
      }
    }
  }

  return filteredLines, filteredColumns
}

func countValid(in []uint16) int {
  result := 0

  for i := 0; i < len(in); i++ {
    if in[i] != EMPTY {
      result++
    }
  }

  return result
}

func initializePossibleShortArray(in [][]uint16) [][]uint16 {
  result := make([][]uint16, len(in))

  for i := 0; i < SIZE; i++ {
    result[i] = make([]uint16, len(in[i]))
  }

  return result
}

func computeLeft(input [SIZE]uint16) uint16 {
  result, current := uint16(0), uint16(0)

  for i := 0; i < len(input); i++ {
    if input[i] > current {
      current = input[i]

      result++
    }
  }

  return result
}

func computeRight(input [SIZE]uint16) uint16 {
  result, current := uint16(0), uint16(0)

  for i := len(input) - 1; i >= 0; i-- {
    if input[i] > current {
      current = input[i]

      result++
    }
  }

  return result
}

func sortedPermutations(input []uint16) [FACTORIAL][SIZE]uint16 {
  result := [FACTORIAL][SIZE]uint16{}
  index := 0
  isFinished := false

  for !isFinished {
    result[index] = clone(input)
    index++

    i := 0
    for i = len(input) - 2; i >= 0; i-- {
      if input[i] < input[i+1] {
        break
      }
    }

    if i == -1 {
      isFinished = true
      break
    }

    //ceilIndex := findCeil(input, input[i], uint16(i))
    ceilIndex, ceil := i+1, input[i+1]

    for k := i + 1; k < len(input); k++ {
      if input[k] > input[i] && input[k] < ceil {
        ceil = input[k]

        ceilIndex = k
      }
    }

    input[i], input[ceilIndex] = input[ceilIndex], input[i]

    //reverseRightOf(input, i)
    for a, b := i+1, len(input)-1; a < b; a, b = a+1, b-1 {
      input[a], input[b] = input[b], input[a]
    }
  }

  return result
}

func clone(input []uint16) [SIZE]uint16 {
  result := [SIZE]uint16{}

  for i := 0; i < SIZE; i++ {
    result[i] = input[i]
  }

  return result
}

func computeVizibility(permutations [FACTORIAL][SIZE]uint16) ([FACTORIAL]uint16, [FACTORIAL]uint16) {
  left := [FACTORIAL]uint16{}
  right := [FACTORIAL]uint16{}

  for i := 0; i < len(permutations); i++ {
    left[i] = computeLeft(permutations[i])
    right[i] = computeRight(permutations[i])
  }

  return left, right
}

// solution[i] --> ColumnOrder[solution[i]]
func convertSolutionToMatrix(solution *[]uint16) [][]int {
  result := make([][]int, SIZE)
  for i := 0; i < SIZE; i++ {
    result[i] = make([]int, SIZE)
  }

  for col := 0; col < SIZE; col++ {
    for line := 0; line < SIZE; line++ {
      result[line][ColumnOrder[col]] = int(permutations[(*solution)[col]][line])
    }
  }

  return result
}

func countTrueBool(in [FACTORIAL]bool) int {
  result := 0

  for i := 0; i < len(in); i++ {
    if in[i] {
      result++
    }
  }

  return result
}

func countTrue(in []uint16) int {
  result := 0

  for i := 0; i < len(in); i++ {
    if in[i] != EMPTY {
      result++
    }
  }

  return result
}

func updatePossibleColumns(clues []int, possibleLines, possibleColumns *[SIZE][FACTORIAL]bool) {
  for i := 0; i < SIZE; i++ { // cols
    top := uint16(clues[i])
    bottom := uint16(clues[SIZE+SIZE+SIZE-1-i])

    for p := 0; p < FACTORIAL; p++ {
      possibleColumns[i][p] = (top == 0 || leftVizibility[p] == top) && (bottom == 0 || rightVizibility[p] == bottom)

      //if (top == 0 || leftVizibility[p] == top) && (bottom == 0 || rightVizibility[p] == bottom) {
      //  possibleColumns[i][p] = true
      //}
    }
  }
}

func updateColumnsBasedOnLines(clues []int, possibleLines, possibleColumns *[SIZE][FACTORIAL]bool) {
  for index := 0; index < SIZE; index++ { // lines
    for i := 0; i < FACTORIAL; i++ {
      if possibleColumns[0][i] && permutations[i][index] > uint16(SIZE-clues[len(clues)-1-index]+1) {
        possibleColumns[0][i] = false
      }
    }

    for i := 0; i < FACTORIAL; i++ {
      if possibleColumns[SIZE-1][i] && permutations[i][index] > uint16(SIZE-clues[index+SIZE]+1) {
        possibleColumns[SIZE-1][i] = false
      }
    }

  }
}

func filterColumn(columnNumber int, line int, left int, possibleLines, possibleColumns [SIZE][FACTORIAL]bool) {
  for i := 0; i < FACTORIAL; i++ {
    if possibleColumns[columnNumber][i] && permutations[i][line] > uint16(SIZE-left+1) {
      possibleColumns[columnNumber][i] = false
    }
  }
}

func updateLinesBasedOnColumns(clues []int, possibleLines, possibleColumns *[SIZE][FACTORIAL]bool) {
  for col := 0; col < SIZE; col++ { // cols
    for i := 0; i < FACTORIAL; i++ {
      if possibleLines[0][i] && permutations[i][col] > uint16(SIZE-clues[col]+1) {
        possibleLines[0][i] = false
      }
    }

    for i := 0; i < FACTORIAL; i++ {
      if possibleLines[SIZE-1][i] && permutations[i][col] > uint16(SIZE-clues[SIZE+SIZE+SIZE-1-col]+1) {
        possibleLines[SIZE-1][i] = false
      }
    }
  }
}

func updatePossibleLines(clues []int, possibleLines, possibleColumns *[SIZE][FACTORIAL]bool) {
  for i := 0; i < SIZE; i++ { // lines
    left := uint16(clues[len(clues)-1-i])
    right := uint16(clues[i+SIZE])

    for p := 0; p < FACTORIAL; p++ {
      possibleLines[i][p] = (left == 0 || leftVizibility[p] == left) && (right == 0 || rightVizibility[p] == right)
    }
  }
}
________________________________________________
package kata

//
// Sketch:
//
// Start with a grid of the options to build a skyscraper on a field.
// The clues reduces the options for skysrapers on a field.
// Start a trial & error backtrack algorithm
// - The rule for one height per row and column could reduces the options on a field.
// - The clue could reduced the options if some fields in the row/column are reduced.
//
// Optimize the runtime by pre-calculated lookup tables.
// Invest in source code size and memory size to reduce runtime.
//
// No multi-core/-thread optimization. Code uses one thread only.
//

import "fmt"

// ----------------------- Constants and Types ----------------------

// Options for a skyscraper.
// One bit as opton for skyscraper.
type skyscraperOptions int16

const (
  rowSize             int               = 7
  maxClue             int               = rowSize
  gridSize            int               = rowSize * rowSize
  skyscraperOption1   skyscraperOptions = 1
  skyscraperOption2   skyscraperOptions = 2
  skyscraperOption3   skyscraperOptions = 4
  skyscraperOption4   skyscraperOptions = 8
  skyscraperOption5   skyscraperOptions = 16
  skyscraperOption6   skyscraperOptions = 32
  skyscraperOption7   skyscraperOptions = 64
  skyscraperOptionAll skyscraperOptions = 1 + 2 + 4 + 8 + 16 + 32 + 64
)

// A row of fields with options for skyscrapers.
type skyscraperRow [rowSize]skyscraperOptions

// One dimension array to store all fields of the grid.
// Store row 1, row 2, .. row 4.
type skyscraperGrid [gridSize]skyscraperOptions

// Number of options for skyscrapters on a field.
// Index: options
// Value: Number of options = number of bits.
// The vales were generated before final source code version by function
// printOptions2count.
var options2count = [128]int8{0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2,
  3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3,
  2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4,
  5, 4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3,
  3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3,
  4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7}

// The highest option of an option set.
// Index is the combination of options.
// Value is the highest option in the combination.
// The values were generated before final source code version by function
// printHiLoOption
var highestOption = [128]skyscraperOptions{0, 1, 2, 2, 4, 4, 4,
  4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
  32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
  32, 32, 32, 32, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
  64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
  64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
  64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64}

// The lowest option of an option set.
// Index is the combination of options.
// Value is the lowest option in the combination.
// The values were generated before final source code version by function
// printHiLoOption
var lowestOption = [128]skyscraperOptions{0, 1, 2, 1, 4, 1, 2, 1,
  8, 1, 2, 1, 4, 1, 2, 1, 16, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2,
  1, 32, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16, 1, 2, 1, 4,
  1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 64, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1,
  4, 1, 2, 1, 16, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 32, 1,
  2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16, 1, 2, 1, 4, 1, 2, 1, 8,
  1, 2, 1, 4, 1, 2, 1}

// Map from cell to all other cells in same row and column.
// Index is the index of a cell in the grid.
// Value is an array with index to all cells in the row and the column.
// The vales were generated before final source code version by function
// printCell2neighbors
var cell2neighbors = [49][12]int{
  {1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42},
  {0, 2, 3, 4, 5, 6, 8, 15, 22, 29, 36, 43},
  {0, 1, 3, 4, 5, 6, 9, 16, 23, 30, 37, 44},
  {0, 1, 2, 4, 5, 6, 10, 17, 24, 31, 38, 45},
  {0, 1, 2, 3, 5, 6, 11, 18, 25, 32, 39, 46},
  {0, 1, 2, 3, 4, 6, 12, 19, 26, 33, 40, 47},
  {0, 1, 2, 3, 4, 5, 13, 20, 27, 34, 41, 48},
  {8, 9, 10, 11, 12, 13, 0, 14, 21, 28, 35, 42},
  {7, 9, 10, 11, 12, 13, 1, 15, 22, 29, 36, 43},
  {7, 8, 10, 11, 12, 13, 2, 16, 23, 30, 37, 44},
  {7, 8, 9, 11, 12, 13, 3, 17, 24, 31, 38, 45},
  {7, 8, 9, 10, 12, 13, 4, 18, 25, 32, 39, 46},
  {7, 8, 9, 10, 11, 13, 5, 19, 26, 33, 40, 47},
  {7, 8, 9, 10, 11, 12, 6, 20, 27, 34, 41, 48},
  {15, 16, 17, 18, 19, 20, 0, 7, 21, 28, 35, 42},
  {14, 16, 17, 18, 19, 20, 1, 8, 22, 29, 36, 43},
  {14, 15, 17, 18, 19, 20, 2, 9, 23, 30, 37, 44},
  {14, 15, 16, 18, 19, 20, 3, 10, 24, 31, 38, 45},
  {14, 15, 16, 17, 19, 20, 4, 11, 25, 32, 39, 46},
  {14, 15, 16, 17, 18, 20, 5, 12, 26, 33, 40, 47},
  {14, 15, 16, 17, 18, 19, 6, 13, 27, 34, 41, 48},
  {22, 23, 24, 25, 26, 27, 0, 7, 14, 28, 35, 42},
  {21, 23, 24, 25, 26, 27, 1, 8, 15, 29, 36, 43},
  {21, 22, 24, 25, 26, 27, 2, 9, 16, 30, 37, 44},
  {21, 22, 23, 25, 26, 27, 3, 10, 17, 31, 38, 45},
  {21, 22, 23, 24, 26, 27, 4, 11, 18, 32, 39, 46},
  {21, 22, 23, 24, 25, 27, 5, 12, 19, 33, 40, 47},
  {21, 22, 23, 24, 25, 26, 6, 13, 20, 34, 41, 48},
  {29, 30, 31, 32, 33, 34, 0, 7, 14, 21, 35, 42},
  {28, 30, 31, 32, 33, 34, 1, 8, 15, 22, 36, 43},
  {28, 29, 31, 32, 33, 34, 2, 9, 16, 23, 37, 44},
  {28, 29, 30, 32, 33, 34, 3, 10, 17, 24, 38, 45},
  {28, 29, 30, 31, 33, 34, 4, 11, 18, 25, 39, 46},
  {28, 29, 30, 31, 32, 34, 5, 12, 19, 26, 40, 47},
  {28, 29, 30, 31, 32, 33, 6, 13, 20, 27, 41, 48},
  {36, 37, 38, 39, 40, 41, 0, 7, 14, 21, 28, 42},
  {35, 37, 38, 39, 40, 41, 1, 8, 15, 22, 29, 43},
  {35, 36, 38, 39, 40, 41, 2, 9, 16, 23, 30, 44},
  {35, 36, 37, 39, 40, 41, 3, 10, 17, 24, 31, 45},
  {35, 36, 37, 38, 40, 41, 4, 11, 18, 25, 32, 46},
  {35, 36, 37, 38, 39, 41, 5, 12, 19, 26, 33, 47},
  {35, 36, 37, 38, 39, 40, 6, 13, 20, 27, 34, 48},
  {43, 44, 45, 46, 47, 48, 0, 7, 14, 21, 28, 35},
  {42, 44, 45, 46, 47, 48, 1, 8, 15, 22, 29, 36},
  {42, 43, 45, 46, 47, 48, 2, 9, 16, 23, 30, 37},
  {42, 43, 44, 46, 47, 48, 3, 10, 17, 24, 31, 38},
  {42, 43, 44, 45, 47, 48, 4, 11, 18, 25, 32, 39},
  {42, 43, 44, 45, 46, 48, 5, 12, 19, 26, 33, 40},
  {42, 43, 44, 45, 46, 47, 6, 13, 20, 27, 34, 41}}

// Options for a given clue
// The vales were generated before final source code version by function
// printClue2row
var clue2row = [8]skyscraperRow{
  {127, 127, 127, 127, 127, 127, 127},
  {64, 63, 63, 63, 63, 63, 63},
  {63, 95, 127, 127, 127, 127, 127},
  {31, 63, 127, 127, 127, 127, 127},
  {15, 31, 63, 127, 127, 127, 127},
  {7, 15, 31, 63, 127, 127, 127},
  {3, 7, 15, 31, 63, 127, 127},
  {1, 2, 4, 8, 16, 32, 64}}

// Information to use the clue
type clueInfo struct {
  offset    int // Offset in skyscraperGrid
  increment int // increment in the grid
}

// Start index and index increment of the clues.
// Index in the clue array is the index in this table.
// Value is the start index and index increment in the skyscraperGrid.
// The vales were generated before final source code version by function
// printClueIndex2info
var clueIndex2info = [28]clueInfo{
  {offset: 0, increment: 7},
  {offset: 1, increment: 7},
  {offset: 2, increment: 7},
  {offset: 3, increment: 7},
  {offset: 4, increment: 7},
  {offset: 5, increment: 7},
  {offset: 6, increment: 7},
  {offset: 6, increment: -1},
  {offset: 13, increment: -1},
  {offset: 20, increment: -1},
  {offset: 27, increment: -1},
  {offset: 34, increment: -1},
  {offset: 41, increment: -1},
  {offset: 48, increment: -1},
  {offset: 48, increment: -7},
  {offset: 47, increment: -7},
  {offset: 46, increment: -7},
  {offset: 45, increment: -7},
  {offset: 44, increment: -7},
  {offset: 43, increment: -7},
  {offset: 42, increment: -7},
  {offset: 42, increment: 1},
  {offset: 35, increment: 1},
  {offset: 28, increment: 1},
  {offset: 21, increment: 1},
  {offset: 14, increment: 1},
  {offset: 7, increment: 1},
  {offset: 0, increment: 1}}

// Status of the grid during the trial & error backtrack algorithm.
type gridStatus int8

const (
  statusSolvable gridStatus = iota
  statusSolved   gridStatus = iota
  statusFaulty   gridStatus = iota
)

// ----------------------- Source code generators -------------------

// Number of 1 bits.
// Only for not-negative numbers.
func ones(x int) int {
  var counter int = 0
  for x > 0 {
    counter += x & 1
    x >>= 1
  }
  return counter
}

// Generate and print the table options to option-count.
// Output is used to initize options2count.
func printOptions2count() {
  var options2count [skyscraperOptionAll + 1]int8
  for i := range options2count {
    // Each option is a 1 bit
    options2count[i] = int8(ones(i))
  }
  fmt.Printf("options2count = %#v\n", options2count)
}

// Generate and print the tables highestOption and lowestOption.
// Generate table of highest skyscraper in an option set and
// table of lowest skyscraper in an option set.
func printHiLoOption() {
  var highestOption [skyscraperOptionAll + 1]skyscraperOptions
  var lowestOption [skyscraperOptionAll + 1]skyscraperOptions
  h := skyscraperOption1
  for optionSet := skyscraperOption1; optionSet <= skyscraperOptionAll; optionSet++ {
    l := skyscraperOptionAll
    for opt := skyscraperOption1; opt < skyscraperOptionAll; opt <<= 1 {
      if opt&optionSet > 0 {
        if h < opt {
          h = opt
        }
        if l > opt {
          l = opt
        }
      }
    }
    highestOption[optionSet] = h
    lowestOption[optionSet] = l
  }
  fmt.Printf("highestOption = %#v\n", highestOption)
  fmt.Printf("lowestOption = %#v\n", lowestOption)
}

// Calculate the clue of a row.
// The clue value is the number of visible skyscrapers in the row.
func clue(row skyscraperRow) int8 {
  var sum int8 = 0
  var max skyscraperOptions = 0
  for _, v := range row {
    if v > max {
      sum++
      max = v
    }
  }
  return sum
}

// Generate and print the table clue to skyscraper options row.
// A most clue values can be realized by several skyscraper rows.
// The function calculates the options for skyscraper in the cells
// for each clue value.
// Output is used to initize clue2row.
func printClue2row() {
  var clue2row [maxClue + 1]skyscraperRow
  // Generate all permutations and calculate the clue for each
  // possible row of skyscrapers.
  var row skyscraperRow
  for i := range row {
    row[i] = 1 << uint(i)
  }
  var permutate func(dst int)
  permutate = func(dst int) {
    if dst > rowSize {
      // row is one permutation.
      // Calculates the clue value for this permutation.
      c := clue(row)
      // include the permutation in the table
      for index := 0; index < rowSize; index++ {
        clue2row[c][index] |= row[index]
      }
      return
    }
    permutate(dst + 1)
    for src := dst + 1; src < rowSize; src++ {
      row[dst], row[src] = row[src], row[dst]
      permutate(dst + 1)
      row[dst], row[src] = row[src], row[dst]
    }
  }
  permutate(0)
  // Special case: clue 0 gives no information.
  // All skyscrapers in each cell is possible.
  for i := 0; i < rowSize; i++ {
    clue2row[0][i] = skyscraperOptionAll
  }
  fmt.Printf("clue2row = %#v\n", clue2row)
}

// Generate and print the table from clue index to clue info struct.
// The clue info contains the info needed to use the clue value.
// The info struct contains the index of the first cell in the grid
// and the increment to the next index.
func printClueIndex2info() {
  var clueIndex2info [4 * rowSize]clueInfo
  dst := 0
  gridIndex := 0
  // The clue values are given around the grid.
  // 1) row above the grid
  for i := 0; i < rowSize; i++ {
    clueIndex2info[dst].offset = gridIndex
    gridIndex++
    clueIndex2info[dst].increment = +rowSize
    dst++
  }
  // 2) column right of the grid
  // Same first field in the grid
  gridIndex--
  for i := 0; i < rowSize; i++ {
    clueIndex2info[dst].offset = gridIndex
    gridIndex += rowSize
    clueIndex2info[dst].increment = -1
    dst++
  }
  // 3) row below the grid
  // Same first field in the grid
  gridIndex -= rowSize
  for i := 0; i < rowSize; i++ {
    clueIndex2info[dst].offset = gridIndex
    gridIndex--
    clueIndex2info[dst].increment = -rowSize
    dst++
  }
  // 4) column left of the grind
  // Same first field in the grid
  gridIndex++
  for i := 0; i < rowSize; i++ {
    clueIndex2info[dst].offset = gridIndex
    gridIndex -= rowSize
    clueIndex2info[dst].increment = +1
    dst++
  }
  fmt.Printf("clueIndex2info = %#v\n", clueIndex2info)
}

// Generate the map neighbors.
// The index in the array is a grid array.
// The value is an array of index values in the grid.
// This allows fast scanning of all cells in the same row and column.
func printCell2neighbors() {
  var cell2neighbors [gridSize][2*rowSize - 2]int
  for gridIndex := range cell2neighbors {
    row := gridIndex / rowSize
    col := gridIndex % rowSize
    neighbors := &cell2neighbors[gridIndex]
    neighborsIndex := 0
    for r := 0; r < rowSize; r++ {
      g := r + row*rowSize
      if g != gridIndex {
        neighbors[neighborsIndex] = g
        neighborsIndex++
      }
    }
    for c := 0; c < rowSize; c++ {
      g := col + c*rowSize
      if g != gridIndex {
        neighbors[neighborsIndex] = g
        neighborsIndex++
      }
    }
  }
  fmt.Printf("cell2neighbors = %#v\n", cell2neighbors)
}

// Calculate and print the constances used by the algorithm.
// The constant arrays are calculated before compile and runtime,
// therefore the time is not part of the runtime of the solution.
func printSourceCodeConstants() {
  printOptions2count()
  printHiLoOption()
  printCell2neighbors()
  printClue2row()
  printClueIndex2info()
}

// ----------------------- Format converter -------------------------

// Convert a single option to the selected height.
func option2height(option skyscraperOptions) int {
  switch option {
  case skyscraperOption1:
    return 1
  case skyscraperOption2:
    return 2
  case skyscraperOption3:
    return 3
  case skyscraperOption4:
    return 4
  case skyscraperOption5:
    return 5
  case skyscraperOption6:
    return 6
  case skyscraperOption7:
    return 7
  default:
    // error case
    return -1
  }
}

// Generate the solution array out of a solved grid.
func solvedGrid2solution(grid *skyscraperGrid) [][]int {
  solution := make([][]int, rowSize)
  for i := range solution {
    solution[i] = make([]int, rowSize)
  }
  for i, opt := range grid {
    solution[i/rowSize][i%rowSize] = option2height(opt)
  }
  return solution
}

// ----------------------- Puzzle solver ----------------------------

// Calculates the options for the skyscraper heights based on the clues.
func calculateOptions(clues []int) skyscraperGrid {
  // init the grid with all skyscraper heights possible on each cell.
  var grid skyscraperGrid
  for i := range grid {
    grid[i] = skyscraperOptionAll
  }
  // reduce the options according to each clue
  for clueIndex, clue := range clues {
    gridIndex := clueIndex2info[clueIndex].offset
    gridIncrement := clueIndex2info[clueIndex].increment
    for _, opt := range clue2row[clue] {
      grid[gridIndex] &= opt
      gridIndex += gridIncrement
    }
  }
  return grid
}

// Reduce the options by the rules.
func reduceOptions(grid *skyscraperGrid) {
  createdNewOneOption := true
  for createdNewOneOption {
    createdNewOneOption = false
    // Only one skyscraper height per row and column.
    // -> If a skyscraper with height H is the only option for one field,
    // than no other H skyscraper is allowed in the row and column.
    for index, opt := range grid {
      if options2count[opt] == 1 {
        noOpt := ^opt
        for _, neighbor := range cell2neighbors[index] {
          old := grid[neighbor]
          new := old & noOpt
          grid[neighbor] = new
          if new == 0 {
            // no solution is possible, dead end of the search
            return
          }
          if new != old && options2count[new] == 1 {
            createdNewOneOption = true
          }
        }
      }
    }
  }
  // Other reductions are possible but the reduction needs
  // more time than the reduction reduce in the other steps.
}

// Reduce the options by the rules after setting one skyscrapper.
// Returns true if an option is reduced to one skyscrapper.
// On a true return more reduce steps could be usefull.
func reduceOptionsAfterTrial(grid *skyscraperGrid, index int) bool {
  createdNewOneOption := false
  noOpt := ^grid[index]
  for _, neighbor := range cell2neighbors[index] {
    old := grid[neighbor]
    new := old & noOpt
    grid[neighbor] = new
    if new != old && options2count[new] == 1 {
      createdNewOneOption = true
    }
  }
  return createdNewOneOption
}

// Calculate the minimal and maximal possible clue value.
func clueRange(grid *skyscraperGrid, info clueInfo) (minClue, maxClue int) {
  var lowestMark skyscraperOptions = 0
  var highestMark skyscraperOptions = 0
  gridIndex := info.offset
  for i := 0; i < rowSize; i++ {
    opt := grid[gridIndex]
    highestNow := highestOption[opt]
    lowestNow := lowestOption[opt]
    if lowestNow > highestMark {
      minClue++
    }
    if highestNow > lowestMark {
      maxClue++
    }
    // Update the markers of lowest and highest skyscraper so far
    if lowestNow > lowestMark {
      lowestMark = lowestNow
    }
    if highestNow > highestMark {
      highestMark = highestNow
    }
    // to next grid cell in the row
    gridIndex += info.increment
  }
  return
}

// Determin the status of the grid.
func checkStatus(grid *skyscraperGrid, clues []int) gridStatus {
  // check if at least one option is possible in any cell
  for _, opt := range grid {
    if opt == 0 {
      // A cell with no option for a skyscraper:
      // it is a grid in a dead end of the search tree
      return statusFaulty
    }
  }
  // check if all clues could be fullfild with the options
  for clueIndex, clue := range clues {
    if clue > 0 {
      // Check only the "real" clues with a value > 0.
      // Clue value == 0 means, no clue is given in this view direction
      minClue, maxClue := clueRange(grid, clueIndex2info[clueIndex])
      if clue < minClue || maxClue < clue {
        // the options are inconsistent to the clue -> faulty
        return statusFaulty
      }
    }
  }
  // Summary after the two checks:
  // the grid is consistent to all rules and to all clues.
  // Check if all cells have exact one option.
  for _, opt := range grid {
    if options2count[opt] != 1 {
      // More than 1 option for this field.
      // -> go deeper in the search tree.
      return statusSolvable
    }
  }
  // Results:
  //  All clues are fullfild.
  //  Exact 1 option in all grid cells
  // Hence the puzzle is solved.
  return statusSolved
}

// Determin index of the field best for the trial step.
// Criterion: number of options small as possible (but above 1).
func bestTrialField(grid *skyscraperGrid) int {
  // any cell has a value below this initial value
  minValue := options2count[skyscraperOptionAll] + 1
  minIndex := -1
  for i, opt := range grid {
    c := options2count[opt]
    if 1 < c && c < minValue {
      minValue = c
      minIndex = i
    }
  }
  if minIndex < 0 {
    // Runs in this case if the program is buggy.
    panic("no trial grid cell found")
  }
  return minIndex
}

// Try to find a solution by placing a skyscrapper.
// The index of the last skyscraper set is trialIndex.
// If no skyscrapper was set pass -1
// Returns nil if no solution is possible.
func trial(grid skyscraperGrid, clues []int, trialIndex int) *skyscraperGrid {
  if trialIndex >= 0 && reduceOptionsAfterTrial(&grid, trialIndex) {
    reduceOptions(&grid)
  }
  switch checkStatus(&grid, clues) {
  case statusSolved:
    return &grid
  case statusFaulty:
    return nil
  case statusSolvable:
    index := bestTrialField(&grid)
    currentOptions := grid[index]
    for opt := skyscraperOption1; opt < skyscraperOptionAll; opt <<= 1 {
      if opt&currentOptions != 0 {
        grid[index] = opt
        solution := trial(grid, clues, index)
        if solution != nil {
          return solution
        }
      }
    }
    return nil
  }
  panic("invalid status code")
  return nil
}

func SolvePuzzle(clues []int) [][]int {
  if len(clues) != 4*rowSize {
    panic("clues array size invalid")
  }
  grid := calculateOptions(clues)
  reduceOptions(&grid)
  solution := trial(grid, clues, -1)
  if solution == nil {
    panic("no solution found")
  }
  return solvedGrid2solution(solution)
}
