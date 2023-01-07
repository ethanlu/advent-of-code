using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;

namespace adventofcode.year2022;

public class Day23 : Solution
{
    private List<Point2D> _startingTiles;
    
    public Day23(string year, string day) : base(year, day)
    {
        _startingTiles = new List<Point2D>();

        var y = 0;
        foreach (var l in LoadInputAsLines())
        {
            var x = 0;
            foreach (var c in l)
            {
                if (c == '#')
                {
                    _startingTiles.Add(new Point2D(x, y));
                }
                x++;
            }
            y++;
        }
    }

    public override string PartOne()
    {
        var simulation = new PlantSimulation(_startingTiles);
        var emptyTiles = simulation.Run(10);
        return Convert.ToString(emptyTiles);
    }

    public override string PartTwo()
    {
        var simulation = new PlantSimulation(_startingTiles);
        var emptyTiles = simulation.Run();
        return Convert.ToString(emptyTiles);
    }
    
    internal enum Direction
    {
        North = 0,  South = 1, West = 2, East = 3
    }

    internal class PlantSimulation
    {
        private HashSet<Point2D> _plantTiles;

        public PlantSimulation(List<Point2D> plantTiles)
        {
            _plantTiles = new HashSet<Point2D>();
            foreach (var p in plantTiles)
            {
                _plantTiles.Add(p);
            }
        }

        private char[,] ToGrid()
        {
            var minX = 99999;
            var maxX = -99999;
            var minY = 99999;
            var maxY = -99999;
            foreach (var p in _plantTiles)
            {
                minX = minX > p.X() ? p.X() : minX;
                maxX = maxX < p.X() ? p.X() : maxX;
                minY = minY > p.Y() ? p.Y() : minY;
                maxY = maxY < p.Y() ? p.Y() : maxY;
            }
            var width = (maxX - minX) + 1;
            var height = (maxY - minY) + 1;
            var grid = new char[width, height];

            foreach (var y in Enumerable.Range(0, grid.GetLength(1)))
            {
                foreach (var x in Enumerable.Range(0, grid.GetLength(0)))
                {
                    grid[x, y] = '.';
                }
            }
            
            var offsetX = Math.Abs(minX);
            var offsetY = Math.Abs(minY);
            foreach (var p in _plantTiles)
            {
                grid[p.X() + offsetX, p.Y() + offsetY] = '#';
            }

            return grid;
        }

        public int Run(int rounds=-1, bool verbose=false)
        {
            var moveOrder = new Queue<Direction>();
            moveOrder.Enqueue(Direction.North);
            moveOrder.Enqueue(Direction.South);
            moveOrder.Enqueue(Direction.West);
            moveOrder.Enqueue(Direction.East);
            
            var candidateTiles = new Dictionary<Point2D, List<Point2D>>();
            var round = 0;
            var hasMovements = true;
            do
            {
                
                if (round == rounds)
                {
                    break;
                }

                if (verbose)
                {
                    var g = ToGrid();
                    Draw<char>.ShowGrid(g);
                    Console.WriteLine($"Move : {moveOrder.Aggregate("", (acc, m) => acc + (int) m)}");
                    Console.WriteLine($"Round : {round}");
                }
                
                // pick next tile to move
                foreach (var source in _plantTiles)
                {
                    if (!_plantTiles.Contains(source + new Point2D(-1, -1)) && !_plantTiles.Contains(source + new Point2D(0, -1)) && !_plantTiles.Contains(source + new Point2D(1, -1)) &&
                        !_plantTiles.Contains(source + new Point2D(-1, 0)) && !_plantTiles.Contains(source + new Point2D(1, 0)) &&
                        !_plantTiles.Contains(source + new Point2D(-1, 1)) && !_plantTiles.Contains(source + new Point2D(0, 1)) && !_plantTiles.Contains(source + new Point2D(1, 1))
                       )
                    {
                        // does not need to move
                        continue;
                    }

                    var delta = new Point2D(0, 0);
                    foreach (var d in moveOrder.ToList())
                    {
                        if (d == Direction.North && !_plantTiles.Contains(source + new Point2D(-1, -1)) && !_plantTiles.Contains(source + new Point2D(0, -1)) && !_plantTiles.Contains(source + new Point2D(1, -1)))
                        {
                            delta = new Point2D(0, -1);
                            break;
                        }

                        if (d == Direction.South && !_plantTiles.Contains(source + new Point2D(-1, 1)) && !_plantTiles.Contains(source + new Point2D(0, 1)) && !_plantTiles.Contains(source + new Point2D(1, 1)))
                        {
                            delta = new Point2D(0, 1);
                            break;
                        }

                        if (d == Direction.West && !_plantTiles.Contains(source + new Point2D(-1, -1)) && !_plantTiles.Contains(source + new Point2D(-1, 0)) && !_plantTiles.Contains(source + new Point2D(-1, 1)))
                        {
                            delta = new Point2D(-1, 0);
                            break;
                        }

                        if (d == Direction.East && !_plantTiles.Contains(source + new Point2D(1, -1)) && !_plantTiles.Contains(source + new Point2D(1, 0)) && !_plantTiles.Contains(source + new Point2D(1, 1)))
                        {
                            delta = new Point2D(1, 0);
                            break;
                        }
                    }

                    if (delta.X() == 0 && delta.Y() == 0)
                    {
                        // cannot move
                        continue;
                    }

                    var targetTile = source + delta;
                    if (!candidateTiles.ContainsKey(targetTile))
                    {
                        candidateTiles.Add(targetTile, new List<Point2D>());
                    }

                    candidateTiles[targetTile].Add(source);
                }

                // update plant tiles based on candidate tiles
                hasMovements = candidateTiles.Count > 0;
                foreach (var (target, sources) in candidateTiles)
                {
                    if (sources.Count == 1)
                    {
                        // candidate tile only has one candidate, so it can be moved to
                        _plantTiles.Add(target);
                        _plantTiles.Remove(sources[0]);
                    }

                    // remove candidate tile after processing
                    candidateTiles.Remove(target);
                }

                // update move order
                moveOrder.Enqueue(moveOrder.Dequeue());
                round++;
            } while (hasMovements);
            
            var grid = ToGrid();
            Draw<char>.ShowGrid(grid);
            Console.WriteLine($"Move : {moveOrder.Aggregate("", (acc, m) => acc + (int)m)}");
            Console.WriteLine($"Round : {round}");

            return rounds > 0 ? grid.GetLength(0) * grid.GetLength(1) - _plantTiles.Count : round;
        }
    }
}