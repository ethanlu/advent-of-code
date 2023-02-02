using adventofcode.common;
using adventofcode.common.graph.search;
using adventofcode.common.grid;

namespace adventofcode.year2018;

public class Day06 : Solution
{
    private List<Point2D> _coordinates;
    private Grid _grid;
    private int _minX;
    private int _maxX;
    private int _minY;
    private int _maxY;
    
    public Day06(string year, string day) : base(year, day)
    {
        _minX = 99999;
        _maxX = 0;
        _minY = 99999;
        _maxY = 0;
        _coordinates = new List<Point2D>();
        foreach (var line in LoadInputAsLines())
        {
            var tmp = line.Split(", ");
            var p = new Point2D(Convert.ToInt32(tmp[0]), Convert.ToInt32(tmp[1]));
            _coordinates.Add(p);
            _minX = _minX > p.X() ? p.X() : _minX;
            _maxX = _maxX < p.X() ? p.X() : _maxX;
            _minY = _minY > p.Y() ? p.Y() : _minY;
            _maxY = _maxY < p.Y() ? p.Y() : _maxY;
        }
        _grid = new Grid(_coordinates, _minX, _maxX, _minY, _maxY);
    }

    public override string PartOne()
    {
        var area = 0;
        for (int i = 0; i < _coordinates.Count; i++)
        {
            try
            {
                var ff = new FloodFill(new AreaSearchState(_grid, _coordinates[i], i, 0, 0, 99999));
                var states = ff.Fill();

                area = area < states.Count ? states.Count : area;
            }
            catch (Exception e)
            {
                Console.WriteLine($"{_coordinates[i]} is an infinite region");
            }
        }

        return Convert.ToString(area);
    }

    public override string PartTwo()
    {
        var safe = 0;
        for (int x = _minX; x <= _maxX; x++)
        {
            for (int y = _minY; y <= _maxY; y++)
            {
                var distance = 0;
                foreach (var p in _coordinates)
                {
                    distance += Math.Abs(p.X() - x) + Math.Abs(p.Y() - y);
                }
                if (distance <= 10000)
                {
                    safe++;
                }
            }
        }

        return Convert.ToString(safe);
    }

    private class Grid
    {
        private Dictionary<Point2D, int> _grid;
        private int _minX;
        private int _maxX;
        private int _minY;
        private int _maxY;
        
        public Grid(List<Point2D> coordinates, int minX, int maxX, int minY, int maxY)
        {
            _minX = minX;
            _maxX = maxX;
            _minY = minY;
            _maxY = maxY;
            _grid = new Dictionary<Point2D, int>();
            for (int x = _minX; x <= _maxX; x++)
            {
                for (int y = _minY; y <= _maxY; y++)
                {
                    var p = new Point2D(x, y);
                    var closest = 99999;
                    var closestIndex = -1;
                    var multiple = false;
                    for (int i = 0; i < coordinates.Count; i++)
                    {
                        var c = coordinates[i];
                        var distance = Math.Abs(p.X() - c.X()) + Math.Abs(p.Y() - c.Y());
                        if (closest == distance)
                        {
                            multiple = true;
                        }
                        if (closest > distance)
                        {
                            multiple = false;
                            closest = distance;
                            closestIndex = i;
                        }
                    }
                    _grid.Add(p, multiple ? -1 : closestIndex);
                }
            }
        }

        public int? ValueAt(Point2D position)
        {
            if (_grid.ContainsKey(position))
            {
                return _grid[position];
            }

            return null;
        }
    }

    private class AreaSearchState : SearchState
    {
        private Grid _grid;
        private Point2D _position;
        private int _id;
        
        public AreaSearchState(Grid grid, Point2D position, int id, int gain, int cost, int maxCost) : base($"{id}:{position}", gain, cost, maxCost)
        {
            _id = id;
            _grid = grid;
            _position = position;
        }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();
            var offsets = new List<Point2D>() {new Point2D(0, -1), new Point2D(1, -1), new Point2D(1, 0), new Point2D(1, 1), new Point2D(0, 1), new Point2D(-1, 1), new Point2D(-1, 0), new Point2D(-1, -1)};

            foreach (var p in offsets)
            {
                var value = _grid.ValueAt(_position + p);
                if (value is null)
                {
                    throw new Exception("Infinite region");
                }
                if (value == _id)
                {
                    states.Add(new AreaSearchState(_grid, _position + p, _id, _gain + 1, _cost + 1, _maxCost));
                }
            }

            return states;
        }
    }
}