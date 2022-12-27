using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.range;
using System.Text.RegularExpressions;

namespace adventofcode.year2022;

public class Day15 : Solution
{
    private List<Sensor> _sensors;
    private HashSet<Point> _beacons;

    public Day15(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();
        _sensors = new List<Sensor>();
        _beacons = new HashSet<Point>();

        foreach (var line in input)
        {
            var match = Regex.Match(line, @"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$");
            var sp = new Point(Convert.ToInt32(match.Groups[1].Value), Convert.ToInt32(match.Groups[2].Value));
            var bp = new Point(Convert.ToInt32(match.Groups[3].Value), Convert.ToInt32(match.Groups[4].Value));
            
            _sensors.Add(new Sensor(sp, bp));
            _beacons.Add(bp);
        }
    }

    public override string PartOne()
    {
        var targetY = 2000000;
        var intervals = new List<Interval>();
        foreach (var sensor in _sensors)
        {
            var i = sensor.CoveragXAtY(targetY);

            if (!(i is null))
            {
                intervals.Add(i);
            }
        }

        // from coverage of all sensors at target y, add up the interval ranges but account for possible beacons that are in those ranges
        var totalRange = 0;
        var beaconsAtY = 0;
        var coverage = new SignalCoverage(intervals);
        foreach (var i in coverage.Intervals())
        {
            totalRange += i.Right() - i.Left() + 1;

            foreach (var b in _beacons)
            {
                if (b.Y() == targetY && i.Contains(b.X()))
                {
                    beaconsAtY++;
                }
            }
        }

        totalRange -= beaconsAtY;

        return Convert.ToString(totalRange);
    }

    public override string PartTwo()
    {
        var beaconX = -1;
        var beaconY = -1;
        
        var maxRange = 4000000;
        var maxInterval = new Interval(0, maxRange);
        for (var targetY = 0; targetY <= maxRange; targetY++)
        {
            var intervals = new List<Interval>();
            foreach (var sensor in _sensors)
            {
                var i = sensor.CoveragXAtY(targetY);

                if (i is not null)
                {
                    intervals.Add(i);
                }
            }
            
            // from coverage of all sensors at target y, there should be only one target y where the interval range does not cover the max range
            var coverage = new SignalCoverage(intervals);
            var tmp = maxInterval.Intersect(coverage.Intervals().First());
            if (tmp is null)
            {
                throw new Exception("Unexpected failure in intersecting intervals");
            }

            if (!maxInterval.Equals(tmp))
            {
                beaconY = targetY;
                beaconX = tmp.Left() == 0 ? tmp.Right() + 1 : tmp.Left() - 1;
                break;
            }
        }

        Console.WriteLine($"x : {beaconX}");
        Console.WriteLine($"y : {beaconY}");

        var frequency = Convert.ToInt64(beaconX) * 4000000L + Convert.ToInt64(beaconY);

        return Convert.ToString(frequency);
    }
}

internal class Sensor
{
    private Point _sensorPoint;
    private int _radius;

    public Sensor(Point sensor, Point beacon)
    {
        _sensorPoint = sensor;
        _radius = Math.Abs(_sensorPoint.X() - beacon.X()) + Math.Abs(_sensorPoint.Y() - beacon.Y());
    }

    public Interval? CoveragXAtY(int y)
    {
        if (y >= _sensorPoint.Y() - _radius && y <= _sensorPoint.Y() + _radius)
        {
            var diffY = Math.Abs(_sensorPoint.Y() - y);
            var diffX = Math.Abs(_radius - diffY);
            var minX = _sensorPoint.X() - diffX;
            var maxX = _sensorPoint.X() + diffX;
            
            return new Interval(minX, maxX);
        }

        return null;
    }
}

internal class SignalCoverage
{
    private List<Interval> _intervals;

    public SignalCoverage(List<Interval> intervals)
    {
        _intervals = new List<Interval>();

        // combine overlapping coverages
        intervals.Sort();
        Interval? currentInterval = null;
        foreach (var i in intervals)
        {
            if (currentInterval is null)
            {
                currentInterval = i;
            }
            else
            {
                var tmp = currentInterval.Union(i);
                if (tmp is null)
                {
                    _intervals.Add(currentInterval);
                    currentInterval = i;
                }
                else
                {
                    currentInterval = tmp;
                }
            }
        }

        if (currentInterval is not null)
        {
            _intervals.Add(currentInterval);
        }
    }

    public List<Interval> Intervals()
    {
        return _intervals;
    }
}