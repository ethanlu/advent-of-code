using adventofcode.common;

namespace adventofcode.year2017;

public class Day10 : Solution
{
    private string _input;
    
    public Day10(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var knothash = new KnotHash(_input.Split(",").Select(x => Convert.ToInt32(x)).ToArray(), 256);
        
        return Convert.ToString(knothash.Round());
    }

    public override string PartTwo()
    {
        var knothash = new KnotHash(_input, 256);

        return Convert.ToString(knothash.GenerateHash());
    }

    internal class KnotHash
    {
        private List<int> _lengths;
        private int[] _data;
        private int _position;
        private int _skip;
        
        public KnotHash(int[] lengths, int marks)
        {
            _lengths = new List<int>(lengths);
            _data = new int[marks];
            _position = 0;
            _skip = 0;

            for (int i = 0; i < marks; i++)
            {
                _data[i] = i;
            }
        }

        public KnotHash(string input, int marks)
        {
            _lengths = new List<int>(input.ToCharArray().Select(x => (int) x).Concat(new List<int>(){17, 31, 73, 47, 23}).ToArray());
            _data = new int[marks];
            _position = 0;
            _skip = 0;

            for (int i = 0; i < marks; i++)
            {
                _data[i] = i;
            }
        }

        private void Reverse(int start, int length)
        {
            var end = start + length - 1 < _data.Length ? start + length - 1: (start + length - 1) % _data.Length;

            for (int i = 0; i < length; i += 2)
            {
                (_data[start], _data[end]) = (_data[end], _data[start]);

                start = start + 1 >= _data.Length ? 0 : start + 1;
                end = end - 1 < 0 ? _data.Length - 1 : end - 1;
            }
        }

        public int Round()
        {
            foreach (var length in _lengths)
            {
                if (length > _data.Length)
                {
                    continue;
                }

                Reverse(_position, length);
                _position = _position + _skip + length < _data.Length ? _position + _skip + length : (_position + _skip + length) % _data.Length;
                _skip++;
            }
            
            return _data[0] * _data[1];
        }

        public string GenerateHash()
        {
            foreach (var round in Enumerable.Range(1, 64))
            {
                Round();
            }

            var denseHash = new int[_data.Length / 16];
            for (int i = 0; i < _data.Length; i += 16)
            {
                denseHash[i / 16] = Enumerable.Range(i + 1, 15).Select(index => _data[index]).Aggregate(_data[i], (acc, n) => acc ^ n);
            }

            return denseHash.Aggregate("", (acc, n) => acc + n.ToString("x2"));
        }
    }
}