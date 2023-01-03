namespace adventofcode.common.graph.search;

public interface ISearchPath : IComparable<ISearchPath>
{
    int Depth();
    int Cost();
    int Gain();
    int PotentialGain();
    List<ISearchState> SearchStates();
    ISearchPath Add(ISearchState state);
    ISearchPath CreateCopy();
}