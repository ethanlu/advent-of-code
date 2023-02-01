using adventofcode.common;

namespace adventofcode.year2018;

public class Day05 : Solution
{
    private string _input;
    
    public Day05(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var p = new Polymer(_input);

        return Convert.ToString(p.Reduce().Length);
    }

    public override string PartTwo()
    {
        var shortest = _input.Length;
        for (int i = 'A'; i <= 'Z'; i++)
        {
            var p = new Polymer(_input.Replace(((char) i).ToString(), "").Replace(((char) (i + 32)).ToString(), ""));
            var l = p.Reduce().Length;

            if (shortest > l)
            {
                shortest = l;
            }
        }

        return Convert.ToString(shortest);
    }

    private class Polymer
    {
        private string _polymer;
        
        public Polymer(string polymer)
        {
            _polymer = polymer;
        }

        public string Reduce()
        {
            var reducedPolymer = new Stack<char>();
            reducedPolymer.Push(_polymer[0]);
            for (int i = 1; i < _polymer.Length; i++)
            {
                var current = _polymer[i];
            
                if (reducedPolymer.Count == 0)
                {   // polymer has no stable units, so add to stack and advance
                    reducedPolymer.Push(current);
                    continue;
                }

                if (Math.Abs(reducedPolymer.Peek() - current) == 32)
                {   // polyer end reacts next unit, so remove end from polyer stack and advance
                    reducedPolymer.Pop();
                }
                else
                {   // no reaction, add unit to polymer stack and advance
                    reducedPolymer.Push(current);
                }
            }

            return string.Join(string.Empty, reducedPolymer);
        }
    }
}