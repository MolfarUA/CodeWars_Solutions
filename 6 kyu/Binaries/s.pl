package Solution;

use 5.30.0;
use strict;
use warnings;
use bigint;
use Exporter qw(import);
our @EXPORT_OK = qw(code decode);

sub code {
    join('', map { $_ = sprintf('%b', $_); $_ = ('0' x (length()-1))."1$_";  } split('', shift));
}
sub decode {
    my $n = shift;
    my @s = split('', $n);
    my $i = 0;
    my $z = 0;
    my $r = '';
    while ($i < @s) {
       if ($s[$i++] == 1) {
          my $t = substr($n, $i, $z+1);
          $r .= oct('0b'.$t);
          $z = 0;
          $i += length($t);
       }
       else {
          $z++
       }
    }
    return $r;
}
__________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(code decode);

sub code {
    my $s = shift;
    my %dict = ('0' => '10', '1' => '11', '2' => '0110', '3' => '0111', '4' => '001100', '5' => '001101', '6' => '001110', '7' => '001111', '8' => '00011000', '9' => '00011001');
    my $res = '';
    for (my $i = 0; $i < length($s); $i++) {
        my $u = substr($s, $i, 1);
        my $v = $dict{$u};
        $res .= $v;
    }
    return $res;
}

sub decode {
    my $s = shift;
    my $ch = '1'; my $res = ""; my $l = -1;
    while ($s) {
        my $l = index($s, $ch) + 1;
        my $ss = substr($s, $l, $l);
        my $n = oct("0b". $ss);
        $res .= $n;
        $s = substr($s, $l * 2);
    }
    return $res;
}
