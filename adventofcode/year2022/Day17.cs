using adventofcode.common;
using adventofcode.common.grid;

namespace adventofcode.year2022;

public class Day17 : Solution
{
    private string _input;
    private readonly List<char[,]> _templates = new List<char[,]>()
    {
        new char[4, 1]
        {
            {'#'}, {'#'}, {'#'}, {'#'},
        },
        new char[3, 3]
        {
            {' ', '#', ' '},
            {'#', '#', '#'},
            {' ', '#', ' '},
        },
        new char[3, 3]
        {
            {'#', ' ', ' '},
            {'#', ' ', ' '},
            {'#', '#', '#'},
        },
        new char[1, 4]
        {
            {'#', '#', '#', '#'}
        },
        new char[2, 2]
        {
            {'#', '#'},
            {'#', '#'}
        },
    };

    public Day17(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var simulation = new RockFall(_templates, _input, 7,2022L);
        var rockHeight = simulation.Simulate();

        return Convert.ToString(rockHeight);
    }

    public override string PartTwo()
    {
        var simulation = new RockFall(_templates, _input, 7, 1000000000000L);
        var rockHeight = simulation.Simulate();

        return Convert.ToString(rockHeight);
    }

    internal readonly struct SimulationState
    {
        public SimulationState(int rockHash, int step, long rockCount, long rockHeight)
        {
            RockHash = rockHash;
            Step = step;
            RockCount = rockCount;
            RockHeight = rockHeight;
        }

        public int RockHash { get; }
        public int Step { get; }
        public long RockCount { get; }
        public long RockHeight { get; }
    }

    internal class Block
    {
        private List<Point2D> _rocks;
        private int _height;

        public Block(char[,] rocks, Point2D origin)
        {
            var width = rocks.GetLength(0);
            _height = rocks.GetLength(1);

            _rocks = new List<Point2D>(
                (from y in Enumerable.Range(0, _height) from x in Enumerable.Range(0, width) select (new Point2D(x, y) + origin, rocks[x, y]))
                .Where(x => x.Item2 == '#')
                .Select(x => x.Item1)
                .ToList()
            );
        }

        public Block(List<Point2D> rocks, int height)
        {
            _rocks = rocks;
            _height = height;
        }

        public int Height()
        {
            return _height;
        }

        private Point2D Delta(char direction)
        {
            var delta = new Point2D(0, 0);
            switch (direction)
            {
                case '<':
                    delta += new Point2D(-1, 0);
                    break;
                case '>':
                    delta += new Point2D(1, 0);
                    break;
                default:
                    delta += new Point2D(0, -1);
                    break;
            }

            return delta;
        }
        
        public int TopY()
        {
            return _rocks.Select(r => r.Y()).Aggregate(0, (highest, y) => y > highest ? y : highest);
        }

        public int BottomY()
        {
            return _rocks.Select(r => r.Y()).Aggregate(_height, (lowest, y) => y < lowest ? y : lowest);
        }

        public List<Point2D> Position()
        {
            return _rocks;
        }

        public List<Point2D> Peek(char direction)
        {
            var delta = Delta(direction);
            return new List<Point2D>(_rocks.Select(r => r + delta));
        }

        public void Move(char direction)
        {
            var delta = Delta(direction);
            _rocks = new List<Point2D>(_rocks.Select(r => r + delta));
        }
    }

    internal class RockFall
    {
        const int Height = 10000;
        private const int PagninationThreshold = 10;
        private const long SnapshotThreshold = 500000L;
        private const int SnapshotHeight = 100;
        
        private char[] _jetstream;
        private char[,] _chamber;
        private readonly List<char[,]> _templates;
        private Point2D _rockOrigin;
        private long _limit;
        
        public RockFall(List<char[,]> templates, string jetstream, int width, long limit)
        {
            _templates = templates;
            _jetstream = jetstream.ToCharArray();
            _rockOrigin = new Point2D(2, 3);
            _limit = limit;
            _chamber = new char[width, Height];
        }

        private int LineToNumber(int y)
        {
            return Convert.ToInt32(Enumerable.Range(0, _chamber.GetLength(0)).Aggregate("", (acc, x) => acc + (_chamber[x, y] == '#' ? "1" : "0")), 2);
        }

        private bool Collision(List<Point2D> peek)
        {
            return peek.Select(rock => rock.X()).Where(x => x < 0).Count() > 0 ||
                   peek.Select(rock => rock.X()).Where(x => x >= _chamber.GetLength(0)).Count() > 0 ||
                   peek.Select(rock => rock.Y()).Where(y => y < 0).Count() > 0 ||
                   peek.Select(rock => _chamber[rock.X(), rock.Y()]).Where(c => c == '#').Count() > 0;
        }

        public void Show(Block? fallingRock, int limitY=0)
        {
            var fallingPoint2Ds = (fallingRock is not null ? fallingRock.Position() : new List<Point2D>()).ToHashSet();
            for (int y = Math.Max(_rockOrigin.Y(), fallingRock is not null ? fallingRock.TopY() : 0); y >= limitY; y--)
            {
                Console.Write("|");
                for (int x = 0; x < _chamber.GetLength(0); x++)
                {
                    var p = new Point2D(x, y);

                    if (fallingPoint2Ds.Contains(p))
                    {
                        Console.Write('@');
                        continue;
                    }

                    if (_rockOrigin.Equals(p))
                    {
                        Console.Write('+');
                        continue;
                    }

                    switch (_chamber[x, y])
                    {
                        case '#':
                            Console.Write('#');
                            break;
                        default:
                            Console.Write('.');
                            break;
                    }
                }
                Console.WriteLine("|");
            }
            Console.WriteLine(string.Join("",Enumerable.Repeat("-", _chamber.GetLength(0) + 2)));
        }

        private void Paginate(ref Block? currentRock, ref int rockHeight, ref long totalRockHeight)
        {
            if (SnapshotHeight > _rockOrigin.Y())
            {
                throw new Exception("Tried to take too big of a snapshot");
            }

            // cutoff Point2D should be the smallest of all of the second largest y Point2D that has a # for every x column
            var paginateAtY = _rockOrigin.Y() - SnapshotHeight * 2;
            
            // create new chamber
            var newChamber = new char[_chamber.GetLength(0), _chamber.GetLength(1)];
            for (int y = paginateAtY; y <= _rockOrigin.Y(); y++)
            {
                for (int x = 0; x < newChamber.GetLength(0); x++)
                {
                    newChamber[x, y - paginateAtY] = _chamber[x, y];
                }
            }
            _chamber = newChamber;
            
            // apply offset to _rockOrigin, currentRock, and rockHeight
            _rockOrigin -= new Point2D(0, paginateAtY);

            if (currentRock is not null)
            {
                currentRock = new Block(
                    currentRock.Position().Select(x => x - new Point2D(0, paginateAtY)).ToList(),
                    currentRock.Height()
                );
            }

            rockHeight -= paginateAtY;
            totalRockHeight += paginateAtY;
        }

        private int RockHash()
        {
            // from rockOrigin's Y, get the top SnapshotHeight worth of rocks and convert to decimal
            return Enumerable.Range(_rockOrigin.Y() - SnapshotHeight, SnapshotHeight).Reverse()
                .Select(y => LineToNumber(y)).Aggregate(0, (acc, yHash) => acc + yHash);
        }

        public long Simulate()
        {
            var rockCount = 0L;
            var templateIndex = 0;
            var jetstreamIndex = 0;
            var rockFalling = true;

            // paginate these along with _chamber and _rockOrigin
            var totalRockHeight = 0L;
            var rockHeight = 0;
            var currentRock = new Block(_templates[templateIndex], _rockOrigin);
            
            bool cycleDetected = false;
            var step = 0;
            SimulationState? baseState = null;
            while (true)
            {
                step++;
                
                // no rock is falling, so create new rock from next template
                if (!rockFalling)
                {
                    templateIndex = (templateIndex + 1) % _templates.Count;
                    currentRock = new Block(_templates[templateIndex], _rockOrigin);
                    rockFalling = true;
                    continue;
                }

                // current jetstream acts on rock
                var peekHorizontal = currentRock.Peek(_jetstream[jetstreamIndex]);
                if (!Collision(peekHorizontal))
                {
                    currentRock.Move(_jetstream[jetstreamIndex]);
                }
                jetstreamIndex = (jetstreamIndex + 1) % _jetstream.Length;

                // move rock down if possible
                var peekDown = currentRock.Peek('v');
                if (!Collision(peekDown))
                {
                    currentRock.Move('v');
                }
                else
                {
                    // rock is at rest, update chamber and source
                    foreach (var p in currentRock.Position())
                    {
                        _chamber[p.X(), p.Y()] = '#';
                        rockHeight = p.Y() + 1 > rockHeight ? p.Y() + 1 : rockHeight;
                    }
                    
                    // update rock origin if the difference between it and the highest rock is less than 3
                    if (_rockOrigin.Y() - rockHeight < 3)
                    {
                        _rockOrigin = new Point2D(_rockOrigin.X(), rockHeight + 3);
                    }
                    
                    rockCount++;
                    currentRock = null;
                    rockFalling = false;
                    
                    if (!cycleDetected && rockCount >= SnapshotThreshold)
                    {
                        if (baseState is null)
                        {
                            baseState = new SimulationState(RockHash(), step, rockCount, totalRockHeight + rockHeight);
                        }
                        else
                        {
                            var currentState = new SimulationState(RockHash(), step, rockCount, totalRockHeight + rockHeight);

                            if (currentState.RockHash == baseState?.RockHash)
                            {
                                var rockCountPerCycle = currentState.RockCount - baseState?.RockCount;
                                var rockHeightPerCycle = currentState.RockHeight - baseState?.RockHeight;
                            
                                Console.WriteLine($"Cycle length : {currentState.Step - baseState?.Step}");
                                Console.WriteLine($"Rock Count Per Cycle : {rockCountPerCycle}");
                                Console.WriteLine($"Rock Height Per Height : {rockHeightPerCycle}");

                                var additionalCyclesNeeded = (_limit - rockCount) / rockCountPerCycle;
                                var additionalRockCountAdded = additionalCyclesNeeded * rockCountPerCycle;
                                var additionalRockHeightAdded = additionalCyclesNeeded * rockHeightPerCycle;
                            
                            
                                Console.WriteLine($"Cycles needed : {additionalCyclesNeeded}");
                                Console.WriteLine($"Rocks Added : {additionalRockCountAdded}");
                                Console.WriteLine($"Rock Height Added : {additionalRockHeightAdded}");

                                totalRockHeight += additionalRockHeightAdded ?? 0;
                                rockCount += additionalRockCountAdded ?? 0;
                            
                                cycleDetected = true;
                            }
                        }
                    }

                    if (rockCount >= _limit)
                    {
                        break;
                    }
                }

                // perform pagination if chamber is near the max limit
                if (_rockOrigin.Y() >= _chamber.GetLength(1) - PagninationThreshold)
                {
                    Paginate(ref currentRock, ref rockHeight, ref totalRockHeight);
                }
            }

            return totalRockHeight + rockHeight;
        }
    }
}