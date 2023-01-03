namespace adventofcode.common.graph.search;

public interface ISearchState : IComparable<ISearchState>, IEquatable<ISearchState>
{
    public string Id();
    public int Cost();
    public int Gain();
    public int PotentialGain();
    public int MaxCost();
    public List<ISearchState> NextSearchStates(ISearchState? previousSearchState);
}