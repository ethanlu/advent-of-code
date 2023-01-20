using adventofcode.common;

namespace adventofcode.year2017;

public class Day06 : Solution
{
    private string _input;
    
    public Day06(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var mr = new MemoryRepair(_input);
        var cycles = mr.Reallocate();

        return Convert.ToString(cycles);
    }

    public override string PartTwo()
    {
        var mr = new MemoryRepair(_input);
        mr.Reallocate();
        var cycles = mr.Reallocate();

        return Convert.ToString(cycles);
    }

    internal class MemoryRepair
    {
        private List<int> _memoryBanks;

        public MemoryRepair(string data)
        {
            _memoryBanks = data.Split("\t").Select(x => Convert.ToInt32(x)).ToList();
        }

        private string MemoryHash()
        {
            return string.Join(".", _memoryBanks);
        }

        public int Reallocate()
        {
            var cycles = 0;
            var hash = MemoryHash();
            var configurations = new HashSet<string>();

            while (!configurations.Contains(hash))
            {
                configurations.Add(hash);

                var (reallocationIndex, blocksToReallocate) = _memoryBanks.Select((x, i) => (i, x)).Aggregate((0, 0), (acc, kv) => acc.Item2 < kv.x ? (kv.i, kv.x) : acc);

                _memoryBanks[reallocationIndex] = 0;
                foreach (var i in Enumerable.Range(1, blocksToReallocate))
                {
                    _memoryBanks[(reallocationIndex + i) % _memoryBanks.Count]++;
                }

                
                hash = MemoryHash();
                cycles++;
            }

            return cycles;
        }
    }
}