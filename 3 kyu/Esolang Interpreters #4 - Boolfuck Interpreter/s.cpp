5861487fdb20cff3ab000030
  
  
#include <cstdlib>
#include <string>
#include <vector>
#include <stack>
#include <map>

char *boolfuck (const char *code, const char *input) 
{
    std::map<int, int> other_brace;
    std::stack<int> loops;
    for( int i=0; code[i] != 0; i++ )
        switch( code[i] ){
            case '[': loops.push(i); break;
            case ']': other_brace[i] = loops.top();
                      other_brace[loops.top()] = i;
                      loops.pop();
        }

    int iptr = 0;
    int optr = 0;
    int mptr = 0;
    std::string out;
    std::vector<uint8_t> mem = {0};
    int rbit, mbit;

    for(int cptr=0; code[cptr]!=0; cptr++ ){
        switch(code[cptr]){
            case '+': mem[mptr>>3] ^= 1 << (mptr&7); break;
            case ',': rbit = !!(input[iptr>>3] & 1 << (iptr&7));
                      mbit = !!(  mem[mptr>>3] & 1 << (mptr&7));
                      if( rbit != mbit ) mem[mptr>>3] ^= 1 << (mptr&7);
                      if( input[iptr>>3]) iptr++;
                      break;
            case ';': if( optr>>3 == out.size()) out.push_back(0);
                      mbit = !!(  mem[mptr>>3] & 1 << (mptr&7));
                      out[optr>>3] |= mbit << (optr&7);
                      optr++;
                      break;
            case '>': mptr++;
                      if(mptr>>3 == mem.size()) mem.push_back(0);
                      break;
            case '<': mptr--;
                      if(mptr < 0){
                          mem.insert(mem.begin(), 0);
                          mptr = 7;
                      }
                      break;
            case '[': mbit = !!(  mem[mptr>>3] & 1 << (mptr&7));
                      if( !mbit ) cptr = other_brace[cptr];
                      break;
            case ']': mbit = !!(  mem[mptr>>3] & 1 << (mptr&7));
                      if(  mbit ) cptr = other_brace[cptr];
        }
    }
    char *output = new char[out.length() + 1];
    std::strcpy(output, out.c_str());
    return output;
}
_____________________________
#include <cstdlib>

char readBit(const char* input, int isize, int& p) {
  if (!input || p >= isize) {
    return 0;
  }

  int byte = p >> 3;
  return (input[byte] >> (p++ & 7)) & 1;
}

void writeBit(std::vector<char>& output, int& p, char v) {
  int byte = p >> 3;
  if (output.size() < size_t(byte + 1)) {
    output.push_back(0);
  }
  v = (v << (p++ & 7));
  output[byte] |= v;
}

void buildLoopMap(std::map<int, int>& map, const char* code) {
  std::stack<int> stack;
  int i = 0; char c;
  while (( c = code[i]) != 0) {
    if (c == '[') {
      stack.push(i);
    } else if (c == ']') {
      int first = stack.top();
      stack.pop();
      map[first] = i;
      map[i] = first;
    }
    i++;
  }
}

char *boolfuck (const char *code, const char *input) {
  std::vector<char> output;
  std::vector<char> cells(30000, 0);
  int p = 0;
  int maxp = 0;
  int ip = 0; // input stream pointer
  int op = 0; // output stream pointer
  int isize = strlen(input) * 8;

  std::map<int, int> block;
  buildLoopMap(block, code);

  int i = 0; char c;
  while (( c = code[i]) != 0) {
    switch (c) {
      case '+': cells[p] ^= 1; break; // flip
      case ',': cells[p] = readBit(input, isize, ip); break; // read
      case ';': writeBit(output, op, cells[p]); break; // write
      case '<': if (p == 0) cells.insert(cells.begin(), 0); else p--; break;
      case '>': if (cells.size() - 1) cells.push_back(0); p++; maxp = maxp < p ? p : maxp; break;
      case '[': if (!cells[p]) {
        // skip to ]
        i = block[i];
      }
      break;
      case ']': {
        if (cells[p]) {
          i = block[i] - 1;
        }
      }
      break;
    }

    i++;
  }

  std::string str(output.begin(), output.end());
  char* out = (char*) calloc (str.size() + 1, 1);
  strncpy(out, str.c_str(), str.size());
  return out;
}
_____________________________
#include <cstdlib>
#include <string>
#include <map>

char *boolfuck(const char *code, const char *input)
{
    struct
    {
        operator char *()
        {
            return strdup((std::move(buf) + acc).data());
        }
        
        void operator ()(bool b)
        {
            acc |= b << bp++;
            if (bp == 8) bp = 0, buf += acc, acc = 0;
        }
        
    private:
        std::string buf;
        char bp = 0, acc = 0;
    } output;

    auto getb = [input, bp = 0]() mutable -> bool
    {
        if (bp == 8) bp = 0, ++input;
        return *input && *input >> bp++ & 1;
    };
    
    std::map<long long, bool> mem;
    long long mp = 0;
    
    for (size_t clen = strlen(code), ip = 0; ip < clen; ++ip)
    {
        switch (code[ip])
        {
        case '+':
        {
            mem[mp] ^= 1;
            break;
        }
        case ',':
        {
            mem[mp] = getb();
            break;
        }
        case ';':
        {
            output(mem[mp]);
            break;
        }
        case '<':
        {
            --mp;
            break;
        }
        case '>':
        {
            ++mp;
            break;
        }
        case '[':
        {
            if (!mem[mp])
            {
                int brackets_count = 0; // count ] to skip
                while (code[++ip] != ']' || brackets_count != 0)
                {
                    switch (code[ip])
                    {
                    case '[': ++brackets_count; break;
                    case ']': --brackets_count;
                    }
                }
            }
            break;
        }
        case ']':
        {
            if (mem[mp])
            {
                int brackets_count = 0; // count [ to skip
                while (code[--ip] != '[' || brackets_count != 0)
                {
                    switch (code[ip])
                    {
                    case ']': ++brackets_count; break;
                    case '[': --brackets_count;
                    }
                }
            }
        }
        }
    }

    return output;
}
