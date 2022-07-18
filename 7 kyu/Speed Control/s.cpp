56484848ba95170a8000004d
  
  
class GpsSpeed
{
public:
  static int gps(int s, std::vector<double> &x) {
      if(x.size() < 1)
          return 0;
      std::vector<double> bar(x.size());
      std::transform(x.begin()+1, x.end(), x.begin(), bar.begin(), std::minus<double>());
      return (3600 * (*max_element(bar.begin(), bar.end())) / s);
  }

};
_____________________________
class GpsSpeed
{
public:
    static int gps(int s, std::vector<double> &x)
    {
      int max = 0;
      
      for (int i = 1; i < x.size(); ++i) {
        double dist = x[i] - x[i - 1];
        double speed = dist * 3600.0 / s;
        if (speed > max) {
          max = speed;
        }
      }
        
      return max;
    }
};
_____________________________
class GpsSpeed
{
public:
    static int gps(int s, std::vector<double> &x);
};

int GpsSpeed::gps(int s, std::vector<double> &x)
{
    double maxDis, subDis;
    int res = 0;
    if(x.size() > 1)
    {
        for(int i = 1; i < x.size(); ++i)
        {
            subDis = x[i] - x[i - 1];
            maxDis = (maxDis > subDis) ? maxDis : subDis;
        }
        
        res = maxDis * 3600 / s;
    }
    
    return res;
}
