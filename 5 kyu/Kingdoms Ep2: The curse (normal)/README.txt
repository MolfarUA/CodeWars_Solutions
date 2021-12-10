You are travelling and you see some strong villagers trying to battle unsuccessfully with one skinny man. When you approach them, the peasants tell you that man is the cursed priest from the village. Now he lives among the tombs, cries out and nobody can understand him because he can not pronounce any entire word. You decided to try to help him.

Given the string speech and the array vocabulary. You should return a string where each word in the priest's speech is replaced with the appropriate word from vocabulary. After every replacement, remove the appropriate word from vocabulary. Sometimes, it might seem unclear which word exactly is appropriate but, after reducing the size of vocabulary, there will be only one possible final answer.

Notes:
Words in the priest's speech always consist of lowercase letters and at least one asterisk. Each asterisk is replacing one character;
speech consists of these words, as described above, spaces and marks ?!,. ;
There might be more words in vocabulary than words in speech;
The length of an encoded word must be the same as an appropriate word of vocabulary;
The minimum length of a word is 3.
Example:
Given a speech "a**? *c*. **e," and a vocabulary of ["ace", "acd", "abd"], the expected answer is "abd? acd. ace,".
