using System.Text.RegularExpressions;
using adventofcode.common;
using adventofcode.common.graph;

namespace adventofcode.year2017;

public class Day07 : Solution
{
    private List<(string, int)> _programs;
    private List<(string, List<string>)> _supports;
    
    public Day07(string year, string day) : base(year, day)
    {
        _programs = new List<(string, int)>();
        _supports = new List<(string, List<string>)>();

        foreach (var line in LoadInputAsLines())
        {
            var match = Regex.Match(line, @"^([a-z]+) \((\d+)\)(.*)$");
            
            _programs.Add((match.Groups[1].Value, Convert.ToInt32(match.Groups[2].Value)));
            if (match.Groups[3].Value != "")
            {
                _supports.Add((match.Groups[1].Value, new List<string>(match.Groups[3].Value.Substring(4).Split(", "))));
            }
        }
    }

    public override string PartOne()
    {
        var tower = new ProgramTower(_programs, _supports);

        return Convert.ToString(tower.Root().Name());
    }

    public override string PartTwo()
    {
        var tower = new ProgramTower(_programs, _supports);

        return Convert.ToString(tower.FindImbalance(tower.Root(), 0));
    }

    private class ProgramTower
    {
        private Dictionary<string, Node> _programs;
        private Node _root;
        
        public ProgramTower(List<(string, int)> programs, List<(string, List<string>)> supports)
        {
            int TotalChildrenWeight(Node node)
            {
                if (node.AdjacentNodes().Count == 0)
                {
                    return node.Weight();
                }
                
                foreach (var child in node.AdjacentNodes())
                {
                    if (child.Value == 0)
                    {
                        node.AddNode(child.Key, TotalChildrenWeight((Node) child.Key));
                    }
                }

                return node.Weight() + node.AdjacentNodes().Values.Sum();
            }

            _programs = new Dictionary<string, Node>(programs.Select(tuple => new KeyValuePair<string, Node>(tuple.Item1, new Node(tuple.Item1, tuple.Item1, tuple.Item2))));

            foreach (var (name, children) in supports)
            {
                foreach (var child in children)
                {
                    _programs[name].AddNode(_programs[child], 0);
                }
            }

            _root = _programs.First().Value;
            while (_root.Parent() is not null)
            {
                _root = (Node) _root.Parent()!;
            }

            TotalChildrenWeight(_root);
        }

        public Node Root()
        {
            return _root;
        }

        public int FindImbalance(Node node, int delta)
        {
            var childWeights = new Dictionary<int, List<Node>>();
            foreach (var kv in node.AdjacentNodes())
            {
                if (!childWeights.ContainsKey(kv.Value))
                {
                    childWeights.Add(kv.Value, new List<Node>());
                }
                childWeights[kv.Value].Add((Node) kv.Key);
            }

            if (childWeights.Count > 1)
            {
                var tmp = childWeights.ToList();
                var diff = tmp[0].Value.Count > 1 ? tmp[0].Key - tmp[1].Key : tmp[1].Key - tmp[0].Key;
                var targetWeight = tmp[0].Value.Count > 1 ? tmp[0].Key : tmp[1].Key;

                foreach (var child in node.AdjacentNodes())
                {
                    if (child.Value != targetWeight)
                    {
                        return FindImbalance((Node) child.Key, diff);
                    }
                }
            }

            return node.Weight() + delta;
        }
    }
}