using System.Collections.Generic;

namespace solution.year2022
{
    public class Day02 : Solution
    {
        private string[] input;
        private Dictionary<char, int> choiceScore = new Dictionary<char, int>() 
        {
            {'R', 1},
            {'P', 2},
            {'S', 3},
        };
        private Dictionary<char, int> outcomeScore = new Dictionary<char, int>()
        {
            {'L', 0},
            {'D', 3},
            {'W', 6}
        };

        public Day02(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();
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
        
            int score = 0;
            char opponent = 'x';
            char you = 'x';
            for (int i = 0; i < this.input.Length; i++)
            {
                opponent = choiceMap[this.input[i][0]];
                you = choiceMap[this.input[i][2]];

                // add score based on your choice
                score += this.choiceScore[you];
                
                if (opponent == you)
                {
                    score += this.outcomeScore['D'];
                }
                
                // add score based on outcome
                if (opponent == 'R')
                {
                    score += you == 'P' ? this.outcomeScore['W'] : this.outcomeScore['L'];
                }
                if (opponent == 'P')
                {
                    score += you == 'S' ? this.outcomeScore['W'] : this.outcomeScore['L'];
                }
                if (opponent == 'S')
                {
                    score += you == 'R' ? this.outcomeScore['W'] : this.outcomeScore['L'];
                }
            }

            return System.Convert.ToString(score);
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
        
            int score = 0;
            char opponent = 'x';
            char outcome = 'x';
            char you = 'x';
            for (int i = 0; i < this.input.Length; i++)
            {
                opponent = choiceMap[this.input[i][0]];
                outcome = choiceMap[this.input[i][2]];

                // add score based on outcome
                score += this.outcomeScore[outcome];

                // add score based on choice
                if (outcome == 'D')
                {
                    you = opponent;
                }
                if (outcome == 'L')
                {
                    you = opponent == 'R' ? 'S' : opponent == 'P' ? 'R' : 'P';
                }
                if (outcome == 'W')
                {
                    you = opponent == 'R' ? 'P' : opponent == 'P' ? 'S' : 'R';
                }
                score += this.choiceScore[you];
                
            }

            return System.Convert.ToString(score);
        }
        
    }
}