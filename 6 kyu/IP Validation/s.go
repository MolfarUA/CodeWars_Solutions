515decfd9dcfc23bb6000006


package kata

import "net"
func Is_valid_ip(ip string) bool {
  res := net.ParseIP(ip)
  if res == nil {
    return false
  }
  return true
}
_____________________________
package kata

import "net"

func Is_valid_ip(ip string) bool {
  if r := net.ParseIP(ip); r == nil {
    return false
  }
  return true
}
_____________________________
package kata

import "net"

func Is_valid_ip(ip string) bool {
  return net.ParseIP(ip) != nil
}
