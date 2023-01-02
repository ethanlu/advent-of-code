namespace adventofcode.common.graph.search;

public class AStar
{
    private ISearchPath _start;
    private ISearchState _end;
    private HashSet<string> _visited;
    private IHeuristic _heuristic;
    private bool _verbose;

    public AStar(ISearchPath start, ISearchState end, IHeuristic? heuristic)
    {
        _start = start;
        _end = end;
        _visited = new HashSet<string>();
        _heuristic = heuristic ?? new Heuristic();
    }

    public void Verbose(bool verbose)
    {
        _verbose = verbose;
    }

    public ISearchPath FindPath()
    {
        var shortest = _start;
        _visited.Add(shortest.SearchStates().Last().Id());
        
        var candidates = new PriorityQueue<ISearchPath, int>();
        candidates.Enqueue(shortest, shortest.Cost() + shortest.Depth() + _heuristic.Cost(shortest.SearchStates().Last(), shortest));

        var i = 0L;
        var trimmed = 0L;
        var completed = 0L;
        do
        {
            var candidate = candidates.Dequeue();

            if (candidate.SearchStates().Last().Id() == _end.Id())
            {
                // destination reached
                shortest = candidate;
                if (_verbose) { Console.WriteLine($"completed : {candidate}"); }
                break;
            }

            foreach (var nextState in candidate.SearchStates().Last().NextSearchStates(candidate.SearchStates().Count > 1 ? candidate.SearchStates()[candidate.SearchStates().Count - 2] : null))
            {
                if (!_visited.Contains(nextState.Id()))
                {
                    var nextPath = candidate.CreateCopy();
                    nextPath.Add(nextState);
                    candidates.Enqueue(nextPath, nextPath.Cost() + nextPath.Depth() + _heuristic.Cost(nextState, nextPath));
                    _visited.Add(nextState.Id());
                }
            }
            i++;
            if (_verbose && i % 1000L == 0L) { Console.WriteLine($"{i} : {candidates.Count} : {completed} : {trimmed}"); }
        } while (candidates.Count > 0);

        return shortest;
    }
}