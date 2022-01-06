#pragma once

#include <map>
#include <cmath>
#include <limits>
#include <string>
#include <cassert>
#include <cstring>
#include <sstream>
#include <ostream>
#include <iostream>
#include <iterator>
#include <optional>
#include <algorithm>

template <std::size_t K>
bool operator==(const std::array<float, K> &one, const std::array<float, K> &two)
{
    auto diff = one;
    std::transform(one.begin(), one.end(), two.begin(), diff.begin(),
                   [](const float o, const float t){
        return std::abs(o - t);
    });

    return std::all_of(diff.begin(), diff.end(), [](const float c) { return c <= 1e-3f; });
}

template <std::size_t K>
class k_means
{
    std::array<float, K> _centroids;
    std::unordered_map<float, std::size_t> _shifts;
    const std::size_t _iterations {};
    const std::array<std::string, K> _labels;

public:
    typedef std::function<float(float, float)> kernel_t;

    k_means(const std::array<std::string, K> &labels, const std::size_t iterations = 20u)
        :
          _iterations(iterations),
          _labels(labels)
    {}

    bool fit(const std::map<std::size_t, std::size_t> &dataset)
    {
        static_assert(K > 1u);

        if (dataset.size() < K)
            throw std::runtime_error("Invalid dataset");

        for (auto i = 0u; i < K; ++i)
        {
            auto iter = dataset.begin();
            std::advance(iter, i * (dataset.size() / (K - 1u)));
            _centroids[i] = iter->first;
        }

        return compute(dataset);
    }

    inline std::string label(float value) const
    {
        return _labels.at(cluster(value, _centroids));
    }

private:
    inline std::size_t cluster(float value, const std::array<float, K> &centroids) const
    {
        if (_shifts.count(value))
            return _shifts.at(value);

        const auto inearest = std::min_element(centroids.begin(), centroids.end(),
                                               [&](const auto a, const auto b) {
            return sqrt(powl(a - value, 2)) < sqrt(powl(b - value, 2));
        });
        return std::distance(centroids.begin(), inearest);
    }

    /// Also if you have trouble discerning if the particular sequence of 1's
    /// is a dot or a dash, assume it's a dot.
    void add_shifts(const std::map<std::size_t, std::size_t> &dataset)
    {
        for (auto iter = dataset.begin(); iter != dataset.end(); ++iter)
        {
            const auto value = iter->first;
            const auto count = iter->second;
            const auto c = cluster(value, _centroids);

            if (std::next(iter) != dataset.end() && iter != dataset.begin())
            {
                const auto p = cluster(value - 2, _centroids);
                const auto n = cluster(value + 2, _centroids);

                if (std::next(iter)->second > count * 2 && p != c && n == c)
                    _shifts[value] = c - 1u;
            }
        }
    }

    bool compute(const std::map<std::size_t, std::size_t> &dataset)
    {
        auto iteration = _iterations;
        std::array<std::size_t, K> masses;

        while (--iteration)
        {
            const auto old_centroids = _centroids;
            std::fill(_centroids.begin(), _centroids.end(), 0u);
            std::fill(masses.begin(), masses.end(), 0u);

            for (const auto &[value, count] : dataset)
            {
                auto c = cluster(value, old_centroids);

                _centroids[c] += count * value;
                masses[c] += count;
            }

            /// Average
            for (auto i = 0u; i < _centroids.size(); ++i)
                _centroids[i] /= masses[i];

            if (old_centroids == _centroids)
            {
                add_shifts(dataset);
                return true;
            }
        }

        return false;
    }

}; /// class k_means

struct rate_info {
    k_means<3u> sections {{"", " ", "  "}};
    k_means<3u> transfer {{".", "-", "-"}};
    bool valid = false;
};

inline void for_each(const char *bits, std::function<void(const char)> callback)
{
    for (auto *c = bits; *c != '\0'; ++c)
        callback(*c);
}

