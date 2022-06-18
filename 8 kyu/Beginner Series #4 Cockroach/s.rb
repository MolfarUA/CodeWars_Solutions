55fab1ffda3e2e44f00000c6


def cockroach_speed(s)
  (s / 0.036).floor
end
__________________________
def cockroach_speed(km_per_hour)
  cm_per_km = 1000 * 100
  seconds_per_hour = 60 * 60
  cm_per_second = km_per_hour * cm_per_km / seconds_per_hour
  cm_per_second.floor
end
__________________________
def cockroach_speed(s)
  (s * (100000/3600.0)).floor
end
__________________________
def cockroach_speed(km_hr)
  (km_hr * 27.7778).floor
end
__________________________
def cockroach_speed(s)
  (s * 1000 * 100 / 60 / 60).floor
end
__________________________
def cockroach_speed(s)
  Integer(s*100000/3600)
end
