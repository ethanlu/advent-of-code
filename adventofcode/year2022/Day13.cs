using adventofcode.common;
using System.Text.Json;

namespace adventofcode.year2022;

public class Day13 : Solution
{
    private JsonElement[] _left;
    private JsonElement[] _right;
    
    public Day13(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();

        _left = new JsonElement[(input.Length + 1) / 3];
        _right = new JsonElement[(input.Length + 1) / 3];
        for (int i = 0; i < input.Length; i+=3)
        {
            _left[i / 3] = JsonSerializer.Deserialize<JsonElement>(input[i]);
            _right[i / 3] = JsonSerializer.Deserialize<JsonElement>(input[i + 1]);
        }
    }

    public override string PartOne()
    {
        var comparer = new PacketComparer();
        
        var order = 0;
        for (int i = 0; i < _left.Length; i++)
        {
            order += comparer.Compare(_left[i], _right[i]) < 0 ? i + 1: 0;
        }

        return Convert.ToString(order);
    }

    public override string PartTwo()
    {
        var items = new JsonElement[_left.Length * 2 + 2];
        items[0] = JsonSerializer.Deserialize<JsonElement>("[[2]]");
        items[1] = JsonSerializer.Deserialize<JsonElement>("[[6]]");
        _left.CopyTo(items, 2);
        _right.CopyTo(items, 2 + _left.Length);
        
        Array.Sort(items, new PacketComparer());

        var key1 = 0;
        var key2 = 0;
        for (int i = 0; i < items.Length; i++)
        {
            if (items[i].ToString() == "[[2]]")
            {
                key1 = i + 1;
            }
            if (items[i].ToString() == "[[6]]")
            {
                key2 = i + 1;
            }
        }

        return Convert.ToString(key1 * key2);
    }
}

internal class PacketComparer : IComparer<JsonElement>
{
    public int Compare(JsonElement a, JsonElement b)
    {
        int _Compare(JsonElement[] left, JsonElement[] right)
        {
            for (int i = 0; i < Math.Min(left.Length, right.Length); i++)
            {
                var l = left[i];
                var r = right[i];
                
                if (l.ValueKind == r.ValueKind)
                {
                    switch (l.ValueKind)
                    {
                        case JsonValueKind.Array:
                            switch (_Compare(l.EnumerateArray().ToArray(), r.EnumerateArray().ToArray()))
                            {
                                case -1:
                                    return -1;
                                case 1:
                                    return 1;
                            }
                            break;
                        case JsonValueKind.Number:
                            if (l.GetInt32() > r.GetInt32())
                            {
                                return 1;
                            }
                            if (l.GetInt32() < r.GetInt32())
                            {
                                return -1;
                            }
                            break;
                        default:
                            throw new Exception($"Unhandled JSON type: {l.ValueKind}");
                    }
                }
                else
                {
                    switch (_Compare(
                                l.ValueKind != JsonValueKind.Array ? new JsonElement[1]{l} : l.EnumerateArray().ToArray(), 
                                r.ValueKind != JsonValueKind.Array ? new JsonElement[1]{r} : r.EnumerateArray().ToArray()))
                    {
                        case -1:
                            return -1;
                        case 1:
                            return 1;
                    }
                }
            }

            // compare item length to determine order
            if (left.Length > right.Length)
            {
                return 1;
            }
            if (left.Length < right.Length)
            {
                return -1;
            }

            return 0;
        }

        return  _Compare(a.EnumerateArray().ToArray(), b.EnumerateArray().ToArray());
    }
}