54cb771c9b30e8b5250011d4


Description:

One man (lets call him Eulampy) has a collection of some almost identical Fabergé eggs. One day his friend Tempter said to him:

        Do you see that skyscraper? And can you tell me a maximal floor that if you drop your egg from will not crack it?
        No, - said Eulampy.
        But if you give me N eggs, - says Tempter - I'l tell you an answer.
        Deal - said Eulampy. But I have one requirement before we start this: if I will see more than M falls of egg, my heart will be crushed instead of egg. So you have only M trys to throw eggs. Would you tell me an exact floor with this limitation?

Task

Your task is to help Tempter - write a function

height :: Integer -> Integer -> Integer
height n m = -- see text

that takes 2 arguments - the number of eggs n and the number of trys m - you should calculate maximum scyscrapper height (in floors), in which it is guaranteed to find an exactly maximal floor from which that an egg won't crack it.

Which means,

    You can throw an egg from a specific floor every try
    Every egg has the same, certain durability - if they're thrown from a certain floor or below, they won't crack. Otherwise they crack.
    You have n eggs and m tries
    What is the maxmimum height, such that you can always determine which floor the target floor is when the target floor can be any floor between 1 to this maximum height?

Examples

height 0 14 = 0
height 2 0  = 0
height 2 14 = 105
height 7 20 = 137979

Data range

n <= 20000
m <= 20000
