using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.range;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day23 : Solution
{
    private List<NanoBot> _bots;
    
    public Day23(string year, string day) : base(year, day)
    {
        _bots = new List<NanoBot>();
        foreach (var line in LoadInputAsLines())
        {
            var match = Regex.Match(line, @"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)");
            _bots.Add(new NanoBot(Convert.ToInt32(match.Groups[1].Value), Convert.ToInt32(match.Groups[2].Value), Convert.ToInt32(match.Groups[3].Value), Convert.ToInt32(match.Groups[4].Value)));
        }
    }

    public override string PartOne()
    {
        var strongest = _bots.Aggregate(_bots.First(), (acc, b) => acc.Radius() < b.Radius() ? b : acc);

        return Convert.ToString(_bots.Aggregate(0, (acc, b) => acc + (strongest.InRange(b.Position()) ? 1 : 0)));
    }

    public override string PartTwo()
    {
        // oct-tree's initial space should be smallest cube that contains all of the bots, but make it a multiple of 2 for easy splitting
        var maxX = _bots.Aggregate(-int.MaxValue, (acc, b) => acc < Math.Abs(b.Position().X()) ? Math.Abs(b.Position().X()) : acc);
        var maxY = _bots.Aggregate(-int.MaxValue, (acc, b) => acc < Math.Abs(b.Position().Y()) ? Math.Abs(b.Position().Y()) : acc);
        var maxZ = _bots.Aggregate(-int.MaxValue, (acc, b) => acc < Math.Abs(b.Position().Z()) ? Math.Abs(b.Position().Z()) : acc);
        var maxSize = (int) Math.Pow(2, Math.Ceiling(Math.Log2(Math.Max(Math.Max(maxX, maxY), maxZ))));
        var tree = new OctTree(_bots, new Box3D(new Point3D(-maxSize, -maxSize, -maxSize), new Point3D(maxSize, maxSize, maxSize)));

        var best = (0, new Point3D(maxX + 1, maxY + 1, maxZ + 1));
        
        var candidates = new PriorityQueue<OctTree, int>();
        candidates.Enqueue(tree, -tree.Bots().Count);
        while (candidates.Count > 0)
        {
            var t = candidates.Dequeue();

            if (t.Size() == 1)
            {   // sector is just a 1x1x1 cube so reached end...
                if (t.Bots().Count >= best.Item1)
                {   // this sector also has at least the same bot count as the currently known best sector...find points that are in range of the bots and pick the closest one to origin
                    foreach (var p in new List<Point3D>()
                             {
                                 t.Space().LeftBottomFront(), t.Space().LeftBottomBack(), t.Space().LeftTopFront(), t.Space().LeftTopBack(),
                                 t.Space().RightBottomFront(), t.Space().RightBottomBack(), t.Space().RightTopFront(), t.Space().RightTopBack(),
                             })
                    {
                        var count = t.Bots().Where(b => b.InRange(p)).ToList().Count;
                        if (count >= best.Item1)
                        {
                            best.Item2 = count > best.Item1 || best.Item2.Magnitude() > p.Magnitude() ? p : best.Item2;
                            best.Item1 = count;
                        }
                    }
                }
                continue;
            }

            t.Divide();
            foreach (var sector in t.Sectors())
            {
                var count = sector.Bots().Count;
                if (count > best.Item1)
                {
                    candidates.Enqueue(sector, -count);
                }
            }
        }

        Console.WriteLine($"{best.Item1} bots in range of coordinate {best.Item2}");
        return Convert.ToString(best.Item2.Magnitude());
    }

    private class NanoBot
    {
        private Point3D _position;
        private int _radius;

        public NanoBot(int x, int y, int z, int radius)
        {
            _position = new Point3D(x, y, z);
            _radius = radius;
        }

        public int Radius() { return _radius; }
        public Point3D Position() { return _position; }
        
        public bool InRange(Point3D p)
        {
            return Math.Abs(p.X() - _position.X()) + Math.Abs(p.Y() - _position.Y()) + Math.Abs(p.Z() - _position.Z()) <= _radius;
        }

        public bool InRange(Box3D box)
        {
            // https://gdbooks.gitbooks.io/3dcollisions/content/Chapter2/static_sphere_aabb.html
            // simpler version of aabb-sphere collision. since we are using only integers for points, the bot's radius forms a quadrahedron instead of a sphere. the points on the surface of the quadrahedron
            // always have a manhattan-distance, from the bot center, of length radius. this means the the closest point from the bot surface to the closest point on the cube must be more than radius length away
            // for it to not be in range

            var xDiff = (_position.X() < box.XInterval().Left() ? Math.Abs(_position.X() - box.XInterval().Left()) : 0) + (_position.X() > box.XInterval().Right() ? Math.Abs(_position.X() - box.XInterval().Right()) : 0);
            var yDiff = (_position.Y() < box.YInterval().Left() ? Math.Abs(_position.Y() - box.YInterval().Left()) : 0) + (_position.Y() > box.YInterval().Right() ? Math.Abs(_position.Y() - box.YInterval().Right()) : 0);
            var zDiff = (_position.Z() < box.ZInterval().Left() ? Math.Abs(_position.Z() - box.ZInterval().Left()) : 0) + (_position.Z() > box.ZInterval().Right() ? Math.Abs(_position.Z() - box.ZInterval().Right()) : 0);

            return (xDiff + yDiff + zDiff) <= _radius;
        }
    }

    private class OctTree
    {
        private List<NanoBot> _bots;
        private Box3D _space;
        private List<OctTree> _sectors;
            
        public OctTree(List<NanoBot> bots, Box3D space)
        {
            _bots = bots;
            _space = space;
            _sectors = new List<OctTree>();
        }

        public List<NanoBot> Bots() { return _bots; }
        public int Size() { return (_space.Width() + _space.Height() + _space.Depth()) / 3; }
        public Box3D Space() { return _space; }
        public List<OctTree> Sectors() { return _sectors; }

        public void Divide()
        {
            // divide the cube into 8 smaller cubes of equal sizes
            // front    back
            // ┌─┬─┐    ┌─┬─┐
            // │3│4│    │7│8│
            // ├─┼─┤    ├─┼─┤
            // │1│2│    │5│6│
            // └─┴─┘    └─┴─┘
            
            var nextSize = Size() / 2;
            var leftBottomFront = _space.LeftBottomFront();
            var rightTopBack = _space.LeftBottomFront() + new Point3D(nextSize, nextSize, nextSize);

            var sectors = new List<Box3D>();
            // cube 1 : cube corners start as is
            sectors.Add(new Box3D(leftBottomFront, rightTopBack));
            
            // cube 2 : cube corners translated along x-axis
            sectors.Add(new Box3D(leftBottomFront + new Point3D(nextSize, 0, 0), rightTopBack + new Point3D(nextSize, 0, 0)));

            // cube 3 : cube corners translated along y-axis
            sectors.Add(new Box3D(leftBottomFront + new Point3D(0, nextSize, 0), rightTopBack + new Point3D(0, nextSize, 0)));

            // cube 4 : cube corners translated along x and y axes
            sectors.Add(new Box3D(leftBottomFront + new Point3D(0, nextSize, nextSize), rightTopBack + new Point3D(0, nextSize, nextSize)));

            // cube 5 : cube corners translated along z-axis
            sectors.Add(new Box3D(leftBottomFront + new Point3D(0, 0, nextSize), rightTopBack + new Point3D(0, 0, nextSize)));

            // cube 6 : cube corners translated along x and z axes
            sectors.Add(new Box3D(leftBottomFront + new Point3D(nextSize, 0, nextSize), rightTopBack + new Point3D(nextSize, 0, nextSize)));

            // cube 7 : cube corners translated along y and z axes
            sectors.Add(new Box3D(leftBottomFront + new Point3D(0, nextSize, nextSize), rightTopBack + new Point3D(0, nextSize, nextSize)));

            // cube 8 : cube corners translated along x, y, and z axes
            sectors.Add(new Box3D(leftBottomFront + new Point3D(nextSize, nextSize, nextSize), _space.RightTopBack()));
            
            foreach (var sector in sectors)
            {
                _sectors.Add(new OctTree(_bots.Where(b => b.InRange(sector)).ToList(), sector));
            }
        }
    }
}