using System.Drawing;
using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;
using System.Text.RegularExpressions;

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
        var map = new Map(_mapRows, _moves);
        var password = map.Walk();
        return Convert.ToString(password);
    }

    public override string PartTwo()
    {
        return Convert.ToString("");
    }
}

enum Direction
{
    Right = 0, Down = 1, Left = 2, Up = 3
}

internal class Map
{
    private int _height;
    private int _width;
    private char[,] _map;
    private List<(char, int)> _moves;
    private Point2D _position;
    private Direction _facing;
    private List<(Point2D, Direction)> _trail;

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
        _facing = Direction.Right;
        _trail = new List<(Point2D, Direction)>();

        _moves = new List<(char, int)>();
        foreach (Match match in Regex.Matches(moves, @"(\d+)([LR]?)"))
        {
            _moves.Add((match.Groups[2].Value.Length > 0 ? match.Groups[2].Value.ToCharArray()[0] : 'X', Convert.ToInt32(match.Groups[1].Value)));
        }
    }

    private char[,] MarkTrail()
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

    public int Walk()
    {
        var step = 0;
        foreach (var (turn, steps) in _moves)
        {
            Point2D delta = new Point2D(0, 0);
            switch (_facing)
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
            
            // move in the direction n steps until run into wall
            foreach (var i in Enumerable.Range(0, steps))
            {
                var peekPosition = _position + delta;

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
                
                // stop movement if it is a wall
                if (_map[peekPosition.X(), peekPosition.Y()] == '#')
                {
                    break;
                }
                
                // otherwise, update trail and move to that position
                _trail.Add((_position, _facing));
                _position = peekPosition;
                step++;
            }

            // turn
            if (turn == 'X')
            {
                continue;
            }
            switch (_facing)
            {
                case Direction.Right:
                    _facing = turn == 'L' ? Direction.Up : Direction.Down;
                    break;
                case Direction.Down:
                    _facing = turn == 'L' ? Direction.Right : Direction.Left;
                    break;
                case Direction.Left:
                    _facing = turn == 'L' ? Direction.Down : Direction.Up;
                    break;
                case Direction.Up:
                    _facing = turn == 'L' ? Direction.Left : Direction.Right;
                    break;
            }
        }
        _trail.Add((_position, _facing));
        
        Draw<char>.ShowGrid(MarkTrail());
        Console.WriteLine($"Steps : {step}");
        Console.WriteLine($"End : ({_position.X()}, {_position.Y()}) [{(int) _facing}]");
        
        return ((_position.Y() + 1) * 1000) + ((_position.X() + 1) * 4) + (int) _facing;
    }
}