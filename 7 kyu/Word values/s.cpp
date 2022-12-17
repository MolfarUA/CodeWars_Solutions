598d91785d4ce3ec4f000018
  
  
std::vector<int> wordValue(std::vector <std::string> arr){
	std::vector<int> vec {};
  for (unsigned long i=0; i<arr.size();i++){
    std::string tempstr=arr[i];      
    int sum=0;
    for (auto c:tempstr)
      if (c!=' ') sum +=c-'a'+1;
    vec.push_back(sum*(i+1));
  }
  return vec;
}
_____________________________
std::vector<int> wordValue(std::vector <std::string> arr){
	std::vector<int> r(arr.size());
  for (size_t i = 0; i < arr.size(); i++)
    for (const auto& c:arr[i])
      if (c != ' ') r[i] += (c - 96) * (i + 1);
  return r;
}
_____________________________
#include <vector>
#include <string>

std::vector<int> wordValue(std::vector <std::string> arr)
{
	  std::vector<int> result;
    int sum = 0;
    for(size_t i = 0;i<arr.size();++i)
    {
        for(char ch : arr[i])
        {
           if(!isspace(ch) && islower(ch))
             sum+=int(ch)-96;
           else if(!isspace(ch) && isupper(ch))
             sum+=int(ch)-64;
        }
        result.push_back(sum*(i+1));
        sum = 0;
    }
    return result;
}
