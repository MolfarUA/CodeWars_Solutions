54b72c16cd7f5154e9000457


using System;
using System.Collections.Generic;
using System.Linq;

public class MorseCodeDecoder
{
  public static string DecodeBits(string bits)
  {
    var cleanedBits = bits.Trim('0');
    var rate = GetRate();
    return cleanedBits
      .Replace(GetDelimiter(7, "0"), "   ")
      .Replace(GetDelimiter(3, "0"), " ")
      .Replace(GetDelimiter(3, "1"), "-")
      .Replace(GetDelimiter(1, "1"), ".")
      .Replace(GetDelimiter(1, "0"), "");
        
    string GetDelimiter(int len, string c) => Enumerable.Range(0, len * rate).Aggregate("", (acc, _) => acc + c);
    int GetRate() => GetLengths("0").Union(GetLengths("1")).Min();
    IEnumerable<int> GetLengths(string del) => cleanedBits.Split(del, StringSplitOptions.RemoveEmptyEntries).Select(s => s.Length);
  }

  public static string DecodeMorse(string morseCode)
  {
    return morseCode
      .Split("   ")
      .Aggregate("", (res, word) => $"{res}{ConvertWord(word)} ")
      .Trim();
      
    string ConvertWord(string word) => word.Split(' ').Aggregate("", (wordRes, c) => wordRes + MorseCode.Get(c));
  }
}
_____________________________
using System;
using System.Text.RegularExpressions;
using System.Linq;
using System.Collections.Generic;

