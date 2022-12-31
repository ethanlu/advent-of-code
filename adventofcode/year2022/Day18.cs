using System.Drawing;
using adventofcode.common;
using adventofcode.common.grid;

namespace adventofcode.year2022;

public class Day18 : Solution
{
    private List<Point3D> _droplets;
    
    public Day18(string year, string day) : base(year, day)
    {
        _droplets = new List<Point3D>();
        foreach (var input in LoadInputAsLines())
        {
            var s = input.Split(',');
            _droplets.Add(new Point3D(s[0], s[1], s[2]));
        }
    }

    public override string PartOne()
    {
        var lava = new Lava(_droplets);
        return Convert.ToString(lava.SurfaceArea());
    }

    public override string PartTwo()
    {
        var lava = new Lava(_droplets);
        var totalSurfaceArea = lava.ExteriorSurfaceArea();
        return Convert.ToString(lava.ExteriorSurfaceArea());
    }
}

internal class Lava
{
    private Dictionary<Point3D, Point3D> _droplets;
    private HashSet<Point3D> _knownOutsidePoints;
    
    public Lava(List<Point3D> droplets)
    {
        _knownOutsidePoints = new HashSet<Point3D>();
        _droplets = new Dictionary<Point3D, Point3D>();
        foreach (var droplet in droplets)
        {
            _droplets.Add(droplet, droplet);
        }
    }

    public int SurfaceArea()
    {
        return _droplets.Select(p => p.Value)
            .Aggregate(0, (acc, p) => acc +
                                      (_droplets.ContainsKey(p + new Point3D(1, 0, 0)) ? 0 : 1) +
                                      (_droplets.ContainsKey(p + new Point3D(-1, 0, 0)) ? 0 : 1) +
                                      (_droplets.ContainsKey(p + new Point3D(0, 1, 0)) ? 0 : 1) +
                                      (_droplets.ContainsKey(p + new Point3D(0, -1, 0)) ? 0 : 1) +
                                      (_droplets.ContainsKey(p + new Point3D(0, 0, 1)) ? 0 : 1) +
                                      (_droplets.ContainsKey(p + new Point3D(0, 0, -1)) ? 0 : 1));
    }
    
    public int ExteriorSurfaceArea()
    {
        bool ContainedInside(Point3D start)
        {
            if (_knownOutsidePoints.Contains(start))
            {
                return false;
            }
            
            var remaining = new Queue<Point3D>();
            remaining.Enqueue(start);
            
            var amountChecked = 0;
            var visited = new HashSet<Point3D>();
            while (remaining.Count > 0)
            {
                var candidate = remaining.Dequeue();

                if (_droplets.ContainsKey(candidate) || visited.Contains(candidate))
                {
                    continue;
                }

                amountChecked++;
                if (amountChecked > _droplets.Count * 6)
                {
                    // worst case scenario is when every droplet is by itself, so only need to check up to 6x the number of droplets
                    break;
                }
                
                visited.Add(candidate);
                remaining.Enqueue(candidate + new Point3D(1, 0, 0));
                remaining.Enqueue(candidate + new Point3D(-1, 0, 0));
                remaining.Enqueue(candidate + new Point3D(0, 1, 0));
                remaining.Enqueue(candidate + new Point3D(0, -1, 0));
                remaining.Enqueue(candidate + new Point3D(0, 0, 1));
                remaining.Enqueue(candidate + new Point3D(0, 0, -1));
            }

            if (remaining.Count > 0)
            {
                foreach (var p in visited)
                {
                    _knownOutsidePoints.Add(p);
                }
            }

            return remaining.Count == 0;
        }
        
        return _droplets.Select(p => p.Value)
            .Aggregate(0, (acc, p) => acc +
                                      (ContainedInside(p + new Point3D(1, 0, 0)) ? 0 : 1) + 
                                      (ContainedInside(p + new Point3D(-1, 0, 0)) ? 0 : 1) + 
                                      (ContainedInside(p + new Point3D(0, 1, 0)) ? 0 : 1) + 
                                      (ContainedInside(p + new Point3D(0, -1, 0)) ? 0 : 1) + 
                                      (ContainedInside(p + new Point3D(0, 0, 1)) ? 0 : 1) + 
                                      (ContainedInside(p + new Point3D(0, 0, -1)) ? 0 : 1));
    }
}