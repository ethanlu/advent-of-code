using System.Collections;
using adventofcode.common;
using System.Text.RegularExpressions;

namespace adventofcode.year2022;

public class Day21 : Solution
{
    private List<(string, string)> _monkeys;
    
    public Day21(string year, string day) : base(year, day)
    {
        _monkeys = new List<(string, string)>();
        foreach (var line in LoadInputAsLines())
        {
            var monkey = line.Split(new string[] {": "}, StringSplitOptions.None);
            _monkeys.Add((monkey[0], monkey[1]));
        }
    }

    public override string PartOne()
    {
        var riddle = new Riddle(_monkeys);
        var root = riddle.SolveRoot();
        return Convert.ToString(root);
    }

    public override string PartTwo()
    {
        var riddle = new Riddle(_monkeys);
        var human = riddle.SolveHuman();
        return Convert.ToString(human);
    }
}

internal class Riddle
{
    private Dictionary<string, long> _answered;
    private Dictionary<string, (string, char, string)> _waiting;
    private Dictionary<string, HashSet<string>> _notification;

    public Riddle(List<(string, string)> monkeys)
    {
        _answered = new Dictionary<string, long>();
        _waiting = new Dictionary<string, (string, char, string)>();
        _notification = new Dictionary<string, HashSet<string>>();

        foreach (var (name, type) in monkeys)
        {
            var answeredMatch = Regex.Match(type, @"^-?\d+$");
            if (answeredMatch.Success)
            {
                // monkey just yells numbers...add it to answered
                _answered.Add(name, Convert.ToInt64(answeredMatch.Groups[0].Value));
            }
            else
            {
                var typeMatch = Regex.Match(type, @"([a-z]+) ([\+\-\*\/]) ([a-z]+)");
                var monkeyA = typeMatch.Groups[1].Value;
                var monkeyB = typeMatch.Groups[3].Value;
                var action = typeMatch.Groups[2].Value[0];
                
                // monkey is waiting for 2 other monkeys...adding it to waiting
                _waiting.Add(name, (monkeyA, action, monkeyB));

                foreach (var monkey in new List<string>() {monkeyA, monkeyB})
                {
                    if (!_notification.ContainsKey(monkey))
                    {
                        _notification.Add(monkey, new HashSet<string>()); 
                    }

                    // for the two monkeys that need to answer...add the waiting monkey to their notification list
                    _notification[monkey].Add(name);
                }
            }
        }
    }

    private void FollowUp(Queue<string> followUp)
    {
        while (followUp.Count != 0)
        {
            var answeredMonkey = followUp.Dequeue();

            // get all monkeys waiting for monkey that has an answer and see if they can get an answer as well
            foreach (var notifiedMonkey in _notification[answeredMonkey])
            {
                if (_answered.ContainsKey(notifiedMonkey))
                {
                    // notified monkey is already in answered so no need to followup
                    continue;
                }

                var (monkeyA, action, monkeyB) = _waiting[notifiedMonkey];
                if (_answered.ContainsKey(monkeyA) && _answered.ContainsKey(monkeyB))
                {
                    // notified monkey's dependents also have answers, so notified monkey can answer as well...add it to answered with answer
                    switch (action)
                    {
                        case '+':
                            _answered.Add(notifiedMonkey, _answered[monkeyA] + _answered[monkeyB]);
                            break;
                        case '-':
                            _answered.Add(notifiedMonkey, _answered[monkeyA] - _answered[monkeyB]);
                            break;
                        case '*':
                            _answered.Add(notifiedMonkey, _answered[monkeyA] * _answered[monkeyB]);
                            break;
                        case '/':
                            _answered.Add(notifiedMonkey, _answered[monkeyA] / _answered[monkeyB]);
                            break;
                        default:
                            throw new Exception($"Unhandled action : {action}");
                    }
                    
                    // remove notified monkey from waiting and add it to followup if it isnt root monkey
                    _waiting.Remove(notifiedMonkey);
                    if (notifiedMonkey != "root")
                    {
                        followUp.Enqueue(notifiedMonkey);
                    }
                }
                else
                {
                    // otherwise, notified monkey is still waiting for another dependent monkey to answer...
                }
            }
            
            // remove answered monkey's notification list
            _notification.Remove(answeredMonkey);
        }
    }

    private long FollowDown(string monkey, long aggregate)
    {
        if (monkey == "humn")
        {
            // reached humn so return aggregate
            return aggregate;
        }

        var answer = _answered.ContainsKey(_waiting[monkey].Item1) ? _answered[_waiting[monkey].Item1] : _answered[_waiting[monkey].Item3];
        var unknownMonkey = !_answered.ContainsKey(_waiting[monkey].Item1) ? _waiting[monkey].Item1 : _waiting[monkey].Item3;
        var action = _waiting[monkey].Item2;

        switch (action)
        {
            case '+':
                // answer + ? = aggregate --> ? = aggregate - answer
                // ? + answer = aggregate --> ? = answer + aggregate
                return FollowDown(unknownMonkey, aggregate - answer);
            case '-':
                if (_answered.ContainsKey(_waiting[monkey].Item1))
                {
                    // answer - ? = aggregate --> ? = answer - aggregate
                    return FollowDown(unknownMonkey, answer - aggregate);
                }
                // ? - answer = aggregate --> ? = aggregate + answer
                return FollowDown(unknownMonkey, aggregate + answer);
            case '*':
                // answer * ? = aggregate --> ? = aggregate / answer
                // ? * answer = aggregate --> ? = aggregate / answer
                return FollowDown(unknownMonkey, aggregate / answer);
            case '/':
                if (_answered.ContainsKey(_waiting[monkey].Item1))
                {
                    // answer / ? = aggregate --> ? = answer / aggregate
                    return FollowDown(unknownMonkey, answer / aggregate);
                }
                // ? / answer = aggregate --> ? = aggregate * answer
                return FollowDown(unknownMonkey, aggregate * answer);
            default:
                throw new Exception($"Unhandled action : {action}");
        }
    }
    
    public long SolveRoot()
    {
        FollowUp(new Queue<string>(_answered.Keys));
        return _answered["root"];
    }

    public long SolveHuman()
    {
        _answered.Remove("humn");
        var followUp = new Queue<string>(_answered.Keys);
        
        // simplify the nested equestion as much as possible by updating all waiting monkeys that do not depend on humn
        FollowUp(followUp);
        
        // once simplified, any monkey that is waiting should have answer from one of its dependents...so follow the monkey that is waiting while reversing the action to get to humn
        return FollowDown(
            !_answered.ContainsKey(_waiting["root"].Item1) ? _waiting["root"].Item1 : _waiting["root"].Item3,
            _answered.ContainsKey(_waiting["root"].Item1) ? _answered[_waiting["root"].Item1] : _answered[_waiting["root"].Item3]
        );
    }
}