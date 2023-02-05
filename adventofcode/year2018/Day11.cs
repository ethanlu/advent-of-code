using adventofcode.common;

namespace adventofcode.year2018;

public class Day11 : Solution
{
    private string _input;
    
    public Day11(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var fg = new FuelGrid(Convert.ToInt32(_input));
        var (x, y, power) = fg.HighestPower(3);
        return Convert.ToString($"{x},{y}");
    }

    public override string PartTwo()
    {
        var fg = new FuelGrid(Convert.ToInt32(_input));
        
        var highestPower = 0;
        var highestX = 0;
        var highestY = 0;
        var highestSize = 0;
        for (int size = 1; size <= 300; size++)
        {
            var (x, y, power) = fg.HighestPower(size);
            if (power > highestPower)
            {
                highestPower = power;
                highestX = x;
                highestY = y;
                highestSize = size;
                Console.WriteLine($"size {size} with power {power} is current largest");
            }
        }
        
        return Convert.ToString($"{highestX},{highestY},{highestSize}");
    }

    private class FuelGrid
    {
        private Dictionary<(int, int), int> _cells;    
        private int _serial;

        public FuelGrid(int serial)
        {
            _serial = serial;
            _cells = new Dictionary<(int, int), int>();

            for (int y = 1; y <= 300; y++)
            {
                for (int x = 1; x <= 300; x++)
                {
                    //https://en.wikipedia.org/wiki/Summed-area_table
                    var bottomLeft = x > 1 ? _cells[(x - 1, y)] : 0;
                    var upperRight = y > 1 ? _cells[(x, y - 1)] : 0;
                    var upperLeft = x > 1 && y > 1 ? _cells[(x - 1, y - 1)] : 0;
                    _cells.Add((x, y), CalculatePower(x, y) + upperRight + bottomLeft - upperLeft);
                }
            }
        }

        public int CalculatePower(int x, int y)
        {
            var rack = x + 10;
            var power = (rack * y + _serial) * rack;
            return (power > 99 ? Convert.ToInt32(power.ToString()[^3].ToString()) : 0) - 5;
        }

        public (int, int, int) HighestPower(int size)
        {
            var highestPower = 0;
            var position = (0, 0);
            
            for (int startY = 1; startY <= 301 - size; startY++)
            {
                for (int startX = 1; startX <= 301 - size; startX++)
                {
                    var bottomLeft = startX - 1 > 0 ? _cells[(startX - 1, startY + size - 1)] : 0;
                    var upperRight = startY - 1 > 0 ? _cells[(startX + size - 1, startY - 1)] : 0;
                    var upperLeft = startX - 1 > 0 && startY - 1 > 0 ? _cells[(startX - 1, startY - 1)] : 0;
                    var bottomRight = _cells[(startX + size - 1, startY + size - 1)];
                    var power = bottomRight - bottomLeft - upperRight + upperLeft;
                    
                    if (power > highestPower)
                    {
                        highestPower = power;
                        position = (startX, startY);
                    }
                }
            }

            return (position.Item1, position.Item2, highestPower);
        }
    }
}