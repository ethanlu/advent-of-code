namespace adventofcode.common.graph.search;

public class AStar
{
    private INode _start;
    private INode _end;
    private HashSet<string> _visited;
    private Func<INode, int> _heuristic;
    

    public AStar(INode start, INode end, Func<INode, int> heuristic)
    {
        _start = start;
        _end = end;
        _visited = new HashSet<string>();
        _heuristic = heuristic;
    }

    public Path FindPath()
    {
        var shortest = new Path();
        shortest.AddNode(_start);
        _visited.Add(_start.Id());
        
        var candidates = new PriorityQueue<Path, int>();
        candidates.Enqueue(shortest, shortest.Cost() + _heuristic(_start));

        do
        {
            var candidate = candidates.Dequeue();

            if (candidate.Nodes().Last().Id() == _end.Id())
            {
                // destination reached
                shortest = candidate;
                break;
            }

            foreach (var neighbor in candidate.Nodes().Last().Neighbors())
            {
                if (!_visited.Contains(neighbor.Id()))
                {
                    var nextPath = new Path(candidate);
                    nextPath.AddNode(neighbor);
                    candidates.Enqueue(nextPath, nextPath.Cost() + _heuristic(neighbor));
                    _visited.Add(neighbor.Id());
                }
            }
        } while (candidates.Count > 0);

        return shortest;
    }
}