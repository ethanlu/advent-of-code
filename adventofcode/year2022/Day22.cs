using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;
using System.Text.RegularExpressions;
using adventofcode.common.range;

namespace adventofcode.year2022;

public class Day22 : Solution
{
    private List<string> _mapRows;
    private string _moves;
    
    public Day22(string year, string day) : base(year, day)
    {
        _mapRows = new List<string>();
        _moves = "";
        
        var readingMoves = false;
        foreach (var line in LoadInputAsLines())
        {
            if (line.Length == 0)
            {
                readingMoves = true;
                continue;
            }
            if (readingMoves)
            {
                _moves += line;
            }
            else
            {
                _mapRows.Add(line);
            }
        }
    }

    public override string PartOne()
    {
        var map = new FlatMap(_mapRows, _moves);
        var password = map.Walk();
        return Convert.ToString(password);
    }

    public override string PartTwo()
    {
        IMap map = _mapRows.Count > 15 ? new BigCubeMap(_mapRows, _moves) : new SmallCubeMap(_mapRows, _moves);
        var password = map.Walk();
        return Convert.ToString(password);
    }
}

enum Direction
{
    Right = 0, Down = 1, Left = 2, Up = 3
}

internal interface IMap
{
    int Walk();
}

internal abstract class Map : IMap
{
    protected int _height;
    protected int _width;
    protected char[,] _map;
    protected List<(char, int)> _moves;
    protected Point2D _position;
    protected Direction _orientation;
    protected List<(Point2D, Direction)> _trail;
    
    public Map(List<string> mapRows, string moves)
    {
        _height = mapRows.Count;
        _width = mapRows.Aggregate(0, (acc, row) => Math.Max(acc, row.Length));
        _map = new char[_width, _height];

        foreach (var y in Enumerable.Range(0, _height))
        {
            foreach (var x in Enumerable.Range(0, _width))
            {
                _map[x, y] = x < mapRows[y].Length ? mapRows[y][x] : ' ';
            }
        }
        
        _position = new Point2D(Enumerable.Range(0, _width).Aggregate(_width, (acc, x) => _map[x, 0] == '.' ? Math.Min(x, acc) : acc), 0);
        _orientation = Direction.Right;
        _trail = new List<(Point2D, Direction)>();

        _moves = new List<(char, int)>();
        foreach (Match match in Regex.Matches(moves, @"(\d+)([LR]?)"))
        {
            _moves.Add((match.Groups[2].Value.Length > 0 ? match.Groups[2].Value.ToCharArray()[0] : 'X', Convert.ToInt32(match.Groups[1].Value)));
        }
    }
    
    protected char[,] MarkTrail()
    {
        var map = new char[_width, _height];

        foreach (var y in Enumerable.Range(0, _height))
        {
            foreach (var x in Enumerable.Range(0, _width))
            {
                map[x, y] = _map[x, y];
            }
        }

        foreach (var (position, facing) in _trail)
        {
            switch (facing)
            {
                case Direction.Right:
                    map[position.X(), position.Y()] = '>';
                    break;
                case Direction.Down:
                    map[position.X(), position.Y()] = 'v';
                    break;
                case Direction.Left:
                    map[position.X(), position.Y()] = '<';
                    break;
                case Direction.Up:
                    map[position.X(), position.Y()] = '^';
                    break;
            }
        }
        map[_position.X(), _position.Y()] = '@';

        return map;
    }

    protected Point2D CurrentDelta()
    {
        Point2D delta = new Point2D(0, 0);
        switch (_orientation)
        {
            case Direction.Right:
                delta = new Point2D(1, 0);
                break;
            case Direction.Down:
                delta = new Point2D(0, 1);
                break;
            case Direction.Left:
                delta = new Point2D(-1, 0);
                break;
            case Direction.Up:
                delta = new Point2D(0, -1);
                break;
        }

        return delta;
    }

