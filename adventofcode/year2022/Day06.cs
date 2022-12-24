namespace adventofcode.year2022
{
    public class Day06 : Solution
    {
        private string _input;

        public Day06(string year, string day) : base(year, day)
        {
            _input = this.LoadInputAsString();
        }

        public override string PartOne()
        {
            var index = 0;
            Queue<char> sequence = new Queue<char>();
            foreach (char x in _input)
            {
                index++;
                
                sequence.Enqueue(x);
                if (index > 4)
                {
                    sequence.Dequeue();
                    
                    if (sequence.ToArray().Distinct().Count() == 4)
                    {
                        break;
                    }
                }
            }

            return Convert.ToString(index);
        }

        public override string PartTwo()
        {
            var index = 0;
            Queue<char> sequence = new Queue<char>();
            foreach (char x in _input)
            {
                index++;
                
                sequence.Enqueue(x);
                if (index > 14)
                {
                    sequence.Dequeue();
                    
                    if (sequence.ToArray().Distinct().Count() == 14)
                    {
                        break;
                    }
                }
            }

            return Convert.ToString(index);
        }
        
    }
}