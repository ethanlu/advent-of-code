namespace adventofcode.common.graph;

public class DirectedGraphNode : Node
{
    private Dictionary<DirectedGraphNode, int> _adjacentNodes;
    
    public DirectedGraphNode(string id, string name, int weight) : base(id, name, weight)
    {
        _adjacentNodes = new Dictionary<DirectedGraphNode, int>();
    }
    
    public DirectedGraphNode AddNode(DirectedGraphNode node, int edgeWeight)
    {
        if (_adjacentNodes.ContainsKey(node))
        {
            _adjacentNodes[node] = edgeWeight;
        }
        else
        {
            _adjacentNodes.Add(node, edgeWeight);
        }
        
        return this;
    }

    public Dictionary<DirectedGraphNode, int> AdjacentNodes()
    {
        return _adjacentNodes;
    }
}