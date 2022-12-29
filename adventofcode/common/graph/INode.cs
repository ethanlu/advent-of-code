namespace adventofcode.common.graph;

public interface INode
{
    string Id();
    string Name();
    int Weight();
    INode AddNode(INode adjacentNode, int edgeWeight);
    List<(INode, int)> AdjacentNodes();
}