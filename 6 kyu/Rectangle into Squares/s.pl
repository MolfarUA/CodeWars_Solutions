55466989aeecab5aac00003e


package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(sq_in_rect);

sub sq_in_rect {
    my ($a, $b) = @_;
    my ($l, $w, @arr) = (0, 0, ());
    if ($a == $b) { return @arr; }
    while ($a > 0 && $b > 0) {
        $l = $a > $b ? $a : $b;
        $w = $a < $b ? $a : $b;
        push @arr, $w;
        $a = $w;
        $b = $l - $w;
    }
    return \@arr;
}
______________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(sq_in_rect);

sub sq_in_rect {
    my ($len, $wid) = @_;
    return [] if ($len == $wid);
    my @ret = ();
    while ($len != $wid) {
        if ($len > $wid) {
            $len -= $wid;
            push(@ret, $wid);
        } else {
            $wid -= $len;
            push(@ret, $len);
        }
    }
    push(@ret, $len);
    \@ret;
}
______________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(sq_in_rect);

sub qrem($$) {
  my ($a, $b) = @_;
  my $v = int($a / $b);
  return ($v, $a - ($v * $b));
}

sub sq_in_rect($$) {
  my ($a, $b) = @_;
  my @squares = ();
  return \@squares if ($a == $b);

  ($a, $b) = ($b, $a) if ($a < $b);

  while ($b > 0) {
    my ($q, $r) = qrem($a, $b);
    push(@squares, map { $b } (1..$q));
    ($a, $b) = ($b, $r);
  }
  return \@squares;
}
