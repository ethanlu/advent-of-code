using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;

namespace adventofcode.year2017;

public class Day22 : Solution
{
    private string[] _input;
    
    public Day22(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var vd = new VirusDiagnostic(_input, new Virus());
        for (int i = 0; i < 10000; i++)
        {
            vd.Burst();
        }
        vd.Show();

        return Convert.ToString(vd.Infected());
    }

    public override string PartTwo()
    {
        var vd = new VirusDiagnostic(_input, new EvolvedVirus());
        for (int i = 0; i < 10000000; i++)
        {
            vd.Burst();
        }
        vd.Show();

        return Convert.ToString(vd.Infected());
    }
    
    private enum Direction
    {
        Up = 0, Down = 1, Left = 2, Right = 3
    }
    
    private interface IVirus
    {
        public Point2D Position();
        public int Burst(Dictionary<Point2D, char> grid);
        public void Move(Dictionary<Point2D, char> grid);
    }

    private class Virus : IVirus
    {
        protected Direction _facing;
        protected Point2D _position;

        public Virus()
        {
            _position = new Point2D(0, 0);
            _facing = Direction.Up;
        }

        public Point2D Position() { return _position; }

        public virtual int Burst(Dictionary<Point2D, char> grid)
        {
            // update direction
            switch (_facing)
            {
                case Direction.Up:
                    _facing = grid[_position] == '#' ? Direction.Right : Direction.Left;
                    break;
                case Direction.Down:
                    _facing = grid[_position] == '#' ? Direction.Left : Direction.Right;
                    break;
                case Direction.Left:
                    _facing = grid[_position] == '#' ? Direction.Up : Direction.Down;
                    break;
                case Direction.Right:
                    _facing = grid[_position] == '#' ? Direction.Down : Direction.Up;
                    break;
            }
            
            // update node state
            grid[_position] = grid[_position] == '#' ? '.' : '#';

            return grid[_position] == '#' ? 1 : 0;
        }

        public void Move(Dictionary<Point2D, char> grid)
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
            if (!grid.ContainsKey(_position))
            {
                grid.Add(_position, '.');
            }
        }
    }

    private class EvolvedVirus : Virus
    {
        public override int Burst(Dictionary<Point2D, char> grid)
        {
            // update direction
            switch (_facing)
            {
                case Direction.Up:
                    switch (grid[_position])
                    {
                        case '.':
                            _facing = Direction.Left;
                            break;
                        case '#':
                            _facing = Direction.Right;
                            break;
                        case 'F':
                            _facing = Direction.Down;
                            break;
                    }
                    break;
                case Direction.Down:
                    switch (grid[_position])
                    {
                        case '.':
                            _facing = Direction.Right;
                            break;
                        case '#':
                            _facing = Direction.Left;
                            break;
                        case 'F':
                            _facing = Direction.Up;
                            break;
                    }
                    break;
                case Direction.Left:
                    switch (grid[_position])
                    {
                        case '.':
                            _facing = Direction.Down;
                            break;
                        case '#':
                            _facing = Direction.Up;
                            break;
                        case 'F':
                            _facing = Direction.Right;
                            break;
                    }
                    break;
                case Direction.Right:
                    switch (grid[_position])
                    {
                        case '.':
                            _facing = Direction.Up;
                            break;
                        case '#':
                            _facing = Direction.Down;
                            break;
                        case 'F':
                            _facing = Direction.Left;
                            break;
                    }
                    break;
            }
            
            // update node state
            var infected = 0;
            switch (grid[_position])
            {
                case '.':
                    grid[_position] = 'W';
                    break;
                case '#':
                    grid[_position] = 'F';
                    break;
                case 'W':
                    grid[_position] = '#';
                    infected++;
                    break;
                case 'F':
                    grid[_position] = '.';
                    break;
            }

            return infected;
        }
    }

    private class VirusDiagnostic
    {
        private Dictionary<Point2D, char> _grid;
        private IVirus _virus;
        private int _infected;

        public VirusDiagnostic(string[] map, IVirus virus)
        {
            _grid = new Dictionary<Point2D, char>();
            _virus = virus;
            _infected = 0;

            var offset = map.Length / 2;
            for (int y = 0; y < map.Length; y++)
            {
                for (int x = 0; x < map[y].Length; x++)
                {
                    _grid.Add(new Point2D(x - offset, y - offset), map[y][x]);
                }
            }
        }

        public int Infected() { return _infected; }

        public void Show()
        {
            var minX = _grid.Aggregate(0, (acc, kv) => kv.Key.X() < acc ? kv.Key.X() : acc) - 1;
            var maxX = _grid.Aggregate(0, (acc, kv) => kv.Key.X() > acc ? kv.Key.X() : acc) + 1;
            var minY = _grid.Aggregate(0, (acc, kv) => kv.Key.Y() < acc ? kv.Key.Y() : acc) - 1;
            var maxY = _grid.Aggregate(0, (acc, kv) => kv.Key.Y() > acc ? kv.Key.Y() : acc) + 1;

            var grid = new char[maxX - minX + 1, maxY - minY + 1];
            for (int x = 0; x <= maxX - minX; x++)
            {
                for (int y = 0; y <= maxY - minY; y++)
                {
                    grid[x, y] = '.';
                }
            }
            foreach (var kv in _grid)
            {
                grid[kv.Key.X() - minX, kv.Key.Y() - minY] = kv.Value;
            }
            grid[_virus.Position().X() - minX, _virus.Position().Y() - minY] = '@';
            Draw<char>.ShowGrid(grid);
        }

        public void Burst()
        {
            _infected += _virus.Burst(_grid);
            _virus.Move(_grid);
        }
    }
}