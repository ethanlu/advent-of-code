namespace adventofcode.common.graph.search;

public abstract class SearchState : ISearchState
{
    protected string _id;
    protected int _gain;
    protected int _cost;
    protected int _maxCost;

    public SearchState(string id, int gain, int cost, int maxCost)
    {
        _id = id;
        _gain = gain;
        _cost = cost;
        _maxCost = maxCost;
    }

    public string Id() { return _id; }
    public int Cost() { return _cost; } 
    public int Gain() { return _gain; }
    public virtual int PotentialGain() { return 0; }

    public int MaxCost() { return _maxCost; }
    
    public int CompareTo(ISearchState? s)
    {
        if (s is null)
        {
            throw new Exception("ISearchState input is null");
        }

        if (Gain() < s.Gain())
        {
            return -1;
        }
        if (Gain() > s.Gain())
        {
            return 1;
        }
        if (Cost() < s.Cost())
        {
            return -1;
        }
        if (Cost() > s.Cost())
        {
            return 1;
        }
        return 0;
    }

    public bool Equals(ISearchState? s)
    {
        if (s is null)
        {
            return false;
        }

        return Id() == s.Id();
    }
    
    public override bool Equals(Object? obj)
    {
        return obj is ISearchState && Equals((ISearchState) obj);
    }
    
    public override int GetHashCode()
    {
        return Id().GetHashCode();
    }

    public override string ToString()
    {
        return $"{_gain}:{_cost}:{_maxCost}";
    }
    
    public abstract List<ISearchState> NextSearchStates(ISearchState? previousSearchState);
}