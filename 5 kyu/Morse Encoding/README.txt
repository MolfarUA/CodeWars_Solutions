Description:

You are writing an encoder/decoder to convert between javascript strings and a binary representation of Morse code.

Each Morse code character is represented by a series of "dots" and "dashes". In binary, a dot is a single bit (1) and a dash is three bits (111). Between each dot or dash within a single character, we place a single zero bit. (I.e. "dot dash" would become 10111.) Separate characters are separated by three zero bits (000). Words are spearated by a single space, which is represented by 7 zero bits (0000000).

Formal Syntax
Binary Morse code has the following syntax: (Where '1' and '0' are literal bits.)

    message    ::= word
                 | word 0000000 message

    word       ::= character
                 | character 000 word

    character  ::= mark
                 | mark 0 character

    mark       ::= dot
                 | dash

    dot (·)    ::= 1

    dash (–)   ::= 111


Morse Code
Chracters in Morse code are traditionally represented by a series of dots and dashes. Below is the full list of characters supported by our Binary Morse code:

A    ·–
B    –···
C    –·–·
D    –··
E    ·
F    ··–·
G    ––·
H    ····
I    ··
J    ·–––
K    –·–
L    ·–··
M    ––
N    –·
O    –––
P    ·––·
Q    ––·–
R    ·–·
S    ···
T    –
U    ··–
V    ···–
W    ·––
X    –··–
Y    –·––
Z    ––··
0    –––––
1    ·––––
2    ··–––
3    ···––
4    ····–
5    ·····
6    –····
7    ––···
8    –––··
9    ––––·
.    ·–·–·–
,    ––··––
?    ··––··
'    ·––––·
!    –·–·––
/    –··–·
(    –·––·
)    –·––·–
&    ·–···
:    –––···
;    –·–·–·
=    –···–
+    ·–·–·
-    –····–
_    ··––·–
"    ·–··–·
$    ···–··–
@    ·––·–·


Note that space itself is not a character but is interpreted as the separater between words.

The first method Morse.encode will take a String representing the message and will return an array of signed 32-bit integers in big-endian order and in two's complement format. (Note: This is the standard format for numbers returned by JavaScript bitwise operators.) Since it is possible that the Morse encoded message will not align perfectly with the binary 32-bit numbers, all unused bits are to be padded with 0's.

The second method Morse.decode will take an array of numbers and return the String representation of the message.
Example

Text content  H           E     L             L             O           [space] W             O               R           L             D       
Morse Code    ····        ·     ·−··          ·−··          −−−                 ·−−           −−−             ·−·         ·−··          −··     
Bit pattern   1010101 000 1 000 101110101 000 101110101 000 11101110111 0000000 101110111 000 11101110111 000 1011101 000 10111010 1000 1110101 00000000000000000
32-bit Value  -1,440,552,402                       | -1,547,992,901                    | -1,896,993,141                      | -1,461,059,584
Hex Value     AA22 EA2E                            | A3BB 80BB                         | 8EEE 2E8B                           | A8EA 0000
              ^        ^          ^        ^        ^         ^       ^         ^       ^         ^        ^        ^         ^         ^        ^       ^
              |        |          |        |        |         |       |         |       |         |        |        |         |         |        |       |
              0        8          16       24       0         8       16        24      0         8        16       24        0         8        16      24


536602df5d0266e7b0000d31
