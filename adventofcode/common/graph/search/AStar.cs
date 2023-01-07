namespace adventofcode.common.graph.search;

public class AStar
{
    private ISearchPath _start;
    private ISearchState _end;
    private HashSet<ISearchState> _visited;
    private bool _verbose;
    private long _lap;

    public AStar(ISearchPath start, ISearchState end)
    {
        _start = start;
        _end = end;
        _visited = new HashSet<ISearchState>();
        _verbose = false;
        _lap = 5000L;
    }

    public void Verbose(bool verbose, long lap)
    {
        _verbose = verbose;
        _lap = lap;
    }

    public ISearchPath FindPath()
    {
        var shortest = _start;
        _visited.Add(shortest.SearchStates().Last());
        
        var candidates = new PriorityQueue<ISearchPath, int>();
        candidates.Enqueue(shortest, shortest.Cost() + shortest.Depth() + shortest.SearchStates().Last().PotentialGain());

        var i = 0L;
        var trimmed = 0L;
        do
        {
            var candidate = candidates.Dequeue();

            if (candidate.SearchStates().Last().Id() == _end.Id())
            {
                // destination reached
                shortest = candidate;
                break;
            }

            foreach (var nextState in candidate.SearchStates().Last().NextSearchStates(candidate.SearchStates().Count > 1 ? candidate.SearchStates()[candidate.SearchStates().Count - 2] : null))
            {
                if (_visited.Contains(nextState))
                {
                    trimmed++;
                    continue;
                }
                var nextPath = candidate.CreateCopy();
                nextPath.Add(nextState);
                candidates.Enqueue(nextPath, nextPath.Cost() + nextPath.Depth() + nextPath.PotentialGain());
                _visited.Add(nextState);
            }
            i++;
            if (_verbose && i % _lap == 0L) { Console.WriteLine($"{i} : {candidates.Count} : {trimmed}"); }
        } while (candidates.Count > 0);

        return shortest;
    }
}