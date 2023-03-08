using adventofcode.common;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day24 : Solution
{
    private Dictionary<GroupUnitType, List<GroupUnit>> _groups;

    public Day24(string year, string day) : base(year, day)
    {
        Reset();
    }

    private void Reset()
    {
        _groups = new Dictionary<GroupUnitType, List<GroupUnit>>();
        _groups.Add(GroupUnitType.ImmuneSystem, new List<GroupUnit>());
        _groups.Add(GroupUnitType.Infection, new List<GroupUnit>());

        var type = GroupUnitType.ImmuneSystem;
        var i = 1;
        foreach (var line in LoadInputAsLines())
        {
            if (line == "" || line == "Immune System:")
            {
                continue;
            }
            if (line == "Infection:")
            {
                type = GroupUnitType.Infection;
                i = 1;
                continue;
            }

            var match = Regex.Match(line, @"(\d+) units each with (\d+) hit points .*with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)");

            var count = Convert.ToInt32(match.Groups[1].Value);
            var hp = Convert.ToInt32(match.Groups[2].Value);
            var attack = Convert.ToInt32(match.Groups[3].Value);
            var attackType = match.Groups[4].Value;
            var initiative = Convert.ToInt32(match.Groups[5].Value);

            var weaknesses = new List<string>();
            var immunities = new List<string>();
            if (line.Contains('('))
            {
                var match2 = Regex.Match(line, @"(\d+) units each with (\d+) hit points \((.*)\) with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)");
                foreach (var tmp in match2.Groups[3].Value.Split("; "))
                {
                    if (tmp.Substring(0, 8) == "weak to ")
                    {
                        weaknesses = tmp.Substring(8).Split(", ").ToList();
                    }
                
                    if (tmp.Substring(0, 10) == "immune to ")
                    {
                        immunities = tmp.Substring(10).Split(", ").ToList();
                    }
                }
            }

            _groups[type].Add(new GroupUnit(i, type, hp, attack, initiative, attackType, weaknesses, immunities, count));
            i++;
        }
    }

    public override string PartOne()
    {
        var iss = new ImmuneSystemSimulator(_groups[GroupUnitType.ImmuneSystem], _groups[GroupUnitType.Infection]);
        var winner = iss.Fight(true);

        Console.WriteLine($"\nwinner : {winner.First().Type()}");

        return Convert.ToString(winner.Aggregate(0, (acc, g) => acc + g.Count()));
    }

    public override string PartTwo()
    {
        var boost = 0;
        var unitsRemaining = 0;
        while (true)
        {
            Reset();
            
            boost++;
            Console.Write($"With boost {boost}.......");

            var iss = new ImmuneSystemSimulator(_groups[GroupUnitType.ImmuneSystem], _groups[GroupUnitType.Infection]);
            iss.Boost(boost);
            
            var winner = iss.Fight(false);
            Console.WriteLine($"winner is {winner.First().Type()}!");
            
            if (winner.First().Type() == GroupUnitType.ImmuneSystem)
            {
                unitsRemaining = winner.Aggregate(0, (acc, g) => acc + g.Count());
                break;
            }
        }

        return Convert.ToString(unitsRemaining);
    }

    private enum GroupUnitType
    {
        ImmuneSystem = 0, Infection = 1
    }

    private class GroupUnit : IComparable<GroupUnit>, IEquatable<GroupUnit>
    {
        private string _id;
        private GroupUnitType _type;
        private int _hp;
        private int _attack;
        private int _initiative;
        private string _attackType;
        private HashSet<string> _weakness;
        private HashSet<string> _immunity;
        private int _count;
        private int _boost;

        public GroupUnit(int i, GroupUnitType type, int hp, int attack, int inititiative, string attackType, List<string> weakness, List<string> immunity, int count)
        {
            _id = $"{type}-{i}";
            _type = type;
            _hp = hp;
            _attack = attack;
            _initiative = inititiative;
            _attackType = attackType;
            _weakness = new HashSet<string>(weakness);
            _immunity = new HashSet<string>(immunity);
            _count = count;
            _boost = 0;
        }
        
        public GroupUnitType Type() { return _type; }
        public int HP() { return _hp; }
        public int Attack() { return _attack + _boost; }
        public int Initiative() { return _initiative; }
        public string AttackType() { return _attackType; }
        public int Count() { return _count; }
        public HashSet<string> Weakness() { return _weakness; }
        public HashSet<string> Immunity() { return _immunity; }

        public void Boost(int boost)
        {
            _boost = boost;
        }

        public int EffectivePower()
        {
            return _count * Attack();
        }

        public int DamageMultiplier(string attackType)
        {
            return 1 * (_weakness.Contains(attackType) ? 2 : 1) * (_immunity.Contains(attackType) ? 0 : 1);
        }
        
        public int TakeDamage(int damage)
        {
            var unitsLost = damage / _hp;
            _count = Math.Max(0, _count - unitsLost);

            return unitsLost;
        }

        public int CompareTo(GroupUnit? other)
        {
            if (other is null) { throw new Exception("GroupUnit input is null"); }
            if (EffectivePower() < other.EffectivePower()) { return -1; }
            if (EffectivePower() > other.EffectivePower()) { return 1; }
            if (Initiative() < other.Initiative()) { return -1; }
            if (Initiative() > other.Initiative()) { return 1; }

            return 0;
        }
        
        public bool Equals(GroupUnit? other)
        {
            if (other is null) { return false; }
            return _id == other._id;
        }
    
        public override bool Equals(Object? other)
        {
            return other is GroupUnit && Equals((GroupUnit) other);
        }
    
        public override int GetHashCode()
        {
            return _id.GetHashCode();
        }

        public override string ToString()
        {
            return _id;
        }
    }

    private class ImmuneSystemSimulator
    {
        private List<GroupUnit> _immuneSystem;
        private List<GroupUnit> _infection;

        public ImmuneSystemSimulator(List<GroupUnit> immuneSystem, List<GroupUnit> infection)
        {
            _immuneSystem = immuneSystem;
            _infection = infection;
        }

        public void Boost(int boost)
        {
            foreach (var g in _immuneSystem)
            {
                g.Boost(boost);
            }
        }

        public List<GroupUnit> Fight(bool verbose)
        {
            var i = 1;
            while (_immuneSystem.Count > 0 && _infection.Count > 0)
            {
                if (verbose)
                {
                    Console.WriteLine($"\nbattle {i}");
                    Console.WriteLine("Immune System:");
                    if (_immuneSystem.Count > 0)
                    {
                        foreach (var g in _immuneSystem)
                        {
                            Console.Write($"Group {g} contains {g.Count()} units with {g.HP()} hp, {g.Attack()} {g.AttackType()} attack, and initiative {g.Initiative()} has effective power {g.EffectivePower()}. ");
                            Console.WriteLine($"[weak to {String.Join(", ", g.Weakness().ToList())}], [immune to {String.Join(", ", g.Immunity().ToList())}]");
                        }
                    }
                    else { Console.WriteLine("No groups remain"); }
                    
                    Console.WriteLine("Infection:");
                    if (_infection.Count > 0)
                    {
                        foreach (var g in _infection)
                        {
                            Console.Write($"Group {g} contains {g.Count()} units with {g.HP()} hp, {g.Attack()} {g.AttackType()} attack, and initiative {g.Initiative()} has effective power {g.EffectivePower()}. ");
                            Console.WriteLine($"[weak to {String.Join(", ", g.Weakness().ToList())}], [immune to {String.Join(", ", g.Immunity().ToList())}]");
                        }
                    }
                    else { Console.WriteLine("No groups remain"); }
                    Console.WriteLine("");
                }

                var selectOrder = new List<GroupUnit>();
                var availableImmuneSystemTargets = new HashSet<GroupUnit>();
                var availableInfectionTargets = new HashSet<GroupUnit>();
                foreach (var g in _immuneSystem)
                {
                    selectOrder.Add(g);
                    availableImmuneSystemTargets.Add(g);
                }
                foreach (var g in _infection)
                {
                    selectOrder.Add(g);
                    availableInfectionTargets.Add(g);
                }
                selectOrder.Sort();
                selectOrder.Reverse();
                
                var attackOrder = new PriorityQueue<(GroupUnit, GroupUnit), int>();

                // target selection phase
                foreach (var g in selectOrder)
                {
                    var targetPool = g.Type() == GroupUnitType.ImmuneSystem ? availableInfectionTargets : availableImmuneSystemTargets;
                    var bestDamage = 0;
                    GroupUnit? bestTarget = null;
                    foreach (var t in targetPool)
                    {
                        var damage = g.EffectivePower() * t.DamageMultiplier(g.AttackType());
                        if (bestTarget is null || damage > bestDamage)
                        {
                            bestDamage = damage;
                            bestTarget = t;
                            continue;
                        }
                        if (damage == bestDamage)
                        {
                            bestTarget = t.EffectivePower() > bestTarget.EffectivePower() || (t.EffectivePower() == bestTarget.EffectivePower() && t.Initiative() > bestTarget.Initiative()) ? t : bestTarget;
                        }
                    }
                    if (bestTarget != null && bestDamage > 0)
                    {   // target found...add attacker and defender to attack queue and remove defender from available targets
                        attackOrder.Enqueue((g, bestTarget), -g.Initiative());
                        targetPool.Remove(bestTarget);
                        if (verbose) { Console.WriteLine($"{g} group would deal {bestTarget} group {bestDamage} damage"); }
                    }
                }

                // attack phase
                if (verbose) { Console.WriteLine(""); }
                var totalUnitsLost = 0;
                while (attackOrder.Count > 0)
                {
                    var (attacker, defender) = attackOrder.Dequeue();
                    var damage = attacker.EffectivePower() * defender.DamageMultiplier(attacker.AttackType());
                    if (damage <= 0)
                    {   // attacker took lethal damage before it could attack and deals no damage...skip
                        continue;
                    }
                    var unitsLost = defender.TakeDamage(damage);
                    if (verbose) { Console.WriteLine($"{attacker} group attacks {defender} group {damage} damage, killing {unitsLost} units"); }

                    totalUnitsLost += unitsLost;
                }
                
                // clean up
                _immuneSystem = _immuneSystem.Where(g => g.EffectivePower() > 0).ToList();
                _infection = _infection.Where(g => g.EffectivePower() > 0).ToList();
                i++;

                if (totalUnitsLost == 0)
                {   // simulation ran into a stalemate...treat it as a loss
                    break;
                }
            }
            
            return _infection.Count > 0 ? _infection : _immuneSystem;
        }
    }
}