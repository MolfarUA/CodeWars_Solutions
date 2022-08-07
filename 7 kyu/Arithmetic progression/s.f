55caf1fd8063ddfa8e000018


module Solution
  implicit none
contains
  function arithmeticSequenceElements(a, d, n) result(sequence)
    integer, intent(in) :: a, d, n
    integer :: index, prevValue
    character(:), allocatable :: sequence
    character(50) :: temp

    sequence = ""
    prevValue = a
    do index = 1, n
      print*, prevValue
    
      if (len(sequence) > 0) then
        sequence = sequence // ", "
      end if
    
      write(temp, *) prevValue
      temp = adjustl(temp)
      sequence = sequence // trim(temp)
      
      prevValue = prevValue + d
    end do
    
    sequence = trim(sequence)
    print*, sequence
    
  end function arithmeticSequenceElements
end module Solution
___________________________
module Solution
  implicit none
contains
  function arithmeticSequenceElements(a, d, n) result(sequence)
    integer, intent(in) :: a, d, n
    integer :: index, prevValue
    character(:), allocatable :: sequence
    character(50) :: temp
    
    print*, a
    print*, d
    print*, n
    
    
    if (n > 0) then
      allocate(character(n*3 - 2) :: sequence)
    else 
      allocate(character(1) :: sequence)
    end if
      
    sequence = ""
    prevValue = a
    do index = 1, n
      print*, prevValue
    
      if (len(sequence) > 0) then
        sequence = sequence // ", "
      end if
    
      write(temp, *) prevValue
      temp = adjustl(temp)
      sequence = sequence // trim(temp)
      
      prevValue = prevValue + d
    end do
    
    sequence = trim(sequence)
    print*, sequence
    
  end function arithmeticSequenceElements
end module Solution
___________________________
module Solution
  implicit none
contains
  pure function arithmeticSequenceElements(a, d, n) result(sequence)
    integer, intent(in) :: a, d, n
    integer j, out
    logical first
    character(36) :: number
    character(:), allocatable :: sequence
    first = .TRUE.
    sequence = ""
    do j = 1, n
      out = int(a) + (j-1) * int(d)
      write(number, *) out
      if (first) then
        sequence = trim(adjustl(number))
        first = .FALSE.
      else
        sequence = sequence//", "//trim(adjustl(number))
      end if
    end do
  end function arithmeticSequenceElements
end module Solution
