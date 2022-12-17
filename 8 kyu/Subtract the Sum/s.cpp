56c5847f27be2c3db20009c3
  
  
#include <string>
using namespace std;

std::vector<std::string> fruits {
"kiwi", "pear", "kiwi", "banana", "melon", "banana", "melon", "pineapple", "apple", "pineapple",
"cucumber", "pineapple", "cucumber", "orange", "grape", "orange", "grape", "apple", "grape", "cherry",
"pear", "cherry", "pear", "kiwi", "banana", "kiwi", "apple", "melon", "banana", "melon",
"pineapple", "melon", "pineapple", "cucumber", "orange", "apple", "orange", "grape", "orange", "grape",
"cherry", "pear", "cherry", "pear", "apple", "pear", "kiwi", "banana", "kiwi", "banana",
"melon", "pineapple", "melon", "apple", "cucumber", "pineapple", "cucumber", "orange", "cucumber", "orange",
"grape", "cherry", "apple", "cherry", "pear", "cherry", "pear", "kiwi", "pear", "kiwi",
"banana", "apple", "banana", "melon", "pineapple", "melon", "pineapple", "cucumber", "pineapple", "cucumber",
"apple", "grape", "orange", "grape", "cherry", "grape", "cherry", "pear", "cherry", "apple",
"kiwi", "banana", "kiwi", "banana", "melon", "banana", "melon", "pineapple", "apple", "pineapple"
};

int sumDigits(int n)
{
	int sum = 0;
	while (n != 0) {
  	sum += n%10;
    n = n/10;
  }
  return sum;
}

string SubtractSum(int n)
{
	int value = n - sumDigits(n);
  if (value > 100)
  	return SubtractSum(value);
  return fruits[value-1];
}
_______________________________________
#include <string>
using namespace std;

string SubtractSum(int n)
{
  return "apple";
}
