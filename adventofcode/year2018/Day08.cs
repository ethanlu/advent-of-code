using adventofcode.common;
using adventofcode.common.graph;

namespace adventofcode.year2018;

public class Day08 : Solution
{
    private string _input;
    
    public Day08(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var nl = new NavigationLicense(_input);
        
        return Convert.ToString(nl.CheckSum());
    }

    public override string PartTwo()
    {
        var nl = new NavigationLicense(_input);
        
        return Convert.ToString(nl.Root().Weight());
    }

    private class NavigationLicense
    {
        private List<int> _license;
        private TreeNode _root;
        private Dictionary<string, List<int>> _metadata;
        private int _nodeCount;
        
        public NavigationLicense(string license)
        {
            _license = new List<int>(license.Split(" ").Select(x => Convert.ToInt32(x)));
            _metadata = new Dictionary<string, List<int>>();
            _nodeCount = 0;
            _root = BuildNode(0).Item1;
        }
        
        private (TreeNode, int) BuildNode(int index)
        {
            var id = $"{_nodeCount}";
            var numChildren = _license[index++];
            var numMetadata = _license[index++];

            _nodeCount++;
            _metadata.Add(id, new List<int>());

            // parse children
            var children = new Dictionary<int, TreeNode>();
            if (numChildren > 0)
            {   // have children, so next sequence of data are children data....
                for (int i = 1; i <= numChildren; i++)
                {   // recurse to build child and its descendents and get the next index in the sequence that contains metadata for current node
                    var (child, nextIndex) = BuildNode(index);
                    index = nextIndex;
                    children.Add(i, child);
                }
            }
            
            // parse metadata
            for (int i = 0; i < numMetadata; i++)
            {
                _metadata[id].Add(_license[index++]);
            }
            
            var weight = _metadata[id].Aggregate(0, (acc, w) => acc + w);
            if (numChildren > 0)
            {
                // has children....weight of node is based on metadata and children
                weight = _metadata[id].Aggregate(0, (acc, childIndex) => acc + (children.ContainsKey(childIndex) ? children[childIndex].Weight() : 0));
            }

            var node = new TreeNode(id, id, weight);
            foreach (var child in children)
            {
                node.AddChild(child.Value, child.Key);
            }

            return (node, index);
        }

        public TreeNode Root() { return _root; }

        public int CheckSum()
        {
            return _metadata.Values.Aggregate(0, (acc, md) => acc + md.Aggregate(0, (acc2, i) => acc2 + i));
        }
    }
}