public class MorseCodeDecoder
{
public static string DecodeMorse(string morseCode) {
  return Regex.Replace(morseCode, @"(?:[\.-]+)|(?:\s+)", MatchReplace);
}

public static string MatchReplace(Match m){
	switch (m.Value){
		case " ": return "";
		case "   ": return " ";
		default: return MorseCode.Get(m.Value);
	}

}

public static string DecodeBits(string bits)
{ 
  var tokens = Regex.Matches(bits.Trim('0'), @"(0+|1+)").OfType<Match>().Select(i=>i.Value).ToList();
	var basis = tokens.Select(i => i.Length).Min();
	var elts = new Dictionary<string, string>{
  	{new string('1', basis), "."},
  	{new string('0', basis), ""},
  	{new string('1', basis*3), "-"},
  	{new string('0', basis*3), " "},
	{new string('0', basis*7), "   "}
  };

  return string.Join("", tokens.Select(i=>elts[i]));

}
}
_____________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;


    #region Performance Tests
    // 5000 iterations of 25 samples
    // ----------------------------------------------------------------------------------------------------
    // Heri                557.97090000006 milliseconds( 557.970900000058 milliseconds )
    // John               1863.96110000125 milliseconds( 1.86396110000125 seconds )
    // Kart                945.18380000019 milliseconds( 945.183800000187 milliseconds )
    // Cyover             6595.73970000066 milliseconds( 6.59573970000066 seconds )
    // Elegant            1739.14760000058 milliseconds( 1.73914760000058 seconds )
    // skaramasakus       1389.43099999985 milliseconds( 1.38943099999985 seconds )
    // Zangief             916.36000000038 milliseconds( 916.360000000376 milliseconds )
    // Patters            1663.71190000012 milliseconds( 1.66371190000012 seconds )
    // maja               1332.10100000045 milliseconds( 1.33210100000045 seconds )
    // Gortha             2364.37030000036 milliseconds( 2.36437030000036 seconds )
    // ArtemVinar         2193.06510000036 milliseconds( 2.19306510000036 seconds )
    // JeremyGibbons       328.00829999991 milliseconds( 328.008299999913 milliseconds )
    // Isimbo             4806.55749999972 milliseconds( 4.80655749999972 seconds )
    // Eivindjk           Infinite Loop
    // StePed             1613.73490000055 milliseconds( 1.61373490000055 seconds )
    // AlexanderG        10724.69799999830 milliseconds( 10.7246979999983 seconds )


    // 100000 iterations of 25 samples
    // ----------------------------------------------------------------------------------------------------
    // Heri               9151.34180002411 milliseconds( 9.15134180002411 seconds )
    // John              61026.27830001890 milliseconds( 1.01710463833365 minutes )
    // Kart              44426.99259997420 milliseconds( 44.4269925999742 seconds )
    // Cyover           242853.19169952000 milliseconds( 4.04755319499201 minutes )
    // Elegant           52908.14400005560 milliseconds( 52.9081440000556 seconds )
    // skaramasakus      66509.96749981870 milliseconds( 1.10849945833031 minutes )
    // Zangief           36684.82579972940 milliseconds( 36.6848257997294 seconds )
    // Patters           55873.88729993120 milliseconds( 55.8738872999312 seconds )
    // maja              62523.89189990680 milliseconds( 1.04206486499845 minutes )
    // Gortha            70792.71890002620 milliseconds( 1.17987864833377 minutes )
    // ArtemVinar        56350.88719984000 milliseconds( 56.35088719984 seconds )
    // JeremyGibbons      6390.31560003896 milliseconds( 6.39031560003896 seconds )
    // Isimbo           138657.23199991000 milliseconds( 2.31095386666517 minutes )
    // Eivindjk         Infinite Loop
    // StePed            31150.01769991190 milliseconds( 31.1500176999119 seconds )
    // AlexanderG       216745.37800067500 milliseconds( 3.61242296667792 minutes )

    //performance test source code: https://1drv.ms/u/s!Aux9kaP8MN9WjUk5G9MtpQwMf91s?e=dIvJmS
    #endregion

   public class MorseCodeDecoder
    {
        private const int CharacterSeperatorLength = 1;
        private const int WordSeperatorLength = 3;
        private const char ZeroBit = '0';
        private const char OneBit = '1';
        private const char Dot = '.';
        private const char Dash = '-';
        private const char Space = ' ';
        
        private enum CodeCharTimeLength
        {
            None = 0,
            Dot = 1,
            Dash = 3
        }

        private enum CodeSeperatorTimeLength
        {
            None = 0,
            DotDash = 1,
            Char = 3,
            Word = 7
        }

        public static string DecodeMorse(string morseCode)
        {
            // clean our input
            morseCode = morseCode.Trim();
            int spaceCount = 0;
            int lastCharIndex = 0;
            // reserve some memory in advance. ideally we would want this to start at count of spaces.
            // the fastest way to get that count would be to iterate the string. 
            // this would cause us to iterate twice, once to count spaces and once to decode
            // getting half size of string should serve as a reasonable base for allocating space in memory.
            StringBuilder builder = new StringBuilder((int)Math.Ceiling(morseCode.Length / 2d));

            // iteration by char should be faster than string split
            // then we enter state machine
            for (int charIndex = 0; charIndex < morseCode.Length; charIndex++)
            {
                // we found the end of a word
                if (spaceCount == MorseCodeDecoder.WordSeperatorLength)
                {
                    builder.Append(MorseCode.Get(morseCode.Substring(lastCharIndex, charIndex - lastCharIndex - MorseCodeDecoder.WordSeperatorLength)));
                    builder.Append(MorseCodeDecoder.Space);
                    spaceCount = 0;
                    lastCharIndex = charIndex;
                }
                // we found a character
                else if (spaceCount == MorseCodeDecoder.CharacterSeperatorLength && morseCode[charIndex] != MorseCodeDecoder.Space)
                {
                    builder.Append(MorseCode.Get(morseCode.Substring(lastCharIndex, charIndex - lastCharIndex - MorseCodeDecoder.CharacterSeperatorLength)));
                    spaceCount = 0;
                    lastCharIndex = charIndex;
                }
                else if (morseCode[charIndex] == MorseCodeDecoder.Space)
                {
                    spaceCount++;
                }

                // wrap things up
                if (charIndex == (morseCode.Length - 1))
                {
                    builder.Append(MorseCode.Get(morseCode.Substring(lastCharIndex)));
                }
            }

            return builder.ToString().Trim();
        }

        public static string DecodeBits(string bits)
        {
            bits = bits.Trim(new char[] { MorseCodeDecoder.ZeroBit });
            int sampleRate = ResolveTransmissionRate(bits);
            StringBuilder builder = new StringBuilder(); // getting number of chars to allocate memory impacted performance more than i can accept.. its 2019, memory is cheap - but time is money
            StringBuilder morseCharacter = new StringBuilder(9); // largest morse character i know of is 9
            char currentBit = bits[0];
            int bitCount = 0;
            CodeSeperatorTimeLength seperator = CodeSeperatorTimeLength.None;
            CodeCharTimeLength codeChar = CodeCharTimeLength.None;

            morseCharacter.EnsureCapacity(9);

            // we traverse to the length to process last bit
            for (int bitIndex = 0; bitIndex <= bits.Length; bitIndex++)
            {
                char bit = bitIndex == (bits.Length) ? currentBit : bits[bitIndex];
                if (bit.Equals(currentBit) && bitIndex < (bits.Length))
                {
                    bitCount++;
                    continue;
                }

                if (currentBit.Equals(ZeroBit))
                {
                    seperator = (CodeSeperatorTimeLength)(bitCount / sampleRate);

                    switch (seperator)
                    {
                        case CodeSeperatorTimeLength.DotDash:
                            // do nothing
                            break;
                        case CodeSeperatorTimeLength.Char:
                            builder.Append(morseCharacter.ToString());
                            builder.Append(MorseCodeDecoder.Space);
                            morseCharacter.Clear();
                            break;
                        case CodeSeperatorTimeLength.Word:
                            builder.Append(morseCharacter.ToString());
                            builder.Append(new string(MorseCodeDecoder.Space, MorseCodeDecoder.WordSeperatorLength));
                            morseCharacter.Clear();
                            break;
                        case CodeSeperatorTimeLength.None:
                        default:
                            break;
                            //throw new Exception("Uknown seperator");
                    }
                }
                else if (currentBit.Equals(OneBit))
                {
                    codeChar = (CodeCharTimeLength)(bitCount / sampleRate);

                    morseCharacter.Append(codeChar == CodeCharTimeLength.Dash ? MorseCodeDecoder.Dash : MorseCodeDecoder.Dot);
                }

                if (bitIndex == (bits.Length))
                {
                    builder.Append(morseCharacter.ToString());
                }

                currentBit = bit;
                bitCount = 1;
            }

            //System.Diagnostics.Debug.Assert(charsCount == MorseCodeDecoder.DecodeMorse(builder.ToString().Trim()).Length);
            return builder.ToString().Trim();
        }


        public static int ResolveTransmissionRate(string bits)
        {
            int rate = bits.Length;
            int currentRate = 0;
            char currentBit = bits[0];

            for (int index = 0; index < bits.Length; index++)
            {
                char bit = bits[index];

                if (currentBit.Equals(bit))
                {
                    currentRate++;
                }

                else //if (!currentBit.Equals(bit))
                {
                    rate = Math.Min(rate, currentRate);
                    currentRate = 1;
                    currentBit = bit;
                }
            }

            return rate;
        }
    }
