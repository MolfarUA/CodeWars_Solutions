536a155256eb459b8700077e
  
  
#include <vector>

std::vector<std::vector<int>> create_spiral(int n) {
    if (n<1) {return {};}
    std::vector<std::vector<int>> spiral(n, std::vector<int>(n));
    
    int i=0, j=0, di=0, dj=1;
    for (int x=1; x<=n*n; x++) {
        spiral[i][j] = x;
        if (i+di<0 || i+di>=n || j+dj<0 || j+dj>=n || spiral[i+di][j+dj]!=0) {
            if      (di== 0 && dj== 1) {di= 1; dj= 0;}
            else if (di== 1 && dj== 0) {di= 0; dj=-1;}
            else if (di== 0 && dj==-1) {di=-1; dj= 0;}
            else if (di==-1 && dj== 0) {di= 0; dj= 1;}
        }
        i+=di; j+=dj;
    }
    return spiral;
}
_________________________
#include <vector>

std::vector<std::vector<int>> create_spiral(int n)
{
    if (n <= 0) return {};
    std::vector<std::vector<int>> result(n);
    for (auto& row: result) row.resize(n);
    int count = 1;
    for (int layer = 0, limit = n - 1; layer * 2 < n; ++layer, --limit)
    {
        int x = layer, y = layer;
        while (x < limit) result[y][x++] = count++;
        while (y < limit) result[y++][x] = count++;
        while (x > layer) result[y][x--] = count++;
        while (y > layer) result[y--][x] = count++;
    }
    if (n % 2) result[n / 2][n / 2] = count;
    return result;
}
_________________________
#include <vector>

std::vector<std::vector<int>> create_spiral(int n)
{
    if (n < 1) return {};
    std::vector<std::vector<int>> result(n, std::vector<int>(n , 0));
    int right = n, bottom = n, top = 0, left = -1, i = 0, j = 0, k = 1, n2 = n * n;
    auto set = [&] () {
      result[j][i] = k;
      k++;
    };
    while (true) {
      if (k > n2) break;
      while (i < right) set(), i++;
      i--, j++, right--;
      if (k > n2) break;
      while (j < bottom) set(), j++;
      j--, i--, bottom--;
      if (k > n2) break;
      while (i > left) set(), i--;
      i++, j--, left++;
      if (k > n2) break;
      while (j > top) set(), j--;
      j++, i++, top++;
    }
    return result;
}
