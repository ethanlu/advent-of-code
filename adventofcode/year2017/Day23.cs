using adventofcode.common;

namespace adventofcode.year2017;

public class Day23 : Solution
{
    private string[] _input;
    
    public Day23(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var cp = new Coprocessor(_input);
        cp.Run(false);
        return Convert.ToString(cp.InstructionCount("mul"));
    }

    public override string PartTwo()
    {
        var cp = new Coprocessor(_input);
        cp.SetRegister("a", 1L);
        cp.Optimize(true);
        cp.Run(true);
        return Convert.ToString(cp.Register("h"));
    }
    
    private class Coprocessor
    {
        private List<string> _instructions;
        private Dictionary<string, long> _registers;
        private Dictionary<string, long> _instructionCount;
        private bool _optimize;

        public Coprocessor(string[] instructions)
        {
            _optimize = false;
            _instructions = new List<string>(instructions);
            _instructionCount = new Dictionary<string, long>()
            {
                {"set", 0}, {"sub", 0}, {"mul", 0}, {"jnz", 0}
            };
            _registers = new Dictionary<string, long>()
            {
                {"a", 0}, {"b", 0}, {"c", 0}, {"d", 0}, {"e", 0}, {"f", 0}, {"g", 0}, {"h", 0}
            };
        }

        private long Value(string value)
        {
            return _registers.ContainsKey(value) ? _registers[value] : Convert.ToInt32(value);
        }

        public void Optimize(bool optimize) { _optimize = optimize; }

        public long Register(string register) { return _registers[register]; }

        public void SetRegister(string register, long value) { _registers[register] = value; }

        public long InstructionCount(string instruction) { return _instructionCount[instruction]; }

        public void Run(bool verbose)
        {
            var index = 0L;
            while (index >= 0L && index < _instructions.Count)
            {
                if (_optimize)
                { 
                    //optimization
                    var lookAhead = Enumerable.Range((int) index, (int) Math.Min(_instructions.Count - index, 16)).Select(i => _instructions[i]).ToList();
                    switch (lookAhead)
                    {
                        case ["set f 1", "set d 2", "set e 2", "set g d", "mul g e", "sub g b", "jnz g 2", "set f 0", "sub e -1", "set g e", "sub g b", "jnz g -8", "sub d -1", "set g d", "sub g b", "jnz g -13"]:
                            // instruction sequence sets f to 0 if b = d * e, where d and e are greater than 2. otherwise, set f to 1
                            _registers["f"] = 1;
                            for (var x = 2; x < _registers["b"] / 2; x++)
                            {
                                if (_registers["b"] % x == 0)
                                {
                                    _registers["f"] = 0;
                                    break;
                                }
                            }
                            _registers["d"] = _registers["b"];
                            _registers["e"] = _registers["b"];
                            _registers["g"] = 0;
                            if (verbose) { Console.WriteLine($"{index + 1}: [{_instructions[(int) index]}] {string.Join(", ", _registers.Select(kv => $"{kv.Key}: {kv.Value}"))} optimized 16 instructions"); }
                            index += 16;
                            break;
                    }
                }

                var parts = _instructions[(int) index].Split(" ");
                switch (parts[0])
                {
                    case "set":
                        _registers[parts[1]] = Value(parts[2]);
                        if (verbose) { Console.WriteLine($"{index + 1}: [{_instructions[(int) index]}] {string.Join(", ", _registers.Select(kv => $"{kv.Key}: {kv.Value}"))}"); }
                        _instructionCount["set"]++;
                        break;
                    case "sub":
                        _registers[parts[1]] -= Value(parts[2]);
                        if (verbose) { Console.WriteLine($"{index + 1}: [{_instructions[(int) index]}] {string.Join(", ", _registers.Select(kv => $"{kv.Key}: {kv.Value}"))}"); }
                        _instructionCount["sub"]++;
                        break;
                    case "mul":
                        _registers[parts[1]] *= Value(parts[2]);
                        if (verbose) { Console.WriteLine($"{index + 1}: [{_instructions[(int) index]}] {string.Join(", ", _registers.Select(kv => $"{kv.Key}: {kv.Value}"))}"); }
                        _instructionCount["mul"]++;
                        break;
                    case "jnz":
                        if (verbose) { Console.WriteLine($"{index + 1}: [{_instructions[(int) index]}] {string.Join(", ", _registers.Select(kv => $"{kv.Key}: {kv.Value}"))}"); }
                        index += Value(parts[1]) != 0 ? Value(parts[2]) : 1;
                        _instructionCount["jnz"]++;
                        continue;
                    default:
                        throw new Exception($"Invalid command : {parts[0]}");
                }
                index += 1;
            }
        }
    }
}