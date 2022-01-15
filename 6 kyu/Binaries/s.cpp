#include <string>
#include <bitset>

namespace coding
{
    std::string code(const std::string &strng)
    {
        std::string str;
        size_t k;

        for(unsigned char num: strng)
        {
            // convert digit symbol into digit
            num -= '0';
            // convert digit into bits
            std::bitset<8> bits(num);

            if(num != 0){
                k = bits.to_string().size() - bits.to_string().find_first_of('1');
                
                // fill by '0'
                str.append(std::string(k - 1, '0'));
                str += '1';
                str.append(bits.to_string(),  bits.to_string().find_first_of('1'), k + 1);
            }else
                str += "10";
        }

        return str;
    }
    std::string decode(const std::string &str)
    {
        std::string strng;
        int count;

        for(size_t i = 0; i < str.size(); i += count*2){
            count = 1;

            count = str.find_first_of('1', i) - i + 1;

            std::bitset<8> bits(str, i + count, count);

            strng.append(std::to_string(bits.to_ulong()));


        }

        return strng;
    }
}
__________________________
#include <string>
#include <bitset>

namespace coding
{
    std::string code(const std::string &strng)
    {
        std::string result;
        for (int i = 0; i<=strng.size(); i++)
        {
          switch (strng[i] - '0') {
            case 0 ... 1:
            result += std::string((std::bitset<1>(strng[i] - '0').to_string().size())-1,'0');
            result += "1";
            result += std::bitset<1>(strng[i] - '0').to_string();
            break;
            case 2 ... 3:
            result += std::string((std::bitset<2>(strng[i] - '0').to_string().size())-1,'0');
            result += "1";
            result += std::bitset<2>(strng[i] - '0').to_string();
            break;
            case 4 ... 7:
            result += std::string((std::bitset<3>(strng[i] - '0').to_string().size())-1,'0');
            result += "1";
            result += std::bitset<3>(strng[i] - '0').to_string();
            break;
            case 8 ... 9:
            result += std::string((std::bitset<4>(strng[i] - '0').to_string().size())-1,'0');
            result += "1";
            result += std::bitset<4>(strng[i] - '0').to_string();
            break;
          }
          
        }
        return result;
    }
    std::string decode(const std::string &str)
    {
        std::string result;
        int numOfBits=0;
        std::string currentNum;
        for (int i = 0; i< str.size(); i++)
        {
          if(numOfBits==0)
          {
          if(str[i] == '1')
          {
            if(str[i+1] == '0')
            {
            result += "0";
            i += 1;
            continue;
            }
            else
            {
            result += "1";
            i+=1;
            continue;
            }
          }
          else
          {
            for (int j = 1;;j++)
            {
              if(str[i+j]=='1')
              {
                numOfBits=j+1;
                i+=j-1;
                break;
              }
            }
          }
          }
          else
          {
              i++;
            for(int j=0;j<numOfBits;j++)
            {
              currentNum += str[i+j];
            }
            i+=numOfBits-1;
            result += std::to_string(std::bitset<64>(currentNum).to_ullong());
            numOfBits = 0;
            currentNum = "";
          }
    }
        return result;
    }
}
__________________________
namespace coding
{
  std::string code(const std::string &strng)
  {
    std::string ret = "";
    for (auto e : strng)
    {
      std::string bits = "";
      int n = e - '0';
      do
        bits += std::to_string(n % 2);
      while ((n /= 2) > 0);
      
      bits += '1' + std::string(bits.length() - 1, '0');
      std::reverse(bits.begin(), bits.end());
      ret += bits;
    }

    return ret;
  }
  
std::string binToDec(const std::string &str)
{
  int result = 0;
  for (const auto& digital : str)
  {
    if (digital == '1')
      result += 1;
    
    result *= 2;
  }

  result /= 2;
  return std::to_string(result);
}
  
  std::string decode(const std::string &str)
  {
    int amountOfZero = 0;
    std::string result;
    for (int i = 0; i < str.length(); )
    {
      if (str[i] == '0')
      {
        ++amountOfZero;
        ++i;
      }
      else
      {
        int k = amountOfZero + 1;
        ++i;
        std::string numberInBinary = str.substr(i, k);
        std::string numberInDec = binToDec(numberInBinary);
        result += numberInDec;
        i = i + k;
        amountOfZero = 0;
      }
    }
    
    return result;
  }
}
__________________________
#include <string>
#include <vector>
#include <sstream>

namespace coding
{
    template <typename T>
    std::string toString (T arg)
    {
        std::stringstream ss;
        ss << arg;
        return ss.str ();
    }
    std::string dec_2_bin(std::string &s)
    {
        std::vector<std::string> dict = {"10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};
        return dict[std::stoi(s)];
    }
    std::string code(const std::string &strng)
    {
        int lg = strng.length();
        std::string ret = "";
        for (int start = 0; start < lg; start += 1)
        {
            std::string d (1, strng[start]);
            ret += dec_2_bin(d);
        }
        return ret;
    }
    std::string decode(const std::string &str)
    {
        std::string ret = "";
        int i = 0;
        int lg = str.length();
        while (i < lg)
        {
            int zero_i = i;
            while ((zero_i < lg) && (str[zero_i] != L'1'))
                zero_i++;
            int l = zero_i - i + 2;
            std::string ss = str.substr(zero_i + 1, (zero_i + l) - (zero_i + 1));
            ret += toString(std::stoi(ss, nullptr, 2));
            i = zero_i + l;
        }
        return ret;
    }
}
__________________________
#include <string>

namespace coding
{
    std::string code(const std::string &strng)
    {
      std::string ans("");
      
      std::string ans2("");
      for(int i = 0; i< strng.size(); i++){
        int x = strng[i]-'0';
        int k=0;
        while(x>1){
          k += 1;
          ans2 = std::to_string(x & 1) + ans2;
          x = x >> 1;
        }
        std::string ans1(k,'0');
        ans2 = std::to_string(x & 1) + ans2;
        ans1 += "1";
        ans = ans + ans1 + ans2;
        ans1.clear();     
        ans2.clear();     
      }
      return ans;
    }
    std::string decode(const std::string &str)
    { 
      std::string ans("");
      int i = 0;
      int mult = 1;
      bool front = true;
      int ans_int=0;
      while( i<=str.size() ){
          if(front) {
            mult *= 2;
            if(str[i]=='1') front = false;
          }
        //not front
          else{
            mult /= 2;
              if(str[i]=='1'){
                  ans_int += mult;
              }
              if( mult == 1){
                  ans += std::to_string(ans_int);
                  front = true;
                  ans_int = 0;
              }
           }
           i++;
       }
       return ans;
    }
}
