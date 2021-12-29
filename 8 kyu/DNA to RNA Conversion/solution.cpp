std::string DNAtoRNA(std::string dna){
  std::replace(dna.begin(), dna.end(), 'T', 'U');
  return dna;
}

_____________________________
std::string DNAtoRNA(std::string dna){
  std::replace(begin(dna), end(dna), 'T', 'U');
  return dna;
}

_____________________________
#include <string>
#include <iostream>

std::string DNAtoRNA(std::string dna){
  for(int i = 0; i < dna.size(); i++){
    dna[i] = (dna[i] == 'T' ? 'U' : dna[i]);
  }
  return dna;
}

_____________________________
#include <string>
#include <cstring>

using namespace std;

string DNAtoRNA(string dna){
  int dnalength = dna.length();
  for(int i = 0; i<dnalength;i++){
    if(dna[i] == 'T'){
      dna[i] = 'U';
    }
  }

  return dna;
}

_____________________________
#include <iostream>
#include <string>
using namespace std;

string DNAtoRNA(string dna)
{
  cin>>dna;
  string wynik;
  for (int i=0; i<dna.size(); ++i)
  {
    if (dna[i]=='T')
    {
      wynik += 'U';
      continue;
    }
    wynik += dna[i];
  }
  return wynik;
}

_____________________________
#include <string>
using namespace std;

std::string DNAtoRNA(std::string dna){
  std::string res = "";
  for(char x : dna){
    if(x=='T') res.push_back('U');
    else res.push_back(x);
  }
  return res;
}