    public int Walk()
    {
        var step = 0;
        foreach (var (turn, steps) in _moves)
        {
            // move in the direction n steps until run into wall
            foreach (var i in Enumerable.Range(0, steps))
            {
                var (nextPosition, orientation) = NextMove(_position);

                // stop movement if it is a wall
                if (_map[nextPosition.X(), nextPosition.Y()] == '#')
                {
                    break;
                }
                
                // otherwise, update trail and move to that position
                _trail.Add((_position, _orientation));
                _position = nextPosition;
                _orientation = orientation;
                step++;
            }

            // turn
            if (turn == 'X')
            {
                continue;
            }
            switch (_orientation)
            {
                case Direction.Right:
                    _orientation = turn == 'L' ? Direction.Up : Direction.Down;
                    break;
                case Direction.Down:
                    _orientation = turn == 'L' ? Direction.Right : Direction.Left;
                    break;
                case Direction.Left:
                    _orientation = turn == 'L' ? Direction.Down : Direction.Up;
                    break;
                case Direction.Up:
                    _orientation = turn == 'L' ? Direction.Left : Direction.Right;
                    break;
            }
        }
        _trail.Add((_position, _orientation));
        
        Draw<char>.ShowGrid(MarkTrail());
        Console.WriteLine($"Steps : {step}");
        Console.WriteLine($"End : ({_position.X()}, {_position.Y()}) [{(int) _orientation}]");
        
        return ((_position.Y() + 1) * 1000) + ((_position.X() + 1) * 4) + (int) _orientation; 
    }
    
    protected abstract (Point2D, Direction) NextMove(Point2D position);
}

internal class FlatMap : Map
{
    public FlatMap(List<string> mapRows, string moves) : base (mapRows, moves) { }

    protected override (Point2D, Direction) NextMove(Point2D position)
    {
        var delta = CurrentDelta();
        var peekPosition = position + delta;
        
        // wrap around because of edge of map
        if (peekPosition.X() < 0 || peekPosition.X() >= _map.GetLength(0) || peekPosition.Y() < 0 || peekPosition.Y() >= _map.GetLength(1))
        { 
            // wrap around X
            if (peekPosition.X() < 0)
            {
                peekPosition = new Point2D(Enumerable.Range(0, _width).Reverse().Aggregate(-1, (acc, x) => _map[x, peekPosition.Y()] != ' ' ? Math.Max(x, acc) : acc), peekPosition.Y());
            }
            if (peekPosition.X() >= _map.GetLength(0))
            {
                peekPosition = new Point2D(Enumerable.Range(0, _width).Aggregate(_width, (acc, x) => _map[x, peekPosition.Y()] != ' ' ? Math.Min(x, acc) : acc), peekPosition.Y());
            }
            // wrap around Y
            if (peekPosition.Y() < 0)
            {
                peekPosition = new Point2D(peekPosition.X(), Enumerable.Range(0, _height).Reverse().Aggregate(-1, (acc, y) => _map[peekPosition.X(), y] != ' ' ? Math.Max(y, acc) : acc));
            }
            if (peekPosition.Y() >= _map.GetLength(1))
            {
                peekPosition = new Point2D(peekPosition.X(), Enumerable.Range(0, _height).Aggregate(_height, (acc, y) => _map[peekPosition.X(), y] != ' ' ? Math.Min(y, acc) : acc));
            }
        }
        // wrap around because of virtual edge of map
        if (_map[peekPosition.X(), peekPosition.Y()] == ' ')
        {
            // wrap around X
            if (delta.X() < 0)
            {
                peekPosition = new Point2D(Enumerable.Range(0, _width).Reverse().Aggregate(-1, (acc, x) => _map[x, peekPosition.Y()] != ' ' ? Math.Max(x, acc) : acc), peekPosition.Y());
            }
            if (delta.X() > 0)
            {
                peekPosition = new Point2D(Enumerable.Range(0, _width).Aggregate(_width, (acc, x) => _map[x, peekPosition.Y()] != ' ' ? Math.Min(x, acc) : acc), peekPosition.Y());
            }
            // wrap around Y
            if (delta.Y() < 0)
            {
                peekPosition = new Point2D(peekPosition.X(), Enumerable.Range(0, _height).Reverse().Aggregate(-1, (acc, y) => _map[peekPosition.X(), y] != ' ' ? Math.Max(y, acc) : acc));
            }
            if (delta.Y() > 0)
            {
                peekPosition = new Point2D(peekPosition.X(), Enumerable.Range(0, _height).Aggregate(_height, (acc, y) => _map[peekPosition.X(), y] != ' ' ? Math.Min(y, acc) : acc));
            }
        }

        return (peekPosition, _orientation);
    }
}

