using adventofcode.common;

namespace adventofcode.year2017;

public class Day08 : Solution
{
    private string[] _input;
    
    public Day08(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var cpu = new CPU(_input);
        cpu.Run();
        
        return Convert.ToString(cpu.Registers().Aggregate(0, (acc, kv) => kv.Value > acc ? kv.Value : acc));
    }

    public override string PartTwo()
    {
        var cpu = new CPU(_input);
        cpu.Run();
        
        return Convert.ToString(cpu.Largest());
    }

    private class CPU
    {
        private List<string> _instructions;
        private Dictionary<string, int> _registers;
        private int _largest;
        
        public CPU(string[] instructions)
        {
            _instructions = new List<string>(instructions);
            _registers = new Dictionary<string, int>();
            _largest = 0;
        }

        private void InitializeRegister(string register)
        {
            if (!_registers.ContainsKey(register))
            {
                _registers.Add(register, 0);
            }
        }

        private bool EvaluateCondition(string register, string condition, int value)
        {
            switch (condition)
            {
                case "<":
                    return _registers[register] < value;
                case ">":
                    return _registers[register] > value;
                case "<=":
                    return _registers[register] <= value;
                case ">=":
                    return _registers[register] >= value;
                case "==":
                    return _registers[register] == value;
                case "!=":
                    return _registers[register] != value;
                default:
                    throw new Exception($"Invalid condition : {condition}");
            }
        }

        public Dictionary<string, int> Registers()
        {
            return _registers;
        }

        public int Largest()
        {
            return _largest;
        }

        public void Run()
        {
            var index = 0;
            while (index < _instructions.Count)
            {
                var instruction = _instructions[index].Split(" ");
                var targetRegister = instruction[0];
                var operation = instruction[1];
                var targetValue = Convert.ToInt32(instruction[2]);
                var conditionRegister = instruction[4];
                var condition = instruction[5];
                var conditionValue = Convert.ToInt32(instruction[6]);
                
                InitializeRegister(targetRegister);
                InitializeRegister(conditionRegister);

                switch (operation)
                {
                    case "inc":
                        _registers[targetRegister] += EvaluateCondition(conditionRegister, condition, conditionValue) ? targetValue : 0;
                        break;
                    case "dec":
                        _registers[targetRegister] -= EvaluateCondition(conditionRegister, condition, conditionValue) ? targetValue : 0;
                        break;
                    default:
                        throw new Exception($"Invalid operation : {operation}");
                }

                _largest = _registers[targetRegister] > _largest ? _registers[targetRegister] : _largest;

                index++;
            }
        }
    }
}