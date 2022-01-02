#include <stddef.h>

int bus_terminus (size_t nb_stops, const short bus_stops[nb_stops][2])
{
  auto bus = 0; // 🚌 :p
  for(size_t i = 0; i<nb_stops; i++)
    {
    bus += bus_stops[i][0];
    bus-= bus_stops[i][1];
  }
  return bus;
}
_____________________________________
#include <stddef.h>

int bus_terminus (size_t nb_stops, const short bus_stops[nb_stops][2])
{
  int bus = 0;
  for(int i = 0; i < nb_stops; i++){
    bus+=bus_stops[i][0]-bus_stops[i][1];   
  }
  return bus;
}
_____________________________________
#include <stddef.h>

int bus_terminus (size_t nb_stops, const short bus_stops[nb_stops][2])
{
  auto bus = 0; // 🚌 :p
  
  for(size_t i = 0; i < nb_stops; i++)
    bus += bus_stops[i][0] - bus_stops[i][1];
  
  return bus;
}
_____________________________________
#include <stddef.h>

int bus_terminus (size_t nb_stops, const short bus_stops[nb_stops][2])
{
  int people = 0;
  
  for(size_t i = 0; i < nb_stops; i++){
    for(size_t j = 0; j < 2; j++){
      if(j == 0)
        people += bus_stops[i][j];
      else
        people -= bus_stops[i][j];
    }
  }
  return people;
}
