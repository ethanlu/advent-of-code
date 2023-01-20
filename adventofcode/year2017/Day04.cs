using adventofcode.common;

namespace adventofcode.year2017;

public class Day04 : Solution
{
    private string[] _input;
    
    public Day04(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var valid = 0;
        foreach (var phrase in _input)
        {
            var words = phrase.Split(" ");
            var unique = new HashSet<string>(words);
            valid += unique.Count == words.Length ? 1 : 0;
        }

        return Convert.ToString(valid);
    }

    public override string PartTwo()
    {
        var valid = 0;
        foreach (var phrase in _input)
        {
            var words = phrase.Split(" ").Select(word => string.Concat(word.OrderBy(c => c))).ToArray();
            var unique = new HashSet<string>(words);
            valid += unique.Count == words.Length ? 1 : 0;
        }

        return Convert.ToString(valid);
    }
}