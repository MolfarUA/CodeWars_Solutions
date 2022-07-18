515decfd9dcfc23bb6000006


using System.Net;
namespace Solution
  {
  class Kata
    {
      public static bool is_valid_IP(string IpAddres)
      {
           IPAddress ip;
            bool validIp = IPAddress.TryParse(IpAddres, out ip);
            return validIp && ip.ToString()==IpAddres;
      }
    }
  }
_____________________________
using System.Text.RegularExpressions;
namespace Solution
  {
  class Kata
    {
      public static bool is_valid_IP(string IpAddres)
      {
         var octet = "([1-9][0-9]{0,2})";
         var reg = $@"{octet}\.{octet}\.{octet}\.{octet}";
         return new Regex(reg).IsMatch(IpAddres);
      }
    }
  }
_____________________________
using System.Net;

namespace Solution
{
  class Kata
  {
    public static bool is_valid_IP(string ipAddres)
    {
      var result = IPAddress.TryParse(ipAddres, out var ip);
      return result && ip.ToString() == ipAddres;
    }
  }
}
