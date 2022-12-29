using adventofcode.common;
using adventofcode.common.graph;
using Path = adventofcode.common.graph.Path;
using System.Text.RegularExpressions;
using adventofcode.common.graph.search;

namespace adventofcode.year2022;

public class Day16 : Solution
{
    private Dictionary<string, Node> _valves;

    public Day16(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();

        var tmp = new Dictionary<string, Node>();
        var _importantValves = new List<string>();
        foreach (var line in input)
        {
            var match = Regex.Match(line, @"^Valve ([A-Z]{2}) has flow rate=(\d+);");
            var valve = new Node(match.Groups[1].Value, match.Groups[1].Value, Convert.ToInt32(match.Groups[2].Value));
            tmp.Add(match.Groups[1].Value, valve);

            if (valve.Weight() != 0 || valve.Id() == "AA")
            {
                _importantValves.Add(valve.Id());
            }
        }
        foreach (var line in input)
        {
            var match = Regex.Match(line, @"^Valve ([A-Z]{2}) has flow rate=\d+; tunnels? leads? to valves? ([A-Z,\s]+)$");
            foreach (var neighbor in match.Groups[2].Value.Split(", "))
            {
                tmp[match.Groups[1].Value].AddNode(tmp[neighbor], 0);
            }
        }
        
        // optimize graph by running shortest path between all valve nodes that have a flow rate > 0 and build a new graph based on the paths
        _valves = new Dictionary<string, Node>();
        var shortestPaths = new List<IPath>();
        foreach (var start in _importantValves)
        {
            foreach (var end in _importantValves)
            {
                if (start != end)
                {
                    var p = new Path();
                    p.AddNode(tmp[start]);
                    var astar = new AStar(p, tmp[end], null);
                    shortestPaths.Add(astar.FindPath());
                }
            }
        }
        foreach (var p in shortestPaths)
        {
            if (!_valves.ContainsKey(p.Nodes().First().Id()))
            {
                _valves.Add(p.Nodes().First().Id(), new Node(p.Nodes().First().Id(), p.Nodes().First().Name(), p.Nodes().First().Weight()));
            }
            if (!_valves.ContainsKey(p.Nodes().Last().Id()))
            {
                _valves.Add(p.Nodes().Last().Id(), new Node(p.Nodes().Last().Id(), p.Nodes().Last().Name(), p.Nodes().Last().Weight()));
            }

            _valves[p.Nodes().First().Id()].AddNode(_valves[p.Nodes().Last().Id()], p.Nodes().Count - 1);
        }
    }

    public override string PartOne()
    {
        var maxDepth = 30;
        var start = new Tunnel(maxDepth);
        start.AddNode(_valves["AA"]);
        var bfs = new BFS(start, maxDepth);
        var paths = bfs.FindPaths();
        
        return Convert.ToString(paths.Last());
    }

    public override string PartTwo()
    {
        return Convert.ToString("");
    }
}

internal class Tunnel : Path
{
    private HashSet<INode> _firstVisit;
    private int _maxDepth;

    public Tunnel(int maxDepth)
    {
        _firstVisit = new HashSet<INode>();
        _maxDepth = maxDepth;
    }

    public Tunnel(Tunnel tunnel) : base(tunnel)
    {
        _firstVisit = new HashSet<INode>(tunnel.FirstVisit());
        _maxDepth = tunnel.MaxDepth();
    }

    public HashSet<INode> FirstVisit()
    {
        return _firstVisit;
    }

    public int MaxDepth()
    {
        return _maxDepth;
    }

    public override void AddNode(INode node, int edgeWeight = 0)
    {
        _nodes.Add(node);
        _cost += edgeWeight;
        _depth++;

        if (!_firstVisit.Contains(node))
        {
            if (node.Id() != "AA")
            {
                _cost++;
            }
            _gain += node.Weight() * (_maxDepth - _cost);
            _firstVisit.Add(node);
        }
    }

    public override IPath CreateCopy()
    {
        return new Tunnel(this);
    }

    public override string ToString()
    {
        return $"[{Gain()}][{Cost()}]" + string.Join("->", _nodes);
    }
}