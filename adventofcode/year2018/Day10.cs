using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day10 : Solution
{
    private string[] _input;
    
    public Day10(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var sm = new StarMessage(_input);
        sm.Search();
        sm.Show();
        return Convert.ToString("");
    }

    public override string PartTwo()
    {
        var sm = new StarMessage(_input);
        var time = sm.Search();
        return Convert.ToString(time);
    }

    private class StarMessage
    {
        private List<Point2D> _stars;
        private List<Point2D> _velocities;
            
        public StarMessage(string[] data)
        {
            _stars = new List<Point2D>();
            _velocities = new List<Point2D>();

            foreach (var d in data)
            {
                var match = Regex.Match(d, @"position=<(.*)> velocity=<(.*)>");
                var position = match.Groups[1].Value.Split(",");
                var speed = match.Groups[2].Value.Split(",");
                _stars.Add(new Point2D(Convert.ToInt32(position[0]), Convert.ToInt32(position[1])));
                _velocities.Add(new Point2D(Convert.ToInt32(speed[0]), Convert.ToInt32(speed[1])));
            }
        }

        public void Show()
        {
            var minX = _stars.Aggregate(99999, (acc, p) => acc > p.X() ? p.X() : acc);
            var maxX = _stars.Aggregate(0, (acc, p) => acc < p.X() ? p.X() : acc);
            var minY = _stars.Aggregate(99999, (acc, p) => acc > p.Y() ? p.Y() : acc);
            var maxY = _stars.Aggregate(0, (acc, p) => acc < p.Y() ? p.Y() : acc);
            var width = maxX - minX + 3;
            var height = maxY - minY + 3;

            var grid = new char[width, height];
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    grid[x, y] = '.';
                }
            }

            var offsetX = -minX;
            var offsetY = -minY;
            foreach (var star in _stars)
            {
                grid[star.X() + offsetX + 1, star.Y() + offsetY + 1] = '#';
            }
            
            Draw<char>.ShowGrid(grid);
        }

        public int Search()
        {
            var previousHeight = _stars.Aggregate(0, (acc, p) => acc < p.Y() ? p.Y() : acc) - _stars.Aggregate(0, (acc, p) => acc > p.Y() ? p.Y() : acc);
            var time = 1;
            while (true)
            {
                var stars = new List<Point2D>();
                for (int i = 0; i < _velocities.Count; i++)
                {
                    stars.Add(_stars[i] + _velocities[i] * time);
                }
                var height = stars.Aggregate(0, (acc, p) => acc < p.Y() ? p.Y() : acc) - stars.Aggregate(0, (acc, p) => acc > p.Y() ? p.Y() : acc);

                if (height > previousHeight)
                {
                    break;
                }

                previousHeight = height;
                time++;
            }
            
            for (int i = 0; i < _velocities.Count; i++)
            {
                _stars[i] +=_velocities[i] * (time - 1);
            }

            return time - 1;
        }
    }
}