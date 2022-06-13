using System;
using System.Linq;

public class Kata {
  public static int MontyHall(int correctDoor, int[] participants) {
    int cor = participants.Count(x => x == correctDoor);
    return 100 - (int)Math.Round(100.0 * cor / participants.Length);
  }
}
_________________________________________________
using System;
using System.Linq;

public class Kata {
  public static int MontyHall(int correctDoor, int[] participants) {
    return (int)Math.Round( (double)(participants.Count(x => x != correctDoor))/participants.Length * 100.0);
  }
}
_________________________________________________
using System;
using System.Linq;
public class Kata 
{
  public static int MontyHall(int correctDoor, int[] participants) 
  {
    return (int)Math.Round(100.0 * participants.Count(x => x != correctDoor) / participants.Length);
  }
}
_________________________________________________
using System;
using System.Linq;


public class Kata {
  public static int MontyHall(int correctDoor, int[] participants) {
    return (int)Math.Round((float)(participants.Count(x => x != correctDoor) * 100)/ participants.Length);
  }
}
