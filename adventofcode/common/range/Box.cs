using adventofcode.common.grid;

namespace adventofcode.common.range;

public class Box : IEquatable<Box>
{
    private readonly bool _invertedX;
    private readonly bool _invertedY;
    private readonly int _width;
    private readonly int _height;
    private readonly Point2D _topLeft;
    private readonly Point2D _bottomRight;
    private readonly Point2D _topRight;
    private readonly Point2D _bottomLeft;
    
    public Box(Point2D topLeft, Point2D bottomRight)
    {
        _topLeft = topLeft;
        _bottomRight = bottomRight;
        _topRight = new Point2D(_bottomRight.X(), _topLeft.Y());
        _bottomLeft = new Point2D(_topLeft.X(), _bottomRight.Y());
        
        _width = Math.Abs(_topRight.X() - _bottomLeft.X());
        _height = Math.Abs(_topLeft.Y() - _bottomRight.Y());
        _invertedX = topLeft.X() > _topRight.X();
        _invertedY = topLeft.Y() < _bottomLeft.Y();
    }

    public Point2D TopLeft() { return _topLeft; }
    public Point2D BottomRight() { return _bottomRight; }
    public Point2D TopRight() { return _topRight; }
    public Point2D BottomLeft() { return _bottomLeft; }
    
    public bool Contains(Point2D p)
    {
        var withinX = _invertedX ? (_topLeft.X() >= p.X() && _bottomRight.X() <= p.X()) : (_topLeft.X() <= p.X() && _bottomRight.X() >= p.X());
        var withinY = _invertedY ? (_bottomLeft.Y() >= p.Y() && _topRight.Y() <= p.Y()) : (_bottomLeft.Y() <= p.Y() && _topRight.Y() >= p.Y());
        return withinX && withinY;
    }
    
    public bool Equals(Box? b)
    {
        return b is not null && _topLeft.Equals(b.TopLeft()) && _bottomRight.Equals(b.BottomRight()) && _topRight.Equals(b.TopRight()) && _bottomLeft.Equals(b.BottomLeft());
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is Box && Equals((Box) obj);
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