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
