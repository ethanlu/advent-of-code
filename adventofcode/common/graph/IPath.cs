namespace adventofcode.common.graph;

public interface IPath : IComparable<IPath>
{
    int Depth();
    int Cost();
    int Gain();
    List<INode> Nodes();
    INode NodeAt(int index);
    void AddNode(INode node, int edgeWeight = 0);
    IPath CreateCopy();
}