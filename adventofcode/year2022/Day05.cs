using System.Collections;
using System.Text.RegularExpressions;

namespace adventofcode.year2022
{
    public class Day05 : Solution
    {
        private string[] _input;
        private Dictionary<int, Stack> _containers = new Dictionary<int, Stack>();
        private List<Match> _moves = new List<Match>();

        public Day05(string year, string day) : base(year, day)
        {
            _input = this.LoadInputAsLines();
        }

        private void Reset()
        {
            _containers = new Dictionary<int, Stack>();
            _moves = new List<Match>();
            
            foreach (var line in _input)
            {
                if (string.IsNullOrEmpty(line) || Regex.Match(line, @"^[\s\d]+$").Success)
                {
                    continue;
                }

                // container layout
                var matches = Regex.Matches(line, @"\[([A-Z])\]");
                if (matches.Count > 0)
                {
                    foreach (Match m in matches)
                    {
                        var index = m.Groups[1].Index / 4;
                        if (!_containers.ContainsKey(index))
                        {
                            _containers.Add(index, new Stack());
                        }
                        _containers[index].Push(m.Groups[1]);
                        //Console.WriteLine(m.Groups[1] +  " at " + m.Groups[1].Index.ToString() + "-" + index);
                    }
                    continue;
                }
                
                // move list
                var match = Regex.Match(line, @"move (\d+) from (\d+) to (\d+)");
                if (match.Success)
                {
                    //Console.WriteLine(match.Groups[1].ToString() + match.Groups[2].ToString() + match.Groups[3].ToString());
                    _moves.Add(match);
                }
            }
            
            // reverse stack
            List<int> keys = new List<int>(_containers.Keys);
            foreach (int key in keys)
            {
                //Console.WriteLine(key + " -> " + string.Join("-", _containers[key].ToArray()));
                _containers[key] = new Stack(_containers[key].ToArray());
            }
        }

        public override string PartOne()
        {
            Reset();
            
            foreach (Match move in _moves)
            {
                var amount = Convert.ToInt32(move.Groups[1].Value);
                var source = Convert.ToInt32(move.Groups[2].Value) - 1;
                var target = Convert.ToInt32(move.Groups[3].Value) - 1;
                for (var i = 0; i < amount; i++)
                {
                    _containers[target].Push(_containers[source].Pop());
                }
            }
            
            var top = "";
            for (var i = 0; i < _containers.Count; i++)
            {
                top += _containers[i].Peek();
            }
            
            return Convert.ToString(top);
        }

        public override string PartTwo()
        {
            Reset();
            
            var tmp = new Stack();
            foreach (Match move in _moves)
            {
                var amount = Convert.ToInt32(move.Groups[1].Value);
                var source = Convert.ToInt32(move.Groups[2].Value) - 1;
                var target = Convert.ToInt32(move.Groups[3].Value) - 1;
                for (var i = 0; i < amount; i++)
                { 
                    tmp.Push(_containers[source].Pop());
                }
                for (var i = 0; i < amount; i++)
                {
                    _containers[target].Push(tmp.Pop());
                }
            }

            var top = "";
            for (var i = 0; i < _containers.Count; i++)
            {
                top += _containers[i].Peek();
            }
            
            return Convert.ToString(top);
        }
        
    }
}