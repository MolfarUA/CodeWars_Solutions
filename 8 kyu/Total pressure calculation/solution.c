double total_pressure(double mM1, double mM2, double gM1, double gM2, double v, double t) {
    return (gM1 / mM1 + gM2 / mM2) * 0.082 * (t + 273.15) / v;
}

#####################
double total_pressure(double M1, double M2, double m1, double m2, double V, double t) {

    double T=t+273.15;
    double R=0.082;
    return (m1/M1+m2/M2)*R*T/V;

}

####################
double total_pressure(double mM1, double mM2, double gM1, double gM2, double v, double t) 
{
    static double R = 0.082;
  
    double tK = 273.15 + t;
      
    return (gM1 / mM1 + gM2 / mM2) * R * tK / v;
}

###############
double total_pressure(double molar_mass1, double molar_mass2, double given_mass1, double given_mass2, double v, double t) {
double R = 0.082;
double T = t + 273.15;
double A = (given_mass1/molar_mass1);
double B = (given_mass2/molar_mass2);
double C = (A+B);
double D = (R*T);
double E = (C*D);
double F = E/v;

return F;//  <----  hajime!

}

################
double total_pressure(double M1, double M2, double m1, double m2, double v, double t) {
  return (m1 / M1 + m2 / M2) * 0.082 * (273.15 + t) / v;
}

#####################
double total_pressure(double molar_mass1, double molar_mass2, double given_mass1, double given_mass2, double v, double t) {
    double a = given_mass1 * 0.001 / molar_mass1;
    double b = given_mass2 * 0.001 / molar_mass2;
    t += 273.15;
    return (((a + b) * 0.082 * t) / v) * 1000;
}

###############
double total_pressure(double molar_mass1, double molar_mass2, double given_mass1, double given_mass2, double v, double t) {
  double res = 0;
  double R = 0.082;
  double T = t + 273.15;
  
  res = ((given_mass1 / molar_mass1) + (given_mass2 / molar_mass2)) * R * T / v;

  return res;
}
