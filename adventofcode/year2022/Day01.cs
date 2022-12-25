using adventofcode.common;

namespace adventofcode.year2022;

public class Day01 : Solution
{
    private string[] _input;
    private List<int> _calories;
    
    public Day01(string year, string day) : base(year, day)
    {
        _input = this.LoadInputAsLines();
        _calories = new List<int>();
    }
        
    public override string PartOne()
    {
        var largestCalorie = 0;
        var currentCalorie = 0;
        foreach (var calorie in _input)
        {
            if (string.IsNullOrEmpty(calorie))
            {
                // blank reached, check if calories is new largest
                if (currentCalorie >= largestCalorie)
                {
                    largestCalorie = currentCalorie;
                }
                _calories.Add(currentCalorie);
                currentCalorie = 0;
            }
            else
            {
                currentCalorie += Convert.ToInt32(calorie);
            }
        }

        return Convert.ToString(largestCalorie);
    }

    public override string PartTwo()
    {
        return Convert.ToString(_calories.OrderByDescending(x => x).Take(3).Sum());
    }
}