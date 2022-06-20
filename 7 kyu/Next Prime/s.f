58e230e5e24dde0996000070


module Solution
  implicit none
  private :: isPrime
  public :: next_prime
contains

  integer(8) pure function next_prime(n)
    integer(8), intent(in) :: n
    integer(8) :: m
    m = n + 1
    do while (1 > 0)
      if (isPrime(m)) then
        next_prime = m
        return
      end if
      m = m + 1
    end do
  end function next_prime
  
  pure FUNCTION isPrime(n) RESULT(res)
    integer(8), INTENT(IN) :: n
    integer(8) :: i
    LOGICAL :: res
    if (n < 2_8) then
      res = .FALSE.
      return
    end if
    if (mod(n, 2_8) == 0) then
      res = (n == 2)
      return
    end if
    do i = 3, int(sqrt(real(n))), 2
      if (mod(n, i) == 0) then
        res = .FALSE.
        return
      end if
    end do
    res = .TRUE.
  END FUNCTION isPrime
  
end module Solution
___________________________
module Solution
  implicit none
  private
  public :: next_prime
contains
  integer(8) pure function next_prime(n)
    integer(8), intent(in) :: n
    integer(8) :: d
    logical :: found
    if (n < 2) then
      next_prime = 2
      return
    end if
    next_prime = n + 1 + mod(n, 2_8)
    do
      d = 3
      found = .true.
      do while (d * d <= next_prime)
        if (mod(next_prime, d) == 0) then
          found = .false.
          exit
        end if
        d = d + 2
      end do
      if (found) then
        return
      end if
      next_prime = next_prime + 2
    end do
  end function next_prime
end module Solution
___________________________
module Solution
  implicit none
  private
  public :: next_prime
contains
  integer(8) pure function next_prime(n)
    implicit none
    integer(8), intent(in) :: n
    integer(8) :: i, limit
    logical :: is_prime

    next_prime = n

    if (next_prime < 2) then
        next_prime = 2
        return
    end if
    
    if (MOD(next_prime, 2_8) == 0 ) then
        next_prime = next_prime + 1 - 2
    end if

    is_prime = .false.
    do while ( .not. is_prime )
        next_prime = next_prime + 2
        is_prime = .true.
        limit = INT(SQRT(REAL(next_prime))) + 1
        i = 3
        do while ( is_prime .and. i < limit )
            is_prime = MOD(next_prime, i) /= 0
            i = i + 1
        end do
    end do
  end function next_prime
end module Solution
