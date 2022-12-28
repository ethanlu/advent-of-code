namespace adventofcode.common.graph.search;

public class AStar
{
    private Path _start;
    private INode _end;
    private HashSet<INode> _visited;
    private IHeuristic _heuristic;
    

    public AStar(Path start, INode end, IHeuristic? heuristic)
    {
        _start = start;
        _end = end;
        _visited = new HashSet<INode>();
        _heuristic = heuristic ?? new Heuristic();
    }

    public Path FindPath()
    {
        var shortest = _start;
        _visited.Add(shortest.Nodes().Last());
        
        var candidates = new PriorityQueue<Path, int>();
        candidates.Enqueue(shortest, shortest.Cost() + _heuristic.Cost(shortest.Nodes().Last(), shortest));

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
                if (!_visited.Contains(neighbor))
                {
                    var nextPath = new Path(candidate).AddNode(neighbor);
                    candidates.Enqueue(nextPath, nextPath.Cost() + _heuristic.Cost(neighbor, nextPath));
                    _visited.Add(neighbor);
                }
            }
        } while (candidates.Count > 0);

        return shortest;
    }
}