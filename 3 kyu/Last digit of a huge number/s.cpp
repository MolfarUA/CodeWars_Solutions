#include <list>
#include <cmath>
#include <iostream>

using namespace std;
int last_digit(list<int> array) {
    int64_t p = 1;
    auto it = array.rbegin();
    while( it != array.rend()) {
        int a = p >= 4 ? 4 + (p % 4) : p;
        int b = *it >= 20 ? 20 + (*it % 20) : *it;
        p = pow(b,a);
        it++;
    }
    return p % 10;
}
________________
#include <list>
#include <iostream>
#include <math.h>

int Modulo(int a, std::string b)
{
	int mod = 0;
	for (int i = 0; i < b.size(); i++)
		mod = (mod * 10 + b[i] - '0') % a;
	return mod;
}

int LastDigit(std::string a, std::string b)
{
	int len_a = a.size(), len_b = b.size();
	if (len_a == 1 && len_b == 1 && b[0] == '0' && a[0] == '0')
		return 1;
	if (len_b == 1 && b[0] == '0')
		return 1;
	if (len_a == 1 && a[0] == '0')
		return 0;
	int exp = (Modulo(4, b) == 0) ? 4 : Modulo(4, b);
	int res = pow(a[len_a - 1] - '0', exp);
	return res % 10;
}


using namespace std;
int last_digit(list<int> array) {
	if (array.empty())
		return 1;
	int x1 = array.front();
	array.pop_front();
	if (array.empty())
		return x1 % 10;
	int x2 = array.front();
	array.pop_front();
	x1 = x1 % 10;
	int mod = 0;
	int x3 = 0;
	bool zero = false;//в конечном итоге показывает равно ли x4 0
	if (!array.empty()) {
		x3 = array.front();
		array.pop_front();
		while (!array.empty()) {
			int xn = array.back();
			array.pop_back();
			if (zero) {
				xn = 1;
				zero = false;
			}
			else
				if (xn == 0)
					zero = true;
		}
	}// если там 2 элемента, то просто пихаем их в предыдущее решение и фиг с ним)
	else {
		std::string str1 = "";
		std::string str2 = "";
		str1 = std::to_string(x1);
		str2 = std::to_string(x2);
		return LastDigit(str1, str2);
	}
	if (zero)
		x3 = 1;
	if (x3 == 0)//по-любому степень у х1 будет 1
		return x1;
	else {
		if (x2 == 0)// степень у х1 - 0, значит ответ 1
			return 1;
		else {
			if (x2 % 2 == 0) {//четное, значит остаток равен 2 или 4
				if (x2 % 4 == 0)//в любой положительной степени число останется кратным 4
					return (int)pow(x1, 4) % 10;
				else {
					if (x3 == 1)//в первой степени остаток таким и останется, в любой > 1 станет кратным 4
						return (int)pow(x1, 2) % 10;
					else
						return (int)pow(x1, 4) % 10;
				}
			}
			else {
				if (x3 % 2 == 0) {//судя по таблице в любой четной степени нечетный остаток станет равным 1
					return x1;
				}
				else//в нечетной степени нечетный остаток себя сохраняет
					return (int)pow(x1, x2 % 4) % 10;
			}
		}
	}
}
______________________
#include <list>
#include <cmath>
using namespace std;
int last_digit(list<int> l) {
  long b=1;
  for(auto i=l.rbegin(); i!=l.rend(); i++)
    b=pow(*i>9?*i%20+20:*i, b<4?b:(b%4+4));
  return b%10;
}
