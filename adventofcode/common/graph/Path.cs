namespace adventofcode.common.graph;

public class Path
{
    private List<INode> _nodes;
    private int _cost;

    public Path()
    {
        _nodes = new List<INode>();
        _cost = 0;
    }

    public Path(Path path)
    {
        _nodes = new List<INode>(path.Nodes());
        _cost = path.Cost();
    }
    
    public Path(List<INode> nodes)
    {
        _nodes = new List<INode>(nodes);
        _cost = _nodes.Aggregate(0, (acc, n) => acc + n.Weight());
    }

    public int Cost()
    {
        return _cost;
    }

    public List<INode> Nodes()
    {
        return _nodes;
    }

    public void AddNode(INode node)
    {
        _nodes.Add(node);
        _cost += node.Weight();
    }
    
    public override string ToString()
    {
        //return $"Path [{Cost()}]: " + string.Join("->", _nodes.Select(n => $"{n.Name()}[{n.Id()}]"));
        return $"Path [{Cost()}]: " + string.Join("->", _nodes.Select(n => $"{n.Name()}"));
    }
}