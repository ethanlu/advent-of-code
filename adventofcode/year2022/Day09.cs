using adventofcode.common;

namespace adventofcode.year2022;

public class Day09 : Solution
{
    private string[] _input;

    public Day09(string year, string day) : base(year, day)
    {
        _input = this.LoadInputAsLines();
    }

    public override string PartOne()
    {
        var rope = new Rope(2);
        foreach (var move in _input)
        {
            var t = move.Split(' ');
            rope.Move(t[0], Convert.ToInt32(t[1]));
        }

        var visible = rope.TailHistory().Count;
        return Convert.ToString(visible);
    }

    public override string PartTwo()
    {
        var rope = new Rope(10);
        foreach (var move in _input)
        {
            var t = move.Split(' ');
            rope.Move(t[0], Convert.ToInt32(t[1]));
        }

        var visible = rope.TailHistory().Count;
        return Convert.ToString(visible);
    }

    internal class Knot
    {
        private (int X, int Y) _position;

        public Knot((int, int) position)
        {
            _position = position;
        }

        public int X()
        {
            return _position.X;
        }

        public int Y()
        {
            return _position.Y;
        }

        public void Step((int, int) delta)
        {
            _position.X += delta.Item1;
            _position.Y += delta.Item2;
        }
    }

    internal class Rope
    {
        private List<Knot> _knots;
        private Dictionary<string, int> _tailLog;
        
        public Rope(int ropeLength)
        {
            _knots = new List<Knot>();
            for (var i = 0; i < ropeLength; i++)
            {
                _knots.Add(new Knot((0, 0)));
            }

            _tailLog = new Dictionary<string, int>();
            RecordTailLocation();
        }

        private void RecordTailLocation()
        {
            var tail = _knots.Last();
            var key = $"{tail.X()}, {tail.Y()}";
            if (!_tailLog.ContainsKey(key))
            {
                _tailLog.Add(key, 0);
            }
            _tailLog[key]++;
        }

        public List<string> TailHistory()
        {
            return _tailLog.Keys.ToList();
        }

        public void Move(string direction, int steps)
        {
            var headDelta = (0, 0);
            switch (direction)
            {
                case "U":
                    headDelta = (0, 1);
                    break;
                case "D":
                    headDelta = (0, -1);
                    break;
                case "L":
                    headDelta = (-1, 0);
                    break;
                case "R":
                    headDelta = (1, 0);
                    break;
            }
            
            
            for (var i = 0; i < steps; i++)
            {
                Knot head = _knots.First();
                head.Step(headDelta);
                
                Knot previousKnot = head;
                for (var j = 1; j < _knots.Count; j++)
                {
                    var currentDelta = (0, 0);
                    Knot currentKnot = _knots[j];
                    
                    var xDiff = Math.Abs(previousKnot.X() - currentKnot.X());
                    var yDiff = Math.Abs(previousKnot.Y() - currentKnot.Y());
            
                    if ((xDiff == 2 && yDiff == 0) || (xDiff == 0 && yDiff == 2))
                    {
                        // previous knot is 2 cardinal cells away from current knot...move current in cardinal direction of previous
                        currentDelta = (
                            previousKnot.X() > currentKnot.X() ? 1 : previousKnot.X() < currentKnot.X() ? -1 : 0,
                            previousKnot.Y() > currentKnot.Y() ? 1 : previousKnot.Y() < currentKnot.Y() ? -1 : 0);
                        currentKnot.Step(currentDelta);
                    }
                    else if ((xDiff == 2 && yDiff == 1) || (xDiff == 1 && yDiff == 2) || (xDiff == 2 && yDiff == 2))
                    {
                        // move current in a diagonal direction closer to previous
                        currentDelta = ((previousKnot.X() > currentKnot.X() ? 1 : -1), (previousKnot.Y() > currentKnot.Y() ? 1 : -1));
                        currentKnot.Step(currentDelta);
                    }

                    if (currentDelta != (0, 0))
                    {
                        previousKnot = currentKnot;
                    }
                    else
                    {
                        break;
                    }
                }
                RecordTailLocation();
            }
        }
    }
}