#include <cstdint>
#include <string>
#include <fmt/core.h>

std::string add_binary(std::uint64_t a, std::uint64_t b) {
  return fmt::format("{:b}", a + b);
}
__________________________________
#include <cstdint>
#include <string>

using namespace std;

string add_binary(uint64_t a, uint64_t b) {
    a += b;
    string output;

    do {
        output = to_string(a % 2) + output;
        a /= 2;
    } while(a > 0);

    return output;
}
__________________________________
#include <cstdint>
#include <string>
#include <bitset>

using namespace std;

std::string add_binary(uint64_t a, uint64_t b) {
  string bi = std::bitset<64>((a + b)).to_string();
  return bi.erase(0, min(bi.find_first_not_of('0'), bi.size()-1));
}
__________________________________
#include <cstdint>
#include <string>
#include <bitset>

std::string add_binary(uint64_t a, uint64_t b) {
    std::string s = std::bitset< 64 >( a + b ).to_string(); 
    s.erase(0, s.find_first_not_of('0'));
    return s.size() > 0 ? s : "0";
}
