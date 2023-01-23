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
}