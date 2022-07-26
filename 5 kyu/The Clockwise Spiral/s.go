536a155256eb459b8700077e


package kata
func CreateSpiral(n int) [][]int {
  if n < 1 { return [][]int{} }
  r := make([][]int, n)
  for i := 0; i < n; i++ { r[i] = make([]int, n) }
  dx, dy, x, y := 1, 0, 0, 0
  for i := 1; i <= n*n; i++ {
    r[y][x] = i
    if x+dx < 0 || x+dx >= n || y+dy < 0 || y+dy >= n || r[y+dy][x+dx] != 0 {
      dx, dy = -dy, dx
    }
    x, y = x+dx, y+dy
  }
  return r
}
_________________________
package kata

type Spiral struct {
  x, y      int
  n         int
  m         [][]int
  direction string
}

var next_dir = map[string]string{
  "right": "down",
  "down":  "left",
  "left":  "top",
  "top":   "right",
}

func (s *Spiral) Init(size int) {
  s.x, s.y = 0, 0
  s.n = size
  s.direction = "right"
  s.m = make([][]int, s.n)
  for i := range s.m {
    s.m[i] = make([]int, s.n)
  }
}

func (s *Spiral) Set(v int) {
  s.m[s.y][s.x] = v
}

func (s *Spiral) Get() [][]int {
  return s.m
}

func (s *Spiral) Move() {
  switch s.direction {
  case "right":
    if s.x+1 < s.n && s.m[s.y][s.x+1] == 0 {
      s.x++
      return
    }
  case "down":
    if s.y+1 < s.n && s.m[s.y+1][s.x] == 0 {
      s.y++
      return
    }
  case "left":
    if s.x-1 >= 0 && s.m[s.y][s.x-1] == 0 {
      s.x--
      return
    }
  case "top":
    if s.y-1 >= 0 && s.m[s.y-1][s.x] == 0 {
      s.y--
      return
    }
  }
  s.direction = next_dir[s.direction]
  s.Move()
}

func CreateSpiral(n int) (m [][]int) {
  if n <= 0 {
    return make([][]int, 0)
  }

  spiral := Spiral{}
  spiral.Init(n)
  counter := 1
  spiral.Set(counter)
  for i := 0; i < n*n-1; i++ {
    spiral.Move()
    counter++
    spiral.Set(counter)
  }
  return spiral.Get()
}
_________________________
package kata

func CreateSpiral(n int) [][]int {
  if n < 1 { return [][]int{} }
  r := make([][]int, n)
  for i := 0; i<n; i++ { r[i] = make([]int, n) }
  r[0][0]=1
  j := 2
  top,bot,left,right := 0,n,0,n
  y, x := 0, 0
  for left<right && top<bot{
    for  x++; x<right; x++ {r[y][x]=j; j++}
    x--
    for y++; y<bot; y++ {r[y][x]=j; j++}
    y--
    for x--; x>=left; x-- {r[y][x]=j; j++}
    x++
    for y--; y>top; y-- {r[y][x]=j; j++}
    y++; right--; left++; top++; bot--
  }
  return r
}
