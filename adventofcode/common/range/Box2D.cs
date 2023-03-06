using adventofcode.common.grid;

namespace adventofcode.common.range;

public class Box2D : IEquatable<Box2D>
{
    private readonly int _width;
    private readonly int _height;
    private readonly Point2D _topLeft;
    private readonly Point2D _bottomRight;
    private readonly Point2D _topRight;
    private readonly Point2D _bottomLeft;
    private readonly Interval _xInterval;
    private readonly Interval _yInterval;
    
    public Box2D(Point2D topLeft, Point2D bottomRight)
    {
        _topLeft = topLeft;
        _bottomRight = bottomRight;
        _topRight = new Point2D(_bottomRight.X(), _topLeft.Y());
        _bottomLeft = new Point2D(_topLeft.X(), _bottomRight.Y());
        
        _width = Math.Abs(_topRight.X() - _bottomLeft.X());
        _height = Math.Abs(_topLeft.Y() - _bottomRight.Y());

        _xInterval = new Interval(Math.Min(_topLeft.X(), _bottomRight.X()), Math.Max(_topLeft.X(), _bottomRight.X()));
        _yInterval = new Interval(Math.Min(_topLeft.Y(), _bottomRight.Y()), Math.Max(_topLeft.Y(), _bottomRight.Y()));
    }

    public Point2D TopLeft() { return _topLeft; }
    public Point2D BottomRight() { return _bottomRight; }
    public Point2D TopRight() { return _topRight; }
    public Point2D BottomLeft() { return _bottomLeft; }

    public int Width() { return _width; }
    public int Height() { return _height; }
    public int Area() { return _width * _height; }

    public bool Overlaps(Box2D other)
    {
        return _xInterval.Overlaps(other._xInterval) && _yInterval.Overlaps(other._yInterval);
    }

    public bool Contains(Point2D p)
    {
        return _xInterval.Contains(p.X()) && _yInterval.Contains(p.Y());
    }

    public bool Contains(Box2D b)
    {
        return Contains(b.TopLeft()) && Contains(b.TopRight()) && Contains(b.BottomLeft()) && Contains(b.BottomRight());
    }

    public Box2D? Intersect(Box2D other)
    {
        if (Overlaps(other))
        {
            var xIntersect = _xInterval.Intersect(other._xInterval)!;
            var yIntersect = _yInterval.Intersect(other._yInterval)!;

            if (_topLeft.Y() > _bottomRight.Y())
            {   // standard Y-axis 
                return new Box2D(new Point2D(xIntersect.Left(), yIntersect.Right()), new Point2D(xIntersect.Right(), yIntersect.Left()));
            }
            else
            {   // inverted Y-axis
                return new Box2D(new Point2D(xIntersect.Left(), yIntersect.Left()), new Point2D(xIntersect.Right(), yIntersect.Right()));
            }
        }

        return null;
    }

    public bool Equals(Box2D? b)
    {
        return b is not null && _topLeft.Equals(b.TopLeft()) && _bottomRight.Equals(b.BottomRight()) && _topRight.Equals(b.TopRight()) && _bottomLeft.Equals(b.BottomLeft());
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is Box2D && Equals((Box2D) obj);
    }
    
    public override int GetHashCode()
    {
        return _topLeft.X() * _topLeft.Y() * 13 + _bottomRight.X() * _bottomRight.Y() * 37;
    }
    
    public override string ToString()
    {
        return $"({_topLeft.X()},{_topLeft.Y()})-({_topRight.X()},{_topRight.Y()})-({_bottomRight.X()},{_bottomRight.Y()})-({_bottomLeft.X()},{_bottomLeft.Y()})";
    }
}