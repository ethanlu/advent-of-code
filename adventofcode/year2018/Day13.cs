using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;

namespace adventofcode.year2018;

public class Day13 : Solution
{
    private string[] _input;
    
    public Day13(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var mt = new MineTrack(_input);
        var p = mt.FirstCrash();
        mt.Show(p);
        return Convert.ToString($"{p.X()},{p.Y()}");
    }

    public override string PartTwo()
    {
        var mt = new MineTrack(_input);
        var p = mt.LastCart();
        mt.Show(p);
        return Convert.ToString($"{p.X()},{p.Y()}");
    }
    
    private enum Direction
    {
        Up = 0, Down = 1, Right = 2, Left = 3
    }

    private class MineCart : IComparable<MineCart>
    {
        private Point2D _position;
        private Direction _facing;
        private int _turnIndex;
        
        public MineCart(Point2D start, Direction facing)
        {
            _position = start;
            _facing = facing;
            _turnIndex = 0;
        }

        public Point2D Position() { return _position; }
        public Direction Facing() { return _facing; }

        public void Move()
        {
            switch (_facing)
            {
                case Direction.Up:
                    _position += new Point2D(0, -1);
                    break;
                case Direction.Down:
                    _position += new Point2D(0, 1);
                    break;
                case Direction.Left:
                    _position += new Point2D(-1, 0);
                    break;
                case Direction.Right:
                    _position += new Point2D(1, 0);
                    break;
            }
        }

        public void Turn(char track)
        {
            switch (track)
            {
                case '/':
                case '\\':
                    switch (_facing)
                    {
                        case Direction.Up:
                            _facing = track == '/' ? Direction.Right : Direction.Left;
                            break;
                        case Direction.Down:
                            _facing = track == '/' ? Direction.Left : Direction.Right;
                            break;
                        case Direction.Left:
                            _facing = track == '/' ? Direction.Down : Direction.Up;
                            break;
                        case Direction.Right:
                            _facing = track == '/' ? Direction.Up : Direction.Down;
                            break;
                    }
                    break;
                case '+':
                    switch (_turnIndex)
                    {
                        case 0: // turn left
                            switch (_facing)
                            {
                                case Direction.Up:
                                    _facing = Direction.Left;
                                    break;
                                case Direction.Down:
                                    _facing = Direction.Right;
                                    break;
                                case Direction.Left:
                                    _facing = Direction.Down;
                                    break;
                                case Direction.Right:
                                    _facing = Direction.Up;
                                    break;
                            }
                            _turnIndex++;
                            break;
                        case 1: // go straight
                            _turnIndex++;
                            break;
                        case 2: // turn right
                            switch (_facing)
                            {
                                case Direction.Up:
                                    _facing = Direction.Right;
                                    break;
                                case Direction.Down:
                                    _facing = Direction.Left;
                                    break;
                                case Direction.Left:
                                    _facing = Direction.Up;
                                    break;
                                case Direction.Right:
                                    _facing = Direction.Down;
                                    break;
                            }
                            _turnIndex = 0;
                            break;
                    }
                    break;
            }
        }
        
        public int CompareTo(MineCart? c)
        {
            if (c is null)
            {
                throw new Exception("MineCart input is null");
            }

            if ((_position.X() + _position.Y()) < (c.Position().X() + c.Position().Y()))
            {
                return -1;
            }
            if ((_position.X() + _position.Y()) > (c.Position().X() + c.Position().Y()))
            {
                return 1;
            }
            return 0;
        }
    }

    private class MineTrack
    {
        private Dictionary<Point2D, char> _tracks;
        private List<MineCart> _carts;
        
