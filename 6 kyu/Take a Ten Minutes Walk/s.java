public class TenMinWalk {
  public static boolean isValid(char[] walk) {
    if (walk.length != 10) {
      return false;
    }
    int x = 0, y = 0;
    for (int i = 0; i < 10; i++) {
      switch (walk[i]) {
        case 'n':
          y++;
          break;
        case 'e':
          x++;
          break;
        case 's':
          y--;
          break;
        case 'w':
          x--;
          break;
      }
    }
    return x == 0 && y == 0;
  }
}
__________________________________________
public class TenMinWalk {
  public static boolean isValid(char[] walk) {
    if (walk.length != 10) return false;
    
    int x = 0, y = 0;
    for (char c: walk) {
      switch (c) {
        case 'n': y++; break;
        case 's': y--; break;
        case 'w': x++; break;
        case 'e': x--; break;
      }
    }
    
    return x == 0 && y == 0;
  }
}
__________________________________________
public class TenMinWalk {
    public static boolean isValid(char[] walk) {
        String s = new String(walk);
        return s.chars().filter(p->p=='n').count()==s.chars().filter(p->p=='s').count()&&
                s.chars().filter(p->p=='e').count()==s.chars().filter(p->p=='w').count()&&s.chars().count()==10;
    }
}
__________________________________________
public class TenMinWalk {
  public static boolean isValid(char[] walk) {
   if(walk.length != 10) {
     return false;
   }
   char north = 'n';
   char west = 'w';
   int sum = 0;
   
   for (char p : walk) {
     if (p == north || p == west) {
       sum+=1;
     } else {
       sum-=1;
     }
   }
   return sum == 0;
  }
}
