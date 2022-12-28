namespace adventofcode.common.graph;

public class Path : IComparable<Path>, IEquatable<Path>
{
    protected List<INode> _nodes;
    protected int _cost;

    public Path()
    {
        _nodes = new List<INode>();
        _cost = 0;
    }
    
    public Path(Path path)
    {
        _nodes = new List<INode>(path.Nodes());
        _cost = ((Path)path).Cost();
    }

    public int Cost()
    {
        return _cost;
    }

    public virtual int Depth()
    {
        return _nodes.Count;
    }

    public List<INode> Nodes()
    {
        return _nodes;
    }

    public virtual Path AddNode(INode node)
    {
        _nodes.Add(node);
        _cost += node.Weight();
        return this;
    }

    public INode NodeAt(int index)
    {
        if (Math.Abs(index) >= _nodes.Count)
        {
            throw new Exception($"Path index out of bound : {index}");
        }

        return index >= 0 ? _nodes[index] : _nodes[_nodes.Count + index];
    }

    public int CompareTo(Path? p)
    {
        if (p is null)
        {
            throw new Exception("Path input is null");
        }

        if (Cost() < p.Cost())
        {
            return -1;
        }
        if (Cost() > p.Cost())
        {
            return 1;
        }
        if (_nodes.Count < p.Nodes().Count)
        {
            return -1;
        }
        if (_nodes.Count > p.Nodes().Count)
        {
            return 1;
        }
        return 0;
    }
    
    public bool Equals(Path? p)
    {
        if (p is null)
        {
            return false;
        }

        if (Cost() != p.Cost())
        {
            return false;
        }

        if (_nodes.Count != p.Nodes().Count)
        {
            return false;
        }

        for (int i = 0; i < _nodes.Count; i++)
        {
            if (_nodes[i].Id() != p.Nodes()[i].Id())
            {
                return false;
            }
        }

        return true;
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is Path && Equals((Path) obj);
    }
    
    public override int GetHashCode()
    {
        return Cost() * 13 + _nodes.Count * 37;
    }
    
    public override string ToString()
    {
        return $"[{Cost()}]" + string.Join("->", _nodes);
    }
}