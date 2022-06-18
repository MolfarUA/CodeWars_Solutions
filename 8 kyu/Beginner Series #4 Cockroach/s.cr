55fab1ffda3e2e44f00000c6


def cockroach_speed(s)
  s // 0.036
end
__________________________
def cockroach_speed(s)
  s * 100_000 // 3600
end
__________________________
def cockroach_speed(s)
  (s * 1000 / 36).to_i
end
__________________________
def cockroach_speed(s)
  (s*27.7778).floor
end
__________________________
def cockroach_speed(s)
  (s / 0.036).floor
end
