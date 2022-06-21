58708934a44cfccca60000c4


function highlight(string $code): string {
  return preg_replace(
    array(
      '/(F+)/', 
      '/(L+)/', 
      '/(R+)/',
      '/(\d+)/',
    ), 
    array(
      '<span style="color: pink">$1</span>', 
      '<span style="color: red">$1</span>', 
      '<span style="color: green">$1</span>',
      '<span style="color: orange">$1</span>',
    ), 
    $code
  );
}
__________________________
function highlight(string $code): string {
  $patterns = [
    '/(F+)/',
    '/(L+)/',
    '/(R+)/',
    '/([0-9]+)/',
  ];
  $replacements = [
    '<span style="color: pink">$1</span>',
    '<span style="color: red">$1</span>',
    '<span style="color: green">$1</span>',
    '<span style="color: orange">$1</span>',
  ];
  return preg_replace($patterns, $replacements, $code);
}
__________________________
function highlight(string $code): string {
  $code = preg_replace('/(F+)/', '<span style="color: pink">$1</span>', $code);
  $code = preg_replace('/(L+)/', '<span style="color: red">$1</span>', $code);
  $code = preg_replace('/(R+)/', '<span style="color: green">$1</span>', $code);
  $code = preg_replace('/([0-9]+)/', '<span style="color: orange">$1</span>', $code);

  return $code;
}