internal class CubeMap : Map
{
    protected List<(Box, Dictionary<Direction, Direction>, Dictionary<Direction, Func<Point2D, Point2D>>)> _wrapMaps;

    public CubeMap(List<string> mapRows, string moves, bool sampleMap=false) : base(mapRows, moves)
    {
        _wrapMaps = new List<(Box, Dictionary<Direction, Direction>, Dictionary<Direction, Func<Point2D, Point2D>>)>();
    }
    
    protected override (Point2D, Direction) NextMove(Point2D position)
    {
        var peekPosition = position + CurrentDelta();
        var orientation = _orientation;

        var sideIndex = 0;
        foreach (var (side, orientationMap, positionMap) in _wrapMaps)
        {
            if (side.Contains(position))
            {
                // moves out of top boundary
                if (peekPosition.Y() < side.TopLeft().Y())
                {
                    orientation = orientationMap[Direction.Up];
                    peekPosition = positionMap[Direction.Up](position);
                    break;
                }
                // moves out of right boundary
                if (peekPosition.X() > side.TopRight().X())
                {
                    orientation = orientationMap[Direction.Right];
                    peekPosition = positionMap[Direction.Right](position);
                    break;
                }
                // moves out of bottom boundary
                if (peekPosition.Y() > side.BottomRight().Y())
                {
                    orientation = orientationMap[Direction.Down];
                    peekPosition = positionMap[Direction.Down](position);
                    break;
                }
                // moves out of left boundary
                if (peekPosition.X() < side.BottomLeft().X())
                {
                    orientation = orientationMap[Direction.Left];
                    peekPosition = positionMap[Direction.Left](position);
                    break;
                }
                // next position stays within side, so no need to adjust position and delta
                break;
            }
            sideIndex++;
        }

        return (peekPosition, orientation);
    }
}

