using adventofcode.common;
using adventofcode.common.grid;

namespace adventofcode.year2017;

public class Day03 : Solution
{
    private int _input;
    
    public Day03(string year, string day) : base(year, day)
    {
        _input = Convert.ToInt32(LoadInputAsString());
    }

    public override string PartOne()
    {
        var db = new SpiralDatabase();
        Point2D? dataPointer = null;
        foreach (var i in Enumerable.Range(1, _input))
        {
            dataPointer = db.Add(i);
        }

        return Convert.ToString(Math.Abs(dataPointer?.X() ?? 0) + Math.Abs(dataPointer?.Y() ?? 0));
    }

    public override string PartTwo()
    {
        var db = new SpiralDatabase();
        var dataPointer = db.Add(1);

        while (db.ValueAt(dataPointer) < _input)
        {
            dataPointer = db.AddNeighbors();
        }

        return Convert.ToString(db.ValueAt(dataPointer));
    }
    
    internal enum Direction
    {
        Right = 0, Up = 1, Left = 2, Down = 3
    }

    internal class SpiralDatabase
    {
        private Dictionary<Point2D, int> _data;
        private Point2D _current;
        private Direction _nextAvailable;
        private List<Point2D> _offsets = new List<Point2D>()
        {
            new Point2D(-1, -1), new Point2D(0, -1), new Point2D(1, -1), 
            new Point2D(-1, 0), new Point2D(1, 0),
            new Point2D(-1, 1), new Point2D(0, 1), new Point2D(1, 1)
        };

        public SpiralDatabase()
        {
            _data = new Dictionary<Point2D, int>();
            _current = new Point2D(0, 0);
            _nextAvailable = Direction.Right;
        }

        public int ValueAt(Point2D dataPointer)
        {
            return _data.ContainsKey(dataPointer) ? _data[dataPointer] : 0;
        }

        public Point2D Add(int number)
        {
            var dataPointer = _current;
            _data[_current] = number;

            switch (_nextAvailable)
            {
                case Direction.Right:
                    _current += new Point2D(1, 0);
                    _nextAvailable = _data.ContainsKey(_current + new Point2D(0, -1)) ? _nextAvailable : Direction.Up;
                    break;
                case Direction.Up:
                    _current += new Point2D(0, -1);
                    _nextAvailable = _data.ContainsKey(_current + new Point2D(-1, 0)) ? _nextAvailable : Direction.Left;
                    break;
                case Direction.Left:
                    _current += new Point2D(-1, 0);
                    _nextAvailable = _data.ContainsKey(_current + new Point2D(0, 1)) ? _nextAvailable : Direction.Down;
                    break;
                case Direction.Down:
                    _current += new Point2D(0, 1);
                    _nextAvailable = _data.ContainsKey(_current + new Point2D(1, 0)) ? _nextAvailable : Direction.Right;
                    break;
                default:
                    throw new Exception($"Invalid direction : {_nextAvailable}");
            }

            return dataPointer;
        }

        public Point2D AddNeighbors()
        {
            var sum = 0;
            foreach (var offset in _offsets)
            {
                var neighbor = _current + offset;
                sum += _data.ContainsKey(neighbor) ? _data[neighbor] : 0;
            }

            return Add(sum);
        }
    }

}