        public MineTrack(string[] map)
        {
            _carts = new List<MineCart>();
            _tracks = new Dictionary<Point2D, char>();

            for (int y = 0; y < map.Length; y++)
            {
                for (int x = 0; x < map[y].Length; x++)
                {
                    var p = new Point2D(x, y);
                    switch (map[y][x])
                    {
                        case '^':
                        case 'v':
                            _carts.Add(new MineCart(p, map[y][x] == '^' ? Direction.Up : Direction.Down));
                            _tracks.Add(p, '|');
                            break;
                        case '<':
                        case '>':
                            _carts.Add(new MineCart(p, map[y][x] == '<' ? Direction.Left : Direction.Right));
                            _tracks.Add(p, '-');
                            break;
                        case '|':
                        case '-':
                        case '/': 
                        case '\\':
                        case '+':
                            _tracks.Add(p, map[y][x]);
                            break;
                        default:
                            continue;
                    }
                }
            }
        }

        public void Show(Point2D crashPoint)
        {
            var maxX = _tracks.Aggregate(0, (acc, kv) => acc < kv.Key.X() ? kv.Key.X() : acc);
            var maxY = _tracks.Aggregate(0, (acc, kv) => acc < kv.Key.Y() ? kv.Key.Y() : acc);
            var grid = new char[maxX +  1, maxY + 1];

            for (int x = 0; x <= maxX; x++)
            {
                for (int y = 0; y <= maxY; y++)
                {
                    var p = new Point2D(x, y);

                    grid[x, y] = ' ';
                    if (_tracks.ContainsKey(p))
                    {
                        grid[x, y] = _tracks[p];
                    }
                }
            }
            foreach (var cart in _carts)
            {
                switch (cart.Facing())
                {
                    case Direction.Up:
                        grid[cart.Position().X(), cart.Position().Y()] = '^';
                        break;
                    case Direction.Down:
                        grid[cart.Position().X(), cart.Position().Y()] = 'v';
                        break;
                    case Direction.Left:
                        grid[cart.Position().X(), cart.Position().Y()] = '<';
                        break;
                    case Direction.Right:
                        grid[cart.Position().X(), cart.Position().Y()] = '>';
                        break;
                }
            }
            
            grid[crashPoint.X(), crashPoint.Y()] = 'X';
            Draw<char>.ShowGrid(grid);
        }

        public Point2D FirstCrash()
        {
            var crashPoint = new Point2D(0, 0);
            var crashed = false;
            while (!crashed)
            {
                var remainingPositions = new HashSet<Point2D>(_carts.Select(c => c.Position()).ToList());
                var nextPositions = new HashSet<Point2D>();
                foreach (var cart in _carts)
                {
                    remainingPositions.Remove(cart.Position());
                    cart.Move();
                    if (remainingPositions.Contains(cart.Position()) || nextPositions.Contains(cart.Position()))
                    {
                        crashed = true;
                        crashPoint = cart.Position();
                        break;
                    }
                    nextPositions.Add(cart.Position());
                    cart.Turn(_tracks[cart.Position()]);
                }
                _carts.Sort();
            }

            return crashPoint;
        }
        
        public Point2D LastCart()
        {
            while (_carts.Count > 1)
            {
                var remainingPositions = new HashSet<Point2D>(_carts.Select(c => c.Position()).ToList());
                var nextPositions = new Dictionary<Point2D, MineCart>();
                var crashPoints = new HashSet<Point2D>();
                foreach (var cart in _carts)
                {
                    remainingPositions.Remove(cart.Position());
                    
                    if (crashPoints.Contains(cart.Position()))
                    {   // a cart crashed into this cart
                        continue;
                    }

                    cart.Move();
                    
                    if (remainingPositions.Contains(cart.Position()))
                    {   // this cart crashed into another cart that didnt move yet
                        crashPoints.Add(cart.Position());
                        continue;
                    }
                    
                    if (nextPositions.ContainsKey(cart.Position()))
                    {   // this cart crashed into another cart that already moved
                        nextPositions.Remove(cart.Position());
                        continue;
                    }
                    
                    nextPositions.Add(cart.Position(), cart);
                    cart.Turn(_tracks[cart.Position()]);
                }

                _carts = new List<MineCart>();
                foreach (var carts in nextPositions.Values)
                {
                    _carts.Add(carts);
                }
                _carts.Sort();
            }

            return _carts.First().Position();
        }
    }
}