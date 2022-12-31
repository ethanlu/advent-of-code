using adventofcode.common;
using adventofcode.common.grid;

namespace adventofcode.year2022;

public class Day14 : Solution
{
    private HashSet<Point2D> _rocks;

    public Day14(string year, string day) : base(year, day)
    {
        _rocks = new HashSet<Point2D>();
        foreach (var line in LoadInputAsLines())
        {
            var Point2Ds = line.Split(" -> ");
            for (int i = 1; i < Point2Ds.Length; i++)
            {
                var start = new Point2D(Point2Ds[i - 1].Split(',')[0], Point2Ds[i - 1].Split(',')[1]);
                var end = new Point2D(Point2Ds[i].Split(',')[0], Point2Ds[i].Split(',')[1]);

                // horizontal
                if (start.X() != end.X())
                {
                    for (int x = Math.Min(start.X(), end.X()); x <= Math.Max(start.X(), end.X()); x++)
                    {
                        _rocks.Add(new Point2D(x, start.Y()));
                    }
                }

                // vertical
                if (start.Y() != end.Y())
                {
                    for (int y = Math.Min(start.Y(), end.Y()); y <= Math.Max(start.Y(), end.Y()); y++)
                    {
                        _rocks.Add(new Point2D(start.X(), y));
                    }
                }
            }
        }
    }

    public override string PartOne()
    {
        var cave = new SandFall(_rocks, new Point2D(500, 0), true);
        int sands = cave.Run();
        cave.ShowCave();
        
        return Convert.ToString(sands);
    }

    public override string PartTwo()
    {
        var cave = new SandFall(_rocks, new Point2D(500, 0), false);
        int sands = cave.Run();
        cave.ShowCave();

        return Convert.ToString(sands);
    }
}

internal class SandFall
{
    private const int Margin = 3;
    
    private char[,] _cave;
    private int _width;
    private int _height;
    private Point2D _sandSource;
    private bool _abyss;

    public SandFall(HashSet<Point2D> rocks, Point2D sandSource, bool abyss)
    {
        _abyss = abyss;
        _width = 1000;
        _height = 0;
        foreach (var p in rocks)
        {
            _height = _height < p.Y() ? p.Y() : _height;
        }
        _height += 3;

        _sandSource = sandSource;
        _cave = new char[_width, _height];
        for (int y = 0; y < _height; y++)
        {
            for (int x = 0; x < _width; x++)
            {
                if (rocks.Contains(new Point2D(x, y)))
                {
                    _cave[x, y] = '#';
                }
                else
                {
                    _cave[x, y] = '.';
                }
            }
        }
    }

    public int Run()
    {
        var sandCount = 0;
        var reachedEnd = false;
        do
        {
            int sandX = _sandSource.X();
            int sandY = _sandSource.Y();

            // drop a grain of sand until it comes to a stop
            var atRest = false;
            do
            {
                // can move down?
                if (sandY + 1 >= _height - 1)
                {
                    if (_abyss)
                    {
                        reachedEnd = true;
                        break;
                    }
                    else
                    {
                        atRest = true;
                        continue;
                    }
                }

                if (_cave[sandX, sandY + 1] == '.')
                {
                    sandY++;
                    continue;
                }

                // can move left and down?
                if (sandX - 1 < 0)
                {
                    reachedEnd = true;
                    break;
                }

                if (_cave[sandX - 1, sandY + 1] == '.')
                {
                    sandX--;
                    sandY++;
                    continue;
                }

                // can move right and down?
                if (sandX + 1 >= _width)
                {
                    reachedEnd = true;
                    break;
                }

                if (_cave[sandX + 1, sandY + 1] == '.')
                {
                    sandX++;
                    sandY++;
                    continue;
                }

                atRest = true;
            } while (!atRest);

            if (!reachedEnd || sandX == _sandSource.X() && sandY == _sandSource.Y())
            {
                sandCount++;
                _cave[sandX, sandY] = 'o';
            }
            
            // sand grain rests at sand source....treat it as the end
            if (sandX == _sandSource.X() && sandY == _sandSource.Y())
            {
                reachedEnd = true;
            }

        } while (!reachedEnd);

        return sandCount;
    }

    public void ShowCave()
    {
        var minX = _width;
        var minY = _height;
        var maxX = 0;
        var maxY = 0;

        for (int y = 0; y < _height; y++)
        {
            for (int x = 0; x < _width; x++)
            {
                if (_cave[x, y] != '.')
                {
                    minX = minX > x ? x : minX;
                    minY = minY > y ? y : minY;
                    maxX = maxX < x ? x : maxX;
                    maxY = maxY < y ? y : maxY;
                }
            }
        }

        minX = Math.Max(0, minX - Margin);
        minY = Math.Max(0, minY - Margin);
        maxX = Math.Min(_width, maxX + Margin + 1);
        maxY = Math.Min(_height, maxY + Margin + 1);

        var line = "";
        for (int x = minX; x < maxX; x++)
        {
            if (_sandSource.X() == x)
            {
                line += _cave[x, minY] == '.' ? "+" : _cave[x, minY];
            }
            else
            {
                line += _cave[x, minY];
            }
        }
        Console.WriteLine(line);

        for (int y = minY + 1; y < maxY - 1; y++)
        {
            line = "";
            for (int x = minX; x < maxX; x++)
            {
                line += _cave[x, y];
            }
            Console.WriteLine(line);
        }

        line = "";
        for (int x = minX; x < maxX; x++)
        {
            if (_abyss)
            {
                line += ".";
            }
            else
            {
                line += "#";
            }
        }
        Console.WriteLine(line);

        Console.WriteLine($"{maxX-minX}x{maxY-minY}");
    }
}