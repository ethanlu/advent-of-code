namespace adventofcode.common.util;

public class IterTools<T>
{
    public static IEnumerable<List<T>> Permutation(List<T> items, int length = -1)
    {
        // https://docs.python.org/3/library/itertools.html#itertools.permutations
        length = length < 0 ? items.Count : length;
        if (length > items.Count)
        {
            yield return new List<T>();
            yield break;
        }

        var indices = Enumerable.Range(0, items.Count).ToArray();
        var cycles = Enumerable.Range(items.Count - length + 1, length).Reverse().ToArray();
        
        yield return new List<T>(items.GetRange(0, length));
        while (true)
        {
            var finished = true;
            
            foreach (var i in Enumerable.Range(0, length).Reverse())
            {
                cycles[i] -= 1;
                if (cycles[i] == 0)
                {
                    var tmp = indices[i];
                    for (int j = i; j < indices.Length - 1; j++)
                    {
                        indices[j] = indices[j + 1];
                    }
                    indices[indices.Length - 1] = tmp;
                    cycles[i] = items.Count - i;
                }
                else
                {
                    var k = cycles[i];
                    var tmp = indices[i];
                    indices[i] = indices[^k];
                    indices[^k] = tmp;

                    var permutation = new List<T>();
                    for (var x = 0; x < length; x++)
                    {
                        permutation.Add(items[indices[x]]);
                    }
                    
                    yield return permutation;
                    finished = false;
                    break;
                }
            }

            if (finished)
            {
                yield break;
            }
        }
    }

    public static IEnumerable<List<T>> Combination(List<T> items, int length=-1)
    {
        // https://docs.python.org/3/library/itertools.html#itertools.permutations
        length = length < 0 ? items.Count : length;
        if (length > items.Count)
        {
            yield return new List<T>();
            yield break;
        }

        var indices = Enumerable.Range(0, items.Count).ToArray();

        yield return new List<T>(items.GetRange(0, length));
        while (true)
        {
            var finished = true;

            var i = 0;
            foreach (var x in Enumerable.Range(0, length).Reverse())
            {
                i = x;
                if (indices[x] != x + items.Count - length)
                {
                    finished = false;
                    break;
                }
            }

            if (finished)
            {
                yield break;
            }

            indices[i] += 1;
            for (int j = i + 1; j < length; j++)
            {
                indices[j] = indices[j - 1] + 1;
            }

            var combination = new List<T>();
            for (var x = 0; x < length; x++)
            {
                combination.Add(items[indices[x]]);
            }
                    
            yield return combination;
        }
    } 
}