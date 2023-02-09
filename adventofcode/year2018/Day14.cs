using adventofcode.common;

namespace adventofcode.year2018;

public class Day14 : Solution
{
    private string _input;
    
    public Day14(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var hc = new HotChocolate();
        var recipes = Convert.ToInt32(_input);
        for (int i = 0; i < (recipes + 10); i++)
        {
            hc.CreateRecipe();
        }
        hc.Show();

        var allRecipes = hc.Recipes();
        return Convert.ToString(string.Join(string.Empty, Enumerable.Range(recipes, 10).Select(i => allRecipes[i]).ToList()));
    }

    public override string PartTwo()
    {
        var hc = new HotChocolate();
        var sequence = _input.ToList().Select(c => Convert.ToInt32(c.ToString())).ToList();

        var recipeIndex = -1;
        var lastCheckedIndex = 0;
        var matchIndex = 0;
        while (true)
        {
            for (int i = 0; i < 1000; i++)
            {
                hc.CreateRecipe();
            }

            var recipes = hc.Recipes();
            while (lastCheckedIndex < recipes.Count)
            {
                if (sequence[matchIndex] == recipes[lastCheckedIndex])
                {
                    matchIndex++;
                    lastCheckedIndex++;
                    
                    if (matchIndex == sequence.Count)
                    {   // found
                        recipeIndex = lastCheckedIndex - sequence.Count;
                        break;
                    }
                }
                else
                {
                    if (matchIndex == 0)
                    {
                        lastCheckedIndex++;
                    }
                    else
                    {
                        matchIndex = 0;
                    }
                }
            }

            if (recipeIndex > -1)
            {
                break;
            }
        }

        return Convert.ToString(recipeIndex);
    }

    private class HotChocolate
    {
        private List<int> _recipes;
        private int[] _current;

        public HotChocolate()
        {
            _recipes = new List<int>(){3, 7};
            _current = new int[2];
            _current[0] = 0;
            _current[1] = 1;
        }

        public List<int> Recipes() { return _recipes; }

        public void Show()
        {
            var scores = new List<string>();
            for (int i = 0; i < _recipes.Count; i++)
            {
                if (i == _current[0])
                {
                    scores.Add($"({_recipes[i]})");
                    continue;
                }

                if (i == _current[1])
                {
                    scores.Add($"[{_recipes[i]}]");
                    continue;
                }

                scores.Add($"{_recipes[i]}");
            }
            
            Console.WriteLine(string.Join(" ", scores));
        }

        public void CreateRecipe()
        {
            foreach (var score in _current.Aggregate(0, (acc, i) => acc + _recipes[i]).ToString().ToCharArray().Select(c => c.ToString()).ToList())
            {
                _recipes.Add(Convert.ToInt32(score));
            }

            for (int i = 0; i < _current.Length; i++)
            {
                _current[i] = (_current[i] + _recipes[_current[i]] + 1) % _recipes.Count;
            }
        }
    }
}