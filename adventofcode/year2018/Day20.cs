using adventofcode.common;
using adventofcode.common.graph.search;
using adventofcode.common.grid;
using adventofcode.common.util;

namespace adventofcode.year2018;

public class Day20 : Solution
{
    private RegexMap _rm;
    private Dictionary<Point2D, int> _shortestPaths;

    public Day20(string year, string day) : base(year, day)
    {
        _rm = new RegexMap();
        _rm.Build(LoadInputAsString());
        
        _shortestPaths = new Dictionary<Point2D, int>();
    }

    public override string PartOne()
    {
        _rm.Show();

        
        var longest = 0;
        foreach (var room in _rm.Map().Where(kv => kv.Value == '.').Select(kv => kv.Key).Reverse().ToList())
        {
            if (!_shortestPaths.ContainsKey(room))
            {
                var start = new SearchPath();
                start.Add(new RoomSearchState(_rm.Map(), new Point2D(0, 0), 0, 0, 99999));
                var astar = new AStar(start, new RoomSearchState(_rm.Map(), room, 0, 0, 99999));

                var path = astar.FindPath();

                for (int l = 0; l < path.SearchStates().Count; l++)
                {
                    var position = ((RoomSearchState) path.SearchStates()[l]).Position();
                    if (!_shortestPaths.ContainsKey(position))
                    {
                        _shortestPaths.Add(position, l);
                    }
                }
            }
            
            longest = longest < _shortestPaths[room] ? _shortestPaths[room] : longest;
        }
        
        return Convert.ToString(longest);
    }

    public override string PartTwo()
    {
        return Convert.ToString(_shortestPaths.Aggregate(0, (acc, kv) => acc + (kv.Value >= 1000 ? 1 : 0)));
    }

    private class RoomSearchState : SearchState
    {
        private Dictionary<Point2D, char> _map;
        private Point2D _position;
        
        public RoomSearchState(Dictionary<Point2D, char> map, Point2D position, int gain, int cost, int maxCost) : base($"{position}", gain, cost, maxCost)
        {
            _map = map;
            _position = position;
        }

        public Point2D Position() { return _position; }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();

            foreach (var delta in new List<Point2D>() {new Point2D(0, -1), new Point2D(1, 0), new Point2D(0, 1), new Point2D(-1, 0)})
            {
                var p = _position + delta;
                if (_map.ContainsKey(p) && _map[p] != '#')
                {
                    states.Add(new RoomSearchState(_map, p + delta, _gain + 1, _cost + 1, _maxCost));
                }
            }

            return states;
        }
    }


    private class RegexMap
    {
        private Dictionary<Point2D, char> _map;

        public RegexMap()
        {
            _map = new Dictionary<Point2D, char>();
            AddRoom(new Point2D(0, 0), 'X');
        }

        private void AddRoom(Point2D s, char c)
        {
            _map.Add(s, c);
            foreach (var p in new List<Point2D>() {s + new Point2D(0, -1), s + new Point2D(1, 0), s + new Point2D(0, 1), s + new Point2D(-1, 0)})
            {
                if (!_map.ContainsKey(p)) { _map.Add(p, '?'); }
            }
        }

        private Point2D Move(Point2D p, char direction)
        {
            var next = p;
            switch (direction)
            {
                case 'N':   // move up
                    next += new Point2D(0, -1);
                    _map[next] = '-';
                    next += new Point2D(0, -1);
                    break;
                case 'E':   // move right
                    next += new Point2D(1, 0);
                    _map[next] = '|';
                    next += new Point2D(1, 0);
                    break;
                case 'S':   // move down
                    next += new Point2D(0, 1);
                    _map[next] = '-';
                    next += new Point2D(0, 1);
                    break;
                case 'W':   // move left
                    next += new Point2D(-1, 0);
                    _map[next] = '|';
                    next += new Point2D(-1, 0);
                    break;
            }

            return next;
        }

        public Dictionary<Point2D, char> Map() { return _map; }

        public void Show()
        {
            var minX = _map.Keys.Aggregate(99999, (acc, p) => acc > p.X() ? p.X() : acc);
            var maxX = _map.Keys.Aggregate(0, (acc, p) => acc < p.X() ? p.X() : acc);
            var minY = _map.Keys.Aggregate(99999, (acc, p) => acc > p.Y() ? p.Y() : acc);
            var maxY = _map.Keys.Aggregate(0, (acc, p) => acc < p.Y() ? p.Y() : acc);
            var width = maxX - minX + 1;
            var height = maxY - minY + 1;
            var grid = new char[width, height];

            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    grid[x, y] = '#';
                }
            }

            foreach (var (p, c) in _map)
            {
                grid[p.X() - minX, p.Y() - minY] = c;
            }
            Draw<char>.ShowGrid(grid);
        }

        public void Build(string input)
        {
            void Parse(Point2D p, string input, int index)
            {
                while (index < input.Length)
                {
                    switch (input[index])
                    {
                        case 'N':
                        case 'E':
                        case 'S':
                        case 'W':
                            p = Move(p, input[index]);
                            if (!_map.ContainsKey(p)) { AddRoom(p, '.'); }
                            index++;
                            break;
                        case '(':   // start of a subgroup
                            var subgroups = new List<string>();
                            var level = 1;
                            var groupStartIndex = index + 1;
                            var groupEndIndex = index + 1;
                            while (level > 0)
                            {
                                groupEndIndex++;
                                switch (input[groupEndIndex])
                                {
                                    case '(':
                                        level++;
                                        break;
                                    case ')':
                                        if (level == 1)
                                        {
                                            subgroups.Add(input.Substring(groupStartIndex, groupEndIndex - groupStartIndex));
                                            groupStartIndex = groupEndIndex + 1;
                                        }
                                        level--;
                                        break;
                                    case '|':
                                        if (level == 1)
                                        {
                                            subgroups.Add(input.Substring(groupStartIndex, groupEndIndex - groupStartIndex));
                                            groupStartIndex = groupEndIndex + 1;
                                        }
                                        break;
                                }
                            }
                            foreach (var subgroup in subgroups)
                            {
                                Parse(p, subgroup, 0);
                            }
                            index = groupEndIndex + 1;
                            break;
                        case '^':
                        case '$':
                            index++;
                            break;
                        default:
                            throw new Exception($"Invalid input character : {input[index]}");
                    }
                }
            }

            Parse(new Point2D(0, 0), input, 0);

            foreach (var p in _map.Keys)
            {
                if (_map[p] == '?') { _map[p] = '#'; }
            }
        }
    }
}