namespace adventofcode.common;

using System.Text.RegularExpressions;

public interface ISolution
{
    string PartOne();
    string PartTwo();
}

public abstract class Solution : ISolution
{
    private readonly string _inputPath;
        
    protected Solution(string year, string day)
    {
        var match = Regex.Match(AppDomain.CurrentDomain.BaseDirectory, @"^(.*/advent-of-code/adventofcode/)");
        if (!match.Success)
        {
            throw new Exception("Could not find base path for data file");
        }
            
        _inputPath = $"{match.Groups[1]}../input/{year}/day{day}.txt";
    }
        
    protected string LoadInputAsString()
    {
        return File.ReadAllText(_inputPath).Replace("\n", "").Trim();
    }

    protected string[] LoadInputAsLines()
    {
        return File.ReadAllLines(_inputPath);
    }

    public abstract string PartOne();
    public abstract string PartTwo();
}