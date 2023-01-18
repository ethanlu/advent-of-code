namespace adventofcode.common;

public interface ISolution
{
    string PartOne();
    string PartTwo();
}

public abstract class Solution : ISolution
{
    private readonly Uri _inputPath;
        
    protected Solution(string year, string day)
    {
        if (Environment.GetEnvironmentVariable("ADVENT_OF_CODE_INPUT") is null)
        {
            throw new Exception("ADVENT_OF_CODE_INPUT environment variable is not set");
        }

        _inputPath = new Uri($"{Environment.GetEnvironmentVariable("ADVENT_OF_CODE_INPUT")}/{year}/day{day}.txt");
    }
        
    protected string LoadInputAsString()
    {
        return File.ReadAllText(_inputPath.AbsolutePath).Replace("\n", "").Trim();
    }

    protected string[] LoadInputAsLines()
    {
        return File.ReadAllLines(_inputPath.AbsolutePath);
    }

    public abstract string PartOne();
    public abstract string PartTwo();
}