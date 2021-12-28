Task:

You are given two sorted lists, with distinct elements. Find the maximum path sum while traversing through the lists.

Points to consider for a valid path:

    A path can start from either list, and can finish in either list.
    If there is an element which is present in both lists (regardless of its index in the lists), you can choose to change your path to the other list.

Return only the maximum path sum.
Example:

[0, 2, 3, 7, 10, 12]
   [1, 5, 7, 8]

Both lists having only 7 as common element, the possible paths would be:

0->2->3->7->10->12 => 34
0->2->3->7->8      => 20
1->5->7->8         => 21
1->5->7->10->12    => 35 (maximum path)

Hence, the output will be 35 in the example above.
Notes:

    The arrays may contain no common terms.
    The common element should only be counted once.
    Aim for a linear time complexity.

    Range of possible inputs: 0 <=len(l1), len(l2) <= 125000
