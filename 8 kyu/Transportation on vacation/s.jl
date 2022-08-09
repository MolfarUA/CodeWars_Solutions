568d0dd208ee69389d000016


module Solution
  export rentalcarcost
  
  rentalcarcost(d) = d < 3 ? 40d :
                     d < 7 ? 40d-20 : 40d-50
end
__________________________
module Solution
  export rentalcarcost
  
  function rentalcarcost(d)
    d >= 7 ? 40d-50 : d >=3 ? 40d-20 : 40d
  end
end
__________________________
module Solution
  export rentalcarcost
  
  function rentalcarcost(d)
    x = 40
    if d < 3 
      d * x
    elseif d < 7 
      (x * d) - 20
    else 
      (x * d) - 50  
    end
  end
end
