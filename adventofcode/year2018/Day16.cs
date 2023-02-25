using System.Collections.Immutable;
using adventofcode.common;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day16 : Solution
{
    private List<Sample> _samples;
    private List<List<int>> _instructions;
    
    public Day16(string year, string day) : base(year, day)
    {
        _instructions = new List<List<int>>();
        var emptyLine = 0;
        var samples = new List<string>();
        foreach (var line in LoadInputAsLines())
        {
            if (line == "")
            {
                emptyLine++;
                continue;
            }

            if (emptyLine <= 1)
            {
                samples.Add(line);
                emptyLine = 0;
            }
            else
            {
                var instruction = line.Split(" ");
                _instructions.Add(new List<int>(){ Convert.ToInt32(instruction[0]), Convert.ToInt32(instruction[1]), Convert.ToInt32(instruction[2]), Convert.ToInt32(instruction[3]) });
            }
        }
        
        _samples = new List<Sample>();
        for (int i = 0; i < samples.Count; i += 3)
        {
            var before = Regex.Match(samples[i], @"Before: \[(\d+), (\d+), (\d+), (\d+)\]");
            var instruction = samples[i + 1].Split(" ");
            var after = Regex.Match(samples[i + 2], @"After:  \[(\d+), (\d+), (\d+), (\d+)\]");
            

            _samples.Add(new Sample(
                new List<int>(){ Convert.ToInt32(before.Groups[1].Value), Convert.ToInt32(before.Groups[2].Value), Convert.ToInt32(before.Groups[3].Value), Convert.ToInt32(before.Groups[4].Value) },
                new List<int>(){ Convert.ToInt32(after.Groups[1].Value), Convert.ToInt32(after.Groups[2].Value), Convert.ToInt32(after.Groups[3].Value), Convert.ToInt32(after.Groups[4].Value) },
                new List<int>(){ Convert.ToInt32(instruction[0]), Convert.ToInt32(instruction[1]), Convert.ToInt32(instruction[2]), Convert.ToInt32(instruction[3]) }
            ));
        }

    }

    public override string PartOne()
    {
        var cpu = new NumericCPU(4);
        var commands = cpu.Commands();

        var sampleCount = 0;
        foreach (var sample in _samples)
        {
            var candidateCount = 0;
            foreach (var command in commands)
            {
                cpu.Registers(sample.Before());
                cpu.Execute(command, sample.Instruction()[1], sample.Instruction()[2], sample.Instruction()[3]);
                candidateCount += cpu.Registers().SequenceEqual(sample.After()) ? 1 : 0;
            }
            sampleCount += candidateCount >= 3 ? 1 : 0;
        }

        return Convert.ToString(sampleCount);
    }

    public override string PartTwo()
    {
        var cpu = new NumericCPU(4);
        var commands = cpu.Commands();
        
        var candidates = new Dictionary<int, HashSet<string>>();
        foreach (var sample in _samples)
        {
            var commandNumber = sample.Instruction()[0];
            var candidateCommands = new HashSet<string>();
            foreach (var command in commands)
            {
                cpu.Registers(sample.Before());
                cpu.Execute(command, sample.Instruction()[1], sample.Instruction()[2], sample.Instruction()[3]);

                if (cpu.Registers().SequenceEqual(sample.After()))
                {
                    candidateCommands.Add(command);
                }
            }
            if (candidateCommands.Count > 0)
            {
                if (!candidates.ContainsKey(commandNumber))
                {
                    candidates.Add(commandNumber, candidateCommands);
                }
                else
                {
                    candidates[commandNumber].IntersectWith(candidateCommands);
                }
            }
        }

        var commandMap = new Dictionary<int, string>();
        while (commandMap.Keys.Count != cpu.Commands().Count)
        {   // candidates should always have one op code that only maps to a single command....
            var kv = candidates.Where(kv => kv.Value.Count == 1).ToList().First();
            commandMap[kv.Key] = kv.Value.First();

            // remove this deduced command from remaining to find the next singled out command
            candidates.Remove(kv.Key);
            foreach (var candidate in candidates)
            {
                candidate.Value.Remove(kv.Value.First());
            }
        }

        cpu.Registers(new List<int>(){0, 0, 0, 0});
        foreach (var instruction in _instructions)
        {
            cpu.Execute(commandMap[instruction[0]], instruction[1], instruction[2], instruction[3]);
        }
        
        return Convert.ToString(cpu.Registers()[0]);
    }
    
    private class Sample
    {
        private List<int> _before;
        private List<int> _after;
        private List<int> _instruction;
        
        public Sample(List<int> before, List<int> after, List<int> instruction)
        {
            _before = before;
            _after = after;
            _instruction = instruction;
        }

        public List<int> Before() { return _before; }
        public List<int> After() { return _after; }
        public List<int> Instruction() { return _instruction; }
    }

    internal class NumericCPU
    {
        protected List<int> _registers;

        public NumericCPU(int numRegisters)
        {
            _registers = new List<int>();
            foreach (var i in Enumerable.Range(1, numRegisters))
            {
                _registers.Add(0);
            }
        }

        public ImmutableList<string> Commands()
        {
            return (new List<string>(){"addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"}).ToImmutableList();
        }

        public List<int> Registers() { return _registers; }
        public void Registers(List<int> registers) { _registers = new List<int>(registers); }

        public void Execute(string command, int a, int b, int c)
        {
            switch (command)
            {
                case "addr":
                    _registers[c] = _registers[a] + _registers[b];
                    break;
                case "addi":
                    _registers[c] = _registers[a] + b;
                    break;
                case "mulr":
                    _registers[c] = _registers[a] * _registers[b];
                    break;
                case "muli":
                    _registers[c] = _registers[a] * b;
                    break;
                case "banr":
                    _registers[c] = _registers[a] & _registers[b];
                    break;
                case "bani":
                    _registers[c] = _registers[a] & b;
                    break;
                case "borr":
                    _registers[c] = _registers[a] | _registers[b];
                    break;
                case "bori":
                    _registers[c] = _registers[a] | b;
                    break;
                case "setr":
                    _registers[c] = _registers[a];
                    break;
                case "seti":
                    _registers[c] = a;
                    break;
                case "gtir":
                    _registers[c] = a > _registers[b] ? 1 : 0;
                    break;
                case "gtri":
                    _registers[c] = _registers[a] > b ? 1 : 0;
                    break;
                case "gtrr":
                    _registers[c] = _registers[a] > _registers[b] ? 1 : 0;
                    break;
                case "eqir":
                    _registers[c] = a == _registers[b] ? 1 : 0;
                    break;
                case "eqri":
                    _registers[c] = _registers[a] == b ? 1 : 0;
                    break;
                case "eqrr":
                    _registers[c] = _registers[a] == _registers[b] ? 1 : 0;
                    break;
            }
        }
    }
}