using adventofcode.common;
using System.Text.RegularExpressions;

namespace adventofcode.year2017;

public class Day18 : Solution
{
    private string[] _input;
    
    public Day18(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var cpu = new DuetCPU(_input, 0, null, null, false);
        cpu.Run();
        return Convert.ToString(cpu.Recover());
    }

    public override string PartTwo()
    {
        var queue1 = new QueueSemaphore();
        var queue2 = new QueueSemaphore();

        var cpus = new List<DuetCPU>()
        {
            new DuetCPU(_input, 0, queue2, queue1,false),
            new DuetCPU(_input, 1, queue1, queue2, false)
        };

        foreach (var cpu in cpus)
        {
            var thread = new Thread(cpu.Run);
            thread.Start();
            thread.Join(5000);
        }

        return Convert.ToString(cpus[1].SendCount());
    }

    private class QueueSemaphore
    {
        private Semaphore _lock;
        private Queue<long> _data;
        
        public QueueSemaphore()
        {
            _lock = new Semaphore(1, 1);
            _data = new Queue<long>();
        }

        public void Enqueue(long value)
        {
            _lock.WaitOne();
            _data.Enqueue(value);
            _lock.Release();
        }

        public int Count()
        {
            _lock.WaitOne();
            var tmp = _data.Count;
            _lock.Release();

            return tmp;
        }

        public long Dequeue()
        {
            _lock.WaitOne();
            var tmp = _data.Dequeue();
            _lock.Release();

            return tmp;
        }
    }

    private class DuetCPU
    {
        private int _id;
        private List<string> _instructions;
        private Dictionary<string, long> _registers;
        private long _sound;
        private long _recover;
        private bool _verbose;
        private QueueSemaphore? _sendQueue;
        private QueueSemaphore? _receiveQueue;
        private long _sendCount;

        public DuetCPU(string[] instructions, int initialValue, QueueSemaphore? sendQueue, QueueSemaphore? receiveQueue, bool verbose)
        {
            _id = initialValue;
            _instructions = new List<string>(instructions);
            _registers = new Dictionary<string, long>();
            _sound = 0;
            _recover = 0;
            _sendQueue = sendQueue;
            _receiveQueue = receiveQueue;
            _verbose = verbose;
            _sendCount = 0;

            foreach (var instruction in _instructions)
            {
                var register = instruction.Split(" ")[1];

                if (Regex.Match(register, @"^[a-z]$").Success && !_registers.ContainsKey(register))
                {
                    _registers.Add(register, initialValue);
                }
            }
        }

        private long Value(string value)
        {
            return _registers.ContainsKey(value) ? _registers[value] : Convert.ToInt32(value);
        }

        public long Recover() { return _recover; }

        public long SendCount() { return _sendCount; }

        public void Run()
        {
            var index = 0L;
            while (index >= 0L && index < _instructions.Count)
            {
                if (_verbose)
                {
                    Console.WriteLine($"[{_id}] : {index + 1}: [{_instructions[(int) index]}] {string.Join(", ", _registers.Select(kv => $"{kv.Key}: {kv.Value}"))}");
                }

                var parts = _instructions[(int) index].Split(" ");
                switch (parts[0])
                {
                    case "snd":
                        if (_sendQueue is null)
                        {
                            _sound = Value(parts[1]);
                        }
                        else
                        {
                            _sendQueue.Enqueue(Value(parts[1]));
                            _sendCount++;
                        }
                        break;
                    case "set":
                        _registers[parts[1]] = Value(parts[2]);
                        break;
                    case "add":
                        _registers[parts[1]] += Value(parts[2]);
                        break;
                    case "mul":
                        _registers[parts[1]] *= Value(parts[2]);
                        break;
                    case "mod":
                        _registers[parts[1]] %= Value(parts[2]);
                        break;
                    case "rcv":
                        if (_receiveQueue is null)
                        {
                            if (Value(parts[1]) != 0)
                            {
                                _recover = _sound;
                                return;
                            }
                        }
                        else
                        {
                            var attempt = 0;
                            while (_receiveQueue.Count() == 0)
                            {
                                attempt++;
                                Thread.Sleep(50);

                                if (attempt > 100)
                                {
                                    return;
                                }
                            }
                            _registers[parts[1]] = _receiveQueue.Dequeue();
                        }
                        break;
                    case "jgz":
                        index += Value(parts[1]) > 0 ? Value(parts[2]) : 1;
                        continue;
                    default:
                        throw new Exception($"Invalid command : {parts[0]}");
                }
                index += 1;
            }
        }
    }
}