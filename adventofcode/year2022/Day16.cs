using adventofcode.common;
using adventofcode.common.graph;
using Path = adventofcode.common.graph.Path;
using adventofcode.common.util;
using System.Text.RegularExpressions;
using adventofcode.common.graph.search;

namespace adventofcode.year2022;

public class Day16 : Solution
{
    private Dictionary<string, Node> _valves;
    private List<Node> _importantValves;

    public Day16(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();

        _valves = new Dictionary<string, Node>();
        _importantValves = new List<Node>();
        foreach (var line in input)
        {
            var match = Regex.Match(line, @"^Valve ([A-Z]{2}) has flow rate=(\d+);");
            var valve = new Node(match.Groups[1].Value, match.Groups[1].Value, Convert.ToInt32(match.Groups[2].Value));
            _valves.Add(match.Groups[1].Value, valve);

            if (valve.Weight() != 0)
            {
                _importantValves.Add(valve);
            }
        }
        foreach (var line in input)
        {
            var match = Regex.Match(line, @"^Valve ([A-Z]{2}) has flow rate=\d+; tunnels? leads? to valves? ([A-Z,\s]+)$");
            foreach (var neighbor in match.Groups[2].Value.Split(", "))
            {
                _valves[match.Groups[1].Value].AddNode(_valves[neighbor], 0);
            }
        }
    }

    private Dictionary<string, Node> OptimizeValves(List<Node> inputValves)
    {
        // optimize graph by running shortest path between all valve nodes that have a flow rate > 0 and build a new graph based on the paths
        var shortestPaths = new List<IPath>();
        foreach (var start in inputValves)
        {
            foreach (var end in inputValves)
            {
                if (start != end)
                {
                    var p = new Path();
                    p.AddNode(start);
                    var astar = new AStar(p, end, null);
                    shortestPaths.Add(astar.FindPath());
                }
            }
        }
        
        var optimizedValves = new Dictionary<string, Node>();
        foreach (var p in shortestPaths)
        {
            if (!optimizedValves.ContainsKey(p.Nodes().First().Id()))
            {
                optimizedValves.Add(p.Nodes().First().Id(), new Node(p.Nodes().First().Id(), p.Nodes().First().Name(), p.Nodes().First().Weight()));
            }
            if (!optimizedValves.ContainsKey(p.Nodes().Last().Id()))
            {
                optimizedValves.Add(p.Nodes().Last().Id(), new Node(p.Nodes().Last().Id(), p.Nodes().Last().Name(), p.Nodes().Last().Weight()));
            }

            optimizedValves[p.Nodes().First().Id()].AddNode(optimizedValves[p.Nodes().Last().Id()], p.Nodes().Count - 1);
        }

        return optimizedValves;
    }

    public override string PartOne()
    {
        // optimize the graph to only be a graph of valve nodes with flow rate > 0 and the starting valve node
        var valves = new List<Node>(_importantValves);
        valves.Add(_valves["AA"]);
        var optimizedValves = OptimizeValves(valves);
        
        // with optimized valve graph, find best path using bfs
        var maxDepth = 30;
        var start = new TunnelPath(maxDepth);
        start.AddNode(optimizedValves["AA"]);
        
        var bfs = new BFS(start, maxDepth);
        var paths = bfs.FindPaths();
        
        return Convert.ToString(paths.Last());
    }

    public override string PartTwo()
    {
        // split the valves with flow rate > 0 evenly into two separate optimized graphs to find the optimal path for you and elephant
        var bestScore = 0;
        TunnelPath? youBest = null;
        TunnelPath? elephantBest = null;
        foreach (var combination in IterTools<Node>.Combination(_importantValves, _importantValves.Count / 2))
        {
            var valvesYou = new List<Node>(combination);
            var handledByYou = combination.ToHashSet();
            var valvesElephant = new List<Node>(_importantValves.Select(x => x).Where(x =>!handledByYou.Contains(x)));
            valvesYou.Add(_valves["AA"]);
            valvesElephant.Add(_valves["AA"]);
            
            Console.WriteLine("#######################");
            Console.WriteLine($"Combination : {string.Join("-", valvesYou)} / {string.Join("-", valvesElephant)}");
        
            var optimizedValvesYou = OptimizeValves(valvesYou);
            var optimizedValvesElephant = OptimizeValves(valvesElephant);
        
            var maxDepth = 26;
            var start = new TunnelPath(maxDepth);
            start.AddNode(optimizedValvesYou["AA"]);
            var bfs = new BFS(start, maxDepth);
            var you = (TunnelPath) bfs.FindPaths().Last();
        
            start = new TunnelPath(maxDepth);
            start.AddNode(optimizedValvesElephant["AA"]);
            bfs = new BFS(start, maxDepth);
            var elephant = (TunnelPath) bfs.FindPaths().Last();

            var currentScore = you.Gain() + elephant.Gain();
            if (bestScore < currentScore)
            {
                bestScore = currentScore;
                youBest = you;
                elephantBest = elephant;
            }
            
            Console.WriteLine($"You        : {you} ");
            Console.WriteLine($"Elephant   : {elephant} ");
            Console.WriteLine($"Score      : {currentScore} ");
            Console.WriteLine($"Best Score : {bestScore} ");
        }
        
        Console.WriteLine(youBest.ToString());
        Console.WriteLine(elephantBest.ToString());

        return Convert.ToString(bestScore);
    }
}

internal class TunnelPath : Path
{
    private HashSet<INode> _firstVisit;
    private int _maxDepth;

    public TunnelPath(int maxDepth)
    {
        _firstVisit = new HashSet<INode>();
        _maxDepth = maxDepth;
    }

    public TunnelPath(TunnelPath TunnelPath) : base(TunnelPath)
    {
        _firstVisit = new HashSet<INode>(TunnelPath.FirstVisit());
        _maxDepth = TunnelPath.MaxDepth();
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
        return new TunnelPath(this);
    }

    public override string ToString()
    {
        return $"[{Gain()}][{Cost()}]" + string.Join("->", _nodes);
    }
}