using adventofcode.common;
using adventofcode.common.graph;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day07 : Solution
{
    private Dictionary<string, DirectedGraphNode> _steps;

    public Day07(string year, string day) : base(year, day)
    {
        _steps = new Dictionary<string, DirectedGraphNode>();
        foreach (var line in LoadInputAsLines())
        {
            var match = Regex.Match(line, @"Step ([A-Z]) must be finished before step ([A-Z]) can begin.");
            var parent = match.Groups[1].Value;
            var child = match.Groups[2].Value;

            if (!_steps.ContainsKey(parent))
            {
                _steps.Add(parent, new DirectedGraphNode(parent, parent, 0));
            }
            if (!_steps.ContainsKey(child))
            {
                _steps.Add(child, new DirectedGraphNode(child, child, 0));
            }
            _steps[parent].AddNode(_steps[child], 1);   // steps that unlock other step
            _steps[child].AddNode(_steps[parent], -1);  // steps that depend on other steps
        }
    }

    public override string PartOne()
    {
        var completed = new HashSet<DirectedGraphNode>();
        var working = new PriorityQueue<DirectedGraphNode, char>();
        foreach (var s in _steps.Values)
        {
            if (s.AdjacentNodes().Where(kv => kv.Value == -1).ToList().Count == 0)
            {
                working.Enqueue(s, s.Name()[0]);
            }
        }
        
        var sequence = new List<string>();
        while (working.Count > 0)
        {
            var s = working.Dequeue();
            completed.Add(s);
            sequence.Add(s.Name());

            foreach (var c in s.AdjacentNodes().Where(kv => kv.Value == 1).Select(kv => kv.Key))
            {
                var hasDependencies = false;
                foreach (var p in c.AdjacentNodes().Where(kv => kv.Value == -1).Select(kv => kv.Key))
                {
                    if (!completed.Contains(p))
                    {
                        hasDependencies = true;
                        break;
                    }
                }
                if (!hasDependencies)
                {
                    working.Enqueue(c, c.Name()[0]);
                }
            }
        }

        return Convert.ToString(string.Join(string.Empty, sequence));
    }

    public override string PartTwo()
    {
        int WorkDuration(string s)
        {
            return s[0] - 64 + 60;
        }

        var workers = 5;
        var completed = new HashSet<DirectedGraphNode>();
        var waiting = new PriorityQueue<DirectedGraphNode, char>();
        var working = new PriorityQueue<(DirectedGraphNode, int), int>();
        foreach (var s in _steps.Values)
        {
            if (s.AdjacentNodes().Where(kv => kv.Value == -1).ToList().Count == 0)
            {
                if (workers > 0)
                {
                    workers--;
                    working.Enqueue((s, WorkDuration(s.Name()) - 1), WorkDuration(s.Name()) - 1);
                }
                else
                {
                    waiting.Enqueue(s, s.Name()[0]);
                }
            }
        }
        
        var sequence = new List<string>();
        var time = 0;
        while (working.Count > 0)
        {
            var (s, timeComplete) = working.Dequeue();
            time = timeComplete > time ? timeComplete : time;
            completed.Add(s);
            workers++;
            
            sequence.Add(s.Name());

            foreach (var c in s.AdjacentNodes().Where(kv => kv.Value == 1).Select(kv => kv.Key))
            {
                var hasDependencies = false;
                foreach (var p in c.AdjacentNodes().Where(kv => kv.Value == -1).Select(kv => kv.Key))
                {
                    if (!completed.Contains(p))
                    {
                        hasDependencies = true;
                        break;
                    }
                }
                if (!hasDependencies)
                { 
                    waiting.Enqueue(c, c.Name()[0]);
                }
            }

            while (workers > 0 && waiting.Count > 0)
            {
                workers--;
                var c = waiting.Dequeue();
                working.Enqueue((c, timeComplete + WorkDuration(c.Name())), timeComplete + WorkDuration(c.Name()));
            }
        }
        time++; // one extra second based on example
        
        Console.WriteLine(string.Join(string.Empty, sequence));

        return Convert.ToString(time);
    }
}