namespace adventofcode.common.graph.search;

public class BFS
{
    private ISearchPath _start;
    private int _maxCost;
    private bool _verbose;
    private long _lap;

    public BFS(ISearchPath start, int maxCost)
    {
        _start = start;
        _maxCost = maxCost;
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
        var candidates = new PriorityQueue<ISearchPath, int>();
        candidates.Enqueue(_start, 0);

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
                if (candidate.Gain() > currentBest.Gain())
                {
                    currentBest = candidate;
                }
                completed++;
                continue;
            }

            foreach (var nextState in candidate.SearchStates().Last().NextSearchStates(candidate.SearchStates().Count > 1 ? candidate.SearchStates()[candidate.SearchStates().Count - 2] : null))
            {
                var potentialCandidate = candidate.CreateCopy();
                potentialCandidate.Add(nextState);
                
                // trim this candidate if it has less gains and potential gains than the current candidate
                if (potentialCandidate.Gain() < currentBest.Gain() && potentialCandidate.Gain() + potentialCandidate.PotentialGain() < currentBest.Gain())
                {
                    trimmed++;
                    continue;
                }
                
                candidates.Enqueue(potentialCandidate, -potentialCandidate.Gain());
            }
            i++;
            if (_verbose && i % _lap == 0L) { Console.WriteLine($"{i} : {candidates.Count} : {completed} : {trimmed}"); }
        } while (candidates.Count > 0);

        return currentBest;
    }
}