namespace adventofcode.common.grid;

public struct Point2D : IEquatable<Point2D>
{
    private readonly int _x;
    private readonly int _y;
    
    public Point2D(int x, int y)
    {
        _x = x;
        _y = y;
    }
    
    public Point2D(string x, string y)
    {
        _x = Convert.ToInt32(x);
        _y = Convert.ToInt32(y);
    }
    
    public Point2D(char x, char y)
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
    
    public static Point2D operator +(Point2D a, Point2D b) => new Point2D(a.X() + b.X(), a.Y() + b.Y());
    public static Point2D operator -(Point2D a, Point2D b) => new Point2D(a.X() - b.X(), a.Y() - b.Y());
    public static Point2D operator *(Point2D a, Point2D b) => new Point2D(a.X() * b.X(), a.Y() * b.Y());
    public static Point2D operator /(Point2D a, Point2D b) => new Point2D(a.X() / b.X(), a.Y() / b.Y());
    public static Point2D operator %(Point2D a, Point2D b) => new Point2D(a.X() % b.X(), a.Y() % b.Y());
    public static Point2D operator +(Point2D a, int b) => new Point2D(a.X() + b, a.Y() + b);
    public static Point2D operator -(Point2D a, int b) => new Point2D(a.X() - b, a.Y() - b);
    public static Point2D operator *(Point2D a, int b) => new Point2D(a.X() * b, a.Y() * b);
    public static Point2D operator /(Point2D a, int b) => new Point2D(a.X() / b, a.Y() / b);
    public static Point2D operator %(Point2D a, int b) => new Point2D(a.X() % b, a.Y() % b);

    public bool Equals(Point2D p)
    {
        return _x == p.X() && _y == p.Y();
    }

    public override bool Equals(Object? obj)
    {
        return obj is Point2D && Equals((Point2D) obj);
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