inline void for_each_word(const char *bits, std::function<void(const char c, std::size_t size)> callback)
{
    char current = '0';
    std::size_t count {};
    bool first = true;

    for_each(bits, [&](const char c)
    {
        if (current != c)
        {
            /// Removing extra 0 from the beginning
            if (count && (!first || current == '1'))
                callback(current, count);

            first = false;

            current = c;
            count = 1u;
            return;
        }

        ++count;
    });

    /// Removing extra 0 from the end
    if (count && current != '0')
        callback(current, count);
}

rate_info detect_rate(const char *bits)
{
    std::map<std::size_t, std::size_t> dataset;

    for_each_word(bits, [&](const char c, std::size_t size)
    {
        assert(c == '0' || c == '1');
        ++dataset[size];
    });

    if (dataset.empty())
        return {};

    if (dataset.size() == 2u)
    {
        if (dataset.begin()->first * 5u < dataset.rbegin()->first)
            ++dataset[0.5 * (dataset.begin()->first + dataset.rbegin()->first)];
    }

    while (dataset.size() < 3u)
        ++dataset[dataset.rbegin()->first * 3u];

    rate_info info;
    info.valid = info.sections.fit(dataset) && info.transfer.fit(dataset);
    return info;
}

std::string decodeBitsAdvanced (const char *bits)
{
    const auto info = detect_rate(bits);
    if (!info.valid)
        return {};

    const auto len = strlen(bits);

    std::stringstream ss;
    for_each_word(bits, [&](const char c, const std::size_t size)
    {
        if (c == '0')
            ss << info.sections.label(size);
        else
            ss << info.transfer.label(size);
    });

    return ss.str();
}

std::string decodeMorse (std::string morseCode)
{
    std::stringstream result;

    /// Tokenizing with single space
    std::stringstream ss(morseCode);
    std::string token;
    while(std::getline(ss, token, ' '))
    {
        if (token.empty())
        {
            result << " ";
            continue;
        }

        try
        {
            result << morse_code.at(token);
        }
        catch (const std::exception &e)
        {
            std::cerr << " ! There is no alias for: \"" << token << "\"" << std::endl;
            throw;
        }
    }

    return result.str();
}

_______________________________________________
#include <numeric>
#include <algorithm>
#include <regex>
#include <cmath>
extern std::map <std::string, std::string> morse_code;

std::string& trim( std::string& s) {
  auto sbegin = std::find(s.begin() ,s.end() , '1');
  s.erase(s.begin(),sbegin);
  auto send=    std::find(s.rbegin(),s.rend(), '1').base();
  s.erase(send,s.end());
  return s;
}

