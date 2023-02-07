using adventofcode.common;

namespace adventofcode.year2018;

public class Day12 : Solution
{
    private string _initial;
    private List<string> _rules;
    
    public Day12(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();
        _initial = input[0].Replace("initial state: ", "");

        _rules = new List<string>();
        for (int i = 2; i < input.Length; i++)
        {
            _rules.Add(input[i]);
        }
    }

    public override string PartOne()
    {
        var gp = new GeothermalPots(_initial, _rules);
        gp.Grow(20L);
        gp.Show();
        
        return Convert.ToString(gp.Pots().Aggregate(0L, (acc, kv) => acc + (kv.Value == '#' ? kv.Key : 0)));
    }

    public override string PartTwo()
    {
        var gp = new GeothermalPots(_initial, _rules);
        gp.Grow(50000000000L);
        gp.Show();
        
        return Convert.ToString(gp.Pots().Aggregate(0L, (acc, kv) => acc + (kv.Value == '#' ? kv.Key : 0)));
    }

    private class GeothermalPots
    {
        private Dictionary<long, char> _pots;
        private Dictionary<string, char> _rules;
        private Dictionary<string, (long, long)> _cache;
        private long _minPot;
        private long _maxPot;

        public GeothermalPots(string initial, List<string> rules)
        {
            _pots = new Dictionary<long, char>();
            _rules = new Dictionary<string, char>();
            _cache = new Dictionary<string, (long, long)>();

            _minPot = initial.Length;
            _maxPot = 0;
            for (int i = 0; i < initial.Length; i++)
            {
                _pots.Add(i, initial[i]);
                if (initial[i] == '#')
                {
                    _minPot = _minPot > i ? i : _minPot;
                    _maxPot = _maxPot < i ? i : _maxPot;
                }
            }
            _pots.Add(-1, '.');
            _pots.Add(-2, '.');
            _pots.Add(-3, '.');
            _pots.Add(-4, '.');
            _pots.Add(initial.Length, '.');
            _pots.Add(initial.Length + 1, '.');
            _pots.Add(initial.Length + 2, '.');
            _pots.Add(initial.Length + 3, '.');

            foreach (var rule in rules)
            {
                var tmp = rule.Split(" => ");
                _rules.Add(tmp[0], tmp[1][0]);
            }
        }
        
        public Dictionary<long, char> Pots() { return _pots; }

        public void Show()
        {
            var keys = _pots.Keys.ToList();
            keys.Sort();
            Console.WriteLine($"{MinPot()} : {string.Join(string.Empty, keys.Select(k => _pots[k]))} : {MaxPot()}");
        }

        public long MinPot() { return _minPot; }
        public long MaxPot() { return _maxPot; }

        public void Grow(long generations)
        {
            var g = 0L;
            while (g < generations)
            {
                g++;

                var next = new Dictionary<long, char>();
                foreach (var kv in _pots)
                {
                    var state = new List<char>();
                    state.Add(_pots.ContainsKey(kv.Key - 2) ? _pots[kv.Key - 2] : '.');
                    state.Add(_pots.ContainsKey(kv.Key - 1) ? _pots[kv.Key - 1] : '.');
                    state.Add(kv.Value);
                    state.Add(_pots.ContainsKey(kv.Key + 1) ? _pots[kv.Key + 1] : '.');
                    state.Add(_pots.ContainsKey(kv.Key + 2) ? _pots[kv.Key + 2] : '.');

                    var key = string.Join(string.Empty, state);
                    var pot = _rules.ContainsKey(key) ? _rules[key] : '.';
                    next.Add(kv.Key, pot);

                    if (!_pots.ContainsKey(kv.Key - 2) && !next.ContainsKey(kv.Key - 2)) { next.Add(kv.Key - 2, '.'); }
                    if (!_pots.ContainsKey(kv.Key - 1) && !next.ContainsKey(kv.Key - 1)) { next.Add(kv.Key - 1, '.'); }
                    if (!_pots.ContainsKey(kv.Key + 1) && !next.ContainsKey(kv.Key + 1)) { next.Add(kv.Key + 1, '.'); }
                    if (!_pots.ContainsKey(kv.Key + 2) && !next.ContainsKey(kv.Key + 2)) { next.Add(kv.Key + 2, '.'); }
                }

                _minPot = next.Aggregate(next.Last().Key, (acc, kv) => kv.Value == '#' && acc > kv.Key ? kv.Key : acc);
                _maxPot = next.Aggregate(next.First().Key, (acc, kv) => kv.Value == '#' && acc < kv.Key ? kv.Key : acc);

                _pots = new Dictionary<long, char>();
                for (long i = _minPot - 4; i <= _maxPot + 4; i++)
                {
                    _pots.Add(i, next[i]);
                }

                var hash = $"{string.Join(string.Empty, _pots.Values)}";
                if (_cache.ContainsKey(hash))
                {
                    var (min, generation) = _cache[hash];
                    var genSkip = generations - generations % g;
                
                    var offset = (_minPot - min) * (genSkip - g);
                    Console.WriteLine($"Cycle detected at generation {generation} and skipping to generation {genSkip} and offsetting {offset} pots");
                    var skipped = new Dictionary<long, char>();
                    foreach (var kv in _pots)
                    {
                        skipped.Add(kv.Key + offset, kv.Value);
                    }
                    _pots = skipped;
                    _minPot += offset;
                    _maxPot += offset;
                    g = genSkip;
                }
                else
                {
                    _cache.Add(hash, (_minPot, g));
                    Console.WriteLine($"generation {g} : {_minPot} : {hash}");
                }
            }
        }
    }
}