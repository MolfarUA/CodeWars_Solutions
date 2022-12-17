5601c5f6ba804403c7000004


import java.text.DecimalFormat;

class Barycenter {
    
    public static double[] barTriang(double[] x, double[] y, double[] z)
    {
        double[] coordinates = new double[2];
        
        for(int i=0;i<2;i++){
            coordinates[i] = Double.parseDouble(new DecimalFormat("##.####").format((x[i]+y[i]+z[i])/3));
        }
        
        return coordinates;
    }
}
__________________________________
class Barycenter {
    
    public static double[] barTriang(double[] x, double[] y, double[] z)
    {
        double[] res = new double[2];
        res[0] = (double)((int)Math.round((x[0]+y[0]+z[0])/3*10000))/10000;
        res[1] = (double)((int)Math.round((x[1]+y[1]+z[1])/3*10000))/10000;
        return res;
    }
}
__________________________________
class Barycenter {
    
    public static double[] barTriang(double[] x, double[] y, double[] z)
    {
        double xCenter = (x[0] + y[0] + z[0]) / 3;
        double yCenter = (x[1] + y[1] + z[1]) / 3;
        xCenter = Double.parseDouble(String.format("%.4f", xCenter));
        yCenter = Double.parseDouble(String.format("%.4f", yCenter));
        return new double[]{xCenter, yCenter};
    }
}
__________________________________
class Barycenter {

    public static double[] barTriang(double[] x, double[] y, double[] z)
    {
      double a = (x[0] + y[0] + z[0]) / 3;
      double b = (x[1] + y[1] + z[1]) / 3;
      
      double aa = (double)Math.round(a * 10000d) / 10000d;
      double bb = (double)Math.round(b * 10000d) / 10000d;
      
      double [] c = {aa, bb};
      return c;
    }
}
