namespace adventofcode.common.graph.search;

public class FloodFill
{
    private ISearchState _start;
    private bool _verbose;
    private long _lap;
    
    public FloodFill(ISearchState start)
    {
        _start = start;
        _verbose = false;
        _lap = 5000L;
    }
    
    public void Verbose(bool verbose, long lap)
    {
        _verbose = verbose;
        _lap = lap;
    }

    public List<ISearchState> Fill()
    {
        var filled = new List<ISearchState>(){_start};
        var visited = new HashSet<ISearchState>(){_start};
        var remaining = new Queue<ISearchState>();
        remaining.Enqueue(_start);

        var i = 0L;
        while (remaining.Count > 0)
        {
            var state = remaining.Dequeue();
            foreach (var candidate in state.NextSearchStates(state))
            {
                if (!visited.Contains(candidate))
                {
                    visited.Add(candidate);
                    filled.Add(candidate);
                    remaining.Enqueue(candidate);
                }
            }
            
            i++;
            if (_verbose && i % _lap == 0L) { Console.WriteLine($"{i} : {remaining.Count} : {filled.Count}"); }
        }

        return filled;
    }
}