using adventofcode.common;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day21 : Solution
{
    private string[] _input;
    
    public Day21(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var cpu = new HaltCPU(_input);
        var values = cpu.Run(false);

        return Convert.ToString(values.First());
    }

    public override string PartTwo()
    {
        var cpu = new HaltCPU(_input);
        var values = cpu.Run(false);

        return Convert.ToString(values.Last());
    }
    
    private class HaltCPU : Day16.NumericCPU
    {
        private List<string> _instructions;
        private int _instructionRegister;
        private int _haltRegister;
        private bool _halts;

        public HaltCPU(string[] instructions) : base (6)
        {
            _halts = true;
            
            _instructionRegister = Convert.ToInt32(Regex.Match(instructions[0], @"#ip (\d+)").Groups[1].Value);
            _instructions = new List<string>();
            for (int i = 1; i < instructions.Length; i++)
            {
                _instructions.Add(instructions[i]);
                if (instructions[i].Substring(0, 4) == "eqrr")
                {
                    _haltRegister = Convert.ToInt32(Regex.Match(instructions[i], @"eqrr (\d+) 0 (\d+)").Groups[1].Value);
                }
            }
        }

        public List<int> Run(bool verbose)
        {
            var values = new List<int>();
            var states = new HashSet<int>();
            var instructionIndex = _registers[_instructionRegister];
            
            _halts = true;

            while (instructionIndex >= 0 && instructionIndex < _instructions.Count)
            {
                if (verbose)
                {
                    Console.Write($"ip={instructionIndex} : [{_registers[0]}, {_registers[1]}, {_registers[2]}, {_registers[3]}, {_registers[4]}, {_registers[5]}] : {_instructions[instructionIndex]}");
                }
                
                //optimization
                var optimized = "";
                var lookAhead = Enumerable.Range(instructionIndex, Math.Min(_instructions.Count - instructionIndex, 8)).Select(i => _instructions[i]).ToList();
                switch (lookAhead)
                { 
                    case ["addi 5 1 2", "muli 2 256 2", "gtrr 2 1 2", "addr 2 3 3", "addi 3 1 3", "seti 25 7 3", "addi 5 1 5", "seti 17 1 3"]:
                        _registers[5] = _registers[1] / 256;
                        optimized = "(optimized)";
                        break;
                }
                
                var instruction = _instructions[instructionIndex].Split(" ");
                _registers[_instructionRegister] = instructionIndex;
                Execute(instruction[0], Convert.ToInt32(instruction[1]), Convert.ToInt32(instruction[2]), Convert.ToInt32(instruction[3]));
                
                if (verbose)
                {
                    Console.WriteLine($" --> [{_registers[0]}, {_registers[1]}, {_registers[2]}, {_registers[3]}, {_registers[4]}, {_registers[5]}] {optimized}");
                }
                
                if (instruction[0] == "eqrr")
                {
                    if (states.Contains(_registers[_haltRegister]))
                    {
                        _halts = false;
                        break;
                    }
                    states.Add(_registers[_haltRegister]);
                    values.Add(_registers[_haltRegister]);
                }
                
                instructionIndex = _registers[_instructionRegister];
                instructionIndex++;
            }

            return values;
        }
    }
}