internal class BigCubeMap : CubeMap
{
    public BigCubeMap(List<string> mapRows, string moves, bool sampleMap=false) : base(mapRows, moves)
    {
        //   0011
        //   0011
        //   22
        //   22
        // 3344
        // 3344
        // 55
        // 55;
        _wrapMaps.Add(( // 0
            new Box(new Point2D(50, 0), new Point2D(99, 49)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Right},
                {Direction.Right, Direction.Right},
                {Direction.Down, Direction.Down},
                {Direction.Left, Direction.Right},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(_wrapMaps[5].Item1.TopLeft().X(), _wrapMaps[5].Item1.BottomLeft().Y() - _wrapMaps[0].Item1.TopRight().X() + position.X())},
                {Direction.Right, (position) => new Point2D(position.X() + 1, position.Y())},
                {Direction.Down, (position) => new Point2D(position.X(), position.Y() + 1)},
                {Direction.Left, (position) => new Point2D(_wrapMaps[3].Item1.TopLeft().X(), _wrapMaps[3].Item1.BottomLeft().Y() - position.Y())},
            }
        ));
        _wrapMaps.Add(( // 1
            new Box(new Point2D(100, 0), new Point2D(149, 49)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Up},
                {Direction.Right, Direction.Left},
                {Direction.Down, Direction.Left},
                {Direction.Left, Direction.Left},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(position.X() - _wrapMaps[1].Item1.TopLeft().X(), _wrapMaps[5].Item1.BottomRight().Y())},
                {Direction.Right, (position) => new Point2D(_wrapMaps[4].Item1.BottomRight().X(), _wrapMaps[4].Item1.BottomRight().Y() - position.Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[2].Item1.TopRight().X(), position.X() - _wrapMaps[2].Item1.TopRight().Y())},
                {Direction.Left, (position) => new Point2D(position.X() - 1, position.Y())},
            }
        ));
        _wrapMaps.Add(( // 2
            new Box(new Point2D(50, 50), new Point2D(99, 99)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Up},
                {Direction.Right, Direction.Up},
                {Direction.Down, Direction.Down},
                {Direction.Left, Direction.Down},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(position.X(), position.Y() - 1)},
                {Direction.Right, (position) => new Point2D(_wrapMaps[2].Item1.TopRight().Y() + position.Y(), _wrapMaps[1].Item1.BottomRight().Y())},
                {Direction.Down, (position) => new Point2D(position.X(), position.Y() + 1)},
                {Direction.Left, (position) => new Point2D(position.Y() - _wrapMaps[2].Item1.TopLeft().X(), _wrapMaps[3].Item1.TopLeft().Y())},
            }
        ));
        _wrapMaps.Add(( // 3
            new Box(new Point2D(0, 100), new Point2D(49, 149)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Right},
                {Direction.Right, Direction.Right},
                {Direction.Down, Direction.Down},
                {Direction.Left, Direction.Right},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(_wrapMaps[2].Item1.TopLeft().X(), _wrapMaps[2].Item1.TopLeft().X() + position.X())},
                {Direction.Right, (position) => new Point2D(position.X() + 1, position.Y())},
                {Direction.Down, (position) => new Point2D(position.X(), position.Y() + 1)},
                {Direction.Left, (position) => new Point2D(_wrapMaps[0].Item1.TopLeft().X(), _wrapMaps[3].Item1.BottomLeft().Y() - position.Y())},
            }
        ));
        _wrapMaps.Add(( // 4
            new Box(new Point2D(50, 100), new Point2D(99, 149)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Up},
                {Direction.Right, Direction.Left},
                {Direction.Down, Direction.Left},
                {Direction.Left, Direction.Left},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(position.X(), position.Y() - 1)},
                {Direction.Right, (position) => new Point2D(_wrapMaps[1].Item1.TopRight().X(), _wrapMaps[4].Item1.BottomRight().Y() - position.Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[5].Item1.TopRight().X(), _wrapMaps[4].Item1.BottomLeft().X() + _wrapMaps[4].Item1.BottomLeft().X() + position.X())},
                {Direction.Left, (position) => new Point2D(position.X() - 1, position.Y())},
            }
        ));
        _wrapMaps.Add(( // 5
            new Box(new Point2D(0, 150), new Point2D(49, 199)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Up},
                {Direction.Right, Direction.Up},
                {Direction.Down, Direction.Down},
                {Direction.Left, Direction.Down},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(position.X(), position.Y() - 1)},
                {Direction.Right, (position) => new Point2D(position.Y() - _wrapMaps[4].Item1.BottomLeft().X() - _wrapMaps[4].Item1.BottomLeft().X(), _wrapMaps[4].Item1.BottomLeft().Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[1].Item1.TopLeft().X() + position.X(), _wrapMaps[0].Item1.TopRight().Y())},
                {Direction.Left, (position) => new Point2D(position.Y() - _wrapMaps[0].Item1.TopLeft().X() - _wrapMaps[0].Item1.TopLeft().X(), _wrapMaps[0].Item1.TopLeft().Y())},
            }
        ));
    }
}

