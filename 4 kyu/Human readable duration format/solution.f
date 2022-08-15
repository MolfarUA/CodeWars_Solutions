52742f58faf5485cae000b9a


MODULE Solution
    IMPLICIT NONE
    PUBLIC:: formatDuration
    PRIVATE
  CONTAINS
    FUNCTION formatDuration(seconds) RESULT(str)
      INTEGER, INTENT(IN):: seconds
      CHARACTER(len = 60):: str
      character(len=:), allocatable :: str_int
      integer :: internal, years, days, hours, minutes
      integer, parameter :: mseconds = 1, &
                            mminutes = 60*mseconds, &
                            mhours = 60*mminutes, &
                            mdays = 24*mhours, &
                            myears = 365*mdays
      logical :: and
      and = .false.
      str_int = repeat(" ", 60)
      if(seconds .eq. 0) then
        str_int = "now" // str_int
      else
        internal = seconds
        years = internal / myears
        internal = internal - years*myears
        days = internal / mdays
        internal = internal - days*mdays
        hours = internal / mhours
        internal = internal - hours*mhours
        minutes = internal / mminutes
        internal = internal - minutes*mminutes
        str_int = add(internal, "second") // str_int
        str_int = add(minutes,  "minute") // str_int
        str_int = add(hours,    "hour")   // str_int
        str_int = add(days,     "day")    // str_int
        str_int = add(years,    "year")   // str_int
      end if
      str = str_int(1:60)
    contains
      function add(duration, name) result(tmp)
        integer, intent(in) :: duration
        character(len=*) :: name
        character(len=:), allocatable :: tmp
        tmp = ""
        if(duration .ne. 0) then
          tmp = to_str(duration) // " " // name
          if(duration .gt. 1) tmp = tmp // "s"
          if(str_int(1:1) .ne. " ") then
            if(.not.and) then
              and = .true.
              tmp = tmp // " and "
            else
              tmp = tmp // ", "
            end if
          end if
        end if
      end function add
      function to_str(int) result(str)
        integer, intent(in) :: int
        character(len=10) :: tmp
        character(len=:), allocatable :: str
        write(tmp, '(I0)') int
        str = trim(tmp)
      end function to_str
    END FUNCTION formatDuration
END MODULE

__________________________________________________
MODULE Solution
    IMPLICIT NONE
    PUBLIC:: formatDuration
    PRIVATE
  CONTAINS
    PURE FUNCTION formatDuration(seconds) RESULT(str)
      INTEGER, INTENT(IN):: seconds
      CHARACTER(len = 60):: str
      ! your code here
      integer :: years, days, hours, minutes, rest
      CHARACTER(len = 10) :: num
      str = "now"
      if (seconds == 0) return
      str = ""
      years = seconds / 60 / 60 / 24 / 365
      days = mod(seconds / 60 / 60 / 24, 365)
      hours = mod(seconds / 60 / 60, 24)
      minutes = mod(seconds / 60, 60)
      rest = mod(seconds, 60)
      if (years /= 0) then
          write(num, '(i10)') years
          str = trim(str) // trim(adjustl(num)) // " year"
          if (years > 1) str = trim(str) // "s"
      end if
      if (days /= 0) then
          write(num, '(i3)') days
          if (str /= "" .and. hours + minutes + rest /= 0) str = trim(str) // ", "
          if (str /= "" .and. hours + minutes + rest == 0) str = trim(str) // " and "
          str = trim(str) // " " // trim(adjustl(num)) // " day"
          if (days > 1) str = trim(str) // "s"
      end if
      if (hours /= 0) then
          write(num, '(i2)') hours
          if (str /= "" .and. minutes + rest /= 0) str = trim(str) // ", "
          if (str /= "" .and. minutes + rest == 0) str = trim(str) // " and "
          str = trim(str) // " " // trim(adjustl(num)) // " hour"
          if (hours > 1) str = trim(str) // "s"
      end if
      if (minutes /= 0) then
          write(num, '(i2)') minutes
          if (str /= "" .and. rest /= 0) str = trim(str) // ", "
          if (str /= "" .and. rest == 0) str = trim(str) // " and "
          str = trim(str) // " " // trim(adjustl(num)) // " minute"
          if (minutes > 1) str = trim(str) // "s"
      end if
      if (rest /= 0) then
          write(num, '(i2)') rest
          if (str /= "") str = trim(str) // " and "
          str = trim(str) // " " // trim(adjustl(num)) // " second"
          if (rest > 1) str = trim(str) // "s"
      end if
      str = adjustl(trim(str))
    END FUNCTION formatDuration
  END MODULE
  
__________________________________________________
MODULE Solution
    IMPLICIT NONE
    PUBLIC:: formatDuration
    PRIVATE
  CONTAINS
    FUNCTION formatDuration(s) RESULT(str)
      INTEGER:: s
      CHARACTER(len = 60):: str
      CHARACTER(len = 6), dimension(5):: periods
      CHARACTER(len = 6) :: tag
      INTEGER, dimension(5) :: sec_in_period
      INTEGER :: seconds, period_value,i
      
      seconds = s
      periods = ["year  ", "day   ","hour  ","minute", "second"]
      sec_in_period = (/31536000,86400,3600,60,1/)
      
      
      if (seconds == 0) then
        str = 'now'
        return
      end if
      
      str = ""
      do i = 1,5 
        period_value = seconds / sec_in_period(i)
         if (period_value > 0) then
          seconds = seconds - period_value * sec_in_period(i)
          ! add connecter
          if (str /= "") then
            if (seconds > 0 ) then 
              str = trim(str) // ", "
            else
              str = trim(str) // " and "
            end if
          end if
          ! convert integer to string ! need to adjust here the number of white spaces
          write(tag,'(I4)') period_value 
          if (period_value < 10) then
            tag = tag(3:)
          else if (period_value < 100) then
            tag = tag(2:)
          end if
          str = trim(str) // trim(tag) // " " // trim(periods(i))
          ! add s
          if (period_value > 1) then
            str = trim(str) // "s"
          end if
        end if
      end do
      str = trim(str(2:))
    END FUNCTION formatDuration
  END MODULE
