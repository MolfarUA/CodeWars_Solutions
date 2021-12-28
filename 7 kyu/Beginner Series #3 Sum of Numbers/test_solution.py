#include <criterion/criterion.h>
#include <stdlib.h>
# include <time.h>
int get_sum(int,int);
Test(Basic_tests, sum_all) {
    cr_assert_eq(get_sum(5 , -1), 14, "Expected %d, instead got %d", 14 , get_sum(5 , -1));
    cr_assert_eq(get_sum(505 , 4), 127759, "Expected %d, instead got %d", 127759 , get_sum(505 , 4));
    cr_assert_eq(get_sum(-50 , 0), -1275, "Expected %d, instead got %d", -1275 , get_sum(-50 , 0));
    cr_assert_eq(get_sum(321 , 123), 44178, "Expected %d, instead got %d", 44178 , get_sum(321 , 123));
    cr_assert_eq(get_sum(-1 , -5), -15, "Expected %d, instead got %d", -15 , get_sum(-1 , -5));
    cr_assert_eq(get_sum(-5 , -5), -5, "Expected %d, instead got %d", -5 , get_sum(-5 , -5));
    cr_assert_eq(get_sum(-50 , 4), -1265, "Expected %d, instead got %d", -1265 , get_sum(-50 , 4));
    cr_assert_eq(get_sum(0 , 0), 0, "Expected %d, instead got %d", 0 , get_sum(0 , 0));
    cr_assert_eq(get_sum(5 , 1), 15, "Expected %d, instead got %d", 15 , get_sum(5 , 1));
    cr_assert_eq(get_sum(-17 , -17), -17, "Expected %d, instead got %d", -17 , get_sum(-17 , -17));
    cr_assert_eq(get_sum(17 , 17), 17, "Expected %d, instead got %d", 17 , get_sum(17 , 17));
}
Test(Random_tests, randomized) {
    srand(time(NULL));
    for(int i = 3; i < 103; i++) {
        int X = (int) (rand() % 1200 - 600);
        int C = (int) (rand() % 1200 - 600);
        int ac = get_sum(C, X);
        int ex = (C + X) * (abs(C - X) + 1) / 2;
        cr_assert_eq(ac , ex , "Expected : %d ,  instead got : %d" , ex, ac);
    }
}
