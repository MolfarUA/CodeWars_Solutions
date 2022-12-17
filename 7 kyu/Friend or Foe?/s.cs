55b42574ff091733d900002f


using System;
using System.Collections.Generic;
using System.Linq;

public static class Kata {
  public static IEnumerable<string> FriendOrFoe (string[] names) {
    return names.Where(name => name.Length == 4);
  }
}
________________________________
using System;
using System.Collections.Generic;

public static class Kata {
  public static IEnumerable<string> FriendOrFoe (string[] names) {
    List<string> listOfFriends=new List<string>();
        foreach (var item in names)
        {
            if (item.Length == 4)
                listOfFriends.Add(item);
        }
        return listOfFriends;
  }
}
________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class Kata {
  public static IEnumerable<string> FriendOrFoe (string[] names) {
    return names.Where(z => z.Length == 4);
  }
}
________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class Kata {
  public static IEnumerable<string> FriendOrFoe (string[] names) {
    List<string> output;
    output = names.Where(c=>c.Length==4).ToList();
    return output.ToArray();
  }
}
