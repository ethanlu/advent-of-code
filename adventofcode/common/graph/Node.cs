namespace adventofcode.common.graph;

public abstract class Node : INode
{
    protected string _id;
    protected string _name;
    protected int _weight;

    public Node(string id, string name, int weight)
    {
        _id = id;
        _name = name;
        _weight = weight;
    }

    public string Id()
    {
        return _id;
    }

    public string Name()
    {
        return _name;
    }

    public int Weight()
    {
        return _weight;
    }

    public abstract List<INode> Neighbors();
}