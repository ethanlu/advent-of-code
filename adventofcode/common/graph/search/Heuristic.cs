namespace adventofcode.common.graph.search;

public class Heuristic : IHeuristic
{
    public Heuristic() { }

    public virtual int Cost(INode node, IPath path) { return 0; }
}