_____________________________
using System;
using System.Collections.Generic;
using System.Text;

public class MorseCodeDecoder
{
    static string[] WordSeparator = new string[] { "   " };
    
    public static string DecodeBits(string bits)
        {
            Console.WriteLine(bits);
            bits = bits.Trim('0');
            List<string> bitseqs = new List<string>();

            char lastchar = bits[0] == '1' ? '0' : '1';
            int minSeqLen = int.MaxValue;
            int currentSeqLen = int.MaxValue;
            
            foreach(char c in bits)
            {
                if(c == lastchar)
                {
                    currentSeqLen++;
                }
                else
                {
                    minSeqLen = currentSeqLen < minSeqLen ? currentSeqLen : minSeqLen;
                    if (currentSeqLen < bits.Length)
                        bitseqs.Add(new string(lastchar, currentSeqLen));
                    lastchar = c;
                    currentSeqLen = 1;
                }
            }

            minSeqLen = currentSeqLen < minSeqLen ? currentSeqLen : minSeqLen;
            bitseqs.Add(new string(lastchar, currentSeqLen));

            StringBuilder morse = new StringBuilder();

            foreach(string s in bitseqs)
            {
                if (s[0] == '0' && s.Length == 3 * minSeqLen)
                {
                    morse.Append(" ");
                }
                else if (s[0] == '0' && s.Length == 7 * minSeqLen)
                {
                    morse.Append("   ");
                }
                else if(s[0] == '1' && s.Length == minSeqLen)
                {
                    morse.Append('.');
                }
                else if(s[0] == '1' && s.Length == 3 * minSeqLen)
                {
                    morse.Append('-');
                }
            }

            return morse.ToString();
        }

        public static string DecodeMorse(string morseCode)
        {
            StringBuilder result = new StringBuilder();
            string[] morsewords = morseCode.Split(WordSeparator, StringSplitOptions.RemoveEmptyEntries);
            foreach (var word in morsewords)
            {
                string[] morsechars = word.Split(' ');
                foreach (var ch in morsechars)
                {
                    result.Append(MorseCode.Get(ch));
                }
                result.Append(" ");
            }
            result.Remove(result.Length - 1, 1);
            return result.ToString();
        }
}
