using adventofcode.common;

namespace adventofcode.year2017;

public class Day16 : Solution
{
    private string[] _input;
    
    public Day16(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString().Split(",");
    }

    public override string PartOne()
    {
        var pd = new ProgramDance(_input, 16);
        pd.Dance();
        
        return Convert.ToString(string.Join(string.Empty, pd.Programs()));
    }

    public override string PartTwo()
    {
        var pd = new ProgramDance(_input, 16);
        var startState = string.Join(string.Empty, pd.Programs());

        var i = 0L;
        var maxCycles = 1000000000L;
        while (i < maxCycles)
        {
            i++;
            pd.Dance();
            var currentState = string.Join(string.Empty, pd.Programs());
            
            if (startState == currentState)
            {
                Console.WriteLine($"Cycle detected at : {i}");
                i = maxCycles - (maxCycles % i);
                Console.WriteLine($"Skipping to {i}");
            }
        }

        return Convert.ToString(string.Join(string.Empty, pd.Programs()));
    }

    private class ProgramDance
    {
        private List<string> _moves;
        private char[] _programs;
        
        public ProgramDance(string[] moves, int num)
        {
            _moves = new List<string>(moves);
            _programs = new char[num];
            for (var i = 0; i < num; i++)
            {
                _programs[i] = (char) (i + 97);
            }
        }

        private int CharPosition(char x)
        {
            return Array.FindIndex(_programs, c => c == x);
        }

        private void Spin(int x)
        {
            var tmp = new char[_programs.Length];
            var index = tmp.Length - x;
            var j = 0;
            for (int i = index; i < tmp.Length; i++)
            {
                tmp[j] = _programs[i];
                j++;
            }
            for (int i = 0; i < index; i++)
            {
                tmp[j] = _programs[i];
                j++;
            }

            _programs = tmp;
        }

        private void Exchange(int a, int b)
        {
            (_programs[a], _programs[b]) = (_programs[b], _programs[a]);
        }

        private void Partner(char a, char b)
        {
            Exchange(CharPosition(a), CharPosition(b));
        }

        public char[] Programs() { return _programs; }

        public void Dance()
        {
            foreach (var move in _moves)
            {
                var dance = move[0];
                var details = move.Substring(1);
                    
                switch (dance)
                {
                    case 's':
                        Spin(Convert.ToInt32(details));
                        break;
                    case 'x':
                        var positions = details.Split("/");
                        Exchange(Convert.ToInt32(positions[0]), Convert.ToInt32(positions[1]));
                        break;
                    case 'p':
                        var programs = details.Split("/");
                        Partner(programs[0][0], programs[1][0]);
                        break;
                    default:
                        throw new Exception($"Invalid dance move : {move[0]}");
                }
            }
        }
    }
}