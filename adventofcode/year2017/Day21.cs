using adventofcode.common;
using adventofcode.common.util;

namespace adventofcode.year2017;

public class Day21 : Solution
{
    private string[] _input;
    
    public Day21(string year, string day) : base(year, day)
    {
        _input = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var fa = new FractalArt(_input);

        for (int i = 0; i < 5; i++)
        {
            fa.Iterate();
        }
        fa.Display();
        
        return Convert.ToString(fa.OnPixels());
    }

    public override string PartTwo()
    {
        var fa = new FractalArt(_input);

        for (int i = 0; i < 18; i++)
        {
            fa.Iterate();
        }
        fa.Display();

        return Convert.ToString(fa.OnPixels());
    }

    private class Canvas : IEquatable<Canvas>
    {
        private char[,] _canvas;
        private int _size;
        
        public Canvas(string[] canvas)
        {
            _size = canvas.Length;
            _canvas = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    _canvas[x, y] = canvas[y][x];
                }
            }
        }

        public Canvas(char[,] canvas, int size)
        {
            _size = size;
            _canvas = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    _canvas[x, y] = canvas[x, y];
                }
            }
        }

        public char[,] Data() { return _canvas; }
        public int Size() { return _size; }

        public Canvas FlipY()
        {
            var canvas = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x <= _size / 2; x++)
                {
                    (canvas[x, y], canvas[_size - 1 - x, y]) = (_canvas[_size - 1 - x, y], _canvas[x, y]);
                }
            }
            return new Canvas(canvas, _size);
        }
        
        public Canvas FlipX()
        {
            var canvas = new char[_size, _size];
            for (int y = 0; y <= _size / 2; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    (canvas[x, y], canvas[x, _size - 1 - y]) = (_canvas[x, _size - 1 -  y], _canvas[x, y]);
                }
            }
            return new Canvas(canvas, _size);
        }

        public Canvas RotateLeft()
        {
            var canvas = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    canvas[x, y] = _canvas[_size - 1 - y, x];
                }
            }
            return new Canvas(canvas, _size);    
        }
        
        public Canvas RotateRight()
        {
            var canvas = new char[_size, _size];
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    canvas[x, y] = _canvas[y, _size - 1 - x];
                }
            }
            return new Canvas(canvas, _size);
        }

        public string Signature()
        {
            var sig = "";
            for (int y = 0; y < _size; y++)
            {
                for (int x = 0; x < _size; x++)
                {
                    sig += _canvas[x, y];
                }
            }
            return sig;
        }
        
        public bool Equals(Canvas? c)
        {
            if (c is null)
            {
                return false;
            }
            
            var sig = c.Signature();
            var startingSig = Signature();
            var candidate = this;
            do
            {
                if (candidate.Signature() == sig)
                {
                    return true;
                }

                if (candidate.FlipY().Signature() == sig)
                {
                    return true;
                }

                if (candidate.FlipX().Signature() == sig)
                {
                    return true;
                }

                candidate = candidate.RotateRight();
            } while (candidate.Signature() != startingSig);
            
            return false;
        }
    }

    private class FractalArt
    {
        private List<(Canvas, Canvas)> _rules;
        private Canvas _canvas;
        
        public FractalArt(string[] rules)
        {
            _rules = new List<(Canvas, Canvas)>();
            foreach (var line in rules)
            {
                var tmp = line.Split(" => ");
                _rules.Add((new Canvas(tmp[0].Split("/")), new Canvas(tmp[1].Split("/"))));
            }
            
            _canvas = new Canvas(new List<string>()
            {
                {".#."},
                {"..#"},
                {"###"}
            }.ToArray());
        }

        public int OnPixels()
        {
            var on = 0;
            for (int y = 0; y < _canvas.Size(); y++)
            {
                for (int x = 0; x < _canvas.Size(); x++)
                {
                    on += (_canvas.Data()[x, y] == '#') ? 1 : 0;
                }
            }
            return on;
        }

        public void Display() { Draw<char>.ShowGrid(_canvas.Data()); }

        public void Iterate()
        {
            // dice up canvas into 2x2 or 3x3 squares
            var squareSize = _canvas.Size() % 2 == 0 ? 2 : 3;
            var numSquares = _canvas.Size() * _canvas.Size() / (squareSize * squareSize);
            var squares = new List<Canvas>();
            for (var i = 0; i < numSquares; i++)
            {
                var offsetY = (i * squareSize / _canvas.Size()) * squareSize;
                var offsetX = i * squareSize % _canvas.Size();
                var canvasData = new char[squareSize, squareSize];
                for (int y = offsetY; y < offsetY + squareSize; y++)
                {
                    for (int x = offsetX; x < offsetX + squareSize; x++)
                    {
                        canvasData[x - offsetX, y - offsetY] = _canvas.Data()[x, y];
                    }
                }
                squares.Add(new Canvas(canvasData, squareSize));
            }

            // enhance diced squares base on rules
            var enhancedSquares = new List<Canvas>();
            foreach (var square in squares)
            {
                foreach (var (inputCanvas, outputCanvas) in _rules)
                {
                    if (inputCanvas.Equals(square))
                    {
                        enhancedSquares.Add(new Canvas(outputCanvas.Data(), outputCanvas.Size()));
                        break;
                    }
                }
            }
            if (enhancedSquares.Count != squares.Count)
            {
                throw new Exception($"Not all squares were enhanced");
            }

            // combine
            var newSize = Convert.ToInt32(Math.Sqrt(numSquares * enhancedSquares[0].Size() * enhancedSquares[0].Size()));
            var combinedData = new char[newSize, newSize];
            var index = 0;
            foreach (var enhancedSquare in enhancedSquares)
            {
                var offsetY = (index * enhancedSquare.Size() / newSize) * enhancedSquare.Size();
                var offsetX = index * enhancedSquare.Size() % newSize;
                for (int y = offsetY; y < offsetY + enhancedSquare.Size(); y++)
                {
                    for (int x = offsetX; x < offsetX + enhancedSquare.Size(); x++)
                    {
                        combinedData[x, y] = enhancedSquare.Data()[x - offsetX, y - offsetY];
                    }
                }
                index++;
            }

            _canvas = new Canvas(combinedData, newSize);
        }
    }
}