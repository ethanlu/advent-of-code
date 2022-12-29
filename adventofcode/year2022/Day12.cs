using adventofcode.common;
using adventofcode.common.graph;
using adventofcode.common.graph.search;
using Path = adventofcode.common.graph.Path;

namespace adventofcode.year2022;

public class Day12 : Solution
{
    private GridNode[,] _grid;
    private GridNode _start;
    private GridNode _end;

    public Day12(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();
        var maxY = input.Length;
        var maxX = input[0].Length;
        _grid = new GridNode[maxX, maxY];

        var y = 0;
        foreach (var line in input)
        {
            var x = 0;
            foreach (var character in line)
            {
                switch (character)
                {
                    case 'S':
                        _start = new GridNode(_grid, 1, $"{x},{y}",character.ToString(), 1);
                        _grid[x, y] = _start;
                        break;
                    case 'E':
                        _end = new GridNode(_grid, 26, $"{x},{y}",character.ToString(), 1);
                        _grid[x, y] = _end;
                        break;
                    default:
                        _grid[x, y] = new GridNode(_grid, character - 96, $"{x},{y}",character.ToString(), 1);
                        break;
                }
                x++;
            }
            y++;
        }

        if (_start is null)
        {
            throw new Exception("Start not found");
        }
        if (_end is null)
        {
            throw new Exception("End not found");
        }
    }

    private void ShowPath(IPath shortest)
    {
        var t = new HashSet<string>();
        foreach (var n in shortest.Nodes())
        {
            t.Add(n.Id());
        }

        for (int y = 0; y < _grid.GetLength(1); y++)
        {
            var line = "";
            for (int x = 0; x < _grid.GetLength(0); x++)
            {
                if (t.Contains(_grid[x, y].Id()))
                {
                    line += " ";
                }
                else
                {
                    line += _grid[x, y].Name();
                }
            }
            Console.WriteLine(line);
        }

        Console.WriteLine(shortest);
    }

    public override string PartOne()
    {
        var start = new Path();
        start.AddNode(_start);
        var astar = new AStar(start, _end, new GridNodeHeuristic(_end));
        var shortest = astar.FindPath();
        
        ShowPath(shortest);
        
        return Convert.ToString(shortest.Nodes().Count - 1);
    }

    public override string PartTwo()
    {
        var start = new Path();
        start.AddNode(_start);
        var astar = new AStar(start, _end, new GridNodeHeuristic(_end));
        var shortest = astar.FindPath();
        
        foreach (var node in _grid)
        {
            if (node.Height() == 1 && node.Id() != _start.Id())
            {
                start = new Path();
                start.AddNode(node);
                astar = new AStar(start, _end, new GridNodeHeuristic(_end));
                var candidate = astar.FindPath();

                if (candidate.Nodes().Last().Id() == _end.Id() && candidate.Nodes().Count < shortest.Nodes().Count)
                {
                    shortest = candidate;
                }
            }
        }
        
        ShowPath(shortest);

        return Convert.ToString(shortest.Nodes().Count - 1);
    }
}

internal class GridNode : Node
{
    private int _x;
    private int _y;
    private int _height;
    private GridNode[,] _grid;

    public GridNode(GridNode[,] grid, int height, string id, string name, int weight) : base(id, name, weight)
    {
        _height = height;
        _x = Convert.ToInt32(id.Split(',')[0]);
        _y = Convert.ToInt32(id.Split(',')[1]);
        _grid = grid;
    }

    public int X()
    {
        return _x;
    }

    public int Y()
    {
        return _y;
    }

    public int Height()
    {
        return _height;
    }

    public override List<(INode, int)> AdjacentNodes()
    {
        var neighbors = new List<(INode, int)>();

        // top
        if (_y + 1 < _grid.GetLength(1) && _grid[_x, _y + 1].Height() - Height() < 2)
        {
            neighbors.Add((_grid[_x, _y + 1], 0));
        }
        // bottom
        if (_y - 1 >= 0  && _grid[_x, _y - 1].Height() - Height() < 2)
        {
            neighbors.Add((_grid[_x, _y - 1], 0));
        }
        // left
        if (_x - 1 >= 0 && _grid[_x - 1, _y].Height() - Height() < 2)
        {
            neighbors.Add((_grid[_x - 1, _y], 0));
        }
        // right
        if (_x + 1 < _grid.GetLength(0) && _grid[_x + 1, _y].Height() - Height() < 2)
        {
            neighbors.Add((_grid[_x + 1, _y], 0));
        }

        return neighbors;
    }
}

internal class GridNodeHeuristic : Heuristic
{
    private GridNode _end;
    public GridNodeHeuristic(GridNode end)
    {
        _end = end;
    }
    
    public override int Cost(INode node, IPath path)
    {
        var n = (GridNode) node;
        return (Math.Abs(_end.X() - n.X()) + Math.Abs(_end.Y() - n.Y()));
    } 
}