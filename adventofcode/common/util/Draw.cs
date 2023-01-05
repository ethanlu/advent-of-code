using adventofcode.common.grid;

namespace adventofcode.common.util;

public class Draw<T>
{
    public static void ShowGrid(T[,] grid)
    {
        foreach (var y in Enumerable.Range(0, grid.GetLength(1)))
        {
            var line = "";
            foreach (var x in Enumerable.Range(0, grid.GetLength(0)))
            {
                line += grid[x, y]!.ToString();
            }
            Console.WriteLine(line);
        }
    }
}