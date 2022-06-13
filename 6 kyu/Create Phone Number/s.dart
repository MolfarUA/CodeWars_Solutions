String createPhoneNumber(List numbers) {
  var n = numbers.join('');
  return '(${n.substring(0, 3)}) ${n.substring(3, 6)}-${n.substring(6)}';
}
_______________________________
String createPhoneNumber(List numbers) {
  var format = "(xxx) xxx-xxxx";
  
  for(var i = 0; i < numbers.length; i++)
  {
    format = format.replaceFirst('x', numbers[i].toString());
  }
  
  return format;
}
_______________________________
String createPhoneNumber(List numbers) => 
  '(' + numbers.getRange(0, 3).join() + 
  ') ' + numbers.getRange(3, 6).join() + 
  '-' + numbers.getRange(6, 10).join();
_______________________________
String createPhoneNumber(List n) {
  return "(${n[0]}${n[1]}${n[2]}) ${n[3]}${n[4]}${n[5]}-${n[6]}${n[7]}${n[8]}${n[9]}";
}
_______________________________
String createPhoneNumber(List<int> numbers) {
  String result = "(xxx) xxx-xxxx";
  numbers.forEach((value) {result = result.replaceFirst(new RegExp(r'x'), value.toString());});
  return(result);
}
_______________________________
/// Creates a phone number out of __ten__ given [numbers] between __0__
/// and __9__ (both inclusive).
///
/// "(XXX) XXX-XXXX" is the format of the returning phone number string.
/// The order of the [numbers] and the numbers in the phone number are the same.
/// [numbers] will not be affected by this function.
///
/// The function throws an [ArgumentError] in the following cases:
/// + [numbers] is [null]
/// + The size of [numbers] is not what is expected (10)
/// + One or more entries of [numbers] are not between 0 and 9
///
/// _Examples:_
/// ```dart
/// createPhoneNumber([0,1,2,3,4,5,6,7,8,9])    // "(012) 345-6789"
/// createPhoneNumber([3,4,2,6,4,7,4,1,3,5])    // "(342) 647-4135"
/// createPhoneNumber(null)                     // ArgumentError
/// createPhoneNumber([0,0,0,0,0,0,0,0,0,0,0])  // ArgumentError
/// createPhoneNumber([0,0,0,0,0,0,0,0,0])      // ArgumentError
/// createPhoneNumber([-1,0,0,0,0,0,0,0,0,-1])  // ArgumentError
/// createPhoneNumber([10,0,0,0,0,0,0,0,0,10])  // ArgumentError
/// ```
String createPhoneNumber(final List<int> numbers) {
  // Checking the input on validity with these functions
  nullCheck(numbers);
  inputSizeCheck(numbers);
  inputValidValuesCheck(numbers);

  // This is the solution
  return '(' +
      numbers.sublist(0, 3).join() +
      ') ' +
      numbers.sublist(3, 6).join() +
      '-' +
      numbers.sublist(6, numbers.length).join();
}

/// The Message for a null as input error
const inputListNullErrorMessage = 'Input must not be null';

/// Creates the message for an input size error
String createInputListSizeErrorMessage(final int expectedListSize) =>
    'Input should have exactly ${expectedListSize} entries';

/// Creates the message for an invalid value error
String createInputListInvalidValueErrorMessage(
        final List<int> expectedListValues) =>
    'Input should only have values from ${expectedListValues.toString()}';

/// Returns the expected input list size
int expectedInputListSize() => 10;

/// Returns the valid input list values
List<int> expectedInputListValues() => [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

/// Throws an [ArgumentError] if [numbers] is null.
void nullCheck(final List<int> numbers) {
  if (numbers == null) {
    throw ArgumentError(inputListNullErrorMessage);
  }
}

/// Throws an [ArgumentError] if [numbers] does not contain the exact amount
/// of expected values.
void inputSizeCheck(final List<int> numbers) {
  if (numbers.length > expectedInputListSize() ||
      numbers.length < expectedInputListSize()) {
    throw ArgumentError.value(numbers.length, 'message',
        createInputListSizeErrorMessage(expectedInputListSize()));
  }
}

/// Throws an [ArgumentError] if [numbers] contains one
/// values that is not valid.
void inputValidValuesCheck(final List<int> numbers) {
  var growableList = List<int>.from(numbers);
  // if there is any element that is not valid
  if (growableList
      .any((element) => !expectedInputListValues().contains(element))) {
    // remove every valid number to make the error message more understandable
    growableList
        .removeWhere((element) => expectedInputListValues().contains(element));
    growableList.join(', ');
    throw ArgumentError.value(growableList, 'message',
        createInputListInvalidValueErrorMessage(expectedInputListValues()));
  }
}
