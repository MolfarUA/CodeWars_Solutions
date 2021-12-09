import codewars_test as test
from random import random

@test.describe('Basic Tests')
def _():
    @test.it("Test")
    def _():
        test.assert_equals(zombie_shootout(3, 10, 10), "You shot all 3 zombies.")
        test.assert_equals(zombie_shootout(100, 8, 200), "You shot 16 zombies before being eaten: overwhelmed.")
        test.assert_equals(zombie_shootout(50, 10, 8), "You shot 8 zombies before being eaten: ran out of ammo.")

        test.assert_equals(zombie_shootout(10, 10, 10), "You shot all 10 zombies.")
        test.assert_equals(zombie_shootout(17, 8, 200), "You shot 16 zombies before being eaten: overwhelmed.")
        test.assert_equals(zombie_shootout(9, 10, 8), "You shot 8 zombies before being eaten: ran out of ammo.")

        test.assert_equals(zombie_shootout(20, 10, 20), "You shot all 20 zombies.")
        test.assert_equals(zombie_shootout(100, 49, 200), "You shot 98 zombies before being eaten: overwhelmed.")
        test.assert_equals(zombie_shootout(50, 10, 19), "You shot 19 zombies before being eaten: ran out of ammo.")

        test.assert_equals(zombie_shootout(50, 10, 49), "You shot 20 zombies before being eaten: overwhelmed.")
        test.assert_equals(zombie_shootout(100, 10, 20), "You shot 20 zombies before being eaten: overwhelmed.")
        test.assert_equals(zombie_shootout(19, 10, 20), "You shot all 19 zombies.")
        test.assert_equals(zombie_shootout(20, 10, 100), "You shot all 20 zombies.")
        test.assert_equals(zombie_shootout(20, 10, 19), "You shot 19 zombies before being eaten: ran out of ammo.")
        test.assert_equals(zombie_shootout(19, 15, 19), "You shot all 19 zombies.")
        test.assert_equals(zombie_shootout(19, 3, 19), "You shot 6 zombies before being eaten: overwhelmed.")

@test.describe("Random Tests")
def _():
    def my_solution(zombies, distance, ammo):
        time = distance*2

        if (time >= zombies and ammo >= zombies): 
            return(f'You shot all {zombies} zombies.') 

        if (time < zombies and ammo >= time):
            return f'You shot {time} zombies before being eaten: overwhelmed.' 

        if (ammo < zombies):   
            return f'You shot {ammo} zombies before being eaten: ran out of ammo.' 
        
    @test.it("Tests")
    def _():
        for _ in range(100):
            zombies, distance, ammo = int(random()*100), int(random()*100), int(random()*100)
            test.assert_equals(zombie_shootout(zombies, distance, ammo), my_solution(zombies, distance, ammo), f"Testing for zombie_shootout({zombies}, {distance}, {ammo})")        
