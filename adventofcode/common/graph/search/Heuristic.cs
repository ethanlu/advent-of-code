namespace adventofcode.common.graph.search;

public class Heuristic : IHeuristic
{
    public virtual int Cost(ISearchState state, ISearchPath path) { return 0; }
}