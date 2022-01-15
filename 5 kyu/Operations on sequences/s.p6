use v6;
unit module Solution;

# input: List of integers; output: List of two not negative integers
sub solve(List $arr --> List) is export(:solve) {
    my $a = $arr[0]; my $b = $arr[1];
    my $i = 1; my $lg = $arr.elems div 2;
    while ($i < $lg) {
        my ($x, $y) = ($a, $b); 
        my ($z, $t) = ($arr[2 * $i], $arr[2 * $i + 1]); 
        $a = abs($x * $z - $y * $t);
        $b = abs($x * $t + $y * $z);
        $i++;
    }
    ($a, $b);
}
