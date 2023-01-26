using adventofcode.common;
using adventofcode.common.grid;
using System.Text.RegularExpressions;

namespace adventofcode.year2017;

public class Day20 : Solution
{
    private string[] _input;
    
    public Day20(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var ps = new ParticleSimulator(_input);
        var closest = ps.Displacements(500);

        return Convert.ToString(closest);
    }

    public override string PartTwo()
    {
        var ps = new ParticleSimulator(_input);
        var remaining = ps.Collisions(500);
        return Convert.ToString(remaining);
    }

    private class ParticleSimulator
    {
        private Dictionary<int, Point3D> _particles;
        private Dictionary<int, Point3D> _velocities;
        private Dictionary<int, Point3D> _accelerations;
        
        public ParticleSimulator(string[] data)
        {
            _particles = new Dictionary<int, Point3D>();
            _velocities = new Dictionary<int, Point3D>();
            _accelerations = new Dictionary<int, Point3D>();

            var i = 0;
            foreach (var line in data)
            {
                var match = Regex.Match(line, @"^p=<(.*)>, v=<(.*)>, a=<(.*)>$");
                var p = match.Groups[1].Value.Split(",");
                var v = match.Groups[2].Value.Split(",");
                var a = match.Groups[3].Value.Split(",");
            
                _particles.Add(i, new Point3D(p[0], p[1], p[2]));
                _velocities.Add(i, new Point3D(v[0], v[1], v[2]));
                _accelerations.Add(i, new Point3D(a[0], a[1], a[2]));
                i++;
            }
        }

        public int Displacements(int ticks)
        {
            var closestIndex = 0;
            var closest = -1L;
            foreach (var i in _particles.Keys)
            {
                // position at time tick = velocity * tick + .5 * acceleration * tick^2
                long x = Convert.ToInt64(_particles[i].X()) + Convert.ToInt64(_velocities[i].X()) * ticks + (Convert.ToInt64(_accelerations[i].X()) * ticks * ticks) / 2;
                long y = Convert.ToInt64(_particles[i].Y()) + Convert.ToInt64(_velocities[i].Y()) * ticks + (Convert.ToInt64(_accelerations[i].Y()) * ticks * ticks) / 2;
                long z = Convert.ToInt64(_particles[i].Z()) + Convert.ToInt64(_velocities[i].Z()) * ticks + (Convert.ToInt64(_accelerations[i].Z()) * ticks * ticks) / 2;

                var distance = Math.Abs(x) + Math.Abs(y) + Math.Abs(z);
                if (closest == -1 || distance < closest)
                {
                    closest = distance;
                    closestIndex = i;
                }
            }

            return closestIndex;
        }

        public int Collisions(int ticks)
        {
            for (int t = 0; t < ticks; t++)
            {
                var collisions = new Dictionary<Point3D, List<int>>();
                foreach (var i in _particles.Keys)
                {
                    _velocities[i] += _accelerations[i];
                    _particles[i] += _velocities[i];

                    if (!collisions.ContainsKey(_particles[i]))
                    {
                        collisions.Add(_particles[i], new List<int>());
                    }
                    collisions[_particles[i]].Add(i);
                }

                foreach (var collision in collisions)
                {
                    if (collision.Value.Count()> 1)
                    {
                        foreach (var i in collision.Value)
                        {
                            _particles.Remove(i);
                            _velocities.Remove(i);
                            _accelerations.Remove(i);
                        }
                    }
                }
            }

            return _particles.Count;
        }
    }
}