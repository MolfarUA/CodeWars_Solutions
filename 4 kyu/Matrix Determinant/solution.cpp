#include <iostream>
#include <vector>

using namespace std;

long long determinant(vector< vector<long long> > m) {
  if (m.size() == 1) return m[0][0];
  long long result = 0;
  for (int i = 0; i < m.size(); i++) {
    vector< vector<long long> > submatrix;
    for (int j = 1; j < m.size(); j++) {
      vector<long long> row;
      for (int k = 0; k < m.size(); k++) if (k != i) row.push_back(m[j][k]);
      submatrix.push_back(row);
    }
    result += determinant(submatrix) * (i % 2 == 0 ? m[0][i] : -m[0][i]);
  }
  return result;
}
_____________________________________________
#include <iostream>
#include <vector>
#include <unordered_set>
#include <stdexcept>

using std::vector;
using std::unordered_set;

long long calc_minor(vector< vector<long long> > &m, size_t n_row, unordered_set<size_t> &except_cols) {
  if (n_row == m.size() - 1) {
    // find item not in the except_cols set
    for (size_t j = 0; j < m.size(); ++j) {
      if (except_cols.find(j) == except_cols.end()) return m[n_row][j];
    }
    throw std::logic_error("should be at least one item for minor");
  }
  
  long long ret = 0;
  long long v = 0;
  bool sign = true;
  for (size_t j = 0; j < m.size(); ++j) {
    if (except_cols.find(j) != except_cols.end()) continue;

    except_cols.insert(j);
    v = m[n_row][j] * calc_minor(m, n_row + 1, except_cols);
    except_cols.erase(j);

    if (sign) ret += v;
    else      ret -= v;

    sign = !sign;
  }

  return ret;
}

long long determinant(vector< vector<long long> > m) {
  if (m.size() == 1) return m[0][0];
  if (m.size() == 2) return m[0][0] * m[1][1] - m[0][1] * m[1][0];
/*  if (m.size() == 3) return m[0][0] * m[1][1] * m[2][2] - m[0][0] * m[1][2] * m[2][1] 
    - m[0][1] * m[1][0] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1]
    - m[0][2] * m[1][1] * m[2][0];
*/
  unordered_set<size_t> except_cols;
  return calc_minor(m, 0, except_cols);
}
_____________________________________________
#include <iostream>
#include <vector>
#include <cmath>

using namespace std;


long long determinant(vector< vector<long long> > m) {
    long long det = 0; // Initialize result
    // Base case: if matrix contains single element
    if (m.size() == 1) {
        return m[0][0];
    }
    else if (m.size() == 2) {
        det = (m[0][0] * m[1][1] - m[0][1] * m[1][0]);
        return det;
    }
    else {
        for (int p = 0; p < m[0].size(); p++) {
            vector <vector<long long>> tempM;
            for (int i = 1; i < m.size(); i++) {
                vector<long long> tempRow;
                for (int j = 0; j < m[i].size(); j++) {
                    if (j != p) {
                        tempRow.push_back(m[i][j]);
                    }
                }
                if (tempRow.size() > 0)
                    tempM.push_back(tempRow);
            }
            det = det + m[0][p] * pow(-1,p) * determinant(tempM);
        }
        return det;
    }
}
_____________________________________________
#include <iostream>
#include <vector>

using namespace std;

long long determinant(vector< vector<long long> > m) {
  // TODO: Return the determinant of the square matrix passed in
  auto n = m.size();
  if (n == 1) return m[0][0];
  else if (n == 2) return m[0][0] * m[1][1] - m[0][1] * m[1][0];
  long long det = 0;
  bool flag = true;
  for (int i = 0; i < n; ++i) {
    vector< vector<long long> > minor;
    for (int j = 1; j < n; ++j) {
      vector<long long> row;
      for (int k = 0; k < n; k++) {
        if (k == i) continue;
        else row.push_back(m[j][k]);
      }
      minor.push_back(row);
    }
    det += m[0][i] * (flag ? determinant(minor) : -determinant(minor));
    flag = !flag;
  }
  return det;
}
