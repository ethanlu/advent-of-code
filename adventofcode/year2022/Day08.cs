namespace adventofcode.year2022
{
    public class Day08 : Solution
    {
        private List<List<int>> _grid = new List<List<int>>();

        public Day08(string year, string day) : base(year, day)
        {
            var input = this.LoadInputAsLines();

            foreach (var line in input)
            {
                _grid.Add(new List<int>(line.ToArray().Select(c => Convert.ToInt32(c.ToString()))));
            }
        }

        private bool IsVisible(int r, int c)
        {
            // edge
            if (r == 0 || r == _grid.Count - 1 || c == 0 || c == _grid[0].Count - 1)
            {
                return true;
            }

            var top = true;
            // top
            for (var row = r - 1; row >= 0; row--)
            {
                top = top && _grid[r][c] > _grid[row][c];
            }
            
            // bottom
            var bottom = true;
            for (var row = r + 1; row < _grid.Count(); row++)
            {
                bottom = bottom && _grid[r][c] > _grid[row][c];
            }
            
            // left
            var left = true;
            for (var col = c - 1; col >= 0; col--)
            {
                left = left && _grid[r][c] > _grid[r][col];
            }
            
            // right
            var right = true;
            for (var col = c + 1; col < _grid[0].Count; col++)
            {
                right = right && _grid[r][c] > _grid[r][col];
            }

            return top || bottom || left || right;
        }
        
        private int ScenicScore(int r, int c)
        {
            // top
            var top = 0;
            for (var row = r - 1; row >= 0; row--)
            {
                top++;
                if (_grid[r][c] <= _grid[row][c])
                {
                    break;
                }
            }
            
            // bottom
            var bottom = 0;
            for (var row = r + 1; row < _grid.Count(); row++)
            {
                bottom++;
                if (_grid[r][c] <= _grid[row][c])
                {
                    break;
                }
            }
            
            // left
            var left = 0;
            for (var col = c - 1; col >= 0; col--)
            {
                left++;
                if (_grid[r][c] <= _grid[r][col])
                {
                    break;
                }
            }
            
            // right
            var right = 0;
            for (var col = c + 1; col < _grid[0].Count; col++)
            {
                right++;
                if (_grid[r][c] <= _grid[r][col])
                {
                    break;
                }
            }

            return top * bottom * left * right;
        }

        public override string PartOne()
        {
            var visible = 0;

            for (var row = 0; row < _grid.Count; row++)
            {
                for (var col = 0; col < _grid[0].Count; col++)
                {
                    visible += this.IsVisible(row, col) ? 1 : 0;
                }
            }

            return Convert.ToString(visible);
        }

        public override string PartTwo()
        {
            var largestScore = 0;

            for (var row = 0; row < _grid.Count; row++)
            {
                for (var col = 0; col < _grid[0].Count; col++)
                {
                    var score = this.ScenicScore(row, col);
                    if (score > largestScore)
                    {
                        largestScore = score;
                    }
                }
            }

            return Convert.ToString(largestScore);
        }
    }
}