object Snail {
  
  def snail(xs: List[List[Int]]): List[Int] = xs match {
    case Nil => Nil
    case x :: xs => x ++ snail(xs.transpose.reverse)
  }    
  
}

#################
object Snail {
  
  def snail(xs: List[List[Int]]): List[Int] = xs match {
    case Nil => Nil
    case x :: rest => x ++ snail(rest.transpose.reverse)
  }
}

#################
object Snail {
  
  def getLastCol(ls: List[List[Int]], acc: List[Int]=List()): List[Int] ={
  if(ls.tail.isEmpty) acc:+ ls.head.last
  else getLastCol(ls.tail,acc:+ls.head.last)
}
def getFirstCol(ls: List[List[Int]], acc: List[Int]=List()): List[Int] ={
  if(ls.tail.isEmpty) acc:+ ls.head.head
  else getFirstCol(ls.tail,acc:+ls.head.head)
}
def deleteLastCol(ls:List[List[Int]], acc:List[List[Int]] = List()): List[List[Int]] =
{
  if(ls.tail.isEmpty) acc:+ ls.head.dropRight(1)
  else deleteLastCol(ls.tail, acc:+ls.head.dropRight(1))
}
def deleteFirstCol(ls:List[List[Int]], acc:List[List[Int]] = List()): List[List[Int]] =
{
  if(ls.tail.isEmpty) acc:+ ls.head.drop(1)
  else deleteFirstCol(ls.tail, acc:+ls.head.drop(1))
}


def snail(ls: List[List[Int]], acc: List[List[Int]] = List(), iter:Int=1): List[Int] = {
  if(ls.head.isEmpty)List()
    
 else if(iter%2==1)
  {
    if(ls.length ==1 && ls.head.length ==1) (acc:+ls.head).flatten
  else snail(deleteLastCol(ls.drop(1)), acc:+ls(0):+getLastCol(ls.drop(1)),iter+1)
  }
  else{
   if(ls.length ==1 && ls.head.length ==1) (acc:+ls.head).flatten
   else snail(deleteFirstCol(ls.dropRight(1)), acc:+ls.takeRight(1)(0).reverse:+getFirstCol(ls.dropRight(1)).reverse, iter+1)
 }
}
}

#########################
object Snail {
  
  def snail(xs: List[List[Int]]): List[Any] = {
  def last_(b:List[List[Int]],l:List[Int]):List[Int]=b match{
   case Nil => throw new Exception("Empty list or wrong demension.")
   case x::Nil => (x.last::l).init.reverse
   case x::xt => last_(xt, x.last::l)
 }
def smaller_sq(a:List[List[Int]],l:List[List[Int]]):List[List[Int]]=a match{
  case Nil => throw new Exception("Empty list.")
  case x::Nil => l:+x.init.tail
  case x::xs => smaller_sq(xs,l:+x.init.tail)
}
def firth(a:List[List[Int]],l:List[Int]):List[Int]=a match{
  case Nil => throw new Exception("Empty list.")
  case x::Nil => (x.head::l).init.tail
  case x::xs => firth(xs,x.head::l)
}
  
  def re(x:List[List[Int]],xl:List[Int],l:List[Int],sw:Int
       ,acc:Int,stop:Int,acc_final:Int,final_stop:Int):List[Int]={
     
     if(acc_final==final_stop) l.reverse
     
     else if(sw==0 && acc!=stop){
        re(x,xl.tail,xl.head::l,sw,acc+1,stop,acc_final+1,final_stop)
      }
     else if(sw==0&& acc==stop){
       re(x,x.last.init.reverse++firth(x,List()),l,1,0,
           (x.last.init.reverse++firth(x,List())).length,acc_final,final_stop)
     }
      else if(sw==1 && acc!=stop){
        re(x,xl.tail,xl.head::l,sw,acc+1,stop,acc_final+1,final_stop)
      }
      else if(sw==1&& acc==stop){
        re(smaller_sq(x.init.tail,List()),
            smaller_sq(x.init.tail,List()).head++last_(smaller_sq(x.init.tail,List()),List()),l,
            0,0,smaller_sq(x.init.tail,List()).head.length+smaller_sq(x.init.tail,List()).length-1,
            acc_final,final_stop)
      }
      else throw new Exception("Error")
   }
   if(xs.isEmpty)List()
   else if(xs.last.isEmpty)List()
   else re(xs,xs.head++last_(xs,List()),List(),0,0,xs.head.length+xs.length-1,0,xs.length*xs.head.length)
   
  }
}
