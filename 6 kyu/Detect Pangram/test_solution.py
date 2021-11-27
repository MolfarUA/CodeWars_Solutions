pangram = "The quick brown fox jumps over the lazy dog."
test.assert_equals(is_pangram(pangram), True)
# pangrams:
pangram1 = "Cwm fjord bank glyphs vext quiz"
pangram2 = "Pack my box with five dozen liquor jugs."
pangram3 = "How quickly daft jumping zebras vex."
pangram4 = "ABCD45EFGH,IJK,LMNOPQR56STUVW3XYZ"
test.assert_equals(is_pangram(pangram1), True, pangram1 + " is a pangram")
test.assert_equals(is_pangram(pangram2), True, pangram2 + " is a pangram")
test.assert_equals(is_pangram(pangram3), True, pangram3 + " is a pangram")  
test.assert_equals(is_pangram(pangram4), True, pangram4 + " is a pangram")

not_pangram1 = "This isn't a pangram!"
test.assert_equals(is_pangram(not_pangram1), False, not_pangram1 + " is not a pangram.")
not_pangram2 = "abcdefghijklmopqrstuvwxyz"
test.assert_equals(is_pangram(not_pangram2), False, not_pangram2 + " is not a pangram.")
not_pangram3 = "Aacdefghijklmnopqrstuvwxyz"
test.assert_equals(is_pangram(not_pangram3), False, not_pangram3 + " is not a pangram.")
