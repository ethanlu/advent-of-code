using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace solution.year2022
{
    public class Day07 : Solution
    {
        private string[] input;
        private Directory root;

        public Day07(string year, string day) : base(year, day)
        {
            this.input = this.LoadInputAsLines();
            this.buildFileSystem();
        }

        private void buildFileSystem()
        {
            this.root = new Directory();
            var currentDirectory = this.root;
            foreach (var line in this.input)
            {
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
                                    currentDirectory = this.root;
                                    break;
                                case "..":
                                    currentDirectory = currentDirectory.Parent;
                                    break;
                                default:
                                    currentDirectory = currentDirectory.Directories[target];
                                    break;
                            }
                            break;
                        case "ls":
                            // do nothing
                            break;
                        default:
                            throw new Exception($"Unrecognized command : {command}");
                    }
                    continue;
                }
                else
                {
                    // showing directory info
                    var parts = line.Split(' ');
                    if (parts[0] == "dir")
                    {
                        var tmp = new Directory();
                        tmp.Name = parts[1];
                        tmp.Parent = currentDirectory;
                        currentDirectory.Directories.Add(tmp.Name, tmp);
                    }
                    else
                    {
                        var tmp = new File();
                        tmp.Name = parts[1];
                        tmp.Size = Convert.ToInt64(parts[0]);
                        currentDirectory.Files.Add(tmp.Name, tmp);
                    }
                    continue;
                }
            }
        }

        public override string PartOne()
        {
            var remainingDirectories = new Stack<Directory>();
            remainingDirectories.Push(this.root);

            var total = 0L;
            while (remainingDirectories.Count > 0)
            {
                var dir = remainingDirectories.Pop();
                var dirsize = dir.Size();
                if (dirsize <= 100000L)
                {
                    total += dirsize;
                }

                foreach (var d in dir.Directories.Values)
                {
                    remainingDirectories.Push(d);
                }
            }

            return System.Convert.ToString(total);
        }

        public override string PartTwo()
        {
            var freeSpaceNeeded = Math.Abs(40000000L - this.root.Size());
            var candidateDirectorySize = new List<long>();
            
            var remainingDirectories = new Stack<Directory>();
            remainingDirectories.Push(this.root);
            while (remainingDirectories.Count > 0)
            {
                var dir = remainingDirectories.Pop();
                var dirsize = dir.Size();
                
                if (dirsize >= freeSpaceNeeded)
                {
                    candidateDirectorySize.Add(dirsize);
                }

                foreach (var d in dir.Directories.Values)
                {
                    remainingDirectories.Push(d);
                }
            }
            candidateDirectorySize.Sort();

            return System.Convert.ToString(candidateDirectorySize.First());
        }
    }

    internal class File
    {
        private string _name;
        private long _size;
        
        public string Name
        {
            get => _name;
            set => _name = value;
        }
        
        public long Size
        {
            get => _size;
            set => _size = value;
        }
    }

    internal class Directory
    {
        private string _name;
        private long _size = -1L;
        private Directory _parent = null;
        private Dictionary<string, Directory> _directories = new Dictionary<string, Directory>();
        private Dictionary<string, File> _files = new Dictionary<string, File>();

        public string Name
        {
            get => _name;
            set => _name = value;
        }

        public Directory Parent
        {
            get => _parent;
            set => _parent = value;
        }

        public Dictionary<string, Directory> Directories
        {
            get => _directories;
        }
        
        public Dictionary<string, File> Files
        {
            get => _files;
        }

        public long Size()
        {
            if (_size < 0)
            {
                var total = 0L;
                foreach (var f in _files)
                {
                    total += f.Value.Size;
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