using adventofcode.common;

namespace adventofcode.year2018;

public class Day25 : Solution
{
    private List<SpaceTimeCoordinate> _coordinates;
    
    public Day25(string year, string day) : base(year, day)
    {
        _coordinates = new List<SpaceTimeCoordinate>();
        foreach (var line in LoadInputAsLines())
        {
            var tmp = line.Split(",");
            _coordinates.Add(new SpaceTimeCoordinate(Convert.ToInt32(tmp[0]), Convert.ToInt32(tmp[1]), Convert.ToInt32(tmp[2]), Convert.ToInt32(tmp[3])));
        }
    }

    public override string PartOne()
    {
        var inRangeMap = new Dictionary<SpaceTimeCoordinate, List<SpaceTimeCoordinate>>();
        foreach (var p1 in _coordinates)
        {
            inRangeMap.Add(p1, new List<SpaceTimeCoordinate>());
            
            foreach (var p2 in _coordinates)
            {
                if (p1.ManhattanDistance(p2) <= 3)
                {
                    inRangeMap[p1].Add(p2);
                }
            }
        }

        var constellations = 0;
        var uncategorizedCoordinates = new HashSet<SpaceTimeCoordinate>(_coordinates);
        while (uncategorizedCoordinates.Count > 0)
        {
            constellations++;
            var p = uncategorizedCoordinates.First();
            uncategorizedCoordinates.Remove(p);

            var neighbors = new Queue<SpaceTimeCoordinate>(inRangeMap[p]);
            var processed = new HashSet<SpaceTimeCoordinate>();
            while (neighbors.Count > 0)
            {
                var n = neighbors.Dequeue();
                uncategorizedCoordinates.Remove(n);
                processed.Add(n);
                foreach (var p2 in inRangeMap[n])
                {   // chain formed
                    if (!processed.Contains(p2))
                    {
                        neighbors.Enqueue(p2);
                    }
                }
            }
        }

        return Convert.ToString(constellations);
    }

    public override string PartTwo()
    {
        return Convert.ToString("ᕕ( ᐛ )ᕗ");
    }

    private class SpaceTimeCoordinate : IEquatable<SpaceTimeCoordinate>
    {
        private int _x;
        private int _y;
        private int _z;
        private int _t;

        public SpaceTimeCoordinate(int x, int y, int z, int t)
        {
            _x = x;
            _y = y;
            _z = z;
            _t = t;
        }

        public int ManhattanDistance(SpaceTimeCoordinate p)
        {
            return Math.Abs(_x - p._x) + Math.Abs(_y - p._y) + Math.Abs(_z - p._z) + Math.Abs(_t - p._t);
        }
        
        public bool Equals(SpaceTimeCoordinate p)
        {
            return _x == p._x && _y == p._y && _z == p._z && _t == p._t;
        }

        public override bool Equals(Object? obj)
        {
            return obj is SpaceTimeCoordinate && Equals((SpaceTimeCoordinate) obj);
        }

        public override int GetHashCode()
        {
            return _x * 13 + _y * 37 + _z * 47 + _t * 53;
        }
    }
}