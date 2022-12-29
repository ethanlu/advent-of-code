using System.Diagnostics;

namespace adventofcode;

using common;
using System.Text.RegularExpressions;

internal class Program
{
    private static ISolution LoadSolution(string year, string day)
    {
        object[] p = {year, day};
        var t = Type.GetType($"adventofcode.year{year}.Day{day}, adventofcode", true);
        if (t is null)
        {
            throw new Exception($"Could not load assembly : adventofcode.year{year}.Day{day}, adventofcode");
        }

        var s = Activator.CreateInstance(t, p) as ISolution;
        if (s is null)
        {
            throw new Exception($"Could not instantiate class : adventofcode.year{year}.Day{day}, adventofcode");
        }

        return s;
    }

    public static void Main(string[] args)
    {
        void Time(TimeSpan ts)
        {
            Console.WriteLine("Elapsed : " + String.Format("{0:00}:{1:00}:{2:00}.{3:00}",
                ts.Hours, ts.Minutes, ts.Seconds,
                ts.Milliseconds / 10));
        }

        if (args.Length != 2)
        {
            throw new ArgumentException("Missing year and/or day");
        }

        if (!Regex.Match(args[0], @"^\d\d\d\d$").Success)
        {
            throw new ArgumentException("Year must be YYYY");
        }
        var year = args[0];
    
        if (!Regex.Match(args[1], @"^\d\d$").Success)
        {
            throw new ArgumentException("Day must be DD");
        }
        var day = args[1];

        ISolution solution = LoadSolution(year, day);
        var timer = new Stopwatch();
        
        Console.WriteLine("-----part one-----");
        timer.Start();
        Console.WriteLine(solution.PartOne());
        timer.Stop();
        Time(timer.Elapsed);

        Console.WriteLine("-----part two-----");
        timer.Reset();
        timer.Start();
        Console.WriteLine(solution.PartTwo());
        timer.Stop();
        Time(timer.Elapsed);
    }
}