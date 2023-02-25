using System.Collections.Immutable;

namespace adventofcode.common.util;

public class MathTools
{
    public static int LCM(int a, int b) { return (int)MathTools.LCM((long) a, (long) b); }
    public static long LCM(long a, long b)
    {
        var larger = Math.Max(a, b);
        var smaller = Math.Min(a, b);

        for (long multiplier = 1; multiplier < smaller; multiplier++)
        {
            if ((larger * multiplier) % smaller == 0)
            {
                return multiplier * larger;
            }
        }
        return a * b;
    }

    public static List<int> Factors(int a)
    {
        var factors = new List<int>();
        foreach (var f in MathTools.Factors((long) a))
        {
            factors.Add((int) f);
        }
        return factors;
    }
    public static List<long> Factors(long a)
    {
        var factors = new HashSet<long>();
        for (long i = 1L; i <= a / 2; i++)
        {
            if (a % i == 0)
            {
                factors.Add(i);
                factors.Add(a / i);
            }
        }
        return factors.ToList().Order().ToList();
    }
}