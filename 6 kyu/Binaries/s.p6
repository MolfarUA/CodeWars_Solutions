use v6;
unit module Solution;

sub encode-digit(Int $d --> Str) {
    "0" x ($d.base(2).chars - 1) ~ "1" ~ $d.base(2)
}

sub code(Str $s --> Str) is export(:code) {
    [~] $s.comb.map: { encode-digit( $_.Int ) }
}

my regex digit { ("0"* "1") {} :my $b = $0; (\d ** {$b.chars}) };

sub decode(Str $s --> Str) is export(:decode) {
    $s ~~ / <digit>+ /;
    [~] $/<digit>.map: {$_.pairs.hash<1>.Str.parse-base(2)}
}
__________________________
use v6;
unit module Solution;

sub code($s) is export(:code) {
    my %dict = ('0' => '10', '1' => '11', '2' => '0110', '3' => '0111', '4' => '001100', '5' => '001101', '6' => '001110', '7' => '001111', '8' => '00011000', '9' => '00011001');
    my $res = '';
    loop (my $i = 0; $i < $s.chars; $i++) {
        my $u = substr($s, $i, 1);
        my $v = %dict{$u};
        $res ~= $v;
    }
    $res;
}

sub decode($s is copy) is export(:decode) {
    my $ch = '1'; my $res = ""; my $l = -1;
    while ($s) {
        my $l = index($s, $ch) + 1;
        my $ss = substr($s, $l, $l);
        my $n = "0b$ss".Int;
        $res ~= $n;
        $s = substr($s, $l * 2);
    }
    $res;
}

