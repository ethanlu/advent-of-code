using adventofcode.common;

namespace adventofcode.year2018;

public class Day01 : Solution
{
    private List<int> _frequencies;
    
    public Day01(string year, string day) : base(year, day)
    {
        _frequencies = new List<int>();
        foreach (var line in LoadInputAsLines())
        {
            _frequencies.Add(Convert.ToInt32(line));
        }
    }

    public override string PartOne()
    {
        return Convert.ToString(_frequencies.Aggregate(0, (acc, f) => acc + f));
    }

    public override string PartTwo()
    {
        var seenFrequencies = new HashSet<int>();
        var frequency = 0;
        var repeat = 0;

        var index = 0;
        while (true)
        {
            frequency += _frequencies[index];
            if (seenFrequencies.Contains(frequency))
            {
                repeat = frequency;
                break;
            }
            seenFrequencies.Add(frequency);
            index = index + 1 >= _frequencies.Count ? 0 : index + 1;
        }
        
        return Convert.ToString(repeat);
    }
}