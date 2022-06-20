55466989aeecab5aac00003e


def sqInRect(l, w)
    rects = []
    while l>0 do
      w,l = [w,l].minmax
      rects << w
      l -= w
    end
    rects.size > 1 ? rects : nil
end
______________________________
def sqInRect(lng, wdth)
  min, max = [lng, wdth].minmax
  min == max ? nil : [min] + (sqInRect(max - min, min) || [min])
end
______________________________
def sqInRect(lng,wdth)
  [lng,wdth].min == 0 ? [] : lng == wdth ? nil :
    [[lng,wdth].min]*([lng,wdth].max/[lng,wdth].min) + 
    sqInRect([lng,wdth].min,[lng,wdth].max % [lng,wdth].min)
end
