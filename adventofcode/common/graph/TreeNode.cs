namespace adventofcode.common.graph;

public class TreeNode : Node
{
    private TreeNode? _parent;
    private Dictionary<TreeNode, int> _children;
    
    public TreeNode(string id, string name, int weight) : base(id, name, weight)
    {
        _parent = null;
        _children = new Dictionary<TreeNode, int>();
    }

    public TreeNode? Parent() { return _parent; }
    public TreeNode Parent(TreeNode parent)
    {
        _parent = parent;
        return this;
    }

    public TreeNode AddChild(TreeNode node, int key)
    {
        if (!_children.ContainsKey(node))
        {
            _children.Add(node, key);
        }
        else
        {
            _children[node] = key;
        }
        node.Parent(this);
        
        return this;
    }

    public Dictionary<TreeNode, int> Children()
    {
        return _children;
    }
}