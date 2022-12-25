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
        
        Console.WriteLine("-----part one-----");
        Console.WriteLine(solution.PartOne());
        
        Console.WriteLine("-----part two-----");
        Console.WriteLine(solution.PartTwo());
    }
}