namespace adventofcode.common.graph;

public interface INode : IComparable<INode>, IEquatable<INode>
{
    string Id();
    string Name();
    int Weight();
}