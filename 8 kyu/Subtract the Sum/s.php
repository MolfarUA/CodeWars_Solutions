56c5847f27be2c3db20009c3


function subtractSum($n) {
  return "apple";
}
_______________________________________
const FRUITS = ['kiwi', 'pear', 'kiwi', 'banana', 'melon', 'banana', 'melon', 'pineapple', 'apple', 'pineapple', 'cucumber', 'pineapple', 'cucumber', 'orange', 'grape', 'orange', 'grape', 'apple', 'grape', 'cherry', 'pear', 'cherry', 'pear', 'kiwi', 'banana', 'kiwi', 'apple', 'melon', 'banana', 'melon', 'pineapple', 'melon', 'pineapple', 'cucumber', 'orange', 'apple', 'orange', 'grape', 'orange', 'grape', 'cherry', 'pear', 'cherry', 'pear', 'apple', 'pear', 'kiwi', 'banana', 'kiwi', 'banana', 'melon', 'pineapple', 'melon', 'apple', 'cucumber', 'pineapple', 'cucumber', 'orange', 'cucumber', 'orange', 'grape', 'cherry', 'apple', 'cherry', 'pear', 'cherry', 'pear', 'kiwi', 'pear', 'kiwi', 'banana', 'apple', 'banana', 'melon', 'pineapple', 'melon', 'pineapple', 'cucumber', 'pineapple', 'cucumber', 'apple', 'grape', 'orange', 'grape', 'cherry', 'grape', 'cherry', 'pear', 'cherry', 'apple', 'kiwi', 'banana', 'kiwi', 'banana', 'melon', 'banana', 'melon', 'pineapple', 'apple', 'pineapple'];

function subtractSum(int $n)
{
    if ($n < 10 || $n > 10000) {
        throw  new \InvalidArgumentException();
    }
    
    $newN = $n - array_sum(str_split($n));
    
    return FRUITS[$newN - 1] ?? subtractSum($newN);
}
_______________________________________
function subtractSum($n) {
  $list = [
    'kiwi' => [1, 3, 24, 26, 47, 49, 68, 70, 91, 93],
    'pear' => [2, 21, 23, 42, 44, 46, 65, 67, 69, 88],
    'banana' => [4, 6, 25, 29, 48, 50, 71, 73, 92, 94, 96],
    'melon' => [5, 7, 28, 30, 32, 51, 53, 74, 76, 95, 97],
    'pineapple' => [8, 10, 12, 31, 33, 52, 56, 75, 77, 79, 98, 100],
    'apple' => [9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99],
    'cucumber' => [11, 13, 34, 55, 57, 59, 78, 80], 
    'orange' => [35, 37, 39, 58, 60, 83],
    'grape' => [38, 40, 61, 82, 84, 86],
    'cherry' => [41, 43, 62, 64, 66, 85, 87, 89]
  ];

  $n -= array_sum(str_split($n));
  
  foreach ($list as $key => $value) {
    if (in_array($n, $value)) {
      return $key;
    }
  }
  
  return subtractSum($n);
}
