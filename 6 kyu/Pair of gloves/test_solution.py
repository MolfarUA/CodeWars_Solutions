describe "Basic tests" do
testV(["red","red"],1)
testV(["red","green","blue"],0)
testV(["gray","black","purple","purple","gray","black"],3)
testV([] of String,0)
testV(["red","green","blue","blue","red","green","red","red","red"],4)
end

def randint(a,b) rand(b-a+1)+a end
def sol(g) g.to_set.reduce(0){|a,b| b=g.count(b); b/=2; a+b} end
colors = ["White","Yellow","Fuchsia","Red","Silver","Gray","Olive","Purple","Maroon","Aqua","Lime","Teal","Green","Blue","Navy","Black"]

describe "Random tests" do

40.times do
  g=(0..randint(1,25)).map{colors[randint(0,colors.size-1)]}
  testV(g.dup,sol(g))
end
end
