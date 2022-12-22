using System;
using System.Text.RegularExpressions;

namespace solution.year2022
{
    public class Day04 : Solution
    {
        private string[] input;

        public Day04(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();
        }

        public override string PartOne()
        {
            var overlap = 0;
            foreach (var assignments in this.input)
            {
                var match = Regex.Match(assignments, @"^(\d+)-(\d+),(\d+)-(\d+)$");
                var start1 = Convert.ToInt32(match.Groups[1].ToString());
                var end1 = Convert.ToInt32(match.Groups[2].ToString());
                var start2 = Convert.ToInt32(match.Groups[3].ToString());
                var end2 = Convert.ToInt32(match.Groups[4].ToString());

                overlap += (start1 <= start2 && end1 >= end2) || (start2 <= start1 && end2 >= end1) ? 1 : 0;
            }
            
            return System.Convert.ToString(overlap);
        }

        public override string PartTwo()
        {
            var overlap = 0;
            foreach (var assignments in this.input)
            {
                var match = Regex.Match(assignments, @"^(\d+)-(\d+),(\d+)-(\d+)$");
                var start1 = Convert.ToInt32(match.Groups[1].ToString());
                var end1 = Convert.ToInt32(match.Groups[2].ToString());
                var start2 = Convert.ToInt32(match.Groups[3].ToString());
                var end2 = Convert.ToInt32(match.Groups[4].ToString());

                overlap += (end1 < start2 || start1 > end2) ? 0 : 1;
            }
            
            return System.Convert.ToString(overlap);
        }
        
    }
}