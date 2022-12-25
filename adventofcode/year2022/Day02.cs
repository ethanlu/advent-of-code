using adventofcode.common;

namespace adventofcode.year2022;

public class Day02 : Solution
{
    private string[] _input;
    private Dictionary<char, int> _choiceScore = new Dictionary<char, int>() 
    {
        {'R', 1},
        {'P', 2},
        {'S', 3},
    };
    private Dictionary<char, int> _outcomeScore = new Dictionary<char, int>()
    {
        {'L', 0},
        {'D', 3},
        {'W', 6}
    };

    public Day02(string year, string day) : base(year, day)
    {
        _input = this.LoadInputAsLines();
    }

    public override string PartOne()
    {
        // rock    : A, X
        // paper   : B, Y
        // scissor : C, Z
        Dictionary<char, char> choiceMap = new Dictionary<char, char>()
        {
            {'A', 'R'},
            {'B', 'P'},
            {'C', 'S'},
            {'X', 'R'},
            {'Y', 'P'},
            {'Z', 'S'},
        };
    
        var score = 0;
        foreach (var play in _input)
        {
            var opponent = choiceMap[play[0]];
            var you = choiceMap[play[2]];

            // add score based on your choice
            score += _choiceScore[you];
            
            if (opponent == you)
            {
                score += _outcomeScore['D'];
            }
            
            // add score based on outcome
            switch (opponent)
            {
                case 'R':
                    score += you == 'P' ? _outcomeScore['W'] : _outcomeScore['L'];
                    break;
                case 'P':
                    score += you == 'S' ? _outcomeScore['W'] : _outcomeScore['L'];
                    break;
                default:
                    score += you == 'R' ? _outcomeScore['W'] : _outcomeScore['L'];
                    break;
            }
        }

        return Convert.ToString(score);
    }

    public override string PartTwo()
    {
        // rock    : A
        // paper   : B
        // scissor : C
        // lose    : X
        // draw    : Y
        // win     : Z
        Dictionary<char, char> choiceMap = new Dictionary<char, char>()
        {
            {'A', 'R'},
            {'B', 'P'},
            {'C', 'S'},
            {'X', 'L'},
            {'Y', 'D'},
            {'Z', 'W'},
        };
    
        var score = 0;
        foreach (var play in _input)
        {
            var opponent = choiceMap[play[0]];
            var outcome = choiceMap[play[2]];

            // add score based on outcome
            score += _outcomeScore[outcome];

            var you = opponent == 'R' ? 'P' : opponent == 'P' ? 'S' : 'R';
            // add score based on choice
            switch (outcome)
            {
                case 'D':
                    you = opponent;
                    break;
                case 'L':
                    you = opponent == 'R' ? 'S' : opponent == 'P' ? 'R' : 'P';
                    break;
            }
            score += _choiceScore[you];
            
        }

        return Convert.ToString(score);
    }
}