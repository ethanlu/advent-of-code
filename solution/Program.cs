using System;
using System.IO;
using System.Net.Mail;
using System.Text.RegularExpressions;

namespace solution
{
    public interface ISolution
    {
        string PartOne();
        string PartTwo();
    }

    public abstract class Solution : ISolution
    {
        protected string year;
        protected string day;
        protected string inputPath;
        
        protected Solution(string year, string day)
        {
            this.year = year;
            this.day = day;
            this.inputPath = $"{AppDomain.CurrentDomain.BaseDirectory}/../../../input/{this.year}/day{this.day}.txt";
        }
        
        protected string LoadInputAsString()
        {
            return File.ReadAllText(this.inputPath).Replace("\n", "").Trim();
        }

        protected string[] LoadInputAsLines()
        {
            return File.ReadAllLines(this.inputPath);
        }

        public abstract string PartOne();
        public abstract string PartTwo();
    }

    internal class Program
    {
        private static ISolution LoadSolution(string year, string day)
        {
            object[] p = {year, day};
            return Activator.CreateInstance(
                Type.GetType($"solution.year{year}.Day{day}, Solution", true), p) as ISolution;
        }

        public static void Main(string[] args)
        {
            try
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
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}