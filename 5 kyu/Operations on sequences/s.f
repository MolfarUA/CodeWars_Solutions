MODULE Solution
  IMPLICIT NONE
  INTEGER, PARAMETER:: j64 = SELECTED_INT_KIND(16)
  !
  PUBLIC :: solve, j64
  PRIVATE
  !
  CONTAINS
  !
  FUNCTION solve(arr) RESULT(res)
    INTEGER(KIND=j64), DIMENSION(:), INTENT(IN) :: arr
    INTEGER(KIND=j64), DIMENSION(2) :: res
    integer(kind=j64) :: x, y, z, a, b
    integer :: i
    x = arr(1)
    y = arr(2)
    do i = 3, size(arr), 2
      a = arr(i)
      b = arr(i + 1)
      z = x * a - y * b
      y = x * b + y * a
      x = z
    end do
    res(1) = abs(x)
    res(2) = abs(y)
  END FUNCTION

END MODULE Solution
_____________________________________
MODULE Solution
  IMPLICIT NONE
  INTEGER, PARAMETER:: j64 = SELECTED_INT_KIND(16)
  !
  PUBLIC :: solve
  PRIVATE :: h
  !
  CONTAINS
  !
  FUNCTION h(a) RESULT(res)
    INTEGER(KIND=j64), DIMENSION(4), INTENT(IN) :: a
    INTEGER(KIND=j64), DIMENSION(2) :: res

    res(1) = ABS(a(1) * a(3) - a(2) * a(4))
    res(2) = ABS(a(1) * a(4) + a(2) * a(3))
  END FUNCTION

  RECURSIVE FUNCTION solve(a) RESULT(res)
    INTEGER(KIND=j64), DIMENSION(:), INTENT(IN) :: a
    INTEGER(KIND=j64), DIMENSION(2) :: res
    INTEGER(KIND=j64), DIMENSION(:), ALLOCATABLE :: res1
    INTEGER(KIND=j64), DIMENSION(2) :: tmp
    INTEGER :: lg

    lg = SIZE(a)
    IF (lg == 4) THEN
      res = h(a)
    ELSE
      tmp = h(a(1:4))
      ALLOCATE(res1(2 + lg - 4))
      res1(1:2) = tmp
      res1(3:lg - 2) = a(5:lg)
      res = solve(res1)
      DEALLOCATE(res1)
    END IF
  END FUNCTION
END MODULE Solution
