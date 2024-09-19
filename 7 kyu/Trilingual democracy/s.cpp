char trilingual_democracy( const std::string& group ) {
  return group[ 0 ] xor group[ 1 ] xor group[ 2 ];
}
___________
#include <string>

// input is a string of three chars from the set
// 'D', 'F', 'I', 'K'; output is a single char from this set
char trilingual_democracy(const std::string& group) {
  int D = 0,
      F = 0,
      I = 0,
      K = 0;
  for(auto i : group){
    D += i == 'D';
    F += i == 'F';
    I += i == 'I';
    K += i == 'K';
  }
  
  if(D == 3 || F == 3 || I == 3 || K==3)
    return D == 3 ? 'D' : F == 3 ? 'F' : I == 3 ? 'I' : 'K';
  
  if(D == 2 || F == 2 || I == 2 || K==2)
    return D == 1 ? 'D' : F == 1 ? 'F' : I == 1 ? 'I' : 'K';

  return D == 0 ? 'D' : F == 0 ? 'F' : I == 0 ? 'I' : 'K';  
}
_________________
#include <string>
using namespace std;
// input is a string of three chars from the set
// 'D', 'F', 'I', 'K'; output is a single char from this set
char trilingual_democracy(const string& group) {
  string s=group;
  sort(s.begin(),s.end());
  int count=1;s+=' ';
  for(int i=0;i<s.length()-1;i++)
  {
    if(s[i]==s[i+1])count++;
    else{
      if(count==3)return s[0];
      if(count==2){
        if(i==1)return s[2];
        if(i==2)return s[0];
        count=1;
      }
    }
  }
  s.pop_back();
  if(s=="DFI")return 'K';
  if(s=="FIK")return 'D';
  if(s=="DIK")return 'F';
  if(s=="DFK")return 'I';

  return '?';
}
