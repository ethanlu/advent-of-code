using adventofcode.common.grid;

namespace adventofcode.common.range;

public class Box3D : IEquatable<Box3D>
{
    private readonly int _width;    // x axis
    private readonly int _height;   // y axis
    private readonly int _depth;    // z axis
    private readonly Interval _xInterval;
    private readonly Interval _yInterval;
    private readonly Interval _zInterval;
    private readonly Point3D _leftBottomFront;
    private readonly Point3D _leftBottomBack;
    private readonly Point3D _leftTopFront;
    private readonly Point3D _leftTopBack;
    private readonly Point3D _rightBottomFront;
    private readonly Point3D _rightBottomBack;
    private readonly Point3D _rightTopFront;
    private readonly Point3D _rightTopBack;

    public Box3D(Point3D leftBottomFront, Point3D rightTopBack)
    {
        _leftBottomFront = leftBottomFront;
        _leftBottomBack = new Point3D(leftBottomFront.X(), leftBottomFront.Y(), rightTopBack.Z());
        _leftTopFront = new Point3D(leftBottomFront.X(), rightTopBack.Y(), leftBottomFront.Z());
        _leftTopBack = new Point3D(leftBottomFront.X(), leftBottomFront.Y(), rightTopBack.Z());
        
        _rightBottomFront = new Point3D(rightTopBack.X(), leftBottomFront.Y(), leftBottomFront.Z());
        _rightBottomBack = new Point3D(rightTopBack.X(), leftBottomFront.Y(), rightTopBack.Z());
        _rightTopFront = new Point3D(rightTopBack.X(), rightTopBack.Y(), leftBottomFront.Z());
        _rightTopBack = rightTopBack;

        _xInterval = new Interval(_leftBottomFront.X(), _rightTopBack.X());
        _yInterval = new Interval(_leftBottomFront.Y(), _rightTopBack.Y());
        _zInterval = new Interval(_leftBottomFront.Z(), _rightTopBack.Z());

        _width = Math.Abs(leftBottomFront.X() - rightTopBack.X());
        _height = Math.Abs(leftBottomFront.Y() - rightTopBack.Y());
        _depth = Math.Abs(leftBottomFront.Z() - rightTopBack.Z());
    }

    public Point3D LeftBottomFront() { return _leftBottomFront; }
    public Point3D LeftBottomBack() { return _leftBottomBack; }
    public Point3D LeftTopFront() { return _leftTopFront; }
    public Point3D LeftTopBack() { return _leftTopBack; }
    public Point3D RightBottomFront() { return _rightBottomFront; }
    public Point3D RightBottomBack() { return _rightBottomBack; }
    public Point3D RightTopFront() { return _rightTopFront; }
    public Point3D RightTopBack() { return _rightTopBack; }
    public int Width() { return _width; }
    public int Height() { return _height; }
    public int Depth() { return _depth; }
    public long Volume() { return _width * _height * _depth; }

    public bool Overlaps(Box3D other)
    {
        return _xInterval.Overlaps(other._xInterval) && _yInterval.Overlaps(other._yInterval) && _zInterval.Overlaps(other._zInterval);
    }
    
    public bool Contains(Point3D point)
    {
        return point.X() >= _leftBottomFront.X() && point.X() <= _rightTopBack.X() &&
               point.Y() >= _leftBottomFront.Y() && point.Y() <= _rightTopBack.Y() &&
               point.Z() >= _leftBottomFront.Z() && point.Z() <= _rightTopBack.Z();
    }

    public bool Contains(Box3D other)
    {
        return Contains(other.LeftBottomFront()) && Contains(other.LeftBottomBack()) && Contains(other.LeftTopFront()) && Contains(other.LeftTopBack()) && 
               Contains(other.RightBottomFront()) && Contains(other.RightBottomBack()) && Contains(other.RightTopFront()) && Contains(other.RightTopBack());
    }

    public Box3D? Intersect(Box3D other)
    {
        if (Overlaps(other))
        {
            var xIntersect = _xInterval.Intersect(other._xInterval)!;
            var yIntersect = _yInterval.Intersect(other._yInterval)!;
            var zIntersect = _zInterval.Intersect(other._zInterval)!;
            
            return new Box3D(new Point3D(xIntersect.Left(), yIntersect.Left(), zIntersect.Left()), new Point3D(xIntersect.Right(), yIntersect.Right(), zIntersect.Right()));
        }

        return null;
    }

    public bool Equals(Box3D? b)
    {
        return b is not null &&
               _leftBottomFront == b.LeftBottomFront() && _leftBottomBack == b.LeftBottomBack() && _leftTopFront == b.LeftTopFront() && _leftTopBack == b.LeftTopBack() && 
               _rightBottomFront == b.RightBottomFront() && _rightBottomBack == b.RightBottomBack() && _rightTopFront == b.RightTopFront() && _rightTopBack == b.RightTopBack();
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is Box3D && Equals((Box3D) obj);
    }
    
    public override int GetHashCode()
    {
        return _leftBottomFront.GetHashCode() * 23 + _rightTopBack.GetHashCode() * 47;
    }
    
    public override string ToString()
    {
        return $"([{_width}x{_height}x{_depth}]@{_leftBottomFront}-{_rightTopBack})";
    }
}