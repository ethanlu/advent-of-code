using adventofcode.common;

namespace adventofcode.year2017;

public class Day17 : Solution
{
    private int _input;
    
    public Day17(string year, string day) : base(year, day)
    {
        _input = Convert.ToInt32(LoadInputAsString());
    }

    public override string PartOne()
    {
        var data = new LinkedList<int>(new List<int>(){0});
        var current = data.First!;
        var currentIndex = 0;
        var step = _input;

        foreach (var i in Enumerable.Range(1, 2017))
        {
            var index = (currentIndex + step) % data.Count;
            var increase = index > currentIndex ? true : false;
            foreach (var j in Enumerable.Range(0, Math.Abs(index - currentIndex)))
            {
                if (increase)
                {
                    currentIndex = currentIndex < data.Count - 1 ? currentIndex + 1 : 0;
                    current = current.Next is not null ? current.Next! : data.First!;
                }
                else
                {
                    currentIndex = currentIndex > 0 ? currentIndex - 1 : data.Count - 1;
                    current = current.Previous is not null ? current.Previous! : data.Last!;
                }
            }
            
            data.AddAfter(current, new LinkedListNode<int>(i));
            current = current.Next!;
            currentIndex += 1;
        }

        return Convert.ToString(current.Next!.Value);
    }

    public override string PartTwo()
    {
        var dataLength = 1L;
        var currentIndex = 0L;
        var step = _input;

        var firstValue = 0L;
        for (long i = 1L; i <= 50000000L; i++)
        {
            var nextIndex = (currentIndex + step) % dataLength;
            dataLength++;

            if (nextIndex == 0L)
            {
                // track current value if it is being inserted into first position
                firstValue = i;
            }

            currentIndex = nextIndex + 1;
        }

        return Convert.ToString(firstValue);
    }
}