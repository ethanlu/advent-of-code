using adventofcode.common;
using adventofcode.common.util;

namespace adventofcode.year2017;

public class Day13 : Solution
{
    private string[] _input;
    
    public Day13(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var fw = new Firewall(_input);
        
        return Convert.ToString(fw.Run(0L).Item2);
    }

    public override string PartTwo()
    {
        var fw = new Firewall(_input);
        var smallestDelay = 0L;
        
        for (long delay = 0; delay < fw.MaxInterval(); delay++)
        {
            var (triggered, severity) = fw.Run(delay);

            if (!triggered)
            {
                smallestDelay = delay;
                break;
            }
        }

        return Convert.ToString(smallestDelay);
    }

    private class Scanner
    {
        private int _depth;
        private int _range;
        private int _interval;

        public Scanner(int depth, int range)
        {
            _depth = depth;
            _range = range;
            _interval = (range - 1) * 2;
        }
        
        public int Depth() { return _depth; }
        public int Range() { return _range; }
        public int Interval() { return _interval; }
    }

    private class Firewall
    {
        private Dictionary<int, Scanner> _scanners;
        private int _maxLayer;
        private long _maxInterval;
        
        public Firewall(string[] scanners)
        {
            _scanners = new Dictionary<int, Scanner>();
            _maxLayer = 0;

            foreach (var s in scanners)
            {
                var t = s.Split(": ");
                var scanner = new Scanner(Convert.ToInt32(t[0]), Convert.ToInt32(t[1]));
                _scanners.Add(scanner.Depth(), scanner);
                _maxLayer = scanner.Depth() > _maxLayer ? scanner.Depth() : _maxLayer;
            }
            
            _maxInterval = _scanners.Values.Select(s => s.Interval()).Distinct().Aggregate((acc, i) => MathTools.LCM(acc, i));
        }

        public long MaxInterval() { return _maxInterval; }

        public (bool, long) Run(long delay)
        {
            var severity = 0L;

            var picosecond = delay;
            var triggered = false;
            for (int layer = 0; layer <= _maxLayer; layer++)
            {
                if (_scanners.ContainsKey(layer) && picosecond % _scanners[layer].Interval() == 0L)
                {
                    triggered = true;
                    severity += _scanners[layer].Depth() * _scanners[layer].Range();
                }
                picosecond++;
            }

            return (triggered, severity);
        }
    }
}