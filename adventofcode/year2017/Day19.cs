using adventofcode.common;
using adventofcode.common.grid;

namespace adventofcode.year2017;

public class Day19 : Solution
{
    private string[] _input;
    
    public Day19(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var tm = new TubeMaze(_input);
        tm.Traverse();
        return Convert.ToString(tm.Path());
    }

    public override string PartTwo()
    {
        var tm = new TubeMaze(_input);
        tm.Traverse();
        return Convert.ToString(tm.Steps());
    }
    
    private enum Direction
    {
        Up = 0, Down = 1, Right = 2, Left = 3
    }

    private class TubeMaze
    {
        private Dictionary<Point2D, char> _tubes;
        private Point2D _position;
        private Direction _facing;
        private string _path;
        private int _steps;
        
        public TubeMaze(string[] map)
        {
            _facing = Direction.Down;
            _tubes = new Dictionary<Point2D, char>();
            _path = "";
            _steps = 0;
            
            for (int y = 0; y < map.Length; y++)
            {
                for (int x = 0; x < map[y].Length; x++)
                {
                    if (map[y][x] != ' ')
                    {
                        var p = new Point2D(x, y);
                        _tubes.Add(p, map[y][x]);

                        if (y == 0)
                        {
                            _position = p;
                        }
                    }
                }
            }
        }

        private Point2D NextPosition(Direction direction) =>
            direction switch
            {
                Direction.Up => _position + new Point2D(0, -1),
                Direction.Down => _position + new Point2D(0, 1),
                Direction.Right => _position + new Point2D(1, 0),
                Direction.Left => _position + new Point2D(-1, 0),
                _ => throw new Exception($"Invalid direction : {direction}")
            };

        public string Path() { return _path; }
        public int Steps() { return _steps; }

        public void Traverse()
        {
            var done = false;
            while (!done)
            {
                switch (_tubes[_position])
                {
                    case '|':
                    case '-':
                        _position = NextPosition(_facing);
                        break;
                    case '+':
                        var nextPosition = NextPosition(_facing);
                        switch (_facing)
                        {
                            case Direction.Up:
                            case Direction.Down:
                                nextPosition = NextPosition(Direction.Left);
                                _facing = Direction.Left;
                                if (!_tubes.ContainsKey(nextPosition))
                                {
                                    nextPosition = NextPosition(Direction.Right);
                                    _facing = Direction.Right;
                                }
                                break;
                            case Direction.Right:
                            case Direction.Left:
                                nextPosition = NextPosition(Direction.Up);
                                _facing = Direction.Up;
                                if (!_tubes.ContainsKey(nextPosition))
                                {
                                    nextPosition = NextPosition(Direction.Down);
                                    _facing = Direction.Down;
                                }
                                break;
                        }
                        _position = nextPosition;
                        break;
                    default:
                        _path += _tubes[_position];
                        
                        _position = NextPosition(_facing);

                        if (!_tubes.ContainsKey(_position))
                        {
                            done = true;
                        }
                        break;
                }
                _steps++;
            }
        }
    }
}