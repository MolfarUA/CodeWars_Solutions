package kata

import (
  "encoding/binary"
	"net"
)

func IpsBetween(first, last string) int {
  firstVal := binary.BigEndian.Uint32(net.ParseIP(first)[12:16]) // last 4 bytes because net/ip supports ipv6
  lastVal := binary.BigEndian.Uint32(net.ParseIP(last)[12:16])
  return int(lastVal) - int(firstVal)
}
__________________
package kata

import (
	"strconv"
	"strings"
)

func IpsBetween(start, end string) int {
	p, q := 0, 0
	for _, s := range strings.Split(start, ".") {
		v, _ := strconv.Atoi(s)
		p = p*256 + v
	}
	for _, s := range strings.Split(end, ".") {
		v, _ := strconv.Atoi(s)
		q = q*256 + v
	}
	return q - p
}
______________________________
package kata
import (
  "strings"
  "strconv"
)

func IpsBetween(start, end string) int {
    return parseIP(end) - parseIP(start)
}

func parseIP(addr string) (ret int) {
    for _, b := range(strings.Split(addr, ".")) {
      val, _ := strconv.Atoi(b)
      ret = (ret << 8) + val
    }
    return
}
