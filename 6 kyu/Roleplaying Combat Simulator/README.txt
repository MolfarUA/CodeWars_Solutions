Description:

In a typical tabetop roleplaying game, combat can be boiled down to rolling a die, adding or subtracting some modifiers, and comparing the result to a target's defense score. If that result is equal to or greater than the target's defense, the attack hits, and a certain amount of damage is subtracted from the target's hit points. If a character's hit points drops to zero or below, they are dead.

Write a class to simulate a basic fight between two characters (the Player Character and the Enemy).

Your class needs to be initialised with the combatants' starting hit points and defense values, and expose two methods: PcAttack and EnemyAttack, each of which take an attackRoll (integer), modifiers (array of integers), and the amount of damage to be dealt on a successful hit.

Use the attackRoll, add or subtract any modifiers (see below), and compare it to the enemy's defense score. If the result is greater than the defense score, subtract the damage from the enemy's health.

Modifiers might change from round to round as the circumstances of the battle change, and can be any integer, even negative. Sometimes, there are no modifiers at all - in this case, either an empty array or null could be passed to your Attack methods.

Here's a quick example of how modifiers work:

In round one, it's the PC's turn. The fight takes place in a cave, and very limited light encroaches from the outside. The low-light makes it difficult to see, so the PC gets a -3 modifier to attack. But the enemy is lying prone and is very easy to hit, equating to a +2 modifier for the character. The PC's modifiers in this round are { -3, 2 }, for a total of -1.

In a subsequent round, the enemy is back on his feet, and has pushed the character into the light. Both combatants are now on an equal footing, so the modifiers are { 0 }.

In a different battle, perhaps in an arena, it may be decided that neither character suffers a particular advantage or disadvantage, so the modifiers might be null.

The tests will initialise your class and call PcAttack and EnemyAttack, checking for the death of either party after each call.



59243a9825ac8e993e000060
