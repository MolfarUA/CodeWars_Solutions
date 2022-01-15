package Solution;

use 5.30.0;
use strict;
use warnings;
use bigint;
use Exporter qw(import);
our @EXPORT_OK = qw(solve);

# parameter: array reference; return an array reference of 2 elements
sub solve {
    my $arr = shift; 
    my $a = @{$arr}[0]; my $b = @{$arr}[1];
    my $i = 1; my $lg = int((scalar @{$arr}) / 2);
    while ($i < $lg) {
        my $x = $a; my $y = $b; my $z = @{$arr}[2 * $i]; my $t = @{$arr}[2 * $i + 1];
        $a = abs($x * $z - $y * $t);
        $b = abs($x * $t + $y * $z);
        $i++;
    }
    return [$a, $b];
}
