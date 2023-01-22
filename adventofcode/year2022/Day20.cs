using adventofcode.common;

namespace adventofcode.year2022;

public class Day20 : Solution
{
    private List<long> _sequence;
    
    public Day20(string year, string day) : base(year, day)
    {
        _sequence = new List<long>();
        foreach (var l in LoadInputAsLines())
        {
            _sequence.Add(Convert.ToInt64(l));
        }
    }

    public override string PartOne()
    {
        var demixer = new Demixer(_sequence, 1, 1);
        var coordinates = demixer.Decrypt();
        
        return Convert.ToString(coordinates);
    }

    public override string PartTwo()
    {
        var demixer = new Demixer(_sequence, 811589153, 10);
        var coordinates = demixer.Decrypt();
        
        return Convert.ToString(coordinates);
    }

    private class Demixer
    {
        private Dictionary<int, LinkedListNode<long>> _sequence;
        private LinkedList<long> _mix;
        private int _zeroIndex;
        private int _length;
        private int _maxCycle;

        public Demixer(List<long> sequence, int key, int maxCycle)
        {
            _sequence = new Dictionary<int, LinkedListNode<long>>();
            _mix = new LinkedList<long>();
            _length = sequence.Count;
            _maxCycle = maxCycle;
            
            _zeroIndex = 0;
            for (int i = 0; i < sequence.Count; i++)
            {
                _zeroIndex = sequence[i] == 0 ? i + 1 : _zeroIndex;
            }

            var n = new LinkedListNode<long>(sequence[0] * key);
            _sequence.Add(1, n);
            _mix.AddFirst(n);
            for (int i = 1; i < sequence.Count - 1; i++)
            {
                n = new LinkedListNode<long>(sequence[i] * key);
                _sequence.Add(i + 1, n);
                _mix.AddAfter(_sequence[i], n);
            }
            n = new LinkedListNode<long>(sequence[^1] * key);
            _sequence.Add(sequence.Count, n);
            _mix.AddLast(n);
        }

        public long Decrypt()
        {
            foreach (var cycle in Enumerable.Range(0, _maxCycle))
            {
                foreach (var (index, node) in _sequence)
                {
                    var shiftAmount = Convert.ToInt32(Math.Abs(node.Value) % (_length - 1));
                    if (shiftAmount == 0)
                    {
                        continue;
                    }
                    shiftAmount = node.Value < 0 ? -(shiftAmount) : shiftAmount;

                    var startNode = _sequence[index];
                    var endNode = _sequence[index];
                    foreach (var i in Enumerable.Range(0, Math.Abs(shiftAmount)))
                    {
                        if (shiftAmount > 0)
                        {
                            endNode = endNode!.Next ?? _mix.First;
                        }
                        else
                        {
                            endNode = endNode!.Previous ?? _mix.Last;
                        }
                    }

                    _mix.Remove(startNode);
                    if (shiftAmount > 0)
                    {
                        _mix.AddAfter(endNode!, startNode);
                    }
                    else
                    {
                        _mix.AddBefore(endNode!, startNode);
                    }
                }
            }

            var coordinates = 0L;
            foreach (var nth in new List<int>() {1000, 2000, 3000})
            {
                var nthNumber = _sequence[_zeroIndex];
                foreach (var i in Enumerable.Range(0, nth % _length))  
                {
                    nthNumber = nthNumber!.Next ?? _mix.First;
                }

                coordinates += nthNumber!.Value;
            }
            
            return coordinates;
        }
    }
}