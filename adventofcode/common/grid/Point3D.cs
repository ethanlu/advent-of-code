namespace adventofcode.common.grid;

public struct Point3D : IEquatable<Point3D>
{
    private readonly int _x;
    private readonly int _y;
    private readonly int _z;
    
    public Point3D(int x, int y, int z)
    {
        _x = x;
        _y = y;
        _z = z;
    }
    
    public Point3D(string x, string y, string z)
    {
        _x = Convert.ToInt32(x);
        _y = Convert.ToInt32(y);
        _z = Convert.ToInt32(z);
    }
    
    public Point3D(char x, char y, char z)
    {
        _x = Convert.ToInt32(x);
        _y = Convert.ToInt32(y);
        _z = Convert.ToInt32(z);
    }
    
    public (int, int, int) Coordinate()
    {
        return (_x, _y, _z);
    }

    public int X()
    {
        return _x;
    }

    public int Y()
    {
        return _y;
    }
    
    public int Z()
    {
        return _z;
    }
    
    public static Point3D operator +(Point3D a, Point3D b) => new Point3D(a.X() + b.X(), a.Y() + b.Y(), a.Z() + b.Z());
    public static Point3D operator -(Point3D a, Point3D b) => new Point3D(a.X() - b.X(), a.Y() - b.Y(), a.Z() - b.Z());
    public static Point3D operator *(Point3D a, Point3D b) => new Point3D(a.X() * b.X(), a.Y() * b.Y(), a.Z() * b.Z());
    public static Point3D operator /(Point3D a, Point3D b) => new Point3D(a.X() / b.X(), a.Y() / b.Y(), a.Z() / b.Z());
    public static Point3D operator %(Point3D a, Point3D b) => new Point3D(a.X() % b.X(), a.Y() % b.Y(), a.Z() % b.Z());
    public static Point3D operator +(Point3D a, int b) => new Point3D(a.X() + b, a.Y() + b, a.Z() + b);
    public static Point3D operator -(Point3D a, int b) => new Point3D(a.X() - b, a.Y() - b, a.Z() - b);
    public static Point3D operator *(Point3D a, int b) => new Point3D(a.X() * b, a.Y() * b, a.Z() * b);
    public static Point3D operator /(Point3D a, int b) => new Point3D(a.X() / b, a.Y() / b, a.Z() / b);
    public static Point3D operator %(Point3D a, int b) => new Point3D(a.X() % b, a.Y() % b, a.Z() % b);

    public bool Equals(Point3D p)
    {
        return _x == p.X() && _y == p.Y() && _z == p.Z();
    }

    public override bool Equals(Object? obj)
    {
        return obj is Point3D && Equals((Point3D) obj);
    }

    public override int GetHashCode()
    {
        return _x * 13 + _y * 37 + _z * 47;
    }
    
    public override string ToString()
    {
        return $"({_x}, {_y}, {_z})";
    }
}