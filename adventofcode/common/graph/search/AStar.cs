namespace adventofcode.common.graph.search;

public class AStar
{
    private Dictionary<ISearchState, ISearchState> _shortestPrevious;
    private Dictionary<ISearchState, int> _score;
    private ISearchState _start;
    private ISearchState _end;
    private bool _verbose;
    private long _lap;

    public AStar(ISearchState start, ISearchState end)
    {
        _shortestPrevious = new Dictionary<ISearchState, ISearchState>();
        _score = new Dictionary<ISearchState, int>();
        _start = start;
        _end = end;
        _verbose = false;
        _lap = 5000L;
        
        _score.Add(_start, 0);
    }

    public void Verbose(bool verbose, long lap)
    {
        _verbose = verbose;
        _lap = lap;
    }

    public ISearchPath FindPath()
    {
        var candidates = new PriorityQueue<ISearchState, int>();
        candidates.Enqueue(_start, _start.Cost() + _start.PotentialGain());

        var i = 0L;
        var trimmed = 0L;

        while (candidates.Count > 0)
        {
            var candidate = candidates.Dequeue();
            if (candidate.Id() == _end.Id())
            {   // destination reached...build shortest path
                var sequence = new Stack<ISearchState>();
                var current = candidate;
                while (_shortestPrevious.ContainsKey(current))
                {
                    sequence.Push(current);
                    current = _shortestPrevious[current];
                }
                sequence.Push(_start);

                var path = new SearchPath();
                while (sequence.Count > 0)
                {
                    path.Add(sequence.Pop());
                }

                return path;
            }

            foreach (var nextState in candidate.NextSearchStates(null))
            {
                var visited = true;
                if (!_score.ContainsKey(nextState))
                {
                    _score.Add(nextState, int.MaxValue);
                    visited = false;
                }
                
                var nextStateScore = _score[candidate] + nextState.Cost();
                if (nextStateScore < _score[nextState])
                {
                    _score[nextState] = nextStateScore;

                    if (!_shortestPrevious.ContainsKey(nextState))
                    {
                        _shortestPrevious.Add(nextState, candidate);
                    }
                    _shortestPrevious[nextState] = candidate;

                    if (!visited)
                    {
                        candidates.Enqueue(nextState, nextState.Cost() + nextState.PotentialGain());
                        continue;
                    }
                }
                trimmed++;
            }
            
            i++;
            if (_verbose && i % _lap == 0L) { Console.WriteLine($"{i} : {candidates.Count} : {trimmed}"); }
        }

        return new SearchPath();
    }
}