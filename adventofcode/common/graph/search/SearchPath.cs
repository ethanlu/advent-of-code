namespace adventofcode.common.graph.search;

public class SearchPath : ISearchPath
{
    private List<ISearchState> _searchStates;
    private int _depth;
    
    public SearchPath()
    {
        _searchStates = new List<ISearchState>();
        _depth = 0;
    }

    public SearchPath(SearchPath p)
    {
        _searchStates = new List<ISearchState>(p.SearchStates());
        _depth = p.SearchStates().Count;
    }

    public int Depth() { return _depth; }
    public int Gain() { return _searchStates.Count > 0 ? _searchStates.Last().Gain() : 0; }
    public int Cost() { return _searchStates.Count > 0 ? _searchStates.Last().Cost() : 0; }

    public List<ISearchState> SearchStates() { return _searchStates; }

    public ISearchPath Add(ISearchState state)
    {
        _searchStates.Add(state);
        _depth++;

        return this;
    }

    public ISearchPath CreateCopy()
    {
        return new SearchPath(this);
    }
    
    public int CompareTo(ISearchPath? p)
    {
        if (p is null)
        {
            throw new Exception("ISearchPath input is null");
        }

        var lastStateCompare = _searchStates.Last().CompareTo(p.SearchStates().Last()); 
        if (lastStateCompare != 0)
        {
            return lastStateCompare;
        }
        if (Depth() < p.Depth())
        {
            return -1;
        }
        if (Depth() > p.Depth())
        {
            return 1;
        }
        return 0;
    }
    
    public override string ToString()
    {
        return $"[{_searchStates.Last().Gain()}][{_searchStates.Last().Cost()}]({_depth})" + string.Join("->", _searchStates);
    }
}