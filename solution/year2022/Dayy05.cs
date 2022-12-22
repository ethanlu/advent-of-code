using System;
using System.Collections;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;

namespace solution.year2022
{
    public class Day05 : Solution
    {
        private string[] input;
        private Dictionary<int, Stack> containers = new Dictionary<int, Stack>();
        private List<Match> moves = new List<Match>();

        public Day05(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();
        }

        private void reset()
        {
            this.containers = new Dictionary<int, Stack>();
            this.moves = new List<Match>();
            
            foreach (var line in this.input)
            {
                if (string.IsNullOrEmpty(line) || Regex.Match(line, @"^[\s\d]+$").Success)
                {
                    continue;
                }

                // container layout
                var matches = Regex.Matches(line, @"\[([A-Z])\]");
                if (matches.Count > 0)
                {
                    var index = 0;
                    foreach (Match m in matches)
                    {
                        index = m.Groups[1].Index / 4;
                        if (!this.containers.ContainsKey(index))
                        {
                            this.containers.Add(index, new Stack());
                        }
                        this.containers[index].Push(m.Groups[1]);
                        //Console.WriteLine(m.Groups[1] +  " at " + m.Groups[1].Index.ToString() + "-" + index);
                    }
                    continue;
                }
                
                // move list
                var match = Regex.Match(line, @"move (\d+) from (\d+) to (\d+)");
                if (match.Success)
                {
                    //Console.WriteLine(match.Groups[1].ToString() + match.Groups[2].ToString() + match.Groups[3].ToString());
                    this.moves.Add(match);
                    continue;
                }
            }
            
            // reverse stack
            List<int> keys = new List<int>(this.containers.Keys);
            foreach (int key in keys)
            {
                //Console.WriteLine(key + " -> " + string.Join("-", this.containers[key].ToArray()));
                this.containers[key] = new Stack(this.containers[key].ToArray());
            }
        }

        public override string PartOne()
        {
            this.reset();

            var amount = 0;
            var source = 0;
            var target = 0;
            foreach (Match move in this.moves)
            {
                amount = Convert.ToInt32(move.Groups[1].Value);
                source = Convert.ToInt32(move.Groups[2].Value) - 1;
                target = Convert.ToInt32(move.Groups[3].Value) - 1;
                for (var i = 0; i < amount; i++)
                {
                    this.containers[target].Push(this.containers[source].Pop());
                }
            }
            
            var top = "";
            for (var i = 0; i < this.containers.Count; i++)
            {
                top += this.containers[i].Peek();
            }
            
            return System.Convert.ToString(top);
        }

        public override string PartTwo()
        {
            this.reset();
            
            var amount = 0;
            var source = 0;
            var target = 0;
            var tmp = new Stack();
            foreach (Match move in this.moves)
            {
                amount = Convert.ToInt32(move.Groups[1].Value);
                source = Convert.ToInt32(move.Groups[2].Value) - 1;
                target = Convert.ToInt32(move.Groups[3].Value) - 1;
                for (var i = 0; i < amount; i++)
                { 
                    tmp.Push(this.containers[source].Pop());
                }
                for (var i = 0; i < amount; i++)
                {
                    this.containers[target].Push(tmp.Pop());
                }
            }

            var top = "";
            for (var i = 0; i < this.containers.Count; i++)
            {
                top += this.containers[i].Peek();
            }
            
            return System.Convert.ToString(top);
        }
        
    }
}