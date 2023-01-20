using adventofcode.common;
using adventofcode.common.util;

namespace adventofcode.year2017;

public class Day02 : Solution
{
    private List<List<int>> _input;
    
    public Day02(string year, string day) : base(year, day)
    {
        _input = new List<List<int>>();
        foreach (var line in LoadInputAsLines())
        {
            _input.Add(line.Split("\t").Select(x => Convert.ToInt32(x)).ToList());
        }
    }

    public override string PartOne()
    {
        var checksum = _input.Aggregate(0, (acc, row) => acc + row.Max() - row.Min());
        return Convert.ToString(checksum);
    }

    public override string PartTwo()
    {
        var checksum = 0;
        foreach (var input in _input)
        {
            foreach (var combination in IterTools<int>.Permutation(input, 2))
            {
                if (combination[0] % combination[1] == 0)
                {
                    checksum += combination[0] / combination[1];
                    break;
                }
            }
        }

        return Convert.ToString(checksum);
    }
}