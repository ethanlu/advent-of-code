using System.Drawing;
using adventofcode.common;
using adventofcode.common.graph.search;
using adventofcode.common.grid;
using adventofcode.common.util;

namespace adventofcode.year2022;

public class Day24 : Solution
{
    private Point2D _start;
    private Point2D _end;
    private string[] _input;
    
    public Day24(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
        
        _start = new Point2D(_input[0].IndexOf('.'), 0);
        _end = new Point2D(_input[^1].IndexOf('.'), _input.Length - 1);
    }

    public override string PartOne()
    {
        var valley = new Valley(_input);
        var start = new ExpeditionState(valley, _start, _end, "S", 0, 0, valley.BlizzardCycle());
        var end = new ExpeditionState(valley, _start, _end, "E", 0, 0, valley.BlizzardCycle());
        var path = new SearchPath();
        path.Add(start);
        var astar = new AStar(path, end);
        var shortest = astar.FindPath();

        var finalState = (ExpeditionState) shortest.SearchStates().Last();
        Console.WriteLine($"Time : {finalState.Cost()}");
        finalState.Show(finalState.Cost());
        Console.WriteLine(shortest);
        
        return Convert.ToString(shortest.Cost());
    }

    public override string PartTwo()
    {
        var valley = new Valley(_input);

        // start to end
        var start = new ExpeditionState(valley, _start, _end, "S", 0, 0, valley.BlizzardCycle());
        var end = new ExpeditionState(valley, _start, _end, "E", 0, 0, valley.BlizzardCycle());
        var path = new SearchPath();
        path.Add(start);
        var astar = new AStar(path, end);
        var shortest = astar.FindPath();

        var finalState = (ExpeditionState) shortest.SearchStates().Last();
        Console.WriteLine($"Time : {finalState.Cost()}");
        finalState.Show(finalState.Cost());
        Console.WriteLine(shortest);
        
        // go back to start from end to pick up snack
        start = new ExpeditionState(valley, _end, _start, "S", 0, finalState.Cost(), valley.BlizzardCycle());
        end = new ExpeditionState(valley, _end, _start,"E", 0, 0, valley.BlizzardCycle());
        path = new SearchPath();
        path.Add(start);
        astar = new AStar(path, end);
        shortest = astar.FindPath();
        
        finalState = (ExpeditionState) shortest.SearchStates().Last();
        Console.WriteLine($"Time : {finalState.Cost()}");
        finalState.Show(finalState.Cost());
        Console.WriteLine(shortest);
        
        // start to end again
        start = new ExpeditionState(valley, _start, _end, "S", 0, finalState.Cost(), valley.BlizzardCycle());
        end = new ExpeditionState(valley, _start, _end, "E", 0, 0, valley.BlizzardCycle());
        path = new SearchPath();
        path.Add(start);
        astar = new AStar(path, end);
        shortest = astar.FindPath();

        finalState = (ExpeditionState) shortest.SearchStates().Last();
        Console.WriteLine($"Time : {finalState.Cost()}");
        finalState.Show(finalState.Cost());
        Console.WriteLine(shortest);

        return Convert.ToString(shortest.Cost());
    }

    internal enum Action
    {
        Up = 0, Down = 1, Left = 2, Right = 3, Wait=4
    }

    internal class Valley
    {
        private int _maxX;
        private int _maxY;
        private HashSet<Point2D> _walls;
        private Dictionary<int, HashSet<Point2D>> _upBlizzards;
        private Dictionary<int, HashSet<Point2D>> _downBlizzards;
        private Dictionary<int, HashSet<Point2D>> _rightBlizzards;
        private Dictionary<int, HashSet<Point2D>> _leftBlizzards;

        public Valley(string[] initialLayoutRows)
        {
            _walls = new HashSet<Point2D>();
            _upBlizzards = new Dictionary<int, HashSet<Point2D>>(){{0, new HashSet<Point2D>()}};
            _downBlizzards = new Dictionary<int, HashSet<Point2D>>(){{0, new HashSet<Point2D>()}};
            _rightBlizzards = new Dictionary<int, HashSet<Point2D>>() {{0, new HashSet<Point2D>()}};
            _leftBlizzards = new Dictionary<int, HashSet<Point2D>>(){{0, new HashSet<Point2D>()}};

            
            _maxY = 0;
            foreach (var l in initialLayoutRows)
            {
                _maxX = 0;
                foreach (var c in l)
                {
                    switch (c)
                    {
                        case '#':
                            _walls.Add(new Point2D(_maxX, _maxY));
                            break;
                        case '^':
                            _upBlizzards[0].Add(new Point2D(_maxX, _maxY));
                            break;
                        case 'v':
                            _downBlizzards[0].Add(new Point2D(_maxX, _maxY));
                            break;
                        case '<':
                            _leftBlizzards[0].Add(new Point2D(_maxX, _maxY));
                            break;
                        case '>':
                            _rightBlizzards[0].Add(new Point2D(_maxX, _maxY));
                            break;
                    }
                    _maxX++;
                }
                _maxY++;
            }
            _maxX--;
            _maxY--;

            // memoize all blizzard locations based on time to be reusable during search
            var minute = 1;
            foreach (var y in Enumerable.Range(0, _maxY))
            {
                foreach (var x in Enumerable.Range(0, _maxX))
                {
                    _upBlizzards.Add(minute, new HashSet<Point2D>());
                    foreach (var b in _upBlizzards[minute - 1])
                    {
                        var p = new Point2D(b.X(), b.Y() - 1);
                        if (_walls.Contains(p))
                        {
                            p = new Point2D(b.X(), _maxY - 1);
                        }
                        _upBlizzards[minute].Add(p);
                    }

                    _downBlizzards.Add(minute, new HashSet<Point2D>());
                    foreach (var b in _downBlizzards[minute - 1])
                    {
                        var p = new Point2D(b.X(), b.Y() + 1);
                        if (_walls.Contains(p))
                        {
                            p = new Point2D(b.X(), 1);
                        }
                        _downBlizzards[minute].Add(p);
                    }

                    _leftBlizzards.Add(minute, new HashSet<Point2D>());
                    foreach (var b in _leftBlizzards[minute - 1])
                    {
                        var p = new Point2D(b.X() - 1, b.Y());
                        if (_walls.Contains(p))
                        {
                            p = new Point2D(_maxX - 1, b.Y());
                        }
                        _leftBlizzards[minute].Add(p);
                    }

                    _rightBlizzards.Add(minute, new HashSet<Point2D>());
                    foreach (var b in _rightBlizzards[minute - 1])
                    {
                        var p = new Point2D(b.X() + 1, b.Y());
                        if (_walls.Contains(p))
                        {
                            p = new Point2D(1, b.Y());
                        }
                        _rightBlizzards[minute].Add(p);
                    }

                    minute++;
                }
            }
        }

