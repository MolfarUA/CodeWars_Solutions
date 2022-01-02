       identification division.
       program-id. countPassengers.
       data division.
       linkage section.
       01  busStops.
           05 arr-length      pic 9(3).
           05 xs              occurs 0 to 100 times 
                              depending on arr-length
                              indexed by i.
              07  people-in   pic 9(3).
              07  people-out  pic 9(3).
       01  result             pic 9(8).
       procedure division using busStops result.
          move 0 to result
          perform varying i from 1 until i > arr-length
            add people-in(i) to result
            subtract people-out(i) from result 
          end-perform
          goback.
       end program countPassengers.
_____________________________________
       identification division.
       program-id. countPassengers.
       data division.
      
       linkage section.
       01  busStops.
           05 arr-length      pic 9(3).
           05 xs              occurs 0 to 100 times 
                              depending on arr-length
                              indexed by i.
              07  people-in   pic 9(3).
              07  people-out  pic 9(3).
       01  result             pic 9(8).
      
       procedure division using busStops result.
      
           move 0 to result
           perform varying i from 1 until i > arr-length
               compute result = result + 
                people-in of xs(i) - people-out of xs(i)
           end-perform
      
           goback.
       end program countPassengers.
