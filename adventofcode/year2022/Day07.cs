using adventofcode.common;

namespace adventofcode.year2022;

public class Day07 : Solution
{
    private Directory _root;

    public Day07(string year, string day) : base(year, day)
    {
        var input = LoadInputAsLines();
        _root = new Directory(null);
        
        var currentDirectory = _root;
        foreach (var line in input)
        {
            if (currentDirectory is null)
            {
                throw new Exception("Current Directory is unexpectedly null!");
            }
            if (line[0] == '$')
            {
                var command = line.Substring(2, 2);
                switch (command)
                {
                    case "cd":
                        var target = line.Substring(5);
                        switch (target)
                        {
                            case "/":
                                currentDirectory = _root;
                                break;
                            case "..":
                                currentDirectory = currentDirectory.Parent();
                                break;
                            default:
                                currentDirectory = currentDirectory.Directories()[target];
                                break;
                        }
                        break;
                    case "ls":
                        // do nothing
                        break;
                    default:
                        throw new Exception($"Unrecognized command : {command}");
                }
            }
            else
            {
                // showing directory info
                var parts = line.Split(' ');
                if (parts[0] == "dir")
                {
                    currentDirectory.Directories().Add(parts[1], new Directory(currentDirectory));
                }
                else
                {
                    currentDirectory.Files().Add(parts[1], new File(Convert.ToInt64(parts[0])));
                }
            }
        }
    }
    
    public override string PartOne()
    {
        var remainingDirectories = new Stack<Directory>();
        remainingDirectories.Push(_root);

        var total = 0L;
        while (remainingDirectories.Count > 0)
        {
            var dir = remainingDirectories.Pop();
            var dirSize = dir.Size();
            if (dirSize <= 100000L)
            {
                total += dirSize;
            }

            foreach (var d in dir.Directories().Values)
            {
                remainingDirectories.Push(d);
            }
        }

        return Convert.ToString(total);
    }

    public override string PartTwo()
    {
        var freeSpaceNeeded = Math.Abs(40000000L - _root.Size());
        var candidateDirectorySize = new List<long>();
        
        var remainingDirectories = new Stack<Directory>();
        remainingDirectories.Push(_root);
        while (remainingDirectories.Count > 0)
        {
            var dir = remainingDirectories.Pop();
            var dirSize = dir.Size();
            
            if (dirSize >= freeSpaceNeeded)
            {
                candidateDirectorySize.Add(dirSize);
            }

            foreach (var d in dir.Directories().Values)
            {
                remainingDirectories.Push(d);
            }
        }
        candidateDirectorySize.Sort();

        return Convert.ToString(candidateDirectorySize.First());
    }
    
    private class File
    {
        private long _size;

        public File(long size)
        {
            _size = size;
        }

        public long Size()
        {
            return _size;
        }
    }

    private class Directory
    {
        private long _size;
        private Directory? _parent;
        private Dictionary<string, Directory> _directories;
        private Dictionary<string, File> _files;

        public Directory(Directory? parent)
        {
            _size = -1L;
            _parent = parent;
            _directories = new Dictionary<string, Directory>();
            _files = new Dictionary<string, File>();
        }

        public Directory? Parent()
        {
            return _parent;
        }

        public Dictionary<string, Directory> Directories()
        {
            return _directories;
        }
    
        public Dictionary<string, File> Files()
        {
            return _files;
        }

        public long Size()
        {
            if (_size < 0)
            {
                var total = 0L;
                foreach (var f in _files)
                {
                    total += f.Value.Size();
                }
                foreach (var d in _directories)
                {
                    total += d.Value.Size();
                }

                _size = total;
            }

            return _size;
        }
    }
}