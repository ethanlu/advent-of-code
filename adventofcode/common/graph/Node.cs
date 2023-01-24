namespace adventofcode.common.graph;

public class Node : INode
{
    private string _id;
    private string _name;
    private int _weight;

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

    public int CompareTo(INode? n)
    {
        if (n is null)
        {
            throw new Exception("INode input is null");
        }

        if (Weight() < n.Weight())
        {
            return -1;
        }
        if (Weight() > n.Weight())
        {
            return 1;
        }
        return 0;
    }
    
    public bool Equals(INode? i)
    {
        if (i is null)
        {
            return false;
        }

        return Id() == i.Id();
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is INode && Equals((INode) obj);
    }
    
    public override int GetHashCode()
    {
        return Weight() * 1337 + Id().GetHashCode();
    }

    public override string ToString()
    {
        return $"{_name}({_weight})";
    }
}