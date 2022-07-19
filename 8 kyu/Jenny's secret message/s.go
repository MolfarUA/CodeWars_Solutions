55225023e1be1ec8bc000390


package kata

import "fmt"

func Greet(name string) string {
  if name == "Johnny" {
    name = "my love"
  }
  return fmt.Sprintf("Hello, %v!", name)
}
__________________________________
package kata

import (
    "fmt"
    "strings"
)

func Greet(name string) string {
  if strings.ToLower(name) == "johnny" {
    name = "my love"
  }
  return fmt.Sprintf("Hello, %s!", name)
}
__________________________________
package kata

import "fmt"

func Greet(name string) string {
  if name == "Johnny" {
    name = "my love"
  }
  return fmt.Sprintf("Hello, %s!", name)
}
__________________________________
package kata

func Greet(name string) string {
  if name == "Johnny" {
    name = "my love"
  }
  return "Hello, " + name + "!"
}
