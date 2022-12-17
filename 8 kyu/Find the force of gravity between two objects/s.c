5b609ebc8f47bd595e000627


double solution(const double* values, const char** units) {
  const double GRAVITY = 6.67E-11;
  double objects[3] = {values[0], values[1], values[2]};  
  
  for( int i = 0; i < 3; i++){        
    if(units[i] == "g") objects[i] /= 1000.0; 
    else if(units[i] == "mg") objects[i] /= 1E+6;
    else if(units[i] == "μg") objects[i] /= 1E+9;
    else if(units[i] == "lb") objects[i] *= 0.453592;    
    else if(units[i] == "cm") objects[i] /= 100.0; 
    else if(units[i] == "mm") objects[i] /= 1000.0; 
    else if(units[i] == "μm") objects[i] /= 1E+6;
    else if(units[i] == "ft") objects[i] *= 0.3048;
  }
  
  return (GRAVITY * objects[0] * objects[1]) / pow(objects[2], 2);
}
____________________________________
#include<string.h>
#define G 6.67e-11

double solution(double* values, const char** units) {
    for(int i = 0; i < 2; ++i) {
        if(strcmp(units[i], "g") == 0) {
            values[i] /= 1000.0;
        }
        else if(strcmp(units[i], "mg") == 0) {
            values[i] /= 1000000.0;
        }
        else if(strcmp(units[i], "μg") == 0 ) {
            values[i] /= 1.0e+9;
        }
        else if(strcmp(units[i], "lb") == 0) {
            values[i] *= 0.453592;
        }
    }
    if(strcmp(units[2], "cm") == 0) {
        values[2] /= 100.0;
    }
    else if(strcmp(units[2], "mm") == 0) {
        values[2] /= 1000.0;
    }
    else if(strcmp(units[2], "μm") == 0) {
        values[2] /= 1000000.0; 
    }
    else if(strcmp(units[2], "ft") == 0) {
        values[2] *= 0.3048;
    }
    
    return G * (values[0] * values[1]) / (values[2] * values[2]);
}
____________________________________
double unitMultiplier(const char* unit){
	if(unit == "g") return 1e-3;
	else if(unit == "mg") return 1e-6;
	else if(unit == "μg") return 1e-9;
	else if(unit == "lb") return 0.453592;
	else if(unit == "cm") return 1e-2;
	else if(unit == "mm") return 1e-3;
	else if(unit == "μm") return 1e-6;
	else if(unit == "ft") return 0.3048;
	else return 1;
}

double solution(const double* values, const char** units) {
	double result = 6.67e-11;
	result *= values[0]*unitMultiplier(units[0]);
	result *= values[1]*unitMultiplier(units[1]);
	result /= values[2]*unitMultiplier(units[2]);
  result /= values[2]*unitMultiplier(units[2]);
	return result;
}
