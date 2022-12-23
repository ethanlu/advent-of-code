using System;
using System.Collections.Generic;

namespace solution.year2022
{
    public class Day10 : Solution
    {
        private CPU _cpu;
        
        public Day10(string year, string day) : base(year, day)
        {
            _cpu = new CPU(this.LoadInputAsLines());
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
            var display = _cpu.CRT();

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
    }

    internal enum State
    {
        Fetch = 1,
        Execute = 2,
        End = 3
    }

    internal class CPU
    {
        private State _state;
        private CRT _crt;
        private string[] _instructions;
        private int _instructionIndex;
        private int _instructionCycle;
        private Dictionary<int, int> _peekCycles;
        private int _cycle;
        private int _x;

        public CPU(string[] instructions)
        {
            _instructions = instructions;
            Reset();
        }

        public int X()
        {
            return _x;
        }

        public Dictionary<int, int> PeekCycles()
        {
            return _peekCycles;
        }

        public CRT CRT()
        {
            return _crt;
        }

        public void Reset()
        {
            _crt = new CRT(6, 40);
            _state = State.Fetch;
            _x = 1;
            _cycle = 0;
            _peekCycles = new Dictionary<int, int>();
            _instructionCycle = 0;
            _instructionIndex = -1;
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

    internal class CRT
    {
        private int _rows;
        private int _cols;
        private char[,] _display;

        public CRT(int rows, int cols)
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