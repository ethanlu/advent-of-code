using adventofcode.common;
using adventofcode.common.graph.search;

namespace adventofcode.year2017;

public class Day24 : Solution
{
    private HashSet<Port> _ports;
    
    public Day24(string year, string day) : base(year, day)
    {
        _ports = new HashSet<Port>();
        foreach (var line in LoadInputAsLines())
        {
            _ports.Add(new Port(line));
        }
    }

    public override string PartOne()
    {
        var start = new StrongestBridgeSearchState(_ports, new Port("0/0"), 0, 0, 0, 99999);
        var path = new SearchPath();
        path.Add(start);
        var bfs = new BFS(path, 99999);
        bfs.Verbose(true, 100000L);

        var best = bfs.FindPath();
        Console.WriteLine(best);
        
        return Convert.ToString(best.Gain());
    }

    public override string PartTwo()
    {
        var start = new LongestBridgeSearchState(_ports, new Port("0/0"), 0, 0, 0, 99999);
        var path = new SearchPath();
        path.Add(start);
        var bfs = new BFS(path, 99999);
        bfs.Verbose(true, 100000L);

        var best = bfs.FindPath();
        Console.WriteLine(best);

        return Convert.ToString(best.SearchStates().Aggregate(0, (acc, s) => acc + ((LongestBridgeSearchState) s).PortStrength()));
    }

    private class Port : IEquatable<Port>
    {
        private int _left;
        private int _right;

        public Port(string port)
        {
            var tmp = port.Split("/");
            _left = Convert.ToInt32(tmp[0]);
            _right = Convert.ToInt32(tmp[1]);
        }

        public int Left() { return _left; }
        public int Right() { return _right; }

        public bool Equals(Port? other)
        {
            if (other is null) { return false; }

            return _left == other.Left() && _right == other.Right();
        }

        public bool Equals(Object other) { return other is Port && Equals((Port) other); }
        public override int GetHashCode() { return Left() * 13 + Right() * 37; }
        public override string ToString() { return $"[{_left + _right}]{_left}/{_right}"; }
    }

    private class StrongestBridgeSearchState : SearchState
    {
        private HashSet<Port> _availablePorts;
        private Port _port;
        private int _openPin;
        
        public StrongestBridgeSearchState(HashSet<Port> availablePorts, Port port, int openPin, int gain, int cost, int maxCost) : base ($"{availablePorts.Count}:{openPin}", gain, cost, maxCost)
        {
            _availablePorts = new HashSet<Port>(availablePorts);
            _availablePorts.Remove(port);
            _port = port;
            _openPin = openPin;
        }

        public override int PotentialGain()
        {
            return _availablePorts.Aggregate(0, (acc, p) => acc + p.Left() + p.Right());
        }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();

            foreach (var p in _availablePorts)
            {
                if (p.Left() == _openPin || p.Right() == _openPin)
                {
                    states.Add(new StrongestBridgeSearchState(_availablePorts, p, p.Left() == _openPin ? p.Right() : p.Left(), _gain + p.Left() + p.Right(), _cost + 1, _maxCost));
                }
            }

            if (states.Count == 0)
            {
                // no more compatible ports, so end bridge search
                states.Add(new StrongestBridgeSearchState(_availablePorts, new Port("0/0"), _openPin, _gain, _maxCost, _maxCost));
            }

            return states;
        }
        
        public override string ToString() { return $"[{_gain}]({_port}):{_openPin}"; }
    }
    
    private class LongestBridgeSearchState : SearchState
    {
        private HashSet<Port> _availablePorts;
        private Port _port;
        private int _openPin;
        
        public LongestBridgeSearchState(HashSet<Port> availablePorts, Port port, int openPin, int gain, int cost, int maxCost) : base ($"{availablePorts.Count}:{openPin}", gain, cost, maxCost)
        {
            _availablePorts = new HashSet<Port>(availablePorts);
            _availablePorts.Remove(port);
            _port = port;
            _openPin = openPin;
        }

        public int PortStrength() { return _port.Left() + _port.Right(); }

        public override int PotentialGain()
        {
            return _availablePorts.Count * 1000 + _availablePorts.Aggregate(0, (acc, p) => acc + p.Left() + p.Right());
        }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();

            foreach (var p in _availablePorts)
            {
                if (p.Left() == _openPin || p.Right() == _openPin)
                {
                    states.Add(new LongestBridgeSearchState(_availablePorts, p, p.Left() == _openPin ? p.Right() : p.Left(), 1000 + _gain + p.Left() + p.Right(), _cost + 1, _maxCost));
                }
            }

            if (states.Count == 0)
            {
                // no more compatible ports, so end bridge search
                states.Add(new LongestBridgeSearchState(_availablePorts, new Port("0/0"), _openPin, _gain, _maxCost, _maxCost));
            }

            return states;
        }
        
        public override string ToString() { return $"[{_gain}]({_port}):{_openPin}"; }
    }
}