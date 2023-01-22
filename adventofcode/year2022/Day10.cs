using adventofcode.common;

namespace adventofcode.year2022;

public class Day10 : Solution
{
    private Cpu _cpu;
    
    public Day10(string year, string day) : base(year, day)
    {
        _cpu = new Cpu(this.LoadInputAsLines());
    }

    public override string PartOne()
    {
        _cpu.AddPeekCycle(20);
        _cpu.AddPeekCycle(60);
        _cpu.AddPeekCycle(100);
        _cpu.AddPeekCycle(140);
        _cpu.AddPeekCycle(180);
        _cpu.AddPeekCycle(220);
        _cpu.Run();

        var total = 0;
        foreach (var peekCycle in _cpu.PeekCycles())
        {
            total += peekCycle.Key * peekCycle.Value;
        }
        
        return Convert.ToString(total);
    }

    public override string PartTwo()
    {
        var display = _cpu.Crt();

        for (int r = 0; r < display.Rows(); r++)
        {
            var line = "";
            for (int c = 0; c < display.Cols(); c++)
            {
                line += display.Show(r, c);
            }
            Console.WriteLine(line);
        }

        return Convert.ToString("");
    }
    
    private enum State
    {
        Fetch = 1,
        Execute = 2,
        End = 3
    }

    private class Cpu
    {
        private State _state;
        private Crt _crt;
        private string[] _instructions;
        private int _instructionIndex;
        private int _instructionCycle;
        private Dictionary<int, int> _peekCycles;
        private int _cycle;
        private int _x;

        public Cpu(string[] instructions)
        {
            _instructions = instructions;
            
            _crt = new Crt(6, 40);
            _state = State.Fetch;
            _x = 1;
            _cycle = 0;
            _peekCycles = new Dictionary<int, int>();
            _instructionCycle = 0;
            _instructionIndex = -1;
        }

        public int X()
        {
            return _x;
        }

        public Dictionary<int, int> PeekCycles()
        {
            return _peekCycles;
        }

        public Crt Crt()
        {
            return _crt;
        }

        public void AddPeekCycle(int cycle)
        {
            _peekCycles.Add(cycle, 0);
        }

        public void Run()
        {
            while (_state != State.End)
            {
                _cycle++;

                if (_state == State.Fetch)
                {
                    // fetch next instruction
                    _instructionIndex++;

                    _state = State.Execute;
                    if (_instructionIndex >= _instructions.Length)
                    {
                        _state = State.End;
                        continue;
                    }
                }
                
                if (_peekCycles.ContainsKey(_cycle))
                {
                    _peekCycles[_cycle] = _x;
                }
                
                _crt.Draw(_cycle - 1, _x);

                if (_state == State.Execute)
                {
                    // process instruction
                    var instruction = _instructions[_instructionIndex].Split(' ');
                    switch (instruction[0])
                    {
                        case "noop":
                            // no operation...ready to process next instruction
                            _instructionCycle = 0;
                            _state = State.Fetch;
                            break;
                        case "addx":
                            // check current instruction execution
                            if (_instructionCycle > 0)
                            {
                                _instructionCycle--;

                                if (_instructionCycle == 0)
                                {
                                    _x += Convert.ToInt32(instruction[1]);
                                    _state = State.Fetch;
                                }
                            }
                            else
                            {
                                _instructionCycle = 1;
                            }
                            break;
                        default:
                            throw new Exception($"Unrecognized instruction : {instruction[0]}");
                    }
                }
            }
        }
    }

    private class Crt
    {
        private int _rows;
        private int _cols;
        private char[,] _display;

        public Crt(int rows, int cols)
        {
            _rows = rows;
            _cols = cols;
            _display = new char[_rows, (_cols)];
        }

        public int Rows()
        {
            return _rows;
        }

        public int Cols()
        {
            return _cols;
        }

        public char Show(int row, int col)
        {
            return _display[row, col];
        }

        public void Draw(int index, int position)
        {
            var row = index / _cols;
            var col = index % _cols;
            _display[row, col] = (col >= position - 1 && col <= position + 1) ? '#' : '.';
        }
    }
}