using adventofcode.common;
using adventofcode.common.graph.search;
using adventofcode.common.grid;
using adventofcode.common.util;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day22 : Solution
{
    private CaveMaze _cave;
    
    public Day22(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();
        _cave = new CaveMaze(input[0], input[1], 500);
    }

    public override string PartOne()
    {
        _cave.Show(5);
        return Convert.ToString(_cave.Risk(_cave.Target()));
    }

    public override string PartTwo()
    {
        var astar = new AStar(
            new CaveSearchState(_cave, _cave.Target(), _cave.Mouth(), CaveTool.Torch, 0, 0, int.MaxValue),
            new CaveSearchState(_cave, _cave.Target(),_cave.Target(), CaveTool.Torch, 0, 0, int.MaxValue)
        );
        astar.Verbose(true, 100000L);
        var path = astar.FindPath();
        
        Console.WriteLine(path);

        return Convert.ToString(path.Cost());
    }

    private class CaveRegion
    {
        private long _geologicIndex;
        private long _erosionIndex;
        private char _type;
        private long _risk;

        public CaveRegion(long geologicIndex, long erosionIndex)
        {
            _geologicIndex = geologicIndex;
            _erosionIndex = erosionIndex;
            _risk = _erosionIndex % 3;

            switch (_risk)
            {
                case 0:
                    _type = '.';
                    break;
                case 1:
                    _type = '=';
                    break;
                case 2:
                    _type = '|';
                    break;
            }
        }
        public long ErosionIndex() { return _erosionIndex; }
        public char Type() { return _type; }
        public long Risk() { return _risk; }
        
        public HashSet<CaveTool> SupportedTools() =>
            _type switch
            {
                '.' => new HashSet<CaveTool>() {CaveTool.ClimbingGear, CaveTool.Torch},
                '=' => new HashSet<CaveTool>() {CaveTool.ClimbingGear, CaveTool.Neither},
                '|' => new HashSet<CaveTool>() {CaveTool.Torch, CaveTool.Neither},
                _ => throw new Exception($"Invalid region type : {_type}")
            };
    }

    private class CaveMaze
    {
        private CaveRegion[,] _cave;
        private int _depth;
        private Point2D _mouth;
        private Point2D _target;

        public CaveMaze(string depth, string target, int margin)
        {
            _depth = Convert.ToInt32(Regex.Match(depth,  @"depth: (\d+)").Groups[1].Value);
            _mouth = new Point2D(0, 0);

            var tmp = target.Split(" ")[1].Split(",");
            _target = new Point2D(Convert.ToInt32(tmp[0]), Convert.ToInt32(tmp[1]));

            var adjustedDepth = Math.Max(_target.X(), _target.Y()) + margin;
            _cave = new CaveRegion[adjustedDepth, adjustedDepth];
            for (int y = 0; y < adjustedDepth; y++)
            {
                for (int x = 0; x < adjustedDepth; x++)
                {
                    long gi = 0;
                    if (x == 0)
                    {
                        gi = y * 48271;
                    }
                    else if (y == 0)
                    {
                        gi = x * 16807;
                    }
                    else if (x == _target.X() && y == _target.Y())
                    {
                        gi = 0;
                    }
                    else
                    {
                        gi = _cave[x - 1, y].ErosionIndex() * _cave[x, y - 1].ErosionIndex();
                    }
                    _cave[x, y] = new CaveRegion(gi, (gi + _depth) % 20183);
                }
            }
        }

        public int Size() { return _cave.GetLength(0); }
        public Point2D Mouth() { return _mouth; }
        public Point2D Target() { return _target; }
        public CaveRegion Region(Point2D p) { return _cave[p.X(), p.Y()]; }

        public void Show(int margin)
        {
            var width = _target.X() + margin + 1;
            var height = _target.Y() + margin + 1;
            var grid = new char[width, height];
            
            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    grid[x, y] = _cave[x, y].Type();
                }
            }
            grid[_mouth.X(), _mouth.Y()] = 'M';
            grid[_target.X(), _target.Y()] = 'T';
            Draw<char>.ShowGrid(grid);
        }

        public long Risk(Point2D target)
        {
            long risk = 0;
            for (int y = 0; y <= target.Y(); y++)
            {
                for (int x = 0; x <= target.X(); x++)
                {
                    risk += _cave[x, y].Risk();
                }
            }

            return risk;
        }
    }
    
    private enum CaveTool
    {
        Neither = 0, Torch = 1, ClimbingGear = 2
    }
    
    private class CaveSearchState : SearchState
    {
        private CaveMaze _cave;
        private Point2D _target;
        private Point2D _position;
        private CaveTool _tool;

        public CaveSearchState(CaveMaze cave, Point2D target, Point2D position, CaveTool tool, int gain, int cost, int maxCost) : base($"{position}:{tool}", gain, cost, maxCost)
        {
            _cave = cave;
            _target = target;
            _position = position;
            _tool = tool;
        }

        public override List<ISearchState> NextSearchStates(ISearchState? previous)
        {
            var states = new List<ISearchState>();

            // change tool
            foreach (var tool in _cave.Region(_position).SupportedTools())
            {
                if (_tool != tool)
                {
                    states.Add(new CaveSearchState(
                        _cave, _target, _position, tool,
                        Math.Abs(_target.X() - _position.X()) + Math.Abs(_target.Y() - _position.Y()), 
                        _cost + 7,
                        _maxCost));
                }
            }

            // move without changing tool
            foreach (var delta in new List<Point2D>() {new Point2D(0, -1), new Point2D(1, 0), new Point2D(0, 1), new Point2D(-1, 0)})
            {
                var p = _position + delta;
                if (p.X() >= 0 && p.X() < _cave.Size() && p.Y() >= 0 && p.Y() < _cave.Size())
                {
                    foreach (var tool in _cave.Region(p).SupportedTools())
                    {
                        if (_tool == tool)
                        {
                            states.Add(new CaveSearchState(
                                _cave, _target, p, tool,
                                Math.Abs(_target.X() - p.X()) + Math.Abs(_target.Y() - p.Y()), 
                                _cost + 1,
                                _maxCost));
                        }
                    }
                }
            }

            return states;
        }

        public override string ToString()
        {
            return $"{_position}:[{_tool}]:[{_gain}, {_cost}]";
        }
    }
}