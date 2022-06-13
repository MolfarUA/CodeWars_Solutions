def monty_hall(correct_door_number, participant_guesses)
  (participant_guesses.grep_v(correct_door_number).size * 100.0 / participant_guesses.size).round
end
_________________________________________________
def monty_hall x,a
  ((1-a.count(x).fdiv(a.size))*100).round
end
_________________________________________________
def monty_hall(correct_door_number, participant_guesses)
  (participant_guesses.count{|g| g != correct_door_number} * 100).fdiv(participant_guesses.size).round
end
_________________________________________________
def monty_hall(correct_door_number, participant_guesses)
  (participant_guesses.count { |d| d != correct_door_number } * 100.0 / participant_guesses.size).round
end
