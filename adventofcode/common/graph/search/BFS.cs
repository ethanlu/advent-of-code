namespace adventofcode.common.graph.search;

public class BFS
{
    private bool _verbose;
    private ISearchPath _start;
    private int _maxCost;

    public BFS(ISearchPath start, int maxCost)
    {
        _start = start;
        _maxCost = maxCost;
        _verbose = false;
    }

    public void Verbose(bool verbose)
    {
        _verbose = verbose;
    }

    public List<ISearchPath> FindPaths(int trimHandicap=0)
    {
        var paths = new List<ISearchPath>();

        var candidates = new Queue<ISearchPath>();
        candidates.Enqueue(_start);

        var currentBest = _start;

        var i = 0L;
        var trimmed = 0L;
        var completed = 0L;
        do
        {
            var candidate = candidates.Dequeue();

            if (candidate.Cost() >= _maxCost)
            {
                // reached max depth...add candidate to list of paths
                paths.Add(candidate);
                if (_verbose) { Console.WriteLine($"completed : {candidate}"); }

                completed++;
                continue;
            }

            foreach (var nextState in candidate.SearchStates().Last().NextSearchStates(candidate.SearchStates().Count > 1 ? candidate.SearchStates()[candidate.SearchStates().Count - 2] : null))
            {
                var potentialCandidate = candidate.CreateCopy();
                potentialCandidate.Add(nextState);
                
                if (potentialCandidate.Gain() < currentBest.Gain() - trimHandicap && (potentialCandidate.Cost() > currentBest.Cost() || potentialCandidate.Depth() > currentBest.Depth()))
                {
                    // trim this potential candidate as it has less gains for higher cost than any of the best
                    if (_verbose) { Console.WriteLine($"trimmed : {potentialCandidate}"); }
                    trimmed++;
                    continue;
                }
                if (potentialCandidate.Gain() > currentBest.Gain())
                {
                    currentBest = potentialCandidate;
                    if (_verbose) { Console.WriteLine($"best candidate : {potentialCandidate}"); }
                }

                candidates.Enqueue(potentialCandidate);
            }
            i++;
            if (_verbose && i % 1000L == 0L) { Console.WriteLine($"{i} : {candidates.Count} : {completed} : {trimmed}"); }
        } while (candidates.Count > 0);

        paths.Sort();
        return paths;
    }
}