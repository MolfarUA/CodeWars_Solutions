package Solution;

use v5.30;
use warnings;
use List::Util qw(sum0);
use experimental qw(declared_refs refaliasing signatures);

use Exporter qw(import);
our @EXPORT_OK = qw(choose_best_sum);

sub choose_best_sum($max, $k, $dstr) {
    my @dists = split m/,/, $dstr =~ s{\s+}{}gr;
    my @combs = 
       sort {$a <=> $b }
       grep {$_ <= $max} 
       map {sum0($_->@*)} combinations(\@dists, $k)->@*;
    
    return -1 unless @combs;
    return $combs[-1];
}

sub combinations ($array, $k, $state = [], $result = []) {
    if ($k == 0) {
        push ($result->@*, $state);
        return $result;
    }

    my $length = scalar $array->@*;
    for (my $i = 0; $i < $length; ++$i) {
        combinations([$array->@[($i + 1) .. $length - 1]], $k - 1, [$state->@*, $array->[$i]], $result);
    }

    return $result;
}
_______________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(choose_best_sum);

use List::Util qw(sum);
use experimental qw(signatures);

sub combinations ($list, $k) { # Trusty combination function.
    return map { [$_] } @$list if $k <= 1;
    
    my @combinations;
    for (my $i = 0; $i + $k <= @$list; ++$i) {
        my $current = $list->[$i];
        my $rest    = [@$list[($i + 1) .. $#$list]];
        push @combinations, [$current, @$_] for combinations($rest, $k - 1);
    }
    
    return @combinations;
}


sub choose_best_sum ($t, $n, $d_string) {
    my @d = split(', ', $d_string);
    
    my @sorted_distances = sort { $b <=> $a } map { sum(@$_) } combinations(\@d, $n);
    for (@sorted_distances) {
        return $_ if $_ <= $t;
    }
    
    return -1;
}
_______________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use List::Util qw(max sum);
use Exporter qw(import);
our @EXPORT_OK = qw(choose_best_sum);

# parameter: maximum sum of distances, number of towns to visit, string of distances
sub choose_best_sum {
    my ($t, $k, $str) = @_;
    my $list = [map {int($_)} split(/,\s+/, $str)];
    return (max grep {$_ <= $t} map {sum @$_} combinations($list, $k)) || -1;
}

sub combinations {
    my ($listref, $n) = @_;
    return map {[$_]} @$listref if ($n <= 1);
    my @ret;
    for (my $i = 0; $i+$n <= @$listref; ++$i) {
        my $val  = $listref->[$i];
        my @rest = @$listref[$i+1..$#$listref];
        push(@ret, [$val, @$_]) for combinations(\@rest, $n-1);
    }
    return @ret;
}
_______________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(choose_best_sum);

sub som {
    my $sum = 0;
    for ( @_ ) { $sum += $_; }
    return $sum;
}
sub combine {
  my ($list, $n) = @_;
  return map [$_], @$list if $n <= 1;
  my @comb;
  for (my $i = 0; $i+$n <= @$list; ++$i) {
    my $val  = $list->[$i];
    my @rest = @$list[$i+1..$#$list];
    push @comb, [$val, @$_] for combine(\@rest, $n-1);
  }
  return @comb;
}
sub aux {
  my ($t, $n, $list) = @_;
  my @res; my $mx = -1; my $r = -1;
  @res = map( som(@$_), @{$list});
  foreach (@res) {
      if (($_ > $mx) && ($_ <= $t)) { 
          $r = $_; $mx = $r; 
      }
  }
  return $r;
}
# parameter maximum sum of distances, number of towns to visit, string of distances
sub choose_best_sum {
    my ($t, $n, $s) = @_; 
    my @a = split /, /, $s;
    my @comb = combine(\@a, $n);
    return aux($t, $n, \@comb);
}
