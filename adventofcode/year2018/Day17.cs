using adventofcode.common;
using adventofcode.common.grid;
using adventofcode.common.util;
using System.Text.RegularExpressions;

namespace adventofcode.year2018;

public class Day17 : Solution
{
    private HashSet<Point2D> _clay;

    public Day17(string year, string day) : base(year, day)
    {
        _clay = new HashSet<Point2D>();
        foreach (var line in LoadInputAsLines())
        {
            var match = Regex.Match(line, @"(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)");
            var v1 = Convert.ToInt32(match.Groups[2].Value);
            var startV2 = Convert.ToInt32(match.Groups[4].Value);
            var endV2 = Convert.ToInt32(match.Groups[5].Value);
            for (int v2 = startV2; v2 <= endV2; v2++)
            {
                _clay.Add(new Point2D(match.Groups[1].Value == "x" ? v1 : v2, match.Groups[1].Value == "x" ? v2 : v1));
            }
        }
    }

    public override string PartOne()
    {
        var wf = new WaterFall(_clay, new Point2D(500, 0));
        wf.Run();
        wf.Show();
        return Convert.ToString(wf.WaterTiles(false));
    }

    public override string PartTwo()
    {
        var wf = new WaterFall(_clay, new Point2D(500, 0));
        wf.Run();
        return Convert.ToString(wf.WaterTiles(true));
    }
    
    private class WaterFall
    {
        private const int Margin = 2;

        private char[,] _ground;
        private int _width;
        private int _height;
        private int _minX;
        private int _maxX;
        private int _maxY;
        private Point2D _waterSource;

        public WaterFall(HashSet<Point2D> clay, Point2D waterSource)
        {
            _minX = clay.Aggregate(99999, (acc, p) => acc > p.X() ? p.X() : acc) - 1;
            _maxX = clay.Aggregate(0, (acc, p) => acc < p.X() ? p.X() : acc) + 1;
            _maxY = clay.Aggregate(0, (acc, p) => acc < p.Y() ? p.Y() : acc) + 1;
            _width = _maxX - _minX + Margin * 2 - 1;
            _height = _maxY + Margin;

            var offsetX = -_minX + Margin - 1;
            
            _ground = new char[_width, _height];
            for (int x = 0; x < _width; x++)
            {
                for (int y = 0; y < _height; y++)
                {
                    _ground[x, y] = '.';
                }
            }
            foreach (var p in clay)
            {
                _ground[p.X() + offsetX, p.Y()] = '#';
            }
            _waterSource = new Point2D(waterSource.X() + offsetX, waterSource.Y());
            _ground[_waterSource.X(), _waterSource.Y()] = '+';
        }

        public void Show()
        {
            Draw<char>.ShowGrid(_ground);
        }

        public int WaterTiles(bool atRestOnly)
        {
            var water = 0;
            for (int x = 0; x < _width; x++)
            {
                for (int y = 1; y < _maxY - 1; y++)
                {
                    water += _ground[x, y] == '~' || (_ground[x, y] == '|' && !atRestOnly) ? 1 : 0;
                }
            }

            return water;
        }

        public void Run()
        {
            var downFlows = new Queue<Point2D>();
            downFlows.Enqueue(_waterSource + new Point2D(0, 1));
            
            while (downFlows.Count > 0)
            {
                var water = downFlows.Dequeue();
                var waterY = water.Y();
                var waterX = water.X();

                if (_ground[waterX, waterY] == '~')
                {
                    downFlows.Enqueue(new Point2D(waterX, waterY - 1));
                    continue;
                }

                var flowDone = false;
                while (true)
                {   // water flows down until it reaches clay, standstill water, or the abyss
                    var nextWaterY = waterY + 1;
                    if (nextWaterY > _maxY) 
                    {   // reached maxY...no need to progress further
                        flowDone = true;
                        break;
                    }
                    if (_ground[waterX, nextWaterY] == '|')
                    {   // reached a downflow already...no need to progress further
                        _ground[waterX, waterY] = '|';
                        flowDone = true;
                        break;
                    }
                    if (_ground[waterX, nextWaterY] == '.')
                    {   // can move down...update current ground tile to water flow and add candidate to queue
                        _ground[waterX, waterY] = '|';
                        waterY = nextWaterY;
                        continue;
                    }
                    break;
                }
                if (flowDone) { continue; }

                // reached clay or standstill water, so try to move left and right until can move down again
                var sideFlows = new List<int>();
                sideFlows.Add(waterX);
                
                // see if left can flow
                var leftWaterX = waterX;
                var leftCanFlow = true;
                while (leftCanFlow)
                {
                    leftWaterX += -1;
                    if (_ground[leftWaterX, waterY] == '.' || _ground[leftWaterX, waterY] == '|')
                    {
                        sideFlows.Add(leftWaterX);
                        if (_ground[leftWaterX, waterY + 1] == '.')
                        {   // after moving left, it can flow downward so add it to flow queue
                            downFlows.Enqueue(new Point2D(leftWaterX, waterY + 1));
                            break;
                        }
                        if (_ground[leftWaterX, waterY + 1] == '|')
                        {   // after moving left, there is an already a downflow so no need to proceed further
                            break;
                        }
                        continue;
                    }
                    leftCanFlow = false;
                }
                
                // see if right can flow
                var rightWaterX = waterX;
                var rightCanFlow = true;
                while (rightCanFlow)
                {
                    rightWaterX += 1;
                    if (_ground[rightWaterX, waterY] == '.' || _ground[rightWaterX, waterY] == '|')
                    {
                        sideFlows.Add(rightWaterX);
                        if (_ground[rightWaterX, waterY + 1] == '.')
                        {   // after moving right, it can flow downward so add it to flow queue
                            downFlows.Enqueue(new Point2D(rightWaterX, waterY + 1));
                            break;
                        }
                        if (_ground[rightWaterX, waterY + 1] == '|')
                        {   // after moving right, there is an already a downflow so no need to proceed further 
                            break;
                        }
                        continue;
                    }
                    rightCanFlow = false;
                }
                
                var c = '|';
                if (!leftCanFlow && !rightCanFlow)
                {   // cannot flow left or right, so add water source to down flow
                    downFlows.Enqueue(new Point2D(waterX, waterY - 1));
                    c = '~';
                }
                foreach (var sideFlowX in sideFlows)
                {
                    _ground[sideFlowX, waterY] = c;
                }
            }
        }
    }
}