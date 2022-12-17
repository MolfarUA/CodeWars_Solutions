5834fec22fb0ba7d080000e8
      
      
       identification division.
       program-id. makeToast.      
       data division.
       linkage section.
       01  num       pic 9(9).        
       01  result    pic 9(8).
       procedure division using num result.
           compute result = function abs(num - 6)
           goback.
       end program makeToast.
________________________
       identification division.
       program-id. makeToast.      
       data division.
       linkage section.
       01  num       pic 9(9).        
       01  result    pic 9(8).
       procedure division using num result.
       compute result = function abs (num - 6).
       end program makeToast.
