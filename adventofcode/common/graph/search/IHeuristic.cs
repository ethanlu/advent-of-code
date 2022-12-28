namespace adventofcode.common.graph.search;

public interface IHeuristic
{
    int Cost(INode node, Path path);
}