        public int BlizzardCycle()
        {
            return (_maxX - 1) * (_maxY - 1);
        }

        public void Show(int minute, Point2D position)
        {
            minute = minute % BlizzardCycle();
            var grid = new char[_maxX + 1, _maxY + 1];
            for (int y = 0; y < grid.GetLength(1); y++)
            {
                for (int x = 0; x < grid.GetLength(0); x++)
                {
                    grid[x, y] = '.';
                    
                    var location = new Point2D(x, y);
                    if (_walls.Contains(location))
                    {
                        grid[x, y] = '#';
                        continue;
                    }
                    
                    if (position == location)
                    {
                        grid[x, y] = '@';
                        continue;
                    }

                    var overlap = 0;
                    if (_upBlizzards[minute].Contains(location))
                    {
                        overlap++;
                        grid[x, y] = '^';
                    }
                    if (_downBlizzards[minute].Contains(location))
                    {
                        overlap++;
                        grid[x, y] = 'v';
                    }
                    if (_leftBlizzards[minute].Contains(location))
                    {
                        overlap++;
                        grid[x, y] = '<';
                    }
                    if (_rightBlizzards[minute].Contains(location))
                    {
                        overlap++;
                        grid[x, y] = '>';
                    }
                    grid[x, y] = overlap > 1 ? overlap.ToString()[0] : grid[x, y];
                }
            }
            
            Draw<char>.ShowGrid(grid);
        }

        public bool ValidPosition(int minute, Point2D candidatePosition)
        {
            minute = minute % BlizzardCycle();
            
            // out of bounds
            if (candidatePosition.X() < 0 || candidatePosition.X() > _maxX || candidatePosition.Y() < 0 || candidatePosition.Y() > _maxY)
            {
                return false;
            }

            // position is a wall
            if (_walls.Contains(candidatePosition))
            {
                return false;
            }

            // up blizzard is in this position at this minute
            if (_upBlizzards[minute].Contains(candidatePosition))
            {
                return false;
            }
            
            // down blizzard is in this position at this minute
            if (_downBlizzards[minute].Contains(candidatePosition))
            {
                return false;
            }
            
            // left blizzard is in this position at this minute
            if (_leftBlizzards[minute].Contains(candidatePosition))
            {
                return false;
            }
            
            // right blizzard is in this position at this minute
            if (_rightBlizzards[minute].Contains(candidatePosition))
            {
                return false;
            }

            return true;
        }
    }

    internal class ExpeditionState : SearchState
    {
        private static Valley _valley = null;
        private static Point2D _end = new Point2D(0, 0);
        private Point2D _position;

        public ExpeditionState(Valley valley, Point2D position, Point2D end, string id, int gain, int cost, int maxCost) : base(id, gain, cost, maxCost)
        {
            _valley = valley;
            _position = position;
            _end = end;
        }
        public ExpeditionState(Point2D position, string id, int gain, int cost, int maxCost) : base(id, gain, cost, maxCost)
        {
            _position = position;
            if (_position == _end)
            {
                // reached end, so set id to "E" to end search
                _id = "E";
            }
            else
            {
                // use position and blizzard state based on time index as fingerprint
                _id = $"{_position.GetHashCode()}{cost % maxCost}";
            }
        }
        
        private Point2D Delta(Action action)
        {
            var delta = new Point2D(0, 0);
            switch (action)
            {
                case Action.Up:
                    delta = new Point2D(0, -1);
                    break;
                case Action.Down:
                    delta = new Point2D(0, 1);
                    break;
                case Action.Left:
                    delta = new Point2D(-1, 0);
                    break;
                case Action.Right:
                    delta = new Point2D(1, 0);
                    break;
            }

            return delta;
        }

        public void Show(int minute)
        {
            _valley!.Show(minute, _position);
        }

        public override int PotentialGain()
        {
            return Math.Abs(_end.X() - _position.X()) + Math.Abs(_end.Y() - _position.Y());
        }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var nextStates = new List<ISearchState>();

            foreach (var action in new List<Action>() {Action.Up, Action.Down, Action.Left, Action.Right, Action.Wait})
            {
                var candidatePosition = _position + Delta(action);
                
                // new position must be valid for it to be a possible search state
                if (_valley.ValidPosition(_cost + 1, candidatePosition))
                {
                    nextStates.Add(new ExpeditionState(candidatePosition, _id, _gain, _cost + 1, _maxCost));
                }
            }

            return nextStates;
        }

        public override string ToString()
        {
            return $"{_position}";
        }
    }
}