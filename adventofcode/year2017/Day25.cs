using System.Text.RegularExpressions;
using adventofcode.common;

namespace adventofcode.year2017;

public class Day25 : Solution
{
    private List<TuringState> _states;
    private string _startingState;
    private int _checksumStep;
    
    public Day25(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();

        _startingState = Regex.Match(input[0], @"Begin in state ([A-Z])\.").Groups[1].Value;
        _checksumStep = Convert.ToInt32(Regex.Match(input[1], @"Perform a diagnostic checksum after (\d+) steps").Groups[1].Value);
        
        _states = new List<TuringState>();
        for (int i = 3; i < input.Length; i += 10)
        {
            var name = Regex.Match(input[i], @"In state ([A-Z]):").Groups[1].Value;
            var write0 = Convert.ToInt32(Regex.Match(input[i + 2], @"Write the value (\d)").Groups[1].Value);
            var move0 = Regex.Match(input[i + 3], @"Move one slot to the (left|right)").Groups[1].Value;
            var continue0 = Regex.Match(input[i + 4], @"Continue with state ([A-Z])").Groups[1].Value;
            var write1 = Convert.ToInt32(Regex.Match(input[i + 6], @"Write the value (\d)").Groups[1].Value);
            var move1 = Regex.Match(input[i + 7], @"Move one slot to the (left|right)").Groups[1].Value;
            var continue1 = Regex.Match(input[i + 8], @"Continue with state ([A-Z])").Groups[1].Value;
            _states.Add(new TuringState(name, write0, move0, continue0, write1, move1, continue1));
        }
    }

    public override string PartOne()
    {
        var tm = new TuringMachine(_states, _startingState, _checksumStep);
        tm.Run();
        tm.Show();
        return Convert.ToString(tm.Checksum());
    }

    public override string PartTwo()
    {
        return Convert.ToString("ᕕ( ᐛ )ᕗ");
    }

    private class TuringState
    {
        private string _name;
        private int _write0;
        private string _move0;
        private string _continue0;
        private int _write1;
        private string _move1;
        private string _continue1;

        public TuringState(string name, int write0, string move0, string continue0, int write1, string move1, string continue1)
        {
            _name = name;
            _write0 = write0;
            _write1 = write1;
            _move0 = move0;
            _move1 = move1;
            _continue0 = continue0;
            _continue1 = continue1;
        }

        public string Name() { return _name; }

        public int Write(int currentValue)
        {
            return currentValue == 0 ? _write0 : _write1;
        }

        public string Move(int currentValue)
        {
            return currentValue == 0 ? _move0 : _move1;
        }

        public string Continue(int currentValue)
        {
            return currentValue == 0 ? _continue0 : _continue1;
        }
    }

    private class TuringMachine
    {
        private LinkedList<int> _tape;
        private LinkedListNode<int> _cursor;
        private Dictionary<string, TuringState> _states;
        private string _state;
        private int _step;
        private int _checksumStep;
        
        public TuringMachine(List<TuringState> states, string startState, int checksumStep)
        {
            _state = startState;
            _step = 0;
            _checksumStep = checksumStep;
            
            _states = new Dictionary<string, TuringState>();
            foreach (var state in states)
            {
                _states.Add(state.Name(), state);
            }

            _cursor = new LinkedListNode<int>(0);
            _tape = new LinkedList<int>();
            _tape.AddFirst(_cursor);
        }

        public void Show()
        {
            var head = _tape.First;
            while (head is not null)
            {
                if (head == _cursor)
                {
                    Console.Write($" [{head.Value}] ");
                }
                else
                {
                    Console.Write($" {head.Value} ");
                }
                head = head.Next;
            }
            Console.WriteLine("");
        }

        public int Checksum()
        {
            var checksum = 0;
            var head = _tape.First;
            while (head is not null)
            {
                checksum += head.Value;
                head = head.Next;
            }
            return checksum;
        }

        public void Run()
        {
            while (_step < _checksumStep)
            {
                var value = _cursor.Value;
                // write new value
                _cursor.Value = _states[_state].Write(value);

                // move cursor
                switch (_states[_state].Move(value))
                {
                    case "left":
                        if (_cursor.Previous is null) { _tape.AddFirst(new LinkedListNode<int>(0)); }
                        _cursor = _cursor.Previous!;
                        break;
                    case "right":
                        if (_cursor.Next is null) { _tape.AddLast(new LinkedListNode<int>(0)); }
                        _cursor = _cursor.Next!;
                        break;
                    default:
                        throw new Exception($"Invalid direction : {_states[_state].Move(value)}");
                }

                // change state
                _state = _states[_state].Continue(value);
                _step++;
            }
        }
    }
}