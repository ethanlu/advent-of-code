namespace adventofcode.common.graph.search;

public class AStar
{
    private IPath _start;
    private INode _end;
    private HashSet<INode> _visited;
    private IHeuristic _heuristic;
    

    public AStar(IPath start, INode end, IHeuristic? heuristic)
    {
        _start = start;
        _end = end;
        _visited = new HashSet<INode>();
        _heuristic = heuristic ?? new Heuristic();
    }

    public IPath FindPath()
    {
        var shortest = _start;
        _visited.Add(shortest.Nodes().Last());
        
        var candidates = new PriorityQueue<IPath, int>();
        candidates.Enqueue(shortest, shortest.Cost() + shortest.Depth() + _heuristic.Cost(shortest.Nodes().Last(), shortest));

        do
        {
            var candidate = candidates.Dequeue();

            if (candidate.Nodes().Last().Id() == _end.Id())
            {
                // destination reached
                shortest = candidate;
                break;
            }

            foreach (var t in candidate.Nodes().Last().AdjacentNodes())
            {
                var adjacentNode = t.Item1;
                var edgeWeight = t.Item2;
                if (!_visited.Contains(adjacentNode))
                {
                    var nextPath = candidate.CreateCopy();
                    nextPath.AddNode(adjacentNode, edgeWeight);
                    candidates.Enqueue(nextPath, nextPath.Cost() + nextPath.Depth() + _heuristic.Cost(adjacentNode, nextPath));
                    _visited.Add(adjacentNode);
                }
            }
        } while (candidates.Count > 0);

        return shortest;
    }
}