58c5577d61aefcf3ff000081
  
  
#include <functional>
void bust (const int length, const int n, std::function<void(const int, const int)> f) {
  int wavelength = 2 * (n - 1);
  int count = 0;
  for (int i = 0; i < n; i++){
    int diff = wavelength - (2 * i);
    for (int j = i; j < length; j += diff, diff = wavelength - diff, count++) {
      f(count, j);
      if (diff == 0) diff = wavelength;
    }
  }
};

std::string encode_rail_fence_cipher(const std::string& str, const int n) {
    std::string encode(str.length(), ' ');
    bust(str.size(), n, [&] (auto order, auto effect) {encode[order] = str[effect];});
    return encode;
}

std::string decode_rail_fence_cipher(const std::string& str, const int n) {
    std::string decode(str.length(), ' ');
    bust(str.size(), n, [&] (auto order, auto effect) {decode[effect] = str[order];});
    return decode;
}
_____________________________
std::string encode_rail_fence_cipher(std::string str, int n) {
    if (str == "") return "";
    int wavelength = 2 * (n-1);
    std::string encode = "";
    for (int i = 0; i < n; i++){
        int diff = wavelength - (2*i);
        for (int j = i; j < (int)str.length(); j += diff, diff = wavelength - diff){
            encode += str[j];
            if (diff == 0) diff = wavelength;
        }
    }
    return encode;
}

std::string decode_rail_fence_cipher(std::string str, int n) {
    if (str == "") return "";
    int wavelength = 2 * (n-1);
    std::string decode(str.length(), ' ');
    int count = 0;
    for (int i = 0; i < n; i++){
        int diff = wavelength - (2*i);
        for (int j = i; j < (int)str.length(); j += diff, diff = wavelength - diff, count++){
            decode[j] = str[count];
            if (diff == 0) diff = wavelength;
        }
    }
    return decode;
}
_____________________________
#include <string>

std::string encode_rail_fence_cipher(const std::string &str, int n) {
// Encodes a string using the Rail Fence Cipher. 
/* n = 5
    0   1   2   3   4   5   6   7   8   9   10  11  12  |  jump1       jump2
0   X                               X                   | (n-1)*2     (n-1)*2
1       X                       X       X               | (n-2)*2     (n-4)*2
2           X               X               X           | (n-3)*2     (n-3)*2
3               X       X                       X       | (n-4)*2     (n-2)*2
4                   X                               X   | (n-1)*2     (n-1)*2

*/
  std::string ret_str = "";
  unsigned pointer, k1, k2, jump1, jump2;
  int row = -1;
  while (n>++row) { //------------- row: 0,1,2,3... ----------------------
    pointer = row;
    k1 = row % (n-1) + 1; jump1 = (n-k1)*2;
    k2 = (n-row-1) % (n-1) + 1; jump2 = (n-k2)*2;
    while (pointer < str.size()){ //------------ reads a line ------------
      ret_str.push_back(str[pointer]);
      pointer += jump1;
      if (pointer >= str.size()) break;
      ret_str.push_back(str[pointer]);
      pointer += jump2;
    }
 }
  return ret_str; //<<-------- coded string
}

std::string decode_rail_fence_cipher(const std::string &str, int n) {
// Decodes a string using the Rail Fence Cipher. 
// The same logic as encoding but applied to output string.  

  std::string ret_str(str.size(),'#');
  unsigned pointer, k1, k2, jump1, jump2, global_pointer = 0;
  int row = -1;
  while (n>++row) { //------------- row: 0,1,2,3... ----------------------
    pointer = row;
    k1 = row % (n-1) + 1; jump1 = (n-k1)*2;
    k2 = (n-row-1) % (n-1) + 1; jump2 = (n-k2)*2;
    while (pointer < str.size()){ //------------ reads a line ------------
      ret_str[pointer] = str[global_pointer]; // and put it back to its place
      pointer += jump1;
      global_pointer++;
      if (pointer >= str.size()) break;
      ret_str[pointer] = str[global_pointer];
      pointer += jump2;
      global_pointer++;
    }
 }
  return ret_str; //<<-------- decoded string
}
