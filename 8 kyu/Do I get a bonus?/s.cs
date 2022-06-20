56f6ad906b88de513f000d96


public static class Kata
{
    public static string bonus_time(int salary, bool bonus)
    {
        return $"${salary * (bonus ? 10 : 1)}";
    }
}
__________________________
public static class Kata
{
    public static string bonus_time(int salary, bool bonus) => "$" + (bonus ? salary * 10 : salary);
}
__________________________
public static class Kata
    {
        public static string bonus_time(int salary, bool bonus)
        {
            return bonus ? $"${salary * 10}" : $"${salary}";
        }
    }
