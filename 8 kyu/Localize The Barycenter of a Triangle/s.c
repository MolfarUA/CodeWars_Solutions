5601c5f6ba804403c7000004


#include <math.h>

typedef struct point {
    double x;
    double y;
} Point;

double round4 (double x) { return round(x * 1e4) / 1e4; }

Point bar_triang (Point a, Point b, Point c)
{
	return (Point) {
		.x = round4((a.x + b.x + c.x) / 3.0),
		.y = round4((a.y + b.y + c.y) / 3.0)
	};
}
__________________________________
typedef struct Point_Coordinates {
    double x;
    double y;
} coords;

coords bar_triang(coords a, coords b, coords c) {
    coords d = {round(((a.x+b.x+c.x)/3)*10000)/10000, round(((a.y+b.y+c.y)/3)*10000)/10000};
    return d;

}
__________________________________
#include <math.h>

typedef struct Point_Coordinates { double x, y; } coords;

double localize(double n) {
    return round((n / 3.0) * 1e4) / 1e4;
}

coords bar_triang(coords a, coords b, coords c) {
    return (coords) { localize(a.x + b.x + c.x),
                      localize(a.y + b.y + c.y) };
}
