using adventofcode.common;
using adventofcode.common.graph;

namespace adventofcode.year2017;

public class Day12 : Solution
{
    private Dictionary<string, Node> _programs;
    
    public Day12(string year, string day) : base(year, day)
    {
        _programs = new Dictionary<string, Node>();
        foreach (var line in LoadInputAsLines())
        {
            var tmp = line.Split(" <-> ");

            if (!_programs.ContainsKey(tmp[0]))
            {
                _programs.Add(tmp[0], new Node(tmp[0], tmp[0], 0));
            }

            foreach (var link in tmp[1].Split(", "))
            {
                if (!_programs.ContainsKey(link))
                {
                    _programs.Add(link, new Node(link, link, 0));
                }

                _programs[tmp[0]].AddNode(_programs[link], 0);
            }
        }
    }

    private List<Node> SpanningTree(Node start)
    {
        var reachable = new List<Node>(){start};
        var visited = new HashSet<Node>(){start};
        var remaining = new Queue<Node>();
        remaining.Enqueue(start);

        while (remaining.Count > 0)
        {
            var node = remaining.Dequeue();
            foreach (var neighbor in node.AdjacentNodes())
            {
                if (!visited.Contains(neighbor.Key))
                {
                    visited.Add((Node) neighbor.Key);
                    reachable.Add((Node) neighbor.Key);
                    remaining.Enqueue((Node) neighbor.Key);
                }
            }
        }

        return reachable;
    }

    public override string PartOne()
    {
        var reachable = SpanningTree(_programs["0"]);

        return Convert.ToString(reachable.Count);
    }

    public override string PartTwo()
    {
        var remaining = new Queue<Node>(_programs.Values);
        var processed = new HashSet<Node>();

        var groups = 0;
        while (remaining.Count > 0)
        {
            var candidate = remaining.Dequeue();
            
            if (!processed.Contains(candidate))
            {
                foreach (var node in SpanningTree(candidate))
                {
                    processed.Add(node);
                }
                
                groups++;
            }
        }

        return Convert.ToString(groups);
    }
}