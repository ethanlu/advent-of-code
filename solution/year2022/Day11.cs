using System;
using System.Collections.Generic;

namespace solution.year2022
{
    public class Day11 : Solution
    {
        private string[] input;

        public Day11(string year, string day) : base(year, day)
        {
            input = LoadInputAsLines();
        }

        public override string PartOne()
        {
            Func<long, long> decreaseWorry = x => x / 3L;
            var game = new Game(input, decreaseWorry);
            
            game.Play(20);
            
            List<int> inspections = new List<int>();
            foreach (Monkey m in game.Monkeys())
            {
                inspections.Add(m.InspectionCount());
            }
            inspections.Sort();

            var total = Convert.ToInt64(inspections[inspections.Count - 1]) * Convert.ToInt64(inspections[inspections.Count - 2]);
            return Convert.ToString(total);
        }

        public override string PartTwo()
        {
            var commonDenominator = 1L;
            for (int i = 0; i < input.Length; i += 7)
            {
                commonDenominator *= Convert.ToInt64(input[i + 3].Trim().Substring("Test: divisible by ".Length));
            }

            Func<long, long> decreaseWorry = x => x % commonDenominator;
            var game = new Game(input, decreaseWorry);
            
            game.Play(10000);
            List<int> inspections = new List<int>();
            foreach (Monkey m in game.Monkeys())
            {
                inspections.Add(m.InspectionCount());
            }
            inspections.Sort();

            var total = Convert.ToInt64(inspections[inspections.Count - 1]) * Convert.ToInt64(inspections[inspections.Count - 2]);
            return Convert.ToString(total);
        }
    }

    internal class Game
    {
        private List<Monkey> _monkeys;

        public Game(string[] input, Func<long, long> decreaseWorry)
        {
            _monkeys = new List<Monkey>();
            for (int i = 0; i < input.Length; i += 7)
            {
                var items = input[i + 1].Trim().Substring("Starting items: ".Length).Split(',');
                var operation = input[i + 2].Trim().Substring("Operation: new = old ".Length).Split(' ');
                var divisor = input[i + 3].Trim().Substring("Test: divisible by ".Length);
                var targetTrue = input[i + 4].Trim().Substring("If true: throw to monkey ".Length);
                var targetFalse = input[i + 5].Trim().Substring("If false: throw to monkey ".Length);
                
                _monkeys.Add(new Monkey(
                    Array.ConvertAll(items, long.Parse), 
                    operation[0],  
                    operation[1],
                    Convert.ToInt32(divisor),
                    Convert.ToInt32(targetTrue),
                    Convert.ToInt32(targetFalse),
                    decreaseWorry
                ));
            }
        }

        public List<Monkey> Monkeys()
        {
            return _monkeys;
        }

        public void Play(int rounds)
        {
            for (int r = 0; r < rounds; r++)
            {
                foreach (Monkey m in _monkeys)
                {
                    while (m.HasItems())
                    {
                        var item = m.Inspect();
                        item = m.IncreaseWorry(item);
                        item = m.DecreaseWorry(item);
                        _monkeys[m.ThrowTo(item)].Catch(item);
                    }
                }
            }
        }
    }

    internal class Monkey
    {
        private Queue<long> _items;
        private string _operation;
        private int _operand;
        private int _divisor;
        private int _targetTrue;
        private int _targetFalse;
        private Func<long, long> _decreaseWorry;
        private int _inspectionCount;

        public Monkey(long[] items, string operation, string operand, int divisor, int targetTrue, int targetFalse, Func<long, long> decreaseWorry)
        {
            _items = new Queue<long>(items);
            _operation = operation == "*" && operand == "old" ? "sq" : operation;
            _operand = _operation != "sq" ? Convert.ToInt32(operand) : 0;
            _divisor = divisor;
            _targetTrue = targetTrue;
            _targetFalse = targetFalse;
            _inspectionCount = 0;
            _decreaseWorry = decreaseWorry;
        }

        public int InspectionCount()
        {
            return _inspectionCount;
        }

        public bool HasItems()
        {
            return _items.Count > 0;
        }

        public long Inspect()
        {
            _inspectionCount++;
            return _items.Dequeue();
        }

        public void Catch(long item)
        {
            _items.Enqueue(item);
        }

        public int ThrowTo(long item)
        {
            return item % _divisor == 0L ? _targetTrue : _targetFalse;
        }

        public long DecreaseWorry(long item)
        {
            return _decreaseWorry(item);
        }

        public long IncreaseWorry(long item)
        {
            switch (_operation)
            {
                case "+":
                    return item + _operand;
                case "*":
                    return item * _operand;
                case "sq":
                    return item * item;
                default:
                    throw new Exception($"Unrecognized operation : {_operation}");
            }
        }
    }
}