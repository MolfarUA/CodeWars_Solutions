package kata

func Persistence(n int) int {
  steps := 0
  for n >= 10 {
    m := 1
    for n > 0 {
      m *= n % 10
      n /= 10
    }
    n = m
    steps++
  }
  return steps
}
________________________________________
package kata

func Persistence(num int) int {
  n := 0;
    for num > 9 {
        n += 1;
        f := 1;
        for num > 0 {
            f *= num % 10;
            num /= 10;
        }
        num = f;
    }
    return n
}
________________________________________
package kata

func Persistence(n int) int {

  x := func(w int) int {
    q := 1

    for w > 0 {
      num := w % 10
      q *= num
      w = w / 10
    }

    return q
  }

  s := 0
  for n >= 10 {
    n = x(n)
    s++
  }

  return s
}
________________________________________
package kata

func Persistence(n int) int {
  return multiplySlice(n, 0)
}

func splitIntToSlice(n int) []int {
  slice := []int{}

  for n > 0 {
    slice = append(slice, n%10)
    n = n / 10
  }

  return slice
}

func multiplySlice(n int, counter int) int {
  slice := splitIntToSlice(n)

  if len(slice) <= 1 {
    return counter
  }

  result := 1
  
  for _, value := range slice {
 
      result = result * value
    
  }

  return multiplySlice(result, counter+1)
}
