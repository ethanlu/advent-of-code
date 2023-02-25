using adventofcode.common;
using adventofcode.common.util;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day19 : Solution
{
    private string[] _input;

    public Day19(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var cpu = new PointerCPU(_input);
        cpu.Run(true);

        return Convert.ToString(cpu.Registers()[0]);
    }

    public override string PartTwo()
    {
        var cpu = new PointerCPU(_input);
        cpu.Registers(new List<int>() {1, 0, 0, 0, 0, 0});
        cpu.Run(true);
        
        return Convert.ToString(cpu.Registers()[0]);
    }

    private class PointerCPU : Day16.NumericCPU
    {
        private List<string> _instructions;
        private int _instructionRegister;

        public PointerCPU(string[] instructions) : base (6)
        {
            _instructionRegister = Convert.ToInt32(Regex.Match(instructions[0], @"#ip (\d+)").Groups[1].Value);
            _instructions = new List<string>();
            for (int i = 1; i < instructions.Length; i++)
            {
                _instructions.Add(instructions[i]);
            }
        }

        public void Run(bool verbose)
        {
            var instructionIndex = _registers[_instructionRegister];
            while (instructionIndex >= 0 && instructionIndex < _instructions.Count)
            {
                if (verbose)
                {
                    Console.Write($"ip={instructionIndex} : [{_registers[0]}, {_registers[1]}, {_registers[2]}, {_registers[3]}, {_registers[4]}, {_registers[5]}] : {_instructions[instructionIndex]}");
                }
                
                //optimization
                var lookAhead = Enumerable.Range(instructionIndex, Math.Min(_instructions.Count - instructionIndex, 13)).Select(i => _instructions[i]).ToList();
                var optimized = "";
                switch (lookAhead)
                { 
                    case ["mulr 5 2 1", "eqrr 1 4 1", "addr 1 3 3", "addi 3 1 3", "addr 5 0 0", "addi 2 1 2", "gtrr 2 4 1" ,"addr 3 1 3", "seti 2 5 3", "addi 5 1 5", "gtrr 5 4 1", "addr 1 3 3", "seti 1 2 3"]:
                        // instruction sequence increments register2 and register5 to find when multiplying them together equals register4
                        //      register2 * register5 = register4
                        // whenever they form the factors of register4, the value of register5 is added to register0. so, register0 will be the sum of all factors of register4
                        _registers[2] = _registers[4];
                        _registers[5] = _registers[4];
                        _registers[0] = MathTools.Factors(_registers[4]).Aggregate(0, (acc, n) => acc + n);
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
                
                instructionIndex = _registers[_instructionRegister];
                instructionIndex++;
            }
        }
    }
}