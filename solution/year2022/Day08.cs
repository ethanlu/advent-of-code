using System;
using System.Collections.Generic;
using System.Linq;

namespace solution.year2022
{
    public class Day08 : Solution
    {
        private string[] input;
        private List<List<int>> grid = new List<List<int>>();

        public Day08(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();

            foreach (var line in this.input)
            {
                this.grid.Add(new List<int>(line.ToArray().Select(c => Convert.ToInt32(c.ToString()))));
            }
        }

        private bool IsVisible(int r, int c)
        {
            // edge
            if (r == 0 || r == this.grid.Count - 1 || c == 0 || c == this.grid[0].Count - 1)
            {
                return true;
            }

            var top = true;
            // top
            for (var row = r - 1; row >= 0; row--)
            {
                top = top && this.grid[r][c] > this.grid[row][c];
            }
            
            // bottom
            var bottom = true;
            for (var row = r + 1; row < this.grid.Count(); row++)
            {
                bottom = bottom && this.grid[r][c] > this.grid[row][c];
            }
            
            // left
            var left = true;
            for (var col = c - 1; col >= 0; col--)
            {
                left = left && this.grid[r][c] > this.grid[r][col];
            }
            
            // right
            var right = true;
            for (var col = c + 1; col < this.grid[0].Count; col++)
            {
                right = right && this.grid[r][c] > this.grid[r][col];
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
                if (this.grid[r][c] <= this.grid[row][c])
                {
                    break;
                }
            }
            
            // bottom
            var bottom = 0;
            for (var row = r + 1; row < this.grid.Count(); row++)
            {
                bottom++;
                if (this.grid[r][c] <= this.grid[row][c])
                {
                    break;
                }
            }
            
            // left
            var left = 0;
            for (var col = c - 1; col >= 0; col--)
            {
                left++;
                if (this.grid[r][c] <= this.grid[r][col])
                {
                    break;
                }
            }
            
            // right
            var right = 0;
            for (var col = c + 1; col < this.grid[0].Count; col++)
            {
                right++;
                if (this.grid[r][c] <= this.grid[r][col])
                {
                    break;
                }
            }

            return top * bottom * left * right;
        }

        public override string PartOne()
        {
            var visible = 0;

            for (var row = 0; row < grid.Count; row++)
            {
                for (var col = 0; col < grid[0].Count; col++)
                {
                    visible += this.IsVisible(row, col) ? 1 : 0;
                }
            }

            return Convert.ToString(visible);
        }

        public override string PartTwo()
        {
            var largestScore = 0;

            for (var row = 0; row < grid.Count; row++)
            {
                for (var col = 0; col < grid[0].Count; col++)
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