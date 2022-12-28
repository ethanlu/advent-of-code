namespace adventofcode.common.graph.search;

public class Heuristic : IHeuristic
{
    public Heuristic() { }

    public virtual int Cost(INode node, Path path) { return 0; }
}