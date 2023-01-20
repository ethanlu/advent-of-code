using adventofcode.common;

namespace adventofcode.year2017;

public class Day01 : Solution
{
    private string _input;
    
    public Day01(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var sum = 0;
        for (int i = 0; i < _input.Length; i++)
        {
            if (i + 1 < _input.Length)
            {
                sum += _input[i] == _input[i + 1] ? Convert.ToInt32(_input[i].ToString()) : 0;
            }
            else
            {
                sum += _input[i] == _input[0] ? Convert.ToInt32(_input[i].ToString()) : 0;
            }
        }

        return Convert.ToString(sum);
    }

    public override string PartTwo()
    {
        var offset = _input.Length / 2;
        var sum = 0;
        for (int i = 0; i < _input.Length; i++)
        {
            if (i + offset < _input.Length)
            {
                sum += _input[i] == _input[i + offset] ? Convert.ToInt32(_input[i].ToString()) : 0;
            }
            else
            {
                sum += _input[i] == _input[(i + offset) % _input.Length] ? Convert.ToInt32(_input[i].ToString()) : 0;
            }
        }

        return Convert.ToString(sum);
    }
}