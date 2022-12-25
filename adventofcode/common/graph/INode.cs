namespace adventofcode.common.graph;

public interface INode
{
    string Id();
    string Name();
    int Weight();
    List<INode> Neighbors();
}