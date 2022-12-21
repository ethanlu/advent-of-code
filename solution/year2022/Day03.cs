using System.Collections.Generic;
using System.Linq;

namespace solution.year2022
{
    public class Day03 : Solution
    {
        private string[] input;

        public Day03(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();
        }

        private int calculatePriority(string s)
        {
            var priority = (int) s[0];
            return priority > 96 ? priority - 96 : priority - 38;
        }

        public override string PartOne()
        {
            var total = 0;
            foreach (var sack in this.input)
            {
                var sack1 = new HashSet<char>(sack.Substring(0, sack.Length / 2).ToCharArray().Distinct());
                var sack2 = new HashSet<char>(sack.Substring(sack.Length / 2).ToCharArray().Distinct());

                sack1.IntersectWith(sack2);
                total += this.calculatePriority(string.Join("", sack1));
            }
            
            return System.Convert.ToString(total);
        }

        public override string PartTwo()
        {
            var total = 0;
            for (int i = 0; i < this.input.Length; i+=3)
            {
                var sack1 = new HashSet<char>(this.input[i].ToCharArray().Distinct());
                var sack2 = new HashSet<char>(this.input[i + 1].ToCharArray().Distinct());
                var sack3 = new HashSet<char>(this.input[i + 2].ToCharArray().Distinct());

                sack1.IntersectWith(sack2);
                sack1.IntersectWith(sack3);
                total += this.calculatePriority(string.Join("", sack1));
            }
            
            return System.Convert.ToString(total);
        }
        
    }
}