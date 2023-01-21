using adventofcode.common;

namespace adventofcode.year2017;

public class Day09 : Solution
{
    private string _input;
    
    public Day09(string year, string day) : base(year, day)
    {
        _input = LoadInputAsString();
    }

    public override string PartOne()
    {
        var gs = new GarbageStream(_input);
        gs.Process();
        
        return Convert.ToString(gs.GroupScore());
    }

    public override string PartTwo()
    {
        var gs = new GarbageStream(_input);
        gs.Process();
        
        return Convert.ToString(gs.GarbageScore());
    }
    
    private enum StreamState
    {
        Free = 0, Group = 1, Garbage = 2, Ignore = 3
    }

    private class GarbageStream
    {
        private string _stream;
        private int _groupScore;
        private int _garbageScore;
        
        public GarbageStream(string stream)
        {
            _stream = stream;
            _groupScore = 0;
            _garbageScore = 0;
        }

        public int GroupScore()
        {
            return _groupScore;
        }

        public int GarbageScore()
        {
            return _garbageScore;
        }

        public void Process()
        {
            var stateStack = new Stack<(StreamState, int)>();
            stateStack.Push((StreamState.Free, 0));
            
            for (int i = 0; i < _stream.Length; i++)
            {
                switch (stateStack.Peek().Item1)
                {
                    case StreamState.Free:
                        switch (_stream[i])
                        {
                            case '{':   // starting group state, so increase score by 1
                                stateStack.Push((StreamState.Group, stateStack.Peek().Item2 + 1));
                                break;
                            case '<':   // starting garbage state
                                stateStack.Push((StreamState.Garbage, 0));
                                break;
                            case ',':   // group separator, so just skip
                                break;
                            default:
                                throw new Exception($"Unexpected character while in free state : {_stream[i]}");
                        }
                        break;
                    case StreamState.Group:
                        switch (_stream[i])
                        {
                            case '{':   // starting a nested group state, so increase score by 1
                                stateStack.Push((StreamState.Group, stateStack.Peek().Item2 + 1));
                                break;
                            case '}':   // closing a group state, add score to total score
                                _groupScore += stateStack.Pop().Item2;
                                break;
                            case '<':   // starting garbage state
                                stateStack.Push((StreamState.Garbage, 0));
                                break;
                        }
                        break;
                    case StreamState.Garbage:
                        switch (_stream[i])
                        {
                            case '>':   // closing garbage state
                                stateStack.Pop();
                                break;
                            case '!':   // starting an ignore state
                                stateStack.Push((StreamState.Ignore, 0));
                                break;
                            default:
                                _garbageScore++;
                                break;
                        }
                        break;
                    case StreamState.Ignore:
                        // in ignore state, so ignore this char and exit the ignore state to resume reading
                        stateStack.Pop();
                        continue;
                    default:
                        throw new Exception($"Invalid stream state : {stateStack.Peek().Item1}");
                }
            }
        }
    }
}