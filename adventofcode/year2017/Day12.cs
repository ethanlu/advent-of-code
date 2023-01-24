using adventofcode.common;
using adventofcode.common.graph;
using adventofcode.common.graph.search;

namespace adventofcode.year2017;

public class Day12 : Solution
{
    private Dictionary<string, DirectedGraphNode> _programs;
    
    public Day12(string year, string day) : base(year, day)
    {
        _programs = new Dictionary<string, DirectedGraphNode>();
        foreach (var line in LoadInputAsLines())
        {
            var tmp = line.Split(" <-> ");

            if (!_programs.ContainsKey(tmp[0]))
            {
                _programs.Add(tmp[0], new DirectedGraphNode(tmp[0], tmp[0], 0));
            }

            foreach (var link in tmp[1].Split(", "))
            {
                if (!_programs.ContainsKey(link))
                {
                    _programs.Add(link, new DirectedGraphNode(link, link, 0));
                }

                _programs[tmp[0]].AddNode(_programs[link], 0);
                _programs[link].AddNode(_programs[tmp[0]], 0);
            }
        }
    }

    public override string PartOne()
    {
        var ff = new FloodFill(new GroupSearchState(_programs["0"], 0, 0, 99999));
        var reachable = ff.Fill();

        return Convert.ToString(reachable.Count);
    }

    public override string PartTwo()
    {
        var remaining = new Queue<DirectedGraphNode>(_programs.Values);
        var processed = new HashSet<DirectedGraphNode>();

        var groups = 0;
        while (remaining.Count > 0)
        {
            var candidate = remaining.Dequeue();
            
            if (!processed.Contains(candidate))
            {
                var ff = new FloodFill(new GroupSearchState(candidate, 0, 0, 99999));
                foreach (GroupSearchState gs in ff.Fill())
                {
                    processed.Add(gs.Program());
                }
                
                groups++;
            }
        }

        return Convert.ToString(groups);
    }

    private class GroupSearchState : SearchState
    {
        private DirectedGraphNode _program;
        
        public GroupSearchState(DirectedGraphNode program, int gain, int cost, int maxCost) : base(program.Id(), gain, cost, maxCost)
        {
            _program = program;
        }

        public DirectedGraphNode Program() { return _program; }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();
            
            foreach (var neighbor in _program.AdjacentNodes())
            {
                states.Add(new GroupSearchState((DirectedGraphNode) neighbor.Key, _gain, _cost, _maxCost));
            }

            return states;
        }
    }
}