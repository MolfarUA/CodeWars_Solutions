59aac7a9485a4dd82e00003e
      
      
       identification division.
       program-id. Cockroaches.
       data division.
       local-storage section.
       01  s         pic x(264).
       01  redefines s.
           05 c      pic x occurs 264 times.
       01  o         pic 9(3).
      
       linkage section.
       01  x.
           05  l      pic 9(2).
           05  m      pic 9(2).
           05  room occurs 2 to 34 times depending on l.
               07  e  pic x occurs 34 times indexed by i j.
                   88 AARRRGGHHHHHcockroach value 'U', 'L', 'D', 'R'.
       01  result.
           03  hole   pic 9(2) occurs 10 times indexed k.
      
       procedure division using x result.
      
          initialize result
      
          set i to 1
          string function trim(function reverse(room(1)))
          into s pointer i
          perform varying j from 1 until j > l
            string e(j, 1) into s pointer i
          end-perform
          string function trim(room(l))
          into s pointer i
          perform varying j from l by -1 until j = 0
              string e(j, m) into s pointer i
          end-perform
          move function concat(function trim(s),s) to s
          
          perform varying i from 2 until i = m
                  after   j from 2 until j = l
              if AARRRGGHHHHHcockroach(j,i)
              evaluate e(j, i)
              when 'U'    compute o = m - i + 1
              when 'L'    compute o = m + j
              when 'D'    compute o = m + l + i
              when other  compute o = 2 * (l + m) - j + 1
              end-evaluate
              perform until c(o) is numeric
                add 1 to o
              end-perform
              move c(o) to k
              add 1 to hole(k + 1)
              end-if
          end-perform
      
          goback.
       end program Cockroaches.
________________________________
       identification division.
       program-id. Cockroaches.
       data division.
       local-storage section.
       01  s         pic x(264).
       01  redefines s.
           05 c      pic x occurs 264 times.
       01  o         pic 9(3).
      
       linkage section.
       01  x.
           05  l      pic 9(2).
           05  m      pic 9(2).
           05  room occurs 2 to 34 times depending on l.
               07  e  pic x occurs 34 times indexed by i j.
                   88 AARRRGGHHHHHcockroach value 'U', 'L', 'D', 'R'.
       01  result.
           03  hole   pic 9(2) occurs 10 times indexed k.
      
       procedure division using x result.
      
          initialize result
      
          set i to 1
          string function trim(function reverse(room(1)))
          into s pointer i
          perform varying j from 1 until j > l
            string e(j, 1) into s pointer i
          end-perform
          string function trim(room(l))
          into s pointer i
          perform varying j from l by -1 until j = 0
              string e(j, m) into s pointer i
          end-perform
          move function concat(function trim(s),s) to s
          
          perform varying i from 2 until i = m
                  after   j from 2 until j = l
              if AARRRGGHHHHHcockroach(j,i)
              evaluate e(j, i)
              when 'U'    compute o = m - i + 1
              when 'L'    compute o = m + j
              when 'D'    compute o = m + l + i
              when other  compute o = 2 * (l + m) - j + 1
              end-evaluate
              perform until c(o) is numeric
                add 1 to o
              end-perform
              move c(o) to k
              add 1 to k hole(k)
              end-if
          end-perform
      
          goback.
       end program Cockroaches.
________________________________
       identification division.
       program-id. Cockroaches.
       data division.
       local-storage section.
       01  y0                     pic s9(3) value -1.
       01  x0                     pic s9(3) value -1.
       01  y                      pic s9(3) value 0.
       01  x                      pic s9(3) value 0.
       01  dy                     pic s9(3) value 0.
       01  dx                     pic s9(3) value 1.
       01  t                      pic s9(3) value 0.
       01  d                      pic 9(3) value 0.
       01  p                      pic x(1) value '#'.
       01  room-matrix.
           05 rows                occurs 99 times.
              07 room             pic x(1)
                                  occurs 99 times.
       linkage section.
       01  room-str.
           05  h                  pic 9(2).
           05  w                  pic 9(2).
           05  row                pic x(34)
                                  occurs 2 to 34 times 
                                  depending on h
                                  indexed by i j.
       01  result.
           03  r pic 9(2)         occurs 10 times.
       procedure division using room-str result.
      
          initialize result
      
          perform varying i from 1 until i > h
              after j from 1 until j > w
            move row(i)(j:1) to room(i,j)
          end-perform
      
          perform forever
            if (x + 1 = w and dx > 0) or (x = 0 and dx < 0) or
               (y + 1 = h and dy > 0) or (y = 0 and dy < 0) then
              move dy to t
              move dx to dy
              multiply -1 by t giving dx
            end-if
            compute d = function ord(room(y + 1, x + 1))
            if d >= 49 and d <= 58 then
              move room(y + 1, x + 1) to p
              evaluate true
                when y0 = -1
                  move y to y0
                  move x to x0
                when y0 = y and x0 = x
                  exit perform
              end-evaluate
            else
              if p <> '#' then
                move p to room(y + 1, x + 1)
              end-if
            end-if
            add dy to y
            add dx to x
          end-perform
      
          perform varying y from 0 until y >= h
              after x from 0 until x >= w
            evaluate true
              when room(y + 1, x + 1) = 'U'
                add 1 to r(function ord(room(1, x + 1)) - 48)
              when room(y + 1, x + 1) = 'D'
                add 1 to r(function ord(room(h, x + 1)) - 48)
              when room(y + 1, x + 1) = 'R'
                add 1 to r(function ord(room(y + 1, w)) - 48)
              when room(y + 1, x + 1) = 'L'
                add 1 to r(function ord(room(y + 1, 1)) - 48)
            end-evaluate
          end-perform
      
          goback.
       end program Cockroaches.
