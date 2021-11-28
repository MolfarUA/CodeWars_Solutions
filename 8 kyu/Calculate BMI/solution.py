def bmi(weight, height):
	bmi = weight/(height**2)
    
	if bmi <= 18.5:
		print("Underweight")
		return "Underweight"
	if bmi <= 25.0:
		print("Normal")
		return "Normal"
	if bmi <= 30.0:
		print("Overweight")
		return "Overweight"
	if bmi > 30:
		print("Obese")
		return "Obese"
##########################
def bmi(weight, height):
    b = weight / height ** 2
    return ['Underweight', 'Normal', 'Overweight', 'Obese'][(b > 30) + (b > 25) + (b > 18.5)]
#####################
def bmi(weight, height):
    bmi = weight / height ** 2
    return 'Underweight' if bmi <= 18.5 else 'Normal' if bmi <= 25.0 else 'Overweight' if bmi <= 30.0 else "Obese"
##################
bmi = lambda w,h: (lambda b=w/h**2: ["Underweight", "Normal", "Overweight", "Obese"][(18.5<b) + (25<b) + (30<b)])()
###############
bmi=lambda w,h:next(s for s,t in zip("Obese Overweight Normal Underweight".split(),(30,25,18.5,0))if w/h/h>t)
#################
def bmi(weight, height):
    result = weight / height / height
    return "Underweight Normal Overweight Obese".split()[
            (result > 18.5) +
            (result > 25.0) +
            (result > 30.0)]
####################
def bmi(weight, height):
    bmeye = (weight/(height**2))
    if bmeye <= 18.5: return("Underweight")
    elif bmeye <= 25.0: return("Normal")
    elif bmeye <= 30.0: return("Overweight")
    elif bmeye > 30: return("Obese")
####################
def bmi(weight, height):
    ratio = weight / height ** 2
    
    if ratio > 18.5:
        if ratio > 25:
            if ratio > 30:
                return 'Obese'
            return 'Overweight'
        return 'Normal'
    return 'Underweight'
######################
arr = zip('Underweight Normal Overweight Obese'.split(), (0, 18.5, 25, 30))

bmi = lambda weight, height: (lambda idx: next(txt for txt, val in reversed(arr) if idx > val))(weight / height ** 2)
##############
def bmi(weight, height):
    n = weight/height/height
    return { 
        n   >  30: 'Obese',
        n <= 30.0: 'Overweight',
        n <= 25.0: 'Normal',
        n <= 18.5: 'Underweight',
    }[True]
################
def bmi(weight, height):
    return ["Overweight","Obese"][weight/(height*height)>30] if weight/(height*height) > 25 else ["Underweight","Normal"][weight/(height*height)>18.5]
###############
def bmi(weight, height):
  bmi_val = weight / height**2
  return get_weight_class(bmi_val)

# bmi_ranges start open bound & end closed bound
def get_weight_class(bmi_val):
  bmi_ranges = [(0, 18.5), (18.5, 25), (25, 30), (30, float("inf"))]
  weight_classes = {
    (0, 18.5): "Underweight",
    (18.5, 25): "Normal",
    (25, 30): "Overweight",
    (30, float("inf")): "Obese",
  }
  # see what range bmi belongs to with binary search
  start = 0
  end = len(bmi_ranges) - 1

  while not(start > end):
    mid_i = start + abs(end - start)//2
    range_start, range_end = bmi_ranges[mid_i]

    if range_start < bmi_val <= range_end:
      return weight_classes[(range_start, range_end)]
    elif bmi_val <= range_start:
      end = mid_i - 1
    elif bmi_val > range_end:
      start = mid_i + 1

  raise ValueError("BMI value out of range.")
######################################################
def bmi(weight, height):
    bmi = weight / height ** 2
    arr = 'Underweight Normal Overweight Obese'.split()
    return arr[(bmi > 18.5) + (bmi > 25) + (bmi > 30)]
##############################
bmi = lambda w, h: (lambda x: [[["Underweight", "Normal"][18.5<x<=25], "Overweight"][25<x<=30], "Obese"][x>30])(w / h**2)
