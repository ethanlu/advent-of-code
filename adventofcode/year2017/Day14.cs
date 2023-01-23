using adventofcode.common;
using adventofcode.common.graph.search;
using Microsoft.VisualBasic;

namespace adventofcode.year2017;

public class Day14 : Solution
{
    private string _input;
    private List<string> _disk;
    private int _diskSize;
    
    public Day14(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
        _disk = new List<string>(); 
        _diskSize = 128;
        
        for (int i = 0; i < 128; i++)
        {
            var kh = new Day10.KnotHash($"{_input}-{i}", 256);
            _disk.Add(string.Join(
                string.Empty,
                kh.GenerateHash().Select(c => Convert.ToString(Convert.ToInt32(c.ToString(), 16), 2).PadLeft(4, '0')))
            );
        }
    }

    public override string PartOne()
    {
        var usedSpace = _disk.Aggregate(0, (totalUsed, row) => totalUsed + row.Aggregate(0, (used, c) => used + (c == '1' ? 1 : 0)));
        
        return Convert.ToString(usedSpace);
    }

    public override string PartTwo()
    {
        var processed = new HashSet<string>();
        var regions = 0;

        for (int y = 0; y < _disk.Count; y++)
        {
            for (int x = 0; x < _disk[y].Length; x++)
            {
                if (!processed.Contains($"{x},{y}") && _disk[y][x] == '1')
                {
                    var ff = new FloodFill(new RegionSearchState(_disk, x, y, 0, 0, 99999));
                    foreach (RegionSearchState rs in ff.Fill())
                    {
                        processed.Add($"{rs.X()},{rs.Y()}");
                    }
                
                    regions++;
                }
            }
        }

        return Convert.ToString(regions);
    }

    private class RegionSearchState : SearchState
    {
        private List<string> _disk;
        private int _x;
        private int _y;
        
        public RegionSearchState(List<string> disk, int x, int y, int gain, int cost, int maxCost) : base($"{x},{y}", gain, cost, maxCost)
        {
            _disk = disk;
            _x = x;
            _y = y;
        }

        public int X() { return _x; }
        public int Y() { return _y; }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();

            if (_x > 0 && _disk[_y][_x - 1] == '1') { states.Add(new RegionSearchState(_disk, _x - 1, _y, _gain, _cost, _maxCost)); }
            if (_x < _disk[0].Length - 1 && _disk[_y][_x + 1] == '1') { states.Add(new RegionSearchState(_disk, _x + 1, _y, _gain, _cost, _maxCost)); }
            if (_y > 0 && _disk[_y - 1][_x] == '1') { states.Add(new RegionSearchState(_disk, _x, _y - 1, _gain, _cost, _maxCost)); }
            if (_y < _disk.Count - 1 && _disk[_y + 1][_x] == '1') { states.Add(new RegionSearchState(_disk, _x, _y + 1, _gain, _cost, _maxCost)); }

            return states;
        }
    }
}