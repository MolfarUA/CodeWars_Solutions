5786f8404c4709148f0006bf


M = (10.67 - 9.45) / (1.83 - 1.52)
B = 10.67 - M * 1.83
  
def starting_mark(height)
  (M * height + B).round(2)
end
____________________________________
def starting_mark height
  (3.935483*height + 3.46806).round 2
end
____________________________________
GUIDELINES = [
  { height: 1.52, mark:  9.45 },
  { height: 1.83, mark: 10.67 }
]

def starting_mark(height)
  (
    GUIDELINES.first.fetch(:mark) + (
      height - GUIDELINES.first.fetch(:height)
    ) * (
      GUIDELINES.last.fetch(:mark) - GUIDELINES.first.fetch(:mark)
    ) / (
      GUIDELINES.last.fetch(:height) - GUIDELINES.first.fetch(:height)
    )
  ).round(2)
end
____________________________________
def starting_mark(height)
  m = (1.83 - 1.52) / (10.67 - 9.45)
  b = 1.83 - (m * 10.67)
  ((height - b)/m).round(2)
end
