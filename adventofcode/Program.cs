using System.Text.RegularExpressions;
using File = System.IO.File;

namespace adventofcode
{
    public interface ISolution
    {
        string PartOne();
        string PartTwo();
    }

    public abstract class Solution : ISolution
    {
        private readonly string _inputPath;
        
        protected Solution(string year, string day)
        {
            var match = Regex.Match(AppDomain.CurrentDomain.BaseDirectory, @"^(.*/advent-of-code/adventofcode/)");
            if (!match.Success)
            {
                throw new Exception("Could not find base path for data file");
            }
            
            _inputPath = $"{match.Groups[1]}../input/{year}/day{day}.txt";
        }
        
        protected string LoadInputAsString()
        {
            return File.ReadAllText(_inputPath).Replace("\n", "").Trim();
        }

        protected string[] LoadInputAsLines()
        {
            return File.ReadAllLines(_inputPath);
        }

        public abstract string PartOne();
        public abstract string PartTwo();
    }

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
}