std::vector<std::pair<int,bool>>& calibrating(std::vector<std::pair<int,bool>>& arr){

  if(arr.size()==0) return arr; // no symbols
  if(arr.size()==1){arr[0].first = 1; return arr;} // one symbols always dot
  
  std::vector<std::pair<int,bool>> signals;
  std::vector<std::pair<int,bool>> pouses;
  std::copy_if(arr.begin(),arr.end(),back_inserter(signals),[](auto val){return val.second;});
  std::copy_if(arr.begin(),arr.end(),back_inserter(pouses),[](auto val){return !val.second;});
    
  auto [min_signal,max_signal] = std::minmax_element(signals.begin(), signals.end());
  auto [min_pouse,max_pouse]   = std::minmax_element(pouses.begin() , pouses.end());
  
  std::cout << "Parameters: min_sig:"<<min_signal->first << " max_signal:" << max_signal->first << " min_space:" << min_pouse->first << " max_space:" <<  max_pouse->first << std::endl;

  float mis = min_signal->first; //MIn Signal
  float mas = max_signal->first; //Max Signal
  float mip = min_pouse->first;  //MIn Pouse
  float map = max_pouse->first;  //MAx Pouse
  
  float dot = std::min(mis,mip); // dot is chousen as minimal received datagram  (it is probably underestimated and usually it is simply 1)
  float dash = mas;              // dash is maximal received signal is usually overestimated
  float pouse = map;             // pouse is maximal received space it is also overestimated
  
  if(mis == mas) dash  = 3* (dot-0.2f  )+0.1f; // in short test messages determined based on dot size;
    else dash-=1.8f*dot;  // in long messages removed overestimation;
  
  if(mip == map) pouse = 7* (dot - 0.2f)+0.1f;
    else pouse-=1.8f*dot;

  float dd_thereshold = (dot + dash)/2;
  float dp_thereshold = (pouse + dash)/2;
  
  // quite inneficient but simple way to define groups  ( k-means analog)
  std::vector<std::pair<int,bool>> dots, dashes,spaces;
  for(int i=0;i<3;i++){
  std::copy_if(arr.begin(),arr.end(),back_inserter(dots),  [dd_thereshold]              (auto val){return val.first<dd_thereshold;});
  if(dots.size())
    dot = std::accumulate(dots.begin(),dots.end(),0.0f,[](float sum,auto pr){return sum + pr.first;})/dots.size();
  std::copy_if(arr.begin(),arr.end(),back_inserter(dashes),[dd_thereshold,dp_thereshold](auto val){return (val.first>=dd_thereshold)&&(val.second ||(val.first<dp_thereshold));});
  if(dashes.size())
    dash = std::accumulate(dashes.begin(),dashes.end(),0.0f,[](float sum,auto pr){return sum + pr.first;})/dashes.size();
  std::copy_if(arr.begin(),arr.end(),back_inserter(spaces),[dp_thereshold]              (auto val){return !val.second &&(val.first>=dp_thereshold);});
  if(spaces.size())
    pouse = std::accumulate(spaces.begin(),spaces.end(),0.0f,[](float sum,auto pr){return sum + pr.first;})/spaces.size();
    
    dd_thereshold = (dot + dash)/2;
    dp_thereshold = (pouse + dash)/2;
    dots.resize(0);dashes.resize(0);spaces.resize(0);
  }
  
  
  if(dot>3){ // TITANIC adjustment: signals are longer 
    dd_thereshold+=1.0f;
    dp_thereshold+=1.0f;
  }
  std::cout << "results: dot:"<<dot << " dash:" << dash<< " pouse:" << pouse << " thereshold:" <<  dd_thereshold << " pouse:"<< dp_thereshold<< std::endl;
  
  for(auto& val:arr){
      if(val.first>dp_thereshold)        val.first = 7;
      else  if(val.first>dd_thereshold)  val.first = 3;
      else                               val.first = 1;
  }
  return arr;
}

std::vector<std::pair<int,bool>> sampling(const std::string& s){
  std::regex word_regex("([1]+|[0]+)");
  auto words_begin = std::sregex_iterator(s.begin(), s.end(), word_regex);
  auto words_end = std::sregex_iterator();
  std::vector<std::pair<int,bool>> ret;
  for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
    std::string match_str = i->str();
    ret.push_back(std::make_pair(match_str.size(),match_str[0]=='1'));
  }
  return ret;
}

std::string decodeBitsAdvanced (const char *bits) {
  std::cout <<"source:'" << bits << "'"<<std::endl;
  std::string signal(bits); 
  signal = trim(signal);
  auto sample = sampling(signal);
  auto calibrated = calibrating(sample);
  std::string result = std::accumulate(calibrated.begin(),calibrated.end(),std::string(""),[](std::string res,std::pair<int,bool> val){
    if(val.second){
      if(val.first == 1) return res + '.';
      else return res + '-';
    }
    else{
      if(val.first == 1) return res ;
      else if(val.first == 3) return res + ' ';
      else return res + "   ";
    }
    return res;
  });
  std::cout <<"result : '" <<result << "'"<<std::endl;
  return result;
}

std::string decodeMorse (std::string morseCode) {
    // ToDo: Accept dots, dashes and spaces, return human-readable message
  std::vector<std::string> tokens;
  std::string token;
  std::string decoded;
  morse_code[" "]=" ";
  
  //token is a string of at least one symbol which ends with space and has sise of at least two symbols
  auto isToken = [](const std::string &s){return  s.size()>1&&std::isspace(s.back());};
  
  //parser
  token = std::accumulate(
    std::find_if(morseCode.begin(), morseCode.end(),std::not1(std::ptr_fun<int, int>(std::isspace))), //start from first non space symbol
    std::find_if(morseCode.rbegin(), morseCode.rend(),std::not1(std::ptr_fun<int, int>(std::isspace))).base(), //end with last not space 
    token,
    [&tokens,isToken](std::string& token,const char c){ token +=c;
      if(isToken(token)){token.pop_back();tokens.push_back(token);token.resize(0);}
      return token;
    });
  tokens.push_back(token); // last token;
  
  //decoder
  if(tokens.size()==1 && token.size()==0)
    return "";
  decoded = std::accumulate(
    tokens.begin(),
    tokens.end(),
    decoded,
    [](std::string& decoded,const std::string& s){
      auto isThere = morse_code.find(s);
      std::string letter = "?";
      if(isThere!=morse_code.end())
        letter = isThere->second;
      decoded +=  letter;return decoded;});
  std::cout << "msg:" << decoded << std::endl;
  return decoded;
}

_______________________________________________
std::vector<int> toOnAndOffTimes(const char* bits) {
  std::vector<int> ret;
  bool isOn = false;
  int cnt = 0;
  while(*bits){
    bool bitIsOn = *bits != '0';
    if(bitIsOn == isOn) {
      cnt++;
    } else {
      if(cnt>0 && (isOn == (ret.size()%2==0))) {
        ret.push_back(cnt);
      }
      cnt = 1;
    }
    isOn = bitIsOn;
    bits++;
  }
  if(isOn) {
    ret.push_back(cnt);
  }
  return ret;
}

std::string decodeOnAndOffTimes(const std::vector<int>& i_data, int longOnTime, int mediumOffTime, int longOffTime) {
  std::string ret;
  bool isOn = true;
  for(const auto& cnt : i_data){
    if(isOn){
      ret += (cnt>=longOnTime)?"-":".";
    } else if(cnt>=mediumOffTime) {
      ret += (cnt>=longOffTime)?"   ":" ";
    }
    isOn = !isOn;
  }
  return ret;
}

std::string decodeBitsAdvanced (const char *bits) {
  auto asCounts = toOnAndOffTimes(bits);
  bool isOn = true;
  int shortestPulse = std::numeric_limits<int>::max();
  int longestOnPulse = 0;
  for(const auto& cnt : asCounts){
    if(cnt<shortestPulse) shortestPulse = cnt;
    if(isOn && (cnt > longestOnPulse)) longestOnPulse = cnt;
    isOn = !isOn;
  }
  int longOn = std::max((longestOnPulse*10)/17, shortestPulse+1); // It just works
  return decodeOnAndOffTimes(asCounts, longOn, longOn, longOn*2 + 1);
}

std::string decodeMorse (std::string morseCode) {
  std::string out;
  std::string symbol = "";
  int spaces = 0;
  for(const auto& c : morseCode){
    if(c==' ') {
      if(!symbol.empty()){
        auto searchResult = morse_code.find(symbol);
        if(searchResult == morse_code.end()) {
          throw std::exception();
        }
        if(spaces>1) out += " ";
        out += searchResult->second;
        spaces = 1;
      } else {
        spaces++;
      }
      symbol = "";
    } else {
      symbol += c;
    }
  }
  if(!symbol.empty()){
    auto searchResult = morse_code.find(symbol);
    if(morse_code.find(symbol) == morse_code.end()) {
      throw std::exception();
    }
    if(spaces>1) out += " ";
    out += searchResult->second;
  }
  return out;
}
_______________________________________________
std::vector<int> toOnAndOffTimes(const char* bits) {
  std::vector<int> ret;
  bool isOn = false;
  int cnt = 0;
  while(*bits){
    bool bitIsOn = *bits != '0';
    if(bitIsOn == isOn) {
      cnt++;
    } else {
      if(cnt>0 && (isOn == (ret.size()%2==0))) {
        ret.push_back(cnt);
      }
      cnt = 1;
    }
    isOn = bitIsOn;
    bits++;
  }
  if(isOn) {
    ret.push_back(cnt);
  }
  return ret;
}

std::string decodeOnAndOffTimes(const std::vector<int>& i_data, int longOnTime, int mediumOffTime, int longOffTime) {
  std::string ret;
  bool isOn = true;
  for(const auto& cnt : i_data){
    if(isOn){
      ret += (cnt>=longOnTime)?"-":".";
    } else if(cnt>=mediumOffTime) {
      ret += (cnt>=longOffTime)?"   ":" ";
    }
    isOn = !isOn;
  }
  return ret;
}

bool parseMorseCode(const std::string& morseCode, std::string& out) {
  std::string symbol = "";
  int spaces = 0;
  for(const auto& c : morseCode){
    if(c==' ') {
      if(!symbol.empty()){
        auto searchResult = morse_code.find(symbol);
        if((searchResult == morse_code.end()) || (searchResult->second.empty())) {
          return false;
        }
        if(spaces>1) out += " ";
        out += searchResult->second;
        spaces = 1;
      } else {
        spaces++;
      }
      symbol = "";
    } else {
      symbol += c;
    }
  }
  if(!symbol.empty()){
    auto searchResult = morse_code.find(symbol);
    if((morse_code.find(symbol) == morse_code.end()) || (searchResult->second.empty())) {
      return false;
    }
    if(spaces>1) out += " ";
    out += searchResult->second;
  }
  return true;
}

class Histogram {
  public:
  std::vector<int> data;
  
  void put(int i, int n){
    while(int(data.size())<=i){
      data.push_back(0);
    }
    data[i] += n;
  }
  
  void print(std::string title) const {
    std::string printStr = title;
    for(size_t i=0;i<data.size();i++){
      printStr += "\n" + std::to_string(i) + ": " + std::to_string(data[i]);
    }
    std::cout << printStr << std::endl;
  }
  
  int min() const {
    for(size_t i=0;i<data.size();i++){
      if(data[i]) return i;
    }
    return -1;
  }
  
  int max() const {
    return int(data.size())-1;
  }
};

std::string decodeBitsAdvanced (const char *bits) {
  auto asCounts = toOnAndOffTimes(bits);
  Histogram histogramOn;
  Histogram histogramOff;
  bool isOn = true;
  for(const auto& cnt : asCounts){
    if(isOn){
      histogramOn.put(cnt, 1);
    } else {
      histogramOff.put(cnt, 1);
    }
    isOn = !isOn;
  }
  histogramOn.print("On:");
  histogramOff.print("Off:");
  int longOn = 4;
  int shortestPulse = histogramOn.min();
  if(histogramOff.min()!=-1){
    shortestPulse = std::min(histogramOn.min(), histogramOff.min());
  }
  if(histogramOff.max()<=10){
    longOn = 0;
  }
  if(histogramOff.max()>=12)
  {
    longOn = (histogramOff.max()*10)/33;
  }
  longOn = std::max(longOn, shortestPulse+1);
  int mediumOff = longOn;
  int longOff = longOn*2 + 1;
  std::string cleanMorse = decodeOnAndOffTimes(asCounts, longOn, mediumOff, longOff);
  std::string out;
  if(!parseMorseCode(cleanMorse, out)) {
    std::cout << "Failed" << std::endl;
    std::cout << cleanMorse << std::endl;
    std::cout << out << std::endl;
    throw std::exception();
  }
  return cleanMorse;
}

std::string decodeMorse (std::string morseCode) {
  std::cout << morseCode << std::endl;
  std::string out;
  parseMorseCode(morseCode, out);
  std::cout << out << std::endl;
  return out;
}
