536a155256eb459b8700077e
      
      
       identification division.
       program-id. CreateSpiral.
       data division.
       working-storage section.
       01  i usage index.
       01  j usage index.
       01  k usage index.
       01  di pic s9.
       01  dj pic s9.
       01  t  pic s9.
       01  i1 usage index.
       01  j1 usage index.
      
       linkage section.
       01  n                 pic 9(2).
       01  result.
           05 res-length     pic 9(2).
           05 row occurs 0 to 99 times depending on res-length.
              07 cell pic 9(4) occurs 99 times.
      
       procedure division using n result.
          move n to res-length
          move 1 to i j k dj
          move 0 to di
          perform until k > n * n
              move k to cell(i, j)
              add 1 to k
              add di to i giving i1
              add dj to j giving j1
              if (i1 = 0 or > n) or (j1 = 0 or > n) or cell(i1, j1) > 0
                  move di to t
                  move dj to di
                  compute dj = -t
              end-if
              add di to i
              add dj to j
          end-perform.
       end program CreateSpiral.
_________________________
       identification division.
       program-id. CreateSpiral.
       data division.
       local-storage section.
       01  x                 pic s9(4) value -1.
       01  y                 pic s9(4) value 0.
       01  dx                pic s9(4) value 1.
       01  dy                pic s9(4) value 0.
       01  l                 pic s9(4).
       01  k                 pic s9(4) value 0.
       01  i                 pic s9(4).
       01  t                 pic s9(4).
       linkage section.
       01  n pic 9(2).
       01  result.
           05 res-length     pic 9(2).
           05 row occurs 0 to 99 times depending on res-length.
              07 cell pic 9(4) occurs 99 times.
       procedure division using n result.
          initialize result
          move n to l res-length
          perform until l <= 0
            perform varying i from 0 until i >= l
              add dx to x
              add dy to y
              if x >= 0 then
                add 1 to k
                move k to cell(y + 1, x + 1)
              end-if
              if l = 0 then goback end-if
            end-perform
            if dy = 0 then subtract 1 from l end-if
            move dx to t
            multiply -1 by dy giving dx
            move t to dy
          end-perform
          goback.
       end program CreateSpiral.
_________________________
       identification division.
       program-id. CreateSpiral.
       data division.
       local-storage section.
       01  i usage index.
       01  j usage index.
       01  dir pic 9.
       01  x   pic 9(4).
      
       linkage section.
       01  n   pic 9(2).
       01  result.
           05 res-length  pic 9(2).
           05 row occurs 0 to 99 times depending on res-length.
              07 cell pic 9(4) occurs 99 times.
      
       procedure division using n result.
      
      * Implementation of Mercy Madmask's Python solution
      * See https://www.codewars.com/kata/reviews/55cfb1ef39cb89255600010b/groups/5e789154c3beb80001da17fc
      
          move n to res-length
          if n = 0 goback end-if
      
          set i, j to 1
          perform varying x from 1 until x > n * n
              move x to cell(i, j)
              evaluate dir
              when 0
                    if j = n or cell(i, j + 1) <> 0
                           add 1 to i, dir
                    else   add 1 to j        end-if
              when 1
                    if i = n or cell(i + 1, j) <> 0
                           subtract 1 from j
                           add      1  to  dir
                    else   add 1 to i        end-if
              when 2
                    if j = 1 or cell(i, j - 1) <> 0
                           subtract 1 from i
                           add      1  to  dir
                    else   subtract 1 from j end-if
              when other
                    if i = 1 or cell(i - 1, j) <> 0
                           add      1  to  j
                           move     0  to  dir
                    else   subtract 1 from i end-if
              end-evaluate
          end-perform
          
          goback.
       end program CreateSpiral.