internal class SmallCubeMap : CubeMap
{
    public SmallCubeMap(List<string> mapRows, string moves) : base(mapRows, moves)
    {
        //     00
        //     00
        // 112233
        // 112233
        //     4455
        //     4455
        _wrapMaps.Add(( // 0
            new Box(new Point2D(8, 0), new Point2D(11, 3)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Down},
                {Direction.Right, Direction.Left},
                {Direction.Down, Direction.Down},
                {Direction.Left, Direction.Down},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(_wrapMaps[0].Item1.TopRight().X() - position.X(), _wrapMaps[1].Item1.TopRight().Y())},
                {Direction.Right, (position) => new Point2D(_wrapMaps[5].Item1.TopRight().X(), _wrapMaps[0].Item1.TopRight().X() - position.Y())},
                {Direction.Down, (position) => new Point2D(position.X(), position.Y() + 1)},
                {Direction.Left, (position) => new Point2D(_wrapMaps[2].Item1.TopRight().Y() + position.Y(), _wrapMaps[2].Item1.TopRight().Y())},
            }
        ));
        _wrapMaps.Add(( // 1
            new Box(new Point2D(0, 4), new Point2D(3, 7)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Down},
                {Direction.Right, Direction.Right},
                {Direction.Down, Direction.Up},
                {Direction.Left, Direction.Up},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(_wrapMaps[0].Item1.TopRight().X() - position.X(), _wrapMaps[0].Item1.TopLeft().Y())},
                {Direction.Right, (position) => new Point2D(position.X() + 1, position.Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[4].Item1.BottomRight().Y() - position.X(), _wrapMaps[4].Item1.BottomRight().Y())},
                {Direction.Left, (position) => new Point2D(_wrapMaps[5].Item1.BottomRight().X() + _wrapMaps[1].Item1.TopLeft().Y() - position.Y(), _wrapMaps[5].Item1.BottomRight().Y())},
            }
        ));
        _wrapMaps.Add(( // 2
            new Box(new Point2D(4, 4), new Point2D(7, 7)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Right},
                {Direction.Right, Direction.Right},
                {Direction.Down, Direction.Right},
                {Direction.Left, Direction.Left},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(_wrapMaps[0].Item1.TopLeft().X(), position.X() - _wrapMaps[2].Item1.TopLeft().X())},
                {Direction.Right, (position) => new Point2D(position.X() + 1, position.Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[4].Item1.TopLeft().X(), _wrapMaps[2].Item1.BottomRight().Y() + _wrapMaps[4].Item1.TopLeft().X() - position.X())},
                {Direction.Left, (position) => new Point2D(position.X() - 1, position.Y())},
            }
        ));
        _wrapMaps.Add(( // 3
            new Box(new Point2D(8, 4), new Point2D(11, 7)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Up},
                {Direction.Right, Direction.Down},
                {Direction.Down, Direction.Down},
                {Direction.Left, Direction.Left},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(position.X(), position.Y() - 1)},
                {Direction.Right, (position) => new Point2D(_wrapMaps[3].Item1.TopRight().Y() + _wrapMaps[5].Item1.TopRight().X() - position.Y(), _wrapMaps[5].Item1.TopRight().Y())},
                {Direction.Down, (position) => new Point2D(position.X(), position.Y() + 1)},
                {Direction.Left, (position) => new Point2D(position.X() - 1, position.Y())},
            }
        ));
        _wrapMaps.Add(( // 4
            new Box(new Point2D(8, 8), new Point2D(11, 11)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Up},
                {Direction.Right, Direction.Right},
                {Direction.Down, Direction.Up},
                {Direction.Left, Direction.Up},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(position.X(), position.Y() - 1)},
                {Direction.Right, (position) => new Point2D(position.X() + 1, position.Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[4].Item1.BottomLeft().Y() - position.X(), _wrapMaps[1].Item1.BottomRight().Y())},
                {Direction.Left, (position) => new Point2D(_wrapMaps[2].Item1.BottomRight().Y() + _wrapMaps[4].Item1.TopLeft().X() - position.Y(), _wrapMaps[2].Item1.BottomRight().Y())},
            }
        ));
        _wrapMaps.Add(( // 5
            new Box(new Point2D(12, 8), new Point2D(15, 11)),
            new Dictionary<Direction, Direction>()
            {
                {Direction.Up, Direction.Left},
                {Direction.Right, Direction.Left},
                {Direction.Down, Direction.Right},
                {Direction.Left, Direction.Left},
            },
            new Dictionary<Direction, Func<Point2D, Point2D>>()
            {
                {Direction.Up, (position) => new Point2D(_wrapMaps[3].Item1.TopRight().X(), _wrapMaps[5].Item1.TopRight().X() + _wrapMaps[5].Item1.TopRight().Y() - position.X())},
                {Direction.Right, (position) => new Point2D(_wrapMaps[0].Item1.TopRight().X(), _wrapMaps[5].Item1.BottomRight().Y() - position.Y())},
                {Direction.Down, (position) => new Point2D(_wrapMaps[1].Item1.TopLeft().X(), _wrapMaps[5].Item1.BottomRight().X() + _wrapMaps[1].Item1.TopLeft().Y() - position.X())},
                {Direction.Left, (position) => new Point2D(position.X() - 1, position.Y())},
            }
        ));
    }
}