using adventofcode.common;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day09 : Solution
{
    private int _players;
    private int _marbles;
    
    public Day09(string year, string day) : base(year, day)
    {
        var match = Regex.Match(LoadInputAsString(), @"(\d+) players; last marble is worth (\d+) points");
        _players = Convert.ToInt32(match.Groups[1].Value);
        _marbles = Convert.ToInt32(match.Groups[2].Value);
    }

    public override string PartOne()
    {
        var mg = new MarbleGame(_players);
        
        return Convert.ToString(mg.Play(_marbles));
    }

    public override string PartTwo()
    {
        var mg = new MarbleGame(_players);
        
        return Convert.ToString(mg.Play(_marbles * 100));
    }

    private class MarbleGame
    {
        private LinkedList<int> _marbles;
        private LinkedListNode<int> _current;
        private Dictionary<int, long> _scores;
        private int _numPlayers;

        public MarbleGame(int numPlayers)
        {
            _current = new LinkedListNode<int>(0);
            _marbles = new LinkedList<int>();
            _marbles.AddFirst(_current);
            
            _numPlayers = numPlayers;
            _scores = new Dictionary<int, long>();
            for (int i = 1; i <= numPlayers; i++)
            {
                _scores.Add(i, 0);
            }
        }

        private void Move(int steps)
        {
            for (int x = 0; x < Math.Abs(steps); x++)
            {
                if (steps > 0)
                {
                    _current = _current.Next!;
                    if (_current is null) { _current = _marbles.First!; }
                }
                else
                {
                    _current = _current.Previous!;
                    if (_current is null) { _current = _marbles.Last!; }
                }
            }
        }

        public long Play(int numMarbles)
        {
            int player = 1;
            for (int i = 1; i <= numMarbles; i++)
            {
                if (i % 23 == 0)
                {
                    Move(-7);
                    _scores[player] += i + _current.Value;
                    var tmp = _current;
                    _current = _current.Next!;
                    _marbles.Remove(tmp);
                }
                else
                {
                    Move(1);
                    _marbles.AddAfter(_current, new LinkedListNode<int>(i));
                    _current = _current.Next!;
                }

                if (_current is null) { _current = _marbles.First!; }

                player = player == _numPlayers ? 1 : player + 1;
            }

            return _scores.Values.Aggregate(0L, (acc, s) => acc > s ? acc : s);
        }
    }
}