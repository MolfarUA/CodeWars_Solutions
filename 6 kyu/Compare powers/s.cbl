55b2549a781b5336c0000103
      
      
       identification division.
       program-id. compare-powers.
      
       data division.
      
       linkage section.
       01  n1.
           05 base1  pic 9(10).
           05 exp1   pic 9(10).
       01  n2.
           05 base2  pic 9(10).
           05 exp2   pic 9(10).
       01 result     pic s9 sign leading.
      
       procedure division using n1 n2 result.
          compute result = function sign(exp2 * function log(base2) -
                                         exp1 * function log(base1)).
       end program compare-powers.
________________________________
       identification division.
       program-id. compare-powers.
       data division.
       local-storage section.
       01  a         pic s9(10)v9(28).
       01  b         pic s9(10)v9(28).
       01  c         pic s9(10)v9(28).
       linkage section.
       01  n1.
           05 x   pic 9(10).
           05 y   pic 9(10).
       01  n2.
           05 v   pic 9(10).
           05 w   pic 9(10).
       01 r       pic s9(1) sign leading.
       procedure division using n1 n2 r.
          move y to a
          move w to b
          compute c = function log(v) * b - 
                      function log(x) * a
          if c < 0 then compute r = -1 end-if
          if c > 0 then compute r =  1 end-if
          goback.
       end program compare-powers.
________________________________
       identification division.
       program-id. compare-powers.
      
       data division.
       local-storage section.
       01  a         pic s9(10)v9(28).
       01  b         pic s9(10)v9(28).
       01  c         pic s9(10)v9(28).
      
       linkage section.
       01  n1.
           05 base  pic 9(10).
           05 exp   pic 9(10).
       01  n2.
           05 base  pic 9(10).
           05 exp   pic 9(10).
       01 result     pic s9(1) sign leading.
      
       procedure division using n1 n2 result.
      
          move exp of n1 to a
          move exp of n2 to b
          compute c = function log(base of n2) * b - 
                      function log(base of n1) * a
          evaluate c
              when < 0   move -1  to result
              when > 0   move  1  to result
          end-evaluate
      
          goback.
       end program compare-powers.
