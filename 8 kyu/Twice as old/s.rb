5b853229cfde412a470000d0


def twice_as_old(dad, son)
    (dad - son * 2).abs
end
______________________________
def twice_as_old(dad, son)

if dad > son * 2
   dad - son * 2
else
  son * 2 - dad
end
end
______________________________
def twice_as_old(dad, son)
  (dad - 2*son).abs
end
