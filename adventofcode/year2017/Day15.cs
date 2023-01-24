using adventofcode.common;

namespace adventofcode.year2017;

public class Day15 : Solution
{
    private string[] _input;
    private long[] _generators;
    private long[] _factors;
    private long _divisor;
    
    public Day15(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
        _factors = new long[2] { 16807L, 48271L };
        _divisor = 2147483647L;
    }

    private void Reset()
    {
        _generators = new long[2];
        _generators[0] = Convert.ToInt64(_input[0].Split(" ")[^1]);
        _generators[1] = Convert.ToInt64(_input[1].Split(" ")[^1]);
    }

    public override string PartOne()
    {
        Reset();
        var pairs = 0L;

        for (long i = 0L; i < 40000000L; i++)
        {
            _generators[0] = _generators[0] * _factors[0] % _divisor;
            _generators[1] = _generators[1] * _factors[1] % _divisor;
                
            pairs += (_generators[0] & 65535L) == (_generators[1] & 65535L) ? 1 : 0;
        }

        return Convert.ToString(pairs);
    }
    
    public override string PartTwo()
    {
        Reset();
        var queues = new Queue<long>[2] { new Queue<long>(), new Queue<long>() };
        var pairs = 0L;

        var i = 0L;
        while (i < 5000000L)
        {
            _generators[0] = _generators[0] * _factors[0] % _divisor;
            _generators[1] = _generators[1] * _factors[1] % _divisor;

            if ((_generators[0] & 3L) == 0L)
            {
                queues[0].Enqueue(_generators[0]);
            }
            if ((_generators[1] & 7L) == 0L)
            {
                queues[1].Enqueue(_generators[1]);
            }

            while (queues[0].Count > 0 && queues[1].Count > 0)
            {
                pairs += (queues[0].Dequeue() & 65535L) == (queues[1].Dequeue() & 65535L) ? 1 : 0;

                i++;
                if (i >= 5000000L)
                {
                    break;
                }
            }
        }

        return Convert.ToString(pairs);
    }
}