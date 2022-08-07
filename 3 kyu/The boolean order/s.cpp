59eb1e4a0863c7ff7e000008
  
  
#include <map>

typedef std::pair<std::string,std::string> s_key;
typedef std::pair<int64_t,int64_t> s_val;
typedef std::map<s_key,s_val> memomap;

memomap solutionMap
{
  { std::make_pair("t", ""), std::make_pair(1, 0) },
  { std::make_pair("f", ""), std::make_pair(0, 1) }
};

// solve the problem for both boolean cases
s_val solve_bi(const std::string &s, const std::string &ops){
  //check memo for solution
  s_key key = std::make_pair(s,ops);
  if (solutionMap.count(key))
  {
    return solutionMap[key];
  }
  
  //no memo, try solve
  //try every root to prevent duplicate results
  int64_t true_count = 0, false_count = 0;
  for (size_t i = 0; i < ops.size(); i++)
  {
    s_val lhs_val = solve_bi(s.substr(0, i + 1), ops.substr(0, i));
    int64_t left_true = lhs_val.first, left_false = lhs_val.second;
    
    s_val rhs_val = solve_bi(s.substr(i + 1), ops.substr(i + 1));
    int64_t right_true = rhs_val.first, right_false = rhs_val.second;
    
    switch (ops[i])
    {
        case '|':
          false_count += left_false * right_false;
           true_count += left_false * right_true;
           true_count += left_true  * right_false;
           true_count += left_true  * right_true;
          break;
        
        case '&':
          false_count += left_false * right_false;
          false_count += left_false * right_true;
          false_count += left_true  * right_false;
           true_count += left_true  * right_true;
          break;
        
        case '^':
          false_count += left_false * right_false;
           true_count += left_false * right_true;
           true_count += left_true  * right_false;
          false_count += left_true  * right_true;
          break;
        
        default: throw;
    }
  }
  solutionMap[key] = std::make_pair(true_count, false_count);
  
  return solutionMap[key];
}

// get the solution for both, return only the true case
int64_t solve(const std::string &s, const std::string &ops)
{
  return solve_bi(s,ops).first;
}
_________________________________________
#include <functional>
#include <iostream>

struct BoolCounts
{
  int64_t trueCount;
  int64_t falseCount;
  BoolCounts();
  BoolCounts(bool);
  BoolCounts(char);
  BoolCounts addCount(bool, int64_t);
  BoolCounts operator+= (BoolCounts);
  void clear();
};

class LogicOperator
{
  std::function<bool(bool, bool)> operator_;
  static bool AND(bool, bool);
  static bool OR(bool, bool);
  static bool XOR(bool, bool);
public:
  LogicOperator(char);
  BoolCounts operator()(BoolCounts,BoolCounts) const;
};

int64_t solve(const std::string &s, const std::string &ops)
{ 
  // initialisating of helper variables
  std::vector<LogicOperator> op;
  op.reserve(ops.size());
  for (char c: ops)
    op.push_back(LogicOperator(c));
  
  std::vector<std::vector<BoolCounts> > matr;
  matr.resize(s.size());
  for (std::size_t i = 0;  i < matr.size(); ++i)
  {
    matr[i].resize(i + 1);
    matr[i][i] = BoolCounts(s[i]);
  }
  
  // calculating of true and false combinations counts
  for (std::size_t i = 1; i < matr.size(); ++i)
  {
    for (int64_t j = i - 1; j >= 0; --j)
    {
       for (std::size_t k = j; k < i; ++k)
       {
           matr[i][j] += op[k]( matr[k][j], matr[i][k+1] );
       }
    }
  }
  
  return matr[matr.size() - 1][0].trueCount;
}

bool LogicOperator::AND(bool b1, bool b2) { return b1 & b2; }

bool LogicOperator::OR(bool b1, bool b2) { return b1 | b2; }

bool LogicOperator::XOR(bool b1, bool b2) { return b1 ^ b2; }

LogicOperator::LogicOperator(char c)
{
  switch (c)
  {
    case '&':
      operator_ = AND;
      break;
    case '|':
      operator_ = OR;
      break;
    case '^':
    default:
      operator_ = XOR;
      break;
  }
}

BoolCounts LogicOperator::operator() (BoolCounts b1, BoolCounts b2) const 
{ 
  BoolCounts result;
  result.addCount(operator_(true, true), b1.trueCount * b2.trueCount);
  result.addCount(operator_(false, true), b1.falseCount * b2.trueCount);
  result.addCount(operator_(true, false), b1.trueCount * b2.falseCount);
  result.addCount(operator_(false, false), b1.falseCount * b2.falseCount);
  return result; 
}

BoolCounts::BoolCounts(): trueCount(0), falseCount(0) {}

BoolCounts::BoolCounts(bool bl): BoolCounts() 
{
  if (bl)
    trueCount = 1;
  else
    falseCount = 1;
}

BoolCounts::BoolCounts(char c): BoolCounts(c == 't') {}

BoolCounts BoolCounts::addCount(bool field, int64_t count)
{
  if (field)
    trueCount += count;
  else
    falseCount += count;
  return *this;
}

BoolCounts BoolCounts::operator+= (BoolCounts bc)
{
  trueCount += bc.trueCount;
  falseCount += bc.falseCount;
  return *this;
}

void BoolCounts::clear()
{
  trueCount = 0;
  falseCount = 0;
}
_________________________________________
#include <assert.h>
#include <stdint.h>
#include <string>
#include <vector>
using namespace std;

using i64 = int64_t;
using vec1 = vector<i64>;
using vec2 = vector<vec1>;
using vec3 = vector<vec2>;

i64 solve(string const& s, string const& ops) {
  assert(s.size() == ops.size() + 1);
  size_t const max_len = s.size() + ops.size();

  // [position][length][value]
  vec3 dp(max_len + 1, vec2(max_len + 1, vec1(2, 0)));  
  for (size_t i = 0; i < s.size(); ++i)
    ++dp[2 * i][1][s[i] == 't'];

  for (size_t l = 3; l <= max_len; l += 2) {
    for (size_t p = 0; p <= max_len - l + 1; p += 2) {
      for (size_t o = p + 1; o <= p + l - 1; o += 2) {
        
        i64 vals[2][2];
        for (size_t i = 0; i < 2; ++i)
          for (size_t j = 0; j < 2; ++j)
            vals[i][j] = dp[p][o - p][i] * dp[o + 1][p + l - o - 1][j]; 

        char const op = ops[o / 2];
        if (op == '&') {
          dp[p][l][0] += vals[0][0] + vals[0][1] + vals[1][0];
          dp[p][l][1] += vals[1][1];
        } else if (op == '|') {
          dp[p][l][0] += vals[0][0];
          dp[p][l][1] += vals[0][1] + vals[1][0] + vals[1][1];
        } else if (op == '^') {
          dp[p][l][0] += vals[0][0] + vals[1][1];
          dp[p][l][1] += vals[0][1] + vals[1][0];
        } else assert(false);
      }
    }
  }

  return dp[0][max_len][1];
}
