namespace adventofcode.common.graph.search;

public interface ISearchPath : IComparable<ISearchPath>
{
    int Depth();
    int Cost();
    int Gain();
    List<ISearchState> SearchStates();
    ISearchPath Add(ISearchState state);
    ISearchPath CreateCopy();
}