Motivation

Natural language texts often have a very high frequency of certain letters, in German for example, almost every 5th letter is an E, but only every 500th is a Q. It would then be clever to choose a very small representation for E. This is exactly what the Huffman compression is about, choosing the length of the representation based on the frequencies of the symbol in the text.
Algorithm

Let's assume we want to encode the word "aaaabcc", then we calculate the frequencies of the letters in the text:
Symbol 	Frequency
a 	4
b 	1
c 	2

Now we choose a smaller representation the more often it occurs, to minimize the overall space needed. The algorithm uses a tree for encoding and decoding:

  .
 / \
a   .
   / \
   b  c

Usually we choose 0 for the left branch and 1 for the right branch (but it might also be swapped). By traversing from the root to the symbol leaf, we want to encode, we get the matching representation. To decode a sequence of binary digits into a symbol, we start from the root and just follow the path in the same way, until we reach a symbol.

Considering the above tree, we would encode a with 0, b with 10 and c with 11. Therefore encoding "aaaabcc" will result in 0000101111.

(Note: As you can see the encoding is not optimal, since the code for b and c have same length, but that is topic of another data compression Kata.)
Tree construction

To build the tree, we turn each symbol into a leaf and sort them by their frequency. In every step, we remove 2 trees with the smallest frequency and put them under a node. This node gets reinserted and has the sum of the frequencies of both trees as new frequency. We are finished, when there is only 1 tree left.

(Hint: Maybe you can do it without sorting in every step?)
Goal

Write functions frequencies, encode and decode.

Note: Frequency lists with just one or less elements should get rejected. (Because then there is no information we could encode, but the length.)
