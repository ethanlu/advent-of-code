using adventofcode.common;
using adventofcode.common.grid;

namespace adventofcode.year2017;

public class Day11 : Solution
{
    private string _input;
    
    public Day11(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var hg = new HexaGrid(_input);
        hg.Trace();
        
        return Convert.ToString(hg.Distance(hg.Position()));
    }

    public override string PartTwo()
    {
        var hg = new HexaGrid(_input);
        hg.Trace();
        
        return Convert.ToString(hg.MaxDistance());
    }

    private class HexaGrid
    {
        private List<string> _path;
        private Point2D _position;
        private int _max_distance;

        public HexaGrid(string path)
        {
            _path = new List<string>(path.Split(",").ToList());
            _position = new Point2D();
            _max_distance = 0;
        }

        public Point2D Position()
        {
            return _position;
        }

        public int MaxDistance()
        {
            return _max_distance;
        }

        public int Distance(Point2D position)
        {
            return Math.Abs(position.X() / 2) + Math.Abs(position.Y() / 2) + (Math.Abs(position.X() % 2) + Math.Abs(position.Y() % 2)) / 2;
        }

        private Point2D Offset(string direction) =>
            direction switch
            {
                "n" => new Point2D(0, -2),
                "s" => new Point2D(0, 2),
                "nw" => new Point2D(-1, -1),
                "ne" => new Point2D(1, -1),
                "sw" => new Point2D(-1, 1),
                "se" => new Point2D(1, 1),
            };

        public void Trace()
        {
            foreach (var step in _path)
            {
                _position += Offset(step);
                
                var distance = Distance(_position);
                _max_distance = distance > _max_distance ? distance : _max_distance;
            }
        }
    }
}