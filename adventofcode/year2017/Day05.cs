using adventofcode.common;

namespace adventofcode.year2017;

public class Day05 : Solution
{
    private string[] _input;
    
    public Day05(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var instructions = _input.Select(i => Convert.ToInt32(i)).ToArray();
        var steps = 0;
        var index = 0;

        while (index < instructions.Length)
        {
            index += instructions[index]++;
            steps++;
        }

        return Convert.ToString(steps);
    }

    public override string PartTwo()
    {
        var instructions = _input.Select(i => Convert.ToInt32(i)).ToArray();
        var steps = 0;
        var index = 0;
        var nextIndex = index;

        while (index < instructions.Length)
        {
            var offset = instructions[index];
            nextIndex += offset;
            instructions[index] += offset >= 3 ? -1 : 1;
            
            steps++;
            index = nextIndex;
        }

        return Convert.ToString(steps);
    }
}