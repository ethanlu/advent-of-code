using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.range;
using adventofcode.common.util;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day03 : Solution
{
    private Dictionary<int, Box2D> _squares;
    
    public Day03(string year, string day) : base(year, day)
    {
        _squares = new Dictionary<int, Box2D>();
        foreach (var line in LoadInputAsLines())
        {
            var match = Regex.Match(line, @"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)");
            var topLeft = new Point2D(Convert.ToInt32(match.Groups[2].Value), Convert.ToInt32(match.Groups[3].Value));
            var bottomRight = topLeft + new Point2D(Convert.ToInt32(match.Groups[4].Value), Convert.ToInt32(match.Groups[5].Value));
            _squares.Add(Convert.ToInt32(match.Groups[1].Value), new Box2D(topLeft, bottomRight));
        }
    }

    public override string PartOne()
    {
        var overlaps = new HashSet<Point2D>();
        foreach (var combination in IterTools<Box2D>.Combination(_squares.Values.ToList(), 2))
        {
            var intersection = combination[0].Intersect(combination[1]);
            if (intersection is not null)
            {
                for (int x = 0; x < intersection.Width(); x++)
                {
                    for (int y = 0; y < intersection.Height(); y++)
                    {
                        overlaps.Add(new Point2D(intersection.TopLeft().X() + x, intersection.TopLeft().Y() + y));
                    }
                }
            }
        }

        return Convert.ToString(overlaps.Count);
    }

    public override string PartTwo()
    {
        var squareID = -1;
        foreach (var a in _squares)
        {
            var overlap = false;
            foreach (var b in _squares)
            {
                if (a.Key == b.Key) { continue; }
                if (a.Value.Intersect(b.Value) is not null)
                {
                    overlap = true;
                    break;
                }
            }

            if (!overlap)
            {
                squareID = a.Key;
                break;
            }
        }

        return Convert.ToString(squareID);
    }
}