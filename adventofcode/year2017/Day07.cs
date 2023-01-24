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
        private Dictionary<string, TreeNode> _programs;
        private TreeNode _root;
        
        public ProgramTower(List<(string, int)> programs, List<(string, List<string>)> supports)
        {
            int TotalChildrenWeight(TreeNode node)
            {
                if (node.Children().Count == 0)
                {
                    return node.Weight();
                }
                
                foreach (var (child, descendentWeight) in node.Children())
                {
                    if (descendentWeight == 0)
                    {
                        node.AddChild(child, TotalChildrenWeight(child));
                    }
                }

                return node.Weight() + node.Children().Values.Select(s => s).Sum();
            }

            _programs = new Dictionary<string, TreeNode>(programs.Select(tuple => new KeyValuePair<string, TreeNode>(tuple.Item1, new TreeNode(tuple.Item1, tuple.Item1, tuple.Item2))));

            foreach (var (parent, children) in supports)
            {
                foreach (var child in children)
                {
                    _programs[parent].AddChild(_programs[child], 0);
                }
            }

            _root = _programs.First().Value;
            while (_root.Parent() is not null)
            {
                _root = _root.Parent()!;
            }

            TotalChildrenWeight(_root);
        }

        public TreeNode Root()
        {
            return _root;
        }

        public int FindImbalance(TreeNode node, int delta)
        {
            var descendentWeights = new Dictionary<int, List<TreeNode>>();
            foreach (var (child, descendentWeight) in node.Children())
            {
                if (!descendentWeights.ContainsKey(descendentWeight))
                {
                    descendentWeights.Add(descendentWeight, new List<TreeNode>());
                }
                descendentWeights[descendentWeight].Add(child);
            }

            if (descendentWeights.Count > 1)
            {
                var tmp = descendentWeights.ToList();
                var diff = tmp[0].Value.Count > 1 ? tmp[0].Key - tmp[1].Key : tmp[1].Key - tmp[0].Key;
                var targetWeight = tmp[0].Value.Count > 1 ? tmp[0].Key : tmp[1].Key;

                foreach (var (child, descendentWeight) in node.Children())
                {
                    if (descendentWeight != targetWeight)
                    {
                        return FindImbalance(child, diff);
                    }
                }
            }

            return node.Weight() + delta;
        }
    }
}