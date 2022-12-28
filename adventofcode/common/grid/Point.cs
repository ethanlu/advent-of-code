namespace adventofcode.common.grid;

public struct Point : IEquatable<Point>
{
    private readonly int _x;
    private readonly int _y;
    
    public Point(int x, int y)
    {
        _x = x;
        _y = y;
    }
    
    public Point(string x, string y)
    {
        _x = Convert.ToInt32(x);
        _y = Convert.ToInt32(y);
    }
    
    public Point(char x, char y)
    {
        _x = Convert.ToInt32(x);
        _y = Convert.ToInt32(y);
    }
    
    public (int, int) Coordinate()
    {
        return (_x, _y);
    }

    public int X()
    {
        return _x;
    }

    public int Y()
    {
        return _y;
    }

    public bool Equals(Point p)
    {
        return _x == p.X() && _y == p.Y();
    }

    public override bool Equals(Object? obj)
    {
        return obj is Point && Equals((Point) obj);
    }

    public override int GetHashCode()
    {
        return _x * 13 + _y * 37;
    }
    
    public override string ToString()
    {
        return $"({_x}, {_y})";
    }
}