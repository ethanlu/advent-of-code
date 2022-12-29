namespace adventofcode.common.graph;

public class Path : IPath, IComparable<IPath>, IEquatable<Path>
{
    protected List<INode> _nodes;
    protected int _depth;
    protected int _cost;
    protected int _gain;

    public Path()
    {
        _nodes = new List<INode>();
        _depth = 0;
        _cost = 0;
        _gain = 0;
    }
    
    public Path(Path path)
    {
        _nodes = new List<INode>(path.Nodes());
        _depth = path.Depth();
        _cost = path.Cost();
        _gain = path.Gain();
    }
    
    public int Depth()
    {
        return _depth;
    }

    public int Cost()
    {
        return _cost;
    }

    public int Gain()
    {
        return _gain;
    }

    public List<INode> Nodes()
    {
        return _nodes;
    }

    public INode NodeAt(int index)
    {
        if (Math.Abs(index) >= _nodes.Count)
        {
            throw new Exception($"Path index out of bound : {index}");
        }

        return index >= 0 ? _nodes[index] : _nodes[_nodes.Count + index];
    }
    
    public virtual void AddNode(INode node, int edgeWeight=0)
    {
        _nodes.Add(node);
        _gain += node.Weight();
        _cost += edgeWeight;
        _depth++;
    }

    public virtual IPath CreateCopy()
    {
        return new Path(this);
    }

    public int CompareTo(IPath? p)
    {
        if (p is null)
        {
            throw new Exception("Path input is null");
        }
        
        if (Gain() < p.Gain())
        {
            return -1;
        }
        if (Gain() > p.Gain())
        {
            return 1;
        }
        if (Cost() < p.Cost())
        {
            return -1;
        }
        if (Cost() > p.Cost())
        {
            return 1;
        }
        if (Depth() < p.Depth())
        {
            return -1;
        }
        if (Depth() > p.Depth())
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
        
        if (Gain() != p.Gain())
        {
            return false;
        }

        if (Cost() != p.Cost())
        {
            return false;
        }

        if (Depth() != p.Depth())
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