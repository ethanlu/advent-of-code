using adventofcode.common;
using adventofcode.common.graph;
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
        var shortestPaths = new List<ISearchPath>();
        foreach (var start in inputValves)
        {
            foreach (var end in inputValves)
            {
                if (!start.Equals(end))
                {
                    var p = new SearchPath();
                    p.Add(new OptimizationState(start, 0, 0, 9999));
                    var astar = new AStar(p, new OptimizationState(end, 0, 0, 9999), null);
                    shortestPaths.Add(astar.FindPath());
                }
            }
        }
        
        var optimizedValves = new Dictionary<string, Node>();
        foreach (var p in shortestPaths)
        {
            var firstNode = ((OptimizationState) p.SearchStates().First()).Valve();
            var lastNode = ((OptimizationState) p.SearchStates().Last()).Valve();
            
            if (!optimizedValves.ContainsKey(firstNode.Id()))
            {
                optimizedValves.Add(firstNode.Id(), new Node(firstNode.Id(), firstNode.Name(), firstNode.Weight()));
            }
            if (!optimizedValves.ContainsKey(lastNode.Id()))
            {
                optimizedValves.Add(lastNode.Id(), new Node(lastNode.Id(), lastNode.Name(), lastNode.Weight()));
            }

            optimizedValves[firstNode.Id()].AddNode(optimizedValves[lastNode.Id()], p.SearchStates().Count - 1);
        }

        return optimizedValves;
    }

    public override string PartOne()
    {
        return "";
        // optimize the graph to only be a graph of valve nodes with flow rate > 0 and the starting valve node
        var valves = new List<Node>(_importantValves);
        valves.Add(_valves["AA"]);
        var optimizedValves = OptimizeValves(valves);
        
        // with optimized valve graph, find best path using bfs
        var maxDepth = 30;
        var start = new SearchPath();
        start.Add(new PressureState(new Dictionary<string, int>(optimizedValves.Keys.ToList().Select(k => new KeyValuePair<string, int>(k, 0))), optimizedValves["AA"], 0, 0, maxDepth));
        
        var bfs = new BFS(start, maxDepth);
        var paths = bfs.FindPaths(100);
        
        Console.WriteLine($"Best path : {paths.Last()}");
        
        return Convert.ToString(paths.Last().SearchStates().Last().Gain());
    }

    public override string PartTwo()
    {
        // split the valves with flow rate > 0 evenly into two separate optimized graphs to find the optimal path for you and elephant
        var bestScore = 0;
        SearchPath? youBest = null;
        SearchPath? elephantBest = null;
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
            var start = new SearchPath();
            start.Add(new PressureState(new Dictionary<string, int>(optimizedValvesYou.Keys.ToList().Select(k => new KeyValuePair<string, int>(k, 0))), optimizedValvesYou["AA"], 0, 0, maxDepth));
            var bfs = new BFS(start, maxDepth);
            var you = (SearchPath) bfs.FindPaths(100).Last();
        
            start = new SearchPath();
            start.Add(new PressureState(new Dictionary<string, int>(optimizedValvesElephant.Keys.ToList().Select(k => new KeyValuePair<string, int>(k, 0))), optimizedValvesElephant["AA"], 0, 0, maxDepth));
            bfs = new BFS(start, maxDepth);
            var elephant = (SearchPath) bfs.FindPaths(100).Last();
        
            var currentScore = you.SearchStates().Last().Gain() + elephant.SearchStates().Last().Gain();
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
        
        Console.WriteLine(youBest!.ToString());
        Console.WriteLine(elephantBest!.ToString());
        
        return Convert.ToString(bestScore);
    }
}

internal class OptimizationState : SearchState
{
    private Node _valve;

    public OptimizationState(Node valve, int gain, int cost, int maxCost) : base(valve.Id(), gain, cost, maxCost)
    {
        _valve = valve;
    }

    public Node Valve() { return _valve; }

    public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
    {
        var states = new List<ISearchState>();

        foreach (var (node, edge) in _valve.AdjacentNodes().Where(n => previousSearchState?.Id() != n.Item1.Id()))
        {
            states.Add(new OptimizationState((Node) node, _gain + node.Weight(), _cost + edge, _maxCost));
        }

        return states;
    }
}

internal class PressureState : SearchState
{
    private Dictionary<string, int> _visitLog;
    private INode _valve;

    public PressureState(Dictionary<string, int> visitLog, INode valve, int gain, int cost, int maxDepth) : base(valve.Id(), gain, cost, maxDepth)
    {
        _visitLog = new Dictionary<string, int>(visitLog);
        _valve = valve;

        _visitLog[_valve.Id()]++;
        _id = $"{_valve.Id()}.{_gain}.{_cost}.{_maxCost}";
    }

    public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
    {
        var states = new List<ISearchState>();

        if (_visitLog.Aggregate(true, (acc, kv) => acc && kv.Value > 0))
        {
            // all valves have been visited, so end prematurely
            states.Add(new PressureState(_visitLog, _valve, _gain, _maxCost, _maxCost));
            
            return states;
        }
        
        // otherwse, keep searching
        foreach (var (node, edgeWeight) in _valve.AdjacentNodes())
        {
            // avoid previous search state unless it is the only option
            if (previousSearchState?.Id() != node.Id() || _valve.AdjacentNodes().Count == 1)
            {
                var cost = _cost + edgeWeight;
                var gain = _gain;
                if (_visitLog[node.Id()] == 0)
                {
                    // first visit to valve turns it on, so calculate total pressure based on remaining time
                    cost += 1;
                    gain += node.Weight() * (_maxCost - cost);
                }
                states.Add(new PressureState(_visitLog, node, gain, cost, _maxCost));
            }
        }

        return states;
    }

    public override string ToString()
    {
        return $"[{_cost}]({_gain}){_valve.Id()}";
    }
}