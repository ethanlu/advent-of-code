using System.Text.RegularExpressions;
using adventofcode.common;

namespace adventofcode.year2018;

public class Day04 : Solution
{
    private Dictionary<int, Guard> _guards;
    
    public Day04(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines().ToList();
        input.Sort();
        
        _guards = new Dictionary<int, Guard>();
        var id = 0;
        var start = 0;
        var end = 0;
        foreach (var line in input)
        {
            var match = Regex.Match(line, @"Guard #(\d+) begins shift");
            if (match.Success)
            {
                id = Convert.ToInt32(match.Groups[1].Value);
                if (!_guards.ContainsKey(id))
                {
                    _guards.Add(id, new Guard(id));
                }
                continue;
            }
            
            match = Regex.Match(line, @":(\d+)] falls asleep");
            if (match.Success)
            {
                start = Convert.ToInt32(match.Groups[1].Value);
                continue;
            }
            
            match = Regex.Match(line, @":(\d+)] wakes up");
            if (match.Success)
            {
                end = Convert.ToInt32(match.Groups[1].Value);
                _guards[id].LogSleep(start, end);
                continue;
            }
        }
    }

    public override string PartOne()
    {
        var id = 0;
        var sleep = 0;
        foreach (var kv in _guards)
        {
            if (kv.Value.TotalSleep() > sleep)
            {
                id = kv.Key;
                sleep = kv.Value.TotalSleep();
            }
        }

        return Convert.ToString(_guards[id].HighestSleepMinute() * id);
    }

    public override string PartTwo()
    {
        var id = 0;
        var sleep = 0;
        foreach (var kv in _guards)
        {
            if (kv.Value.HighestSleepCount() > sleep)
            {
                id = kv.Key;
                sleep = kv.Value.HighestSleepCount();
            }
        }

        return Convert.ToString(_guards[id].HighestSleepMinute() * id);
    }

    private class Guard
    {
        private int _id;
        private int[] _sleep;
        private int _totalSleep;
        private int _highestSleepCount;

        public Guard(int id)
        {
            _id = id;
            _sleep = new int[60];
            _totalSleep = 0;
            _highestSleepCount = 0;
        }

        public int TotalSleep() { return _totalSleep; }
        public int HighestSleepCount() { return _highestSleepCount; }

        public int HighestSleepMinute()
        {
            var largestSleepMinute = 0;
            var sleep = 0;
            for (int i = 0; i < _sleep.Length; i++)
            {
                if (_sleep[i] > sleep)
                {
                    largestSleepMinute = i;
                    sleep = _sleep[i];
                }
            }

            return largestSleepMinute;
        }

        public void LogSleep(int start, int end)
        {
            _totalSleep += end - start;
            for (int i = start; i < end; i++)
            {
                _sleep[i]++;
                _highestSleepCount = _sleep[i] > _highestSleepCount ? _sleep[i] : _highestSleepCount;
            }
        }
    }
}