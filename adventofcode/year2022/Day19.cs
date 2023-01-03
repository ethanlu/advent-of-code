using adventofcode.common;
using adventofcode.common.graph.search;
using System.Text.RegularExpressions;

namespace adventofcode.year2022;

public class Day19 : Solution
{
    private List<(string, Dictionary<string, int>, Dictionary<string, int>, BluePrint)> _startDetails;
    
    public Day19(string year, string day) : base(year, day)
    {
        _startDetails = new List<(string, Dictionary<string, int>, Dictionary<string, int>, BluePrint)>();
        foreach (var input in LoadInputAsLines())
        {
            var match = Regex.Match(input, @"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.");
            var id = match.Groups[1].Value;

            _startDetails.Add((
                id,
                new Dictionary<string, int>()
                {
                    {K.Ore, 0},
                    {K.Clay, 0},
                    {K.Obsidian, 0},
                    {K.Geode, 0},
                },
                new Dictionary<string, int>()
                {
                    {K.Ore, 1},
                    {K.Clay, 0},
                    {K.Obsidian, 0},
                    {K.Geode, 0},
                },
                new BluePrint(Convert.ToInt32(id), new Dictionary<string, Robot>()
                {
                    {K.Ore, new Robot(Convert.ToInt32(match.Groups[2].Value), 0, 0)},
                    {K.Clay, new Robot(Convert.ToInt32(match.Groups[3].Value), 0, 0)},
                    {K.Obsidian, new Robot(Convert.ToInt32(match.Groups[4].Value), Convert.ToInt32(match.Groups[5].Value), 0)},
                    {K.Geode, new Robot(Convert.ToInt32(match.Groups[6].Value), 0, Convert.ToInt32(match.Groups[7].Value))},
                }))
            );
        }
    }

    public override string PartOne()
    {
        var maxTime = 24;
        var bestBuildOrders = new List<SearchPath>();
        foreach (var (id, resources, robots, blueprint) in _startDetails)
        {
            var buildState = new BuildState(id,0, 0, maxTime, 1, resources, robots, blueprint);
            
            var start = new SearchPath();
            start.Add(buildState);

            var bfs = new BFS(start, maxTime);
            var buildOrders = bfs.FindPath();

            bestBuildOrders.Add((SearchPath) buildOrders);
        }

        var qualityLevel = 0;
        foreach (var bo in bestBuildOrders)
        {
            Console.WriteLine($"Best blueprint #{((BuildState) bo.SearchStates().Last()).BluePrintId()} : {bo}");
            qualityLevel += bo.Gain() * Convert.ToInt32(((BuildState) bo.SearchStates().Last()).BluePrintId());
        }

        return Convert.ToString(qualityLevel);
    }

    public override string PartTwo()
    {
        var maxTime = 32;
        var bestBuildOrders = new List<SearchPath>();
        foreach (var (id, resources, robots, blueprint) in _startDetails.Take(3))
        {
            var buildState = new BuildState(id,0, 0, maxTime, 1, resources, robots, blueprint);
            
            var start = new SearchPath();
            start.Add(buildState);

            var bfs = new BFS(start, maxTime);
            var buildOrders = bfs.FindPath();

            bestBuildOrders.Add((SearchPath) buildOrders);
        }

        var qualityLevel = 1;
        foreach (var bo in bestBuildOrders)
        {
            Console.WriteLine($"Best blueprint #{((BuildState) bo.SearchStates().Last()).BluePrintId()} : {bo}");
            qualityLevel *= bo.Gain();
        }

        return Convert.ToString(qualityLevel);
    }
}

internal static class K
{
    public const string Ore = "ore";
    public const string Clay = "clay";
    public const string Obsidian = "obsidian";
    public const string Geode = "geode";
}

internal class Robot
{
    private Dictionary<string, int> _resourceCost;

    public Robot(int oreCost, int clayCost, int obsidianCost)
    {
        _resourceCost = new Dictionary<string, int>() {{K.Ore, oreCost}, {K.Clay, clayCost}, {K.Obsidian, obsidianCost}};
    }

    public int Cost(string resource) { return _resourceCost[resource]; }
}

internal class BluePrint
{
    private int _id;
    private Dictionary<string, Robot> _blueprints;
    private Dictionary<string, int> _maxResourceCost;

    public BluePrint(int id, Dictionary<string, Robot> blueprints)
    {
        _id = id;
        _blueprints = blueprints;
        _maxResourceCost = new Dictionary<string, int>()
        {
            {K.Ore, Math.Max(Math.Max(_blueprints[K.Clay].Cost(K.Ore), _blueprints[K.Obsidian].Cost(K.Ore)), _blueprints[K.Geode].Cost(K.Ore))},
            {K.Clay, _blueprints[K.Obsidian].Cost(K.Clay)},
            {K.Obsidian, _blueprints[K.Geode].Cost(K.Obsidian)}
        };
    }

    public int Id() { return _id; }

    public Robot GetBluePrint(string robot) { return _blueprints[robot]; }

    public int MaxResourceRobotNeeded(string resource) { return _maxResourceCost[resource]; }
}

internal class BuildState : SearchState
{
    private Dictionary<string, int> _resources;
    private Dictionary<string, int> _robots;
    private BluePrint _robotBluePrint;
    
    public BuildState(
        string id, int gain, int cost, int maxCost,
        int timeSkip,
        Dictionary<string, int> resources,
        Dictionary<string, int> robots,
        BluePrint robotBluePrint,
        string buildRobot=""
    ) : base (id, gain, cost, maxCost)
    {
        _resources = new Dictionary<string, int>(resources);
        _robots = new Dictionary<string, int>(robots);
        _robotBluePrint = robotBluePrint;
        
        // update resource totals
        foreach (var (robot, amount) in _robots)
        {
            _resources[robot] += amount * timeSkip;
        }

        _cost += timeSkip;
        _gain = _resources[K.Geode];

        if (buildRobot != "")
        {
            _resources[K.Ore] -= _robotBluePrint.GetBluePrint(buildRobot).Cost(K.Ore);
            _resources[K.Clay] -= _robotBluePrint.GetBluePrint(buildRobot).Cost(K.Clay);
            _resources[K.Obsidian] -= _robotBluePrint.GetBluePrint(buildRobot).Cost(K.Obsidian);
            _robots[buildRobot]++;
        }

        _id = $"[{_gain}:{_cost}]({string.Join(",", _resources.Values)})({string.Join(",", _robots.Values)})";
    }

    public int BluePrintId() { return _robotBluePrint.Id(); }

    private bool CanBuild(string robot)
    {
        // can build if available resources allow it
        return _resources[K.Ore] >= _robotBluePrint.GetBluePrint(robot).Cost(K.Ore) && 
               _resources[K.Clay] >= _robotBluePrint.GetBluePrint(robot).Cost(K.Clay) && 
               _resources[K.Obsidian] >= _robotBluePrint.GetBluePrint(robot).Cost(K.Obsidian);
    }

    private bool ShouldBuild(string robot)
    {
        // only need to build as many resource robot as needed based on maximum cost of each resource
        return _robots[robot] < _robotBluePrint.MaxResourceRobotNeeded(robot);
    }

    public override int PotentialGain()
    {
        return Enumerable.Range(0, _maxCost - _cost).Aggregate(0, (acc, i) => acc + i + _resources[K.Geode]);
    }

    public override List<ISearchState> NextSearchStates(ISearchState? previousSearchState)
    {
        var nextBases = new List<ISearchState>();
        var timeNeeded = 1;
        var builtSomething = false;

        // geode robot should always be built asap
        if (CanBuild(K.Geode))
        {
            // have enough resources to build
            nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint, K.Geode));
            builtSomething = true;
        }
        else if (_robots[K.Obsidian] > 0)
        {
            // not enough resources, but necessary robots in place to timeskip
            timeNeeded = Math.Max(
                (_robotBluePrint.GetBluePrint(K.Geode).Cost(K.Ore) - _resources[K.Ore] + _robots[K.Ore] - 1) / _robots[K.Ore],
                (_robotBluePrint.GetBluePrint(K.Geode).Cost(K.Obsidian) - _resources[K.Obsidian] +_robots[K.Obsidian] - 1) / _robots[K.Obsidian]
            ) + 1;

            if (timeNeeded > 0 && timeNeeded < _maxCost - _cost)
            {
                nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint, K.Geode));
                builtSomething = true;
            }
        }

        if (ShouldBuild(K.Obsidian))
        {
            if (CanBuild(K.Obsidian))
            {
                timeNeeded = 1;
                nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint, K.Obsidian));
                builtSomething = true;
            }
            else if (_robots[K.Clay] > 0)
            {
                timeNeeded = Math.Max(
                    (_robotBluePrint.GetBluePrint(K.Obsidian).Cost(K.Ore) - _resources[K.Ore] + _robots[K.Ore] - 1) / _robots[K.Ore],
                    (_robotBluePrint.GetBluePrint(K.Obsidian).Cost(K.Clay) - _resources[K.Clay] + _robots[K.Clay] - 1) / _robots[K.Clay]
                ) + 1;

                if (timeNeeded > 0 && timeNeeded < _maxCost - _cost)
                {
                    nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint, K.Obsidian));
                    builtSomething = true;
                }
            }
        }

        // only build other robots when possible and have not reached max needed
        foreach (var robot in new List<string>() {K.Clay, K.Ore})
        {
            if (ShouldBuild(robot))
            {
                if (CanBuild(robot))
                {
                    timeNeeded = 1;
                    nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint, robot));
                    builtSomething = true;
                }
                else
                {
                    timeNeeded = (_robotBluePrint.GetBluePrint(robot).Cost(K.Ore) - _resources[K.Ore] + _robots[K.Ore] - 1) / _robots[K.Ore] + 1;

                    if (timeNeeded > 0 && timeNeeded < _maxCost - _cost)
                    {
                        nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint, robot));
                        builtSomething = true;
                    }
                }
            }
        }

        if (!builtSomething)
        {
            // we were not able to build anything immediately next turn nor do any time skip...so only resort is to idle
            timeNeeded = 1;
            nextBases.Add(new BuildState(_id, _gain, _cost, _maxCost, timeNeeded, _resources, _robots, _robotBluePrint));
        }

        return nextBases;
    }

    public override string ToString()
    {
        return _id;
    }
}