using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.graph.search;

namespace adventofcode.year2018;

public class Day15 : Solution
{
    private string[] _input;
    
    public Day15(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var bs = new BattleSimulation(_input, 3);
        var score = bs.Run(false);
        Console.WriteLine($"rounds fought : {bs.Rounds()}");
        Console.WriteLine($"victor : {bs.Victor()}");
        bs.Show();
        return Convert.ToString(score);
    }

    public override string PartTwo()
    {
        var elfHealth = 4;
        var score = 0;
        while (true)
        {
            Console.WriteLine($"\nif elf health is {elfHealth}...");
            
            var bs = new BattleSimulation(_input, elfHealth);
            score = bs.Run(true);
            
            Console.WriteLine($"rounds fought : {bs.Rounds()}");
            Console.WriteLine($"victor : {bs.Victor()}");
            if (bs.Victor() == "elves") { Console.WriteLine($"elf deaths : {bs.ElfDeaths()}"); }

            if (bs.ElfDeaths() == 0)
            {
                bs.Show();
                break;
            }
            elfHealth++;
        }

        return Convert.ToString(score);
    }

    private class Unit : IComparable<Unit>
    {
        private char _type;
        private int _health;
        private int _power;
        private Point2D _position;
        
        public Unit(char type, Point2D position, int health, int power)
        {
            _type = type;
            _position = position;
            _health = health;
            _power = power;
        }

        public char Type() { return _type; }
        public int Health() { return _health; }
        public int Power() { return _power; }
        public Point2D Position() { return _position; }
        public void Damage(int damage) { _health -= damage; }
        public void Move(Point2D position) { _position = position; }
        
        public int CompareTo(Unit u)
        {
            if (u is null) { throw new Exception("Unit input is null"); }
            if (_position.Y() < u.Position().Y()) { return -1; }
            if (_position.Y() > u.Position().Y()) { return 1; }
            if (_position.X() < u.Position().X()) { return -1; }
            if (_position.X() > u.Position().X()) { return 1; }
            return 0;
        }
    }

    private class MeleeSearchState : SearchState
    {
        private Dictionary<Point2D, char> _map;
        private HashSet<Point2D> _occupied;
        private Point2D _position;

        public MeleeSearchState(Dictionary<Point2D, char> map, HashSet<Point2D> occupied, Point2D position, int gain, int cost, int maxCost) : base($"{position}", gain, cost, maxCost)
        {
            _map = map;
            _occupied = occupied;
            _position = position;
        }

        public Point2D Position() { return _position; }

        public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
        {
            var states = new List<ISearchState>();

            foreach (var delta in new List<Point2D>() { new Point2D(0, -1), new Point2D(-1, 0), new Point2D(1, 0), new Point2D(0, 1) })
            {
                var candidate = _position + delta;
                if (_map.ContainsKey(candidate) && _map[candidate] == '.' && !_occupied.Contains(candidate))
                {
                    states.Add(new MeleeSearchState(_map, _occupied, candidate, _gain + 1, _cost + 1, _maxCost));
                }
            }
            
            return states;
        }
    }
    
    private class BattleSimulation
    {
        private Dictionary<Point2D, char> _map;
        private int _width;
        private int _height;
        private List<Unit> _units;
        private int _elfDeaths;
        private int _rounds;

        public BattleSimulation(string[] map, int elfHealth)
        {
            _units = new List<Unit>();
            _map = new Dictionary<Point2D, char>();
            _width = map.Length;
            _height = map[0].Length;
            _elfDeaths = 0;
            _rounds = 0;
            
            for (int y = 0; y < map.Length; y++)
            {
                for (int x = 0; x < map[y].Length; x++)
                {
                    var p = new Point2D(x, y);
                    if (map[y][x] == '#')
                    {
                        _map.Add(p, '#');
                        continue;
                    }
                    _map.Add(p, '.');
                    if (map[y][x] == 'E' || map[y][x] == 'G')
                    {
                        _units.Add(new Unit(map[y][x], p, 200, map[y][x] == 'E' ? elfHealth : 3));
                    }
                }
            }
        }

        private Unit? WeakestTarget(Unit attacker, List<Unit> targets)
        {
            Unit? weakest = null;
            foreach (var target in targets)
            {
                var delta = attacker.Position() - target.Position();
                if (Math.Abs(delta.X()) + Math.Abs(delta.Y()) == 1)
                {   // target is within range for attack
                    if (weakest is null || weakest.Health() > target.Health())
                    {
                        weakest = target;
                    }
                }
            }

            return weakest;
        }
        
        public int Rounds() { return _rounds; }
        public string Victor() { return _units[0].Type() == 'E' ? "elves" : "goblins"; }
        public int ElfDeaths() { return _elfDeaths; }

        public void Show()
        {
            var grid = new char[_width, _height];
            foreach (var (p, c) in _map) { grid[p.X(), p.Y()] = c; }
            foreach (var u in _units) { grid[u.Position().X(), u.Position().Y()] = u.Type(); }
            
            foreach (var y in Enumerable.Range(0, grid.GetLength(1)))
            {
                var line = "";
                foreach (var x in Enumerable.Range(0, grid.GetLength(0)))
                {
                    line += grid[x, y]!.ToString();
                }

                var healths = new List<string>();
                foreach (var u in _units.Where(u => u.Position().Y() == y))
                {
                    healths.Add(u.Health().ToString());
                }

                Console.WriteLine($"{line}    {string.Join(" ", healths)}");
            }
        }

        public int Run(bool endOnElfDeath)
        {
            var victor = '?';
            var deltas = new List<Point2D>() { new Point2D(0, -1), new Point2D(-1, 0), new Point2D(1, 0), new Point2D(0, 1) };
            while (true)
            {
                var occupied = new HashSet<Point2D>(_units.Select(u => u.Position()).ToList());
                foreach (var unit in _units)
                {
                    if (unit.Health() <= 0)
                    {   // unit was killed before it can take its turn
                        continue;
                    }
                    
                    // has targets?
                    var targets = _units.Where(u => u.Health() > 0 && u.Type() != unit.Type()).ToList();
                    if (targets.Count == 0)
                    {   // no more targets! victor has been reached
                        victor = unit.Type();
                        break;
                    }

                    // targets in range?
                    var weakest = WeakestTarget(unit, targets);
                    if (weakest is null)
                    {   // no attack can be made yet made....can move to targets?
                        ISearchPath? shortest = null;
                        foreach (var target in targets)
                        {
                            foreach (var endDelta in deltas)
                            {
                                var targetPosition = target.Position() + endDelta;
                                if (_map.ContainsKey(targetPosition) && _map[targetPosition] == '.' && !occupied.Contains(targetPosition))
                                {   // position is in range...find shortest path from each starting step to see if it is reachable
                                    foreach (var startDelta in deltas)
                                    {
                                        var startPosition = unit.Position() + startDelta;
                                        if (_map.ContainsKey(startPosition) && _map[startPosition] == '.' && !occupied.Contains(startPosition))
                                        {
                                            var end = new MeleeSearchState(_map, occupied, targetPosition, 0, 0, 99999);
                                            var start = new MeleeSearchState(_map, occupied, startPosition, 0, 0, 99999);
                                            var bfs = new AStar(start, end);
                                            var path = bfs.FindPath();

                                            if (path.SearchStates().Count > 0)
                                            {   // path found....replace shortest path of all targets if it is shortest
                                                if (shortest is null || shortest.Cost() > path.Cost())
                                                {
                                                    shortest = path;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        if (shortest is not null)
                        {
                            occupied.Remove(unit.Position());
                            unit.Move(((MeleeSearchState) shortest.SearchStates()[0]).Position());
                            occupied.Add(unit.Position());
                            
                            // targets in range now?
                            weakest = WeakestTarget(unit, targets);
                        }
                    }

                    // can attack target?
                    if (weakest is not null)
                    {   // weakest found...attack!
                        weakest.Damage(unit.Power());
                        if (weakest.Health() <= 0) { occupied.Remove(weakest.Position()); }
                    }
                }

                // remove dead units
                _elfDeaths += _units.Where(u => u.Type() == 'E' && u.Health() < 0).ToList().Count;
                _units = _units.Where(u => u.Health() > 0).ToList();

                if (victor != '?') { break; }
                if (endOnElfDeath && _elfDeaths > 0) { return 0; }

                // prioritize based on positions
                _units.Sort();
                _rounds++;
            }

            return _rounds * _units.Aggregate(0, (acc, u) => acc + (u.Type() == victor ? u.Health() : 0));
        }
    }
}