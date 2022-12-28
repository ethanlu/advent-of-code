namespace adventofcode.common.range;

public class Interval : IComparable<Interval>, IEquatable<Interval>
{
    private readonly int _left;
    private readonly int _right;
    
    public Interval(int left, int right)
    {
        _left = left;
        _right = right;
    }

    public int Left()
    {
        return _left;
    }

    public int Right()
    {
        return _right;
    }

    public bool Overlaps(Interval interval)
    {
        return !(_right < interval.Left() || _left > interval.Right());
    }

    public bool Contains(Interval interval)
    {
        return (_left <= interval.Left() && _right >= interval.Right()) ||
               (interval.Left() <= _left && interval.Right() >= _right);
    }

    public bool Contains(int n)
    {
        return _left <= n && _right >= n;
    }

    public Interval? Union(Interval i)
    {
        if (Overlaps(i))
        {
            return new Interval(Math.Min(_left, i.Left()), Math.Max(_right, i.Right()));
        }

        return null;
    }

    public Interval? Intersect(Interval i)
    {
        if (Overlaps(i))
        {
            return new Interval(Math.Max(_left, i.Left()), Math.Min(_right, i.Right()));
        }

        return null;
    }
    
    public int CompareTo(Interval? i)
    {
        if (i is null)
        {
            throw new Exception("Interval input is null");
        }

        if (_left < i.Left())
        {
            return -1;
        }
        if (_left > i.Left())
        {
            return 1;
        }
        return 0;
    }
    
    public bool Equals(Interval? i)
    {
        return i is not null && _left == i.Left() && _right == i.Right();
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is Interval && Equals((Interval) obj);
    }
    
    public override int GetHashCode()
    {
        return _left * 13 + _right * 37;
    }
    
    public override string ToString()
    {
        return $"({_left}..{_right})";
    }
}