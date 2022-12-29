namespace adventofcode.common.graph.search;

public class BFS
{
    private IPath _start;
    private int _maxCost;

    public BFS(IPath start, int maxCost)
    {
        _start = start;
        _maxCost = maxCost;
    }

    public List<IPath> FindPaths()
    {
        var paths = new List<IPath>();

        var candidates = new Queue<IPath>();
        candidates.Enqueue(_start);

        var currentBest = _start;
        do
        {
            var candidate = candidates.Dequeue();

            if (candidate.Cost() >= _maxCost)
            {
                // reached max depth...add candidate to list of paths
                paths.Add(candidate);
                continue;
            }

            var adjacentNodes = candidate.Nodes().Last().AdjacentNodes();
            foreach (var n in adjacentNodes)
            {
                var node = n.Item1;
                var edgeWeight = n.Item2;
                if (adjacentNodes.Count == 1 || candidate.Nodes().Count < 3 || !node.Equals(candidate.NodeAt(-2)))
                {
                    var potentialCandidate = candidate.CreateCopy();
                    potentialCandidate.AddNode(node, edgeWeight);

                    if (potentialCandidate.Gain() < currentBest.Gain() && potentialCandidate.Depth() > currentBest.Depth())
                    {
                        // trim this potential candidate as it has less gains for higher cost than current best
                        continue;
                    }
                    if (potentialCandidate.Gain() > currentBest.Gain())
                    {
                        currentBest = potentialCandidate;
                    }

                    candidates.Enqueue(potentialCandidate);
                }
            }
        } while (candidates.Count > 0);

        paths.Sort();
        return paths;
    }
}