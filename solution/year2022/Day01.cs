using System.Collections.Generic;
using System.Linq;

namespace solution.year2022
{
    public class Day01 : Solution
    {
        private string[] input;
        private List<int> calories;
        
        public Day01(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();
            this.calories = new List<int>();
        }
            
        public override string PartOne()
        {
            int largestCalorie = 0;
            int currentCalorie = 0;
            for (int i = 0; i < this.input.Length; i++)
            {
                if (string.IsNullOrEmpty(this.input[i]))
                {
                    // blank reached, check if calories is new largest
                    if (currentCalorie >= largestCalorie)
                    {
                        largestCalorie = currentCalorie;
                    }
                    this.calories.Add(currentCalorie);
                    currentCalorie = 0;
                }
                else
                {
                    currentCalorie += System.Convert.ToInt32(this.input[i]);
                }
            }

            return System.Convert.ToString(largestCalorie);
        }

        public override string PartTwo()
        {
            return System.Convert.ToString(this.calories.OrderByDescending(x => x).Take(3).Sum());
        }
        
    }
}