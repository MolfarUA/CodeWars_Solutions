with(Math)circleIntersection=([a,b],[c,d],r)=>(-sin(x=2*acos(hypot(a-c,b-d)/2/r))+x)*r*r|0

_________________________
with(Math)circleIntersection=([o,p],[x,y],r)=>~~(s=2*acos(hypot(o-x,p-y)/2/r),r*r*(s-sin(s)))

________________________
circleIntersection=([a,b],[c,d],r)=>(m=Math,-m.sin(x=2*m.acos(m.hypot(a-c,b-d)/2/r))+x)*r*r|0

________________________
with(Math)circleIntersection=([a,b],[c,d],r)=>r*r*((x=2*acos(hypot(a-c,b-d)/2/r))-sin(x))|0

_________________________
m=Math;circleIntersection=([d,e],[f,g],r)=>r*r*(-m.sin(x=2*m.acos(m.hypot(d-f,e-g)/2/r))+x)^0

_______________________
circleIntersection=([q,w],[e,t],r)=>(m=Math,-m.sin(b=2*m.acos(m.hypot(q-e,w-t)/2/r))+b)*r*r|0
