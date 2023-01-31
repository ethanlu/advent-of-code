using adventofcode.common;
using adventofcode.common.util;

namespace adventofcode.year2018;

public class Day02 : Solution
{
    private string[] _input;
    
    public Day02(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var twiceCount = 0;
        var thriceCount = 0;
        foreach (var line in _input)
        {
            var count = new Dictionary<char, int>();
            foreach (var c in line)
            {
                if (!count.ContainsKey(c))
                {
                    count.Add(c, 0);
                }
                count[c]++;
            }

            var twice = false;
            var thrice = false;
            foreach (var n in count.Values)
            {
                twice = twice || n == 2;
                thrice = thrice || n == 3;
            }
            twiceCount += twice ? 1 : 0;
            thriceCount += thrice ? 1 : 0;
        }
        
        return Convert.ToString(twiceCount * thriceCount);
    }

    public override string PartTwo()
    {
        var commonChars = "";
        foreach (var combination in IterTools<string>.Combination(_input.ToList(), 2))
        {
            commonChars = "";
            var mismatchCount = 0;
            
            for (int i = 0; i < combination[0].Length; i++)
            {
                mismatchCount += combination[0][i] != combination[1][i] ? 1 : 0;
                commonChars += combination[0][i] == combination[1][i] ? combination[1][i] : "";
            }

            if (mismatchCount == 1)
            {
                break;
            }
        }

        return Convert.ToString(commonChars);
    }
}