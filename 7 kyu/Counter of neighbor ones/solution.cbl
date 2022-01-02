       identification division.
       program-id. onesCounter.
       data division.
       working-storage section.
       01  i    usage index.
       01  j    usage index.
       01  k    usage index.
      
       linkage section.
       01  arr.
           05 arr-length     pic 99.
           05 str.
              10 xs          pic 9 occurs 0 to 70 times 
                                  depending on arr-length.
       01  result.
           05 res-length     pic 99.
           05 res            pic 99 occurs 0 to 40 times 
                                  depending on res-length.
      
       procedure division using arr result.
          move 1 to i
          move 0 to res-length
          perform until i > arr-length
              move 0 to k j
              inspect str(i:) tallying j for leading '0'
                                       k for leading '1'
              add j k to i
              if k > 0
                  add 1 to res-length
                  move k to res(res-length)
              end-if
          end-perform
          goback.
       end program onesCounter.
_____________________________________________
       identification division.
       program-id. onesCounter.
       data division.
       working-storage section.
       01  i    usage index.
       01  k    usage index.
       01  tmp  pic x.
      
       linkage section.
       01  arr.
           05 arr-length     pic 99.
           05 str.
              10 xs          pic 9 occurs 0 to 70 times 
                                   depending on arr-length.
       01  result.
           05 res-length     pic 99.
           05 res            pic 99 occurs 0 to 40 times 
                                    depending on res-length.
      
       procedure division using arr result.
          move 1 to i
          move 0 to res-length
          perform until i > arr-length
              unstring str delimited by all '0'
                  into tmp count in k
                  with pointer i
              if k > 0
                  add 1 to res-length
                  move k to res(res-length)
              end-if
          end-perform
          goback.
       end program onesCounter.
_____________________________________________
       identification division.
       program-id. onesCounter.
       data division.
       local-storage section.
       01  flag              pic 9.
       01  x                 pic 99.
       linkage section.
       01  arr.
           05 arr-length     pic 99.
           05 xs             pic 9 occurs 0 to 70 times 
                                  depending on arr-length
                                  indexed by i.
       01  result.
           05 res-length     pic 99.
           05 res            pic 99 occurs 0 to 40 times 
                                  depending on res-length
                                  indexed by j.
       procedure division using arr result.
          add 1 to arr-length
          move 0 to xs(arr-length)
          move 0 to res-length, x, j
          move 1 to flag
          perform varying i from 1 until i > arr-length
            evaluate xs(i)
              when = 1
                add 1 to x
                if flag = 1
                  add 1 to res-length
                  move 0 to flag
                end-if
              when = 0
                move 1 to flag
                if x <> 0
                  add 1 to j
                  move x to res(j)
                  move 0 to x
                end-if
            end-evaluate
          end-perform
          goback.
       end program onesCounter.
_____________________________________________
       identification division.
       program-id. onesCounter.
       data division.
       local-storage section.
       01  flag              pic 9.
       01  cur               pic 99.
      
       linkage section.
       01  arr.
           05 arr-length     pic 99.
           05 xs             pic 9 occurs 0 to 70 times 
                                  depending on arr-length
                                  indexed by i.
       01  result.
           05 res-length     pic 99.
           05 res            pic 99 occurs 0 to 40 times 
                                  depending on res-length
                                  indexed by k.
      
       procedure division using arr result.
      
          move 0 to res-length, cur, k
          move 1 to flag
          perform varying i from 1 until i > arr-length
            if xs(i) = 1
              if flag = 1
                add 1 to res-length
                add 1 to cur
                move 0 to flag
              else
                add 1 to cur
              end-if
            end-if
            if xs(i) = 0 or i = arr-length
                move 1 to flag
                if cur <> 0
                  add 1 to k
                  move cur to res(k)
                  move 0 to cur
                end-if
            end-if
          end-perform
      
          goback.
       end program onesCounter.
