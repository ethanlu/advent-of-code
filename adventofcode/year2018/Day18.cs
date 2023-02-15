using adventofcode.common;
using adventofcode.common.util;

namespace adventofcode.year2018;

public class Day18 : Solution
{
    private string[] _input;
    
    public Day18(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var lc = new LumberCollection(_input);
        foreach (var i in Enumerable.Range(0, 10))
        {
            lc.Step();
        }
        lc.Show();

        return Convert.ToString(lc.Count('|') * lc.Count('#'));
    }

    public override string PartTwo()
    {
        var lc = new LumberCollection(_input);
        var cache = new Dictionary<string, long>();

        var i = 0L;
        while (i < 1000000000L)
        {
            lc.Step();
            var hash = lc.Hash();
            i++;

            if (!cache.ContainsKey(hash))
            {
                cache.Add(hash, i);
            }
            else
            {   // cycle detected...skip ahead
                var diff = i - cache[hash];
                var skipAhead = 1000000000L - ((1000000000L - i) % diff);

                if (skipAhead > i)
                {
                    Console.WriteLine($"Cycle encountered at minute {i} and can skip forward to minute to {skipAhead}");
                    i = skipAhead;
                }
            }
        }
        lc.Show();

        return Convert.ToString(lc.Count('|') * lc.Count('#'));
    }

    private class LumberCollection
    {
        private char[,] _area;
        private int _size;

        public LumberCollection(string[] input)
        {
            _size = input.Length;
            _area = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    _area[x, y] = input[y][x];
                }
            }
        }

        public int Count(char type)
        {
            var count = 0;
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    count += _area[x, y] == type ? 1 : 0;
                }
            }

            return count;
        }

        public string Hash()
        {
            var hash = "";
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    hash += _area[x, y];
                }
            }

            return hash;
        }

        public void Show()
        {
            Draw<char>.ShowGrid(_area);
        }

        public void Step()
        {
            var area = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    var neighbors = new List<char>()
                    {
                        {(x - 1) >= 0 && (y - 1) >= 0 ? _area[x - 1, y - 1] : '?'}, {(y - 1) >= 0 ? _area[x, y - 1] : '?'}, {(x + 1) < _size && (y - 1) >= 0 ? _area[x + 1, y - 1] : '?'}, 
                        {(x - 1) >= 0 ? _area[x - 1, y] : '?'}, {(x + 1) < _size ? _area[x + 1, y] : '?'},
                        {(x - 1) >= 0 && (y + 1) < _size ? _area[x - 1, y + 1] : '?'}, {(y + 1) < _size ? _area[x, y + 1] : '?'}, {(x + 1) < _size && (y + 1) < _size ? _area[x + 1, y + 1] : '?'}, 
                    };
                    
                    switch (_area[x, y])
                    {
                        case '.':
                            area[x, y] =neighbors.Aggregate(0, (acc, c) => acc + (c == '|' ? 1 : 0)) >= 3 ? '|' : _area[x, y];
                            break;
                        case '|':
                            area[x, y] = neighbors.Aggregate(0, (acc, c) => acc + (c == '#' ? 1 : 0)) >= 3 ? '#' : _area[x, y];
                            break;
                        case '#':
                            area[x, y] = neighbors.Aggregate(0, (acc, c) => acc + (c == '#' ? 1 : 0)) >= 1 && neighbors.Aggregate(0, (acc, c) => acc + (c == '|' ? 1 : 0)) >= 1 ? _area[x, y] : '.';
                            break;
                        default:
                            throw new Exception($"Invalid grid state : {_area[x, y]}");
                    }
                }
            }
            _area = area;
        }
    }
}