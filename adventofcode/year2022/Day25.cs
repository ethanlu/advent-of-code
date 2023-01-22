using System.Net;
using adventofcode.common;

namespace adventofcode.year2022;

public class Day25 : Solution
{
    private string[] _snafus;
    
    public Day25(string year, string day) : base(year, day)
    {
        _snafus = LoadInputAsLines();
    }

    public override string PartOne()
    {
        var total = 0L;
        foreach (var snafu in _snafus)
        {
            var decimalNumber = Conversion.ToDecimal(snafu);
            Console.WriteLine($"{snafu} ---> {decimalNumber}");
            total += decimalNumber;
        }
        Console.WriteLine($"Total : {total}");

        return Convert.ToString(Conversion.ToSnafu(total));
    }

    public override string PartTwo()
    {
        return Convert.ToString("ᕕ( ᐛ )ᕗ");
    }

    private class Conversion
    {
        private static (char, char) AddSnafuDigit(char a, char b)
        {
            switch (a.ToString() + b.ToString())
            {
                case "00": return ('0', '0');
                case "01": return ('0', '1');
                case "02": return ('0', '2');
                case "0=": return ('0', '=');
                case "0-": return ('0', '-');
                case "10": return ('0', '1');
                case "11": return ('0', '2');
                case "12": return ('1', '=');
                case "1=": return ('0', '-');
                case "1-": return ('0', '0');
                case "20": return ('0', '2');
                case "21": return ('1', '=');
                case "22": return ('1', '-');
                case "2=": return ('0', '0');
                case "2-": return ('0', '1');
                case "=0": return ('0', '=');
                case "=1": return ('0', '-');
                case "=2": return ('0', '0');
                case "==": return ('-', '1');
                case "=-": return ('-', '2');
                case "-0": return ('0', '-');
                case "-1": return ('0', '0');
                case "-2": return ('0', '1');
                case "-=": return ('-', '2');
                case "--": return ('0', '=');
            }
            throw new Exception($"Unrecognized snafu digits : {a}, {b}");
        }
        
        private static (char, char) DecimalToSnafu(long d)
        {
            switch (d)
            {
                case 0L: return ('0', '0');
                case 1L: return ('0', '1');
                case 2L: return ('0', '2');
                case 3L: return ('1', '=');
                case 4L: return ('1', '-');
            }
            
            throw new Exception($"Unrecognized decimal digit : {d}");
        }
        
        private static long SnafuToDecimal(char c)
        {
            switch (c)
            {
                case '0': return 0L;
                case '1': return 1L;
                case '2': return 2L;
                case '-': return -1L;
                case '=': return -2L;
            }

            throw new Exception($"Unrecognized snafu digit : {c}");
        }

        public static long ToDecimal(string snafuNumber)
        {
            var decimalNumber = 0L;
            
            for (int i = 0; i < snafuNumber.Length; i++)
            {
                decimalNumber += Convert.ToInt64(Math.Pow(5, snafuNumber.Length - 1 - i)) * SnafuToDecimal(snafuNumber[i]);
            }

            return decimalNumber;
        }

        public static string ToSnafu(long decimalNumber)
        {
            string Remainder(long remaining, Queue<long> digits)
            {
                var dividend = remaining / 5;
                
                if (dividend == 0)
                {
                    digits.Enqueue(remaining % 5);
                    
                    // dividend reached 0, construct snafu number using the digits
                    var snafuNumber = new List<char>();
                    var snafuDigitPlace = 0;
                    do
                    {
                        var (carry, snafuDigit) = DecimalToSnafu(digits.Dequeue());
                        if (snafuNumber.Count == snafuDigitPlace)
                        {
                            snafuNumber.Add(snafuDigit);
                        }
                        else
                        {
                            var previousCarry = carry;
                            (carry, snafuDigit) = AddSnafuDigit(snafuDigit, snafuNumber[snafuDigitPlace]);
                            snafuNumber[snafuDigitPlace] = snafuDigit;
                            (carry, snafuDigit) = AddSnafuDigit(previousCarry, carry);
                            snafuNumber.Add(snafuDigit);
                        }
                        
                        if (carry != '0')
                        {
                            snafuNumber.Add(carry);
                        }

                        snafuDigitPlace++;
                    } while (digits.Count > 0);

                    snafuNumber.Reverse();
                    return string.Join("", snafuNumber.SkipWhile(c => c == '0'));
                }

                // can still be divided by 5, so add remainder to digit stack and recurse
                digits.Enqueue(remaining % 5);
                return Remainder(dividend, digits);
            }

            return Remainder(decimalNumber, new Queue<long>());
        }
    }
}