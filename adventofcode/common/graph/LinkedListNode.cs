namespace adventofcode.common.graph;

public class LinkedListNode : Node
{
    private LinkedListNode? _previous;
    private LinkedListNode? _next;
    
    public LinkedListNode(string id, string name, int weight) : base(id, name, weight)
    {
        _previous = null;
        _next = null;
    }

    public LinkedListNode? Previous() { return _previous; }
    public LinkedListNode Previous(LinkedListNode previous)
    {
        _previous = previous;
        return this;
    }

    public LinkedListNode? Next() { return _next; }
    public LinkedListNode Next(LinkedListNode next)
    {
        _next = next;
        return this;
    }
}