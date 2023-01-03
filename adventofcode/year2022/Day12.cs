using adventofcode.common;
using adventofcode.common.graph.search;

namespace adventofcode.year2022;

public class Day12 : Solution
{
    private (int, char)[,] _grid;
    private List<(int, int)> _lowestPoints;
    private StepState _start;
    private StepState _end;

    public Day12(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();
        var maxY = input.Length;
        var maxX = input[0].Length;
        _grid = new (int, char)[maxX, maxY];
        _lowestPoints = new List<(int, int)>();

        var start = (-1, -1);
        var end = (-1, -1);
        var y = 0;
        foreach (var line in input)
        {
            var x = 0;
            foreach (var character in line)
            {
                switch (character)
                {
                    case 'S':
                        start = (x, y);
                        _grid[x, y] = (1, character);
                        break;
                    case 'E':
                        end = (x, y);
                        _grid[x, y] = (26, character);
                        break;
                    default:
                        var height = character - 96;
                        _grid[x, y] = (height, character);

                        if (height == 1)
                        {
                            _lowestPoints.Add((x, y));
                        }

                        break;
                }
                x++;
            }
            y++;
        }
        _end = new StepState(_grid, end.Item1, end.Item2, end.Item1, end.Item2, 26, 0);
        _start = new StepState(_grid, start.Item1, start.Item2, end.Item1, end.Item2, 1, 0);

        if (_start is null)
        {
            throw new Exception("Start not found");
        }
        if (_end is null)
        {
            throw new Exception("End not found");
        }
    }

    private void ShowPath(ISearchPath shortest)
    {
        var t = new HashSet<(int, int)>();
        foreach (StepState n in shortest.SearchStates())
        {
            t.Add((n.X(), n.Y()));
        }

        for (int y = 0; y < _grid.GetLength(1); y++)
        {
            var line = "";
            for (int x = 0; x < _grid.GetLength(0); x++)
            {
                if (t.Contains((x, y)))
                {
                    line += " ";
                }
                else
                {
                    line += _grid[x, y].Item2;
                }
            }
            Console.WriteLine(line);
        }

        Console.WriteLine(shortest);
    }

    public override string PartOne()
    {
        var start = new SearchPath();
        start.Add(_start);
        var astar = new AStar(start, _end);
        var shortest = astar.FindPath();
        
        ShowPath(shortest);
        
        return Convert.ToString(shortest.SearchStates().Count - 1);
    }

    public override string PartTwo()
    {
        var start = new SearchPath();
        start.Add(_start);
        var astar = new AStar(start, _end);
        var shortest = astar.FindPath();
        
        foreach (var (x, y) in _lowestPoints)
        {
            start = new SearchPath();
            start.Add(new StepState(_grid, x, y, _end.X(), _end.Y(),_grid[x, y].Item1, 0));
            astar = new AStar(start, _end);
            var candidate = astar.FindPath();

            if (candidate.SearchStates().Last().Id() == _end.Id() && candidate.SearchStates().Last().Cost() < shortest.SearchStates().Last().Cost())
            {
                shortest = candidate;
            }
        }
        
        ShowPath(shortest);

        return Convert.ToString(shortest.SearchStates().Count - 1);
    }
}

internal class StepState : SearchState
{
    private (int, char)[,] _grid;
    private int _x;
    private int _y;
    private int _endX;
    private int _endY;

    public StepState((int, char)[,] grid, int x, int y, int endX, int endY, int gain, int cost) : base($"{x},{y}", gain, cost, 9999)
    {
        _x = x;
        _y = y;
        _endX = endX;
        _endY = endY;
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

    public override int PotentialGain()
    {
        return (Math.Abs(_endX - _x) + Math.Abs(_endY - _y));
    }

    public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
    {
        var neighbors = new List<ISearchState>();

        // top
        if (_y + 1 < _grid.GetLength(1) && _grid[_x, _y + 1].Item1 -_grid[_x, _y].Item1 < 2 && previousSearchState?.Id() != $"{_x},{_y + 1}")
        {
            neighbors.Add(new StepState(_grid, _x, _y + 1, _endX, _endY, _grid[_x, _y + 1].Item1, Cost() + 1));
        }
        // bottom
        if (_y - 1 >= 0  && _grid[_x, _y - 1].Item1 - _grid[_x, _y].Item1 < 2 && previousSearchState?.Id() != $"{_x},{_y - 1}")
        {
            neighbors.Add(new StepState(_grid, _x, _y - 1, _endX, _endY,_grid[_x, _y - 1].Item1, Cost() + 1));
        }
        // left
        if (_x - 1 >= 0 && _grid[_x - 1, _y].Item1 - _grid[_x, _y].Item1 < 2 && previousSearchState?.Id() != $"{_x - 1},{_y}")
        {
            neighbors.Add(new StepState(_grid, _x - 1, _y, _endX, _endY,_grid[_x - 1, _y].Item1, Cost() + 1));
        }
        // right
        if (_x + 1 < _grid.GetLength(0) && _grid[_x + 1, _y].Item1 - _grid[_x, _y].Item1 < 2 && previousSearchState?.Id() != $"{_x + 1},{_y}")
        {
            neighbors.Add(new StepState(_grid, _x + 1, _y, _endX, _endY,_grid[_x + 1, _y].Item1, Cost() + 1));
        }

        return neighbors;
    }

    public override string ToString()
    {
        return _id;
    }
}