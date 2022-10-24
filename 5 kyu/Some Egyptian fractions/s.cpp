54f8693ea58bce689100065f
  
  
  
#include <string>
using namespace std;

class Decomp {
public:
    static string decompose(const string &nrStr, const string &drStr) {
        long long num = std::stol(nrStr), den = std::stol(drStr);
        vector<string> sequence;
        if (num > den) {
            sequence.push_back(to_string(num/den));
            num %= den;
        }
        
        for (int i = 2; ; i++) {
            if (den <= i * num) {
                sequence.push_back("1/" + to_string(i));
                num = num * i - den;
                den *= i;
            }
            if (num == 0) 
                break;
        }
        
        string result = "";
        for (auto frac : sequence) 
            result += frac + ", ";      
        return "[" + result.substr(0, result.length()-2) + "]";
    }
};
_________________________________
#include <limits>

using namespace std;

class Decomp
{
public:
  static string decompose(const string &nrStr, const string &drStr);
};

/* We use it to simplify the approximated fraction */
unsigned long long gcd(unsigned long long n1, unsigned long long n2)
{
  return (n2 == 0) ? n1 : gcd(n2, n1 % n2);
}

string Decomp::decompose(const string &nrStr, const string &drStr)
{
  std::string retVal = "[";
  unsigned long long fracNr = stoi(nrStr), fracDr = stoi(drStr), apprNr = 0, apprDr = 1;
  /* Check whether the input is invalid */
  if(fracNr==0||fracDr==0)
    return "[]";
  /* The next optional index is calculated as i = iNr / iDr*/
  unsigned long long iNr = apprDr*fracDr, iDr = apprDr*fracNr - apprNr*fracDr;
  /* Eliminate integer part */
  if ((double)fracNr / fracDr >1)
  {
    retVal += to_string(fracNr / fracDr);
    fracNr -= (fracNr / fracDr)*fracDr;
  }
  for (unsigned int i = 1; fracNr != 0 && fracNr*apprDr != apprNr*fracDr; i++)
  {
    
    if (i < numeric_limits<unsigned long long>::max() / (fracNr*apprDr) && fracNr*apprDr*i >= apprNr*i*fracDr + apprDr*fracDr)
    {
      retVal += (retVal.size()>1 ? ", 1/" + to_string(i) : "1/" + to_string(i));
      /* Simplifying the approximated fraction */
      unsigned long long tempNr = (apprNr*i + apprDr) / gcd(apprNr*i + apprDr, apprDr*i), tempDr = apprDr*i / gcd(apprNr*i + apprDr, apprDr*i);
      apprNr = tempNr;
      apprDr = tempDr;
      iNr = apprDr*fracDr;
      iDr = apprDr*fracNr - apprNr*fracDr;
      if (iDr!=0)
        /* Approximating the next index */
        i = (unsigned long long)(iNr / iDr)-1;
    }
  }
  return retVal + "]";
}
