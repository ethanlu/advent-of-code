namespace adventofcode.common.graph.search;

public interface IHeuristic
{
    int Cost(ISearchState state, ISearchPath path);
}