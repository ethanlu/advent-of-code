using adventofcode.common;
using adventofcode.common.range;
using System.Text.RegularExpressions;

namespace adventofcode.year2022;

public class Day04 : Solution
{
    private string[] _input;

    public Day04(string year, string day) : base(year, day)
    {
        _input = this.LoadInputAsLines();
    }

    public override string PartOne()
    {
        var overlap = 0;
        foreach (var assignments in _input)
        {
            var match = Regex.Match(assignments, @"^(\d+)-(\d+),(\d+)-(\d+)$");
            var interval1 = new Interval(Convert.ToInt32(match.Groups[1].ToString()), Convert.ToInt32(match.Groups[2].ToString()));
            var interval2 = new Interval(Convert.ToInt32(match.Groups[3].ToString()), Convert.ToInt32(match.Groups[4].ToString()));

            overlap += interval1.Contains(interval2) ? 1 : 0;
        }
        
        return Convert.ToString(overlap);
    }

    public override string PartTwo()
    {
        var overlap = 0;
        foreach (var assignments in _input)
        {
            var match = Regex.Match(assignments, @"^(\d+)-(\d+),(\d+)-(\d+)$");
            var interval1 = new Interval(Convert.ToInt32(match.Groups[1].ToString()), Convert.ToInt32(match.Groups[2].ToString()));
            var interval2 = new Interval(Convert.ToInt32(match.Groups[3].ToString()), Convert.ToInt32(match.Groups[4].ToString()));

            overlap += interval1.Overlaps(interval2) ? 1 : 0;
        }
        
        return Convert.ToString(overlap);
    }
}