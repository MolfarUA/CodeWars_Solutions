package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(mix);

sub mix {
        
        my ($s1, $s2) = @_;
        my %hash = ();
        
        foreach my $let ( 'a' .. 'z' ) {

                my $cnt1 = () = $s1 =~ /$let/g;
                my $cnt2 = () = $s2 =~ /$let/g;
                my $key = '';

                if ( $cnt1 <= 1 && $cnt2 <= 1 ) {
                        
                        next;
                } elsif ( $cnt1 > $cnt2 ) {
                        
                        $key = "1:" . ($let x $cnt1);
                } elsif ( $cnt1 < $cnt2 ) {
                        
                        $key = "2:" . ($let x $cnt2);
                } else {
                 
                        $key = "=:" . ($let x $cnt1);
                }

                $hash{$key} = 1;
        }

        my @arr = sort { length $b <=> length $a || $a cmp $b } keys %hash;
        return join ('/', @arr);
}

_____________________________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(mix);

sub mix {
    my ($s1, $s2) = @_;
    $s1 =~ s/\s+//g;
    $s2 =~ s/\s+//g;
    $s1 =~ s/\d+//g;
    $s2 =~ s/\d+//g;
    $s1 =~ s/[A-Z]+//g;
    $s2 =~ s/[A-Z]+//g;
    $s1 =~ s/[=+#]+//g;
    $s2 =~ s/[=+#]+//g;

    my @s1_arr = split('', $s1);
    my @s2_arr = split('', $s2);
    my %s1_h;
    my %s2_h;
    foreach my $el (@s1_arr){
        if (exists($s1_h{$el})){
            $s1_h{$el}{1} += 1;
        }else{
            $s1_h{$el} = {1=>1};
        }
    }
    foreach my $el (@s2_arr){
        if (exists($s2_h{$el})){
            $s2_h{$el}{2} += 1;
        }else{
            $s2_h{$el} = {2=>1};
        }
    }
    my %hash_ans;
    my $n;
    my %s3_h = (%s1_h, %s2_h);
    foreach my $key (keys %s3_h){
        if (exists($s2_h{$key}{2})){
            if (!exists($s1_h{$key}{1}) && $s2_h{$key}{2} > 1){
                $n = $key x $s2_h{$key}{2};
                $hash_ans{$n} = "2:";
            }else{
                if ($s2_h{$key}{2} > 1 && $s2_h{$key}{2} > $s1_h{$key}{1}){
                    $n = $key x $s2_h{$key}{2};
                    $hash_ans{$n} = "2:";
                }elsif($s2_h{$key}{2} > 1 && $s2_h{$key}{2} == $s1_h{$key}{1}){
                    $n = $key x $s2_h{$key}{2};
                    $hash_ans{$n} = "=:";
                }elsif($s1_h{$key}{1} > 1 && $s2_h{$key}{2} < $s1_h{$key}{1}){
                    $n = $key x $s1_h{$key}{1};
                    $hash_ans{$n} = "1:";
                }
            }
        }else{
            if ($s1_h{$key}{1} > 1){
                $n = $key x $s1_h{$key}{1};
                $hash_ans{$n} = "1:";
            }
        }
    }
    my $result_str = "";
    foreach my $key (sort { length($b) <=> length($a) or "$hash_ans{$a}" . "$a" cmp "$hash_ans{$b}" . "$b"} keys %hash_ans) {
        $result_str .= "$hash_ans{$key}" . "$key" . "/";
    }
    return substr $result_str, 0, -1;
    
}

_____________________________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(mix);

sub mix {
    my @l;
    for my $char ('a'..'z') {
        my $c1 = () = $_[0] =~ /$char/g;
        my $c2 = () = $_[1] =~ /$char/g;
        my $max = $c1 > $c2 ? $c1 : $c2;
        push @l, qw(= 1 2)[$c1 <=> $c2] . ":" . $char x $max if (1 < $max);
    }
    return join "/", sort {length $b <=> length $a || $a cmp $b} @l;
}

_____________________________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(mix);

use Data::Dumper;


sub normalize
{
    my ($letter, $s1CountHashRef, $s2CountHashRef) = @_;

    my ($c1, $c2) = ($s1CountHashRef->{$letter} || 0, $s2CountHashRef->{$letter} || 0);
    return '1:' . $letter x $c1  if $c1 > $c2;
    return '2:' . $letter x $c2  if $c1 < $c2;
    return '=:' . $letter x $c1;
}


sub mix
{
    my ($s1, $s2) = @_;

    my (%s1Count, %s2Count);
    $s1Count{$1}++  while $s1 =~ m/([a-z])/g;
    $s2Count{$1}++  while $s2 =~ m/([a-z])/g;

    my (%s1Set, %s2Set);
    $s1Count{$_} > 1 and $s1Set{$_} = '[present in set]'  foreach keys %s1Count;
    $s2Count{$_} > 1 and $s2Set{$_} = '[present in set]'  foreach keys %s2Count;
    my %wholeSet = (%s1Set, %s2Set);

    my @terms = map { normalize($_, \%s1Count, \%s2Count) } keys %wholeSet;
    @terms = sort {length($b) <=> length($a) or $a cmp $b} @terms;
    
    return join '/', @terms;
}

_____________________________________________________
package Solution;

use 5.30.0;
use strict;
use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(mix);

sub mix {
    my ($s1, $s2) = @_;
    my $st1 = {};
    my $st2 = {};
    for my $l (split ('', $s1)) {
        if ($l =~ m/[a-z]/) {
            $st1->{$l} .= $l;
        }
    }
    for my $l (split ('', $s2)) {
        if ($l =~ m/[a-z]/) {
            $st2->{$l} .= $l;
        }
    }
    my $max;
    for my $e1 (keys %{$st1}) {
        if (!defined($st2->{$e1})) {
            $max->{$e1}{string_value} = $st1->{$e1};
            $max->{$e1}{string_number} = 1;
            $max->{$e1}{prefix} = ':';
            next;
        }
        $max->{$e1}{string_value} = length $st1->{$e1} > length $st2->{$e1} ? $st1->{$e1} : $st2->{$e1};
        $max->{$e1}{string_number} = length $st1->{$e1} > length $st2->{$e1} ? 1 : 2;
        $max->{$e1}{prefix} = $st1->{$e1} eq $st2->{$e1} ? '=:' : ':';
    }
    for my $e2 (keys %{$st2}) {
        if ($st1->{$e2}) {next;}
        $max->{$e2}{string_value} = $st2->{$e2};
        $max->{$e2}{string_number} = 2;
        $max->{$e2}{prefix} = ':';
    }    
    my @result =
        map { ($_->{prefix} eq ':' ? $_->{string_number} : '').$_->{prefix}.$_->{string_value} }
        sort {
            length $b->{string_value} <=> length $a->{string_value} ||
            $a->{prefix} cmp $b->{prefix} ||
            $a->{string_number} <=> $b->{string_number} ||
            $a->{string_value} cmp $b->{string_value}
        }
        grep { length ($_->{string_value}) > 1 }
        values %{$max};
    return join('/', @result);
}
