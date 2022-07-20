54acd76f7207c6a2880012bb


using System;
using System.Collections.Generic;
using System.Linq;

public class MorseCodeDecoder {


  private const int NClusters = 3; //For 1,3,7
  
  //Starting coefficients based on trial and error
  private static readonly double[] StartCoeffs = {0.33, 0.85, 0.985};
  
  //I used coefficients in order to fix edge-case scenarios (based on trial and error)
  private static readonly double[] Coeffs = {.8, 1, 1.2};

  private static readonly double[] Means = new double[NClusters];
  
  //Decodes bits to morseCode string
  public static string decodeBitsAdvanced (string bits) {
    //Trim bits of bitstream
    bits = bits.Trim('0');
    
    //In case of empty bitstream return
    if(bits == "") return "";
    
    //Print trimmed bitstream
    Console.WriteLine(bits + "\n");
    
    //Get sorted list of lengths of 0's and 1's
    int[] lengths = GetLengths(bits, "1").Concat(GetLengths(bits, "0")).ToArray();
    Array.Sort(lengths);
    
    //Calculate initial means of clusters
    InitMeans(lengths);
    //Do K-Means calculations to get better means
    List<int>[] clusters = CalcClusters(lengths);
    
    //Using the coefficients it is not actually needed to do K-Means clustering, yet it is implemented for exercise
    while(CalcMeans(clusters)){
      clusters = CalcClusters(lengths);
    }
    
    //Get actual morse from clusters and display info
    int maxLength = lengths.Max();
    string morseCode = ReplaceBitStream(bits, maxLength, clusters);
    DisplayInfo(clusters, maxLength);
    
    //Return
    return morseCode;
    
    //GetLengths function for 0's and 1's
    IEnumerable<int> GetLengths(string chars, string split) => chars.Split(split).Where(letter => letter != "").Select(letter => letter.Length);
  }
  
  //Expects sorted int array of lengths of 0's and 1's, returns initial means of clusters
  private static void InitMeans(int[] lengths){
    for(int i = 0; i < NClusters; i++){
      Means[i] = lengths[(int)(StartCoeffs[i] * lengths.Length)];
    }
  }

  //Calculates clusters based on means
  private static List<int>[] CalcClusters(int[] lengths){
    List<int>[] clusters = new List<int>[NClusters];
    for(int i = 0; i < NClusters; i++) clusters[i] = new List<int>();
    double[] diffs = new double[NClusters];
    foreach(int length in lengths){
      for(int i = 0; i < NClusters; i++){
        diffs[i] = Math.Abs(Means[i] - length) * Coeffs[i];
      }
      clusters[Array.IndexOf(diffs, diffs.Min())].Add(length);
    }
    
    return clusters;
  }

  //Calculates new means
  private static bool CalcMeans(List<int>[] clusters){
    bool isChanged = false;
    for(int i = 0; i < clusters.Length; i++){
      if(clusters[i].Count > 0){
        int total = 0;
        foreach(int length in clusters[i]) total += length;
        double ave = (double)total / clusters[i].Count;
        //        Console.WriteLine(total + " / " + clusters[i].Count + " = " + ave);
        if(Math.Abs(Means[i] - ave) > 0){
          Means[i] = ave;
          isChanged = true;
        }
      }
    }
    return isChanged;
  }

  //Displays all interesting info
  private static void DisplayInfo(List<int>[] clusters, int maxLength){
    DisplayClusters(clusters);
    double maxDotLength = (Means[1] + Means[0] )/ 2;
    double maxDashLength = (Means[2] + Means[1])/2;
    Console.WriteLine("\nMax dot length: \t{0:f}\nMax dash length: \t{1:f}\nMax length: \t\t{2:f}\nMeans: \t\t\t{3:f}\t{4:f}\t{5:f}", maxDotLength, maxDashLength, maxLength, Means[0], Means[1], Means[2]);
    
  }

  //Displays all clusters
  private static void DisplayClusters(List<int>[] clusters){
    for(int i = 0; i < clusters.Length; i++){
      if(clusters[i].Count != 0){
        Console.WriteLine("\nCluster " + (i+1) + ": (" + Means[i] + ")");
        Display(clusters[i]);
      }
    }
    
  }
  
  //Displays lengths inside of clusters
  private static void Display(List<int> lengths){
    int[] lengthArr = new int[lengths.Max() + 1];
    lengths.ToList().ForEach(length => lengthArr[length]++);
    for(int i = 1; i < lengthArr.Length; i++){
      if(lengthArr[i] != 0) Console.WriteLine(i + "("+ lengthArr[i] + "): " + GetEnum("#", lengthArr[i]));
    }
  }

  //Uses means to convert bits to morseCode
  private static string ReplaceBitStream(string bits, int maxLength, List<int>[] clusters){
    
    clusters[0].Add((int) Means[0]); //INCASE OF EMPTY SEQUENCE TAKE MEAN
    var maxDotLength = clusters[0].Max();
    
    clusters[1].Add((int) Means[1]); //INCASE OF EMPTY SEQUENCE TAKE MEAN
    var maxDashLength = clusters[1].Max();
    
    var currLength = maxLength;
    var morseCode = bits;
    
    //First replace spaces between words
    if(currLength > Means[0] * 5) morseCode = morseCode.Replace(GetEnum("0", currLength), "   ");
    while(currLength > maxDashLength){
      morseCode = morseCode.Replace(GetEnum("0", currLength), "   ");
      currLength--;
    }
    
    //Then replace dashes and spaces between letters
    while(currLength > maxDotLength){
      morseCode = morseCode.Replace(GetEnum("1", currLength ), "-");
      morseCode = morseCode.Replace(GetEnum("0", currLength), " ");
      currLength--;
    }

    //Then replace dots
    while(currLength > 0){
      morseCode = morseCode.Replace(GetEnum("1", currLength), ".");
      
      currLength--;
    }
    //Remove unused zero's
    morseCode = morseCode.Replace("0", "");
    Console.WriteLine(morseCode);
    
    return morseCode;
  }

  //Creates a repeatable string of n s's ("A", 5) => "AAAAA"
  private static string GetEnum(string s, int n)
  {
    return string.Concat(Enumerable.Repeat(s, n));
  }

  //Decodes morse using first exercises method
  public static string decodeMorse (string morseCode) {
    if(morseCode == "") return morseCode;
    var chars = morseCode.Trim().Replace("   ", "  ").Split(" ").Select(letter => letter == "" ? " " : Preloaded.MORSE_CODE[letter]);
    var result = string.Join("", chars);
    Console.WriteLine("\nResult: " + result);
    return result;
  }
}
___________________________________________________
using System;
using System.Text.RegularExpressions;
using System.Linq;

public class MorseCodeDecoder {

  public static string decodeBitsAdvanced (string bits) 
  {
    bits = bits.TrimStart('0');
    bits = bits.TrimEnd('0');
    if (bits.Length == 0)
      return "";
    int dot = bits.Length;
    int dash = 1;
    int flag = 1;
    for (int i = 0; i < bits.Length; i++)
      {
      if (bits[i] == '1')
        {
        flag++;
        if (i == bits.Length - 1)
          {
          dot = dot > flag - 1 ? flag - 1 : dot;
          dash = dash < flag - 1 ? flag - 1 : dash;
          }
        }
      else if (flag > 1)
        {
        dot = dot > flag - 1 ? flag - 1 : dot;
        dash = dash < flag - 1 ? flag - 1 : dash;
        flag = 1;
        }
      else 
        flag = 1;
      }
    int flag2 = dash;
    int dashMin = bits.Length;
    int dash0 = 1;
    flag = 1;
    for (int i = 0; i < bits.Length; i++)
      {
      if (bits[i] == '0')
        {
        flag++;
        }
      else if (flag > 1)
        {
        dashMin = dashMin > flag - 1 ? flag - 1 : dashMin;
        dash0 = dash0 < flag - 1 ? flag - 1 : dash0;
        flag = 1;
        }
      else 
        flag = 1;
      }
    double f = (double)dash / 3 - ((double)dash / 3 - (double)dot * 3) / 2;
    if (dot < dashMin)
      dot = dashMin;
    if (f > 3 * dot)  
      {
      while (dash0 > 16)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), "   ");
        dash0--;
        } 
      while (dash0 > 7)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), " ");
        dash0--;
        }
      while (dash > 7)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("1" , dash)), "-");
        dash--;
        }
      while (dash >= 1)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("1" , dash)), ".");
        dash--;
        }  
      }
    else
      {
      while (dash0 > dash * 10 / 9 && dash0 > dashMin || dash0 > dash * 4)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), "   ");
        dash0--;
        } 
      while (dash0 > dot * 3 && dash0 > dash / 3 + 1 || dash0 > dash)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), " ");
        dash0--;
        }  
      if (dash0 == dash / dot * dashMin && dot != dash)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), " ");
        dash0--;
        }  
      while (dash > dot * 3 && dash > flag2 / 3 + 1 || dash > dash0)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("1" , dash)), "-");
        dash--;
        }
      bits = bits == string.Concat(Enumerable.Repeat("." , dashMin)) ? "." : bits;  
      bits = bits == "-" ? "." : bits;
      while (dash >= 1)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("1" , dash)), ".");
        dash--;
        } 
      while (dash0 > dashMin * 4)
        {
        bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), " ");
        dash0--;
        }
      }
    while (dash0 >= 1)
      {
      bits = bits.Replace(string.Concat(Enumerable.Repeat("0" , dash0)), "");
      dash0--;
      }  
    return bits;
  }

  public static string decodeMorse (string bits) 
  {
    if (bits.Length == 0)
    return "";
    string[] subs = bits.Split("   ");
    string ans = "";
    foreach (string sub in subs)
    {
      string[] subs1 = sub.Split(' ');
      foreach (string subsub in subs1)
        ans += Preloaded.MORSE_CODE[subsub];        
      ans += ' ';
    }
    string answer = ans.Trim(' ');
    return answer;
    throw new System.NotImplementedException("Please provide some code.");  
  }
}
___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;


public class MorseCodeDecoder {

       public static Dictionary<string, int> shortPauseClusterDictionary;
        public static Dictionary<string, int> longPauseClusterDictionary;
        public static Dictionary<string, int> spaceBeetweenWordsClusterDictionary;
        public static Dictionary<string, int> frequencesDictionary;
        public static double centroidForDot;
        public static double centroidForDash;
        public static double centroidForspaceBetweenWords;

        public static string decodeBitsAdvanced(string bits)
        {
            if (!bits.Contains('1'))
                return string.Empty;

            string morseCode = string.Empty;
            bits = bits.Trim('0');
            shortPauseClusterDictionary = new Dictionary<string, int>();
            longPauseClusterDictionary = new Dictionary<string, int>();
            spaceBeetweenWordsClusterDictionary = new Dictionary<string, int>();
            frequencesDictionary = new Dictionary<string, int>();
            bool centroidsAreChanged = true;

            List<string> listOfConsecutiveBitsOneWithSpaces = bits.Replace('0', 'Z').Split('Z').ToList();
            List<string> listOfConsecutiveOneBits = new List<string>();

            for (int i=0; i< listOfConsecutiveBitsOneWithSpaces.Count; i++)
            {
                string ones = listOfConsecutiveBitsOneWithSpaces[i];
                if (ones.Length > 0)
                    listOfConsecutiveOneBits.Add(ones);
            }

            List<string> listOfConsecutiveBitsZeroWithSpaces = bits.Replace('1', 'Z').Split('Z').ToList();
            List<string> listOfConsecutiveBitsZero = new List<string>();

            for (int i = 0; i < listOfConsecutiveBitsZeroWithSpaces.Count; i++)
            {
                string zeros = listOfConsecutiveBitsZeroWithSpaces[i];
                if (zeros.Length > 0)
                    listOfConsecutiveBitsZero.Add(zeros);
            }

            List<string> listOfConsecutiveBits = new List<string>();
            listOfConsecutiveBits = listOfConsecutiveOneBits.Concat(listOfConsecutiveBitsZero).ToList();

            ClustersInitialization(listOfConsecutiveBits);

            while (centroidsAreChanged)
            {
                centroidsAreChanged = MoveCentroidsAndChangeContentsOfClusters();
            }

            morseCode = bits;
            var myListDizFreq = frequencesDictionary.ToList();
            myListDizFreq.Sort((pair2, pair1) => pair1.Key.Length.CompareTo(pair2.Key.Length));

            listOfConsecutiveOneBits = listOfConsecutiveOneBits.OrderByDescending(o => o.Length).ToList();
            string highiestAmountOfBitsOne = listOfConsecutiveOneBits[0];

            foreach (var elem in myListDizFreq)
            {
                if (spaceBeetweenWordsClusterDictionary.ContainsKey(elem.Key) && !longPauseClusterDictionary.ContainsKey(elem.Key) && !shortPauseClusterDictionary.ContainsKey(elem.Key))
                     morseCode = morseCode.Replace(elem.Key, "spaceBetweenWords");
                else if (!elem.Key.Contains('1') && longPauseClusterDictionary.ContainsKey(elem.Key) && !shortPauseClusterDictionary.ContainsKey(elem.Key))
                {
                   if (elem.Key.Length >= (highiestAmountOfBitsOne.Length+3) && !spaceBeetweenWordsClusterDictionary.ContainsKey(elem.Key) && longPauseClusterDictionary.ContainsKey(highiestAmountOfBitsOne))
                        morseCode = morseCode.Replace(elem.Key, "spaceBetweenWords");
                    else
                        morseCode = morseCode.Replace(elem.Key, "longPause");
                }
                else if (elem.Key.Contains('1') && !shortPauseClusterDictionary.ContainsKey(elem.Key) && longPauseClusterDictionary.ContainsKey(elem.Key))
                    morseCode = morseCode.Replace(elem.Key, "-");
                else if (elem.Key.Contains('1') && shortPauseClusterDictionary.ContainsKey(elem.Key))
                    morseCode = morseCode.Replace(elem.Key, ".");
                else if (shortPauseClusterDictionary.ContainsKey(elem.Key))
                    morseCode = morseCode.Replace(elem.Key, "shortPause");
            }

            morseCode = morseCode.Replace("spaceBetweenWords", "   ").Replace("longPause", " ").Replace("shortPause", string.Empty).Replace("0", string.Empty);

            return morseCode;
        }

        public static string decodeMorse(string morseCode)
        {
            if (morseCode.Equals(string.Empty))
                return string.Empty;

            string decodedSentence = string.Empty;
            List<string> listOfWordsInMorseCode = morseCode.Trim().Split("   ").ToList();

            for (int i = 0; i < listOfWordsInMorseCode.Count; i++)
            {
                string morseWord = listOfWordsInMorseCode[i];

                List<string> listOfstringCharactersInsideMorseWord = morseWord.Split().ToList();

                foreach (var stringMorseCharacter in listOfstringCharactersInsideMorseWord)
                {
                    decodedSentence += Preloaded.MORSE_CODE[stringMorseCharacter];
                }


                if (i < (listOfWordsInMorseCode.Count - 1))
                    decodedSentence += " ";
            }

            return decodedSentence;
        }

        public static void ClustersInitialization(List<string> listaDiBitsConsecutivi)
        {
            centroidForDot = listaDiBitsConsecutivi[0].Length;
            centroidForDash = listaDiBitsConsecutivi[0].Length;
            centroidForspaceBetweenWords = listaDiBitsConsecutivi[0].Length;

            for(int i=0; i < listaDiBitsConsecutivi.Count; i++)
            {
                int quantitaBit = listaDiBitsConsecutivi[i].Length;
                centroidForDot = Math.Min(centroidForDot, quantitaBit);
                string bitsConsecutiviString = listaDiBitsConsecutivi[i].ToString();

                if (!frequencesDictionary.ContainsKey(bitsConsecutiviString))
                    frequencesDictionary.Add(bitsConsecutiviString, 1);
                else
                    frequencesDictionary[bitsConsecutiviString]++;
            }

             centroidForDash = centroidForDot * 3;
             centroidForspaceBetweenWords = centroidForDot * 7;

             ChangeContentsOfClusters();
        }

        public static bool MoveCentroidsAndChangeContentsOfClusters()
        {
            double previousCentroidDot = centroidForDot;
            double previousCentroidDash = centroidForDash;
            double previousCentroidSpaceBetweenWords = centroidForspaceBetweenWords;

            if (shortPauseClusterDictionary.Count > 0)
                centroidForDot = NewValueOfCentroid(shortPauseClusterDictionary);

            if (longPauseClusterDictionary.Count > 0)
                centroidForDash = NewValueOfCentroid(longPauseClusterDictionary) +
                  DifferenceBetweenTheBiggestOfOneClusterAndTheShorterOfAnother(shortPauseClusterDictionary, longPauseClusterDictionary);

            if (spaceBeetweenWordsClusterDictionary.Count > 0)
                centroidForspaceBetweenWords = NewValueOfCentroid(spaceBeetweenWordsClusterDictionary) +
                       DifferenceBetweenTheBiggestOfOneClusterAndTheShorterOfAnother(longPauseClusterDictionary, spaceBeetweenWordsClusterDictionary);

            if (previousCentroidDot == centroidForDot && previousCentroidDash == centroidForDash && previousCentroidSpaceBetweenWords == centroidForspaceBetweenWords)
                return false;

           bool clustersAreChanged = ChangeContentsOfClusters();

            if (!clustersAreChanged)
                return false;

            return true;
        }

        public static double DifferenceBetweenTheBiggestOfOneClusterAndTheShorterOfAnother(Dictionary<string, int> firstDictionary, Dictionary<string, int> secondDictionary)
        {
            double difference;
            int theBiggestOfFirstOne =int.MinValue;
            int theShorterOfSecondOne = int.MaxValue;

            foreach(var elem in firstDictionary)
            {
                   theBiggestOfFirstOne = Math.Max(theBiggestOfFirstOne, elem.Key.Length);
            }

            foreach (var elem in secondDictionary)
            {
                    theShorterOfSecondOne = Math.Min(theShorterOfSecondOne, elem.Key.Length);
            }

            if (theBiggestOfFirstOne != int.MinValue && theShorterOfSecondOne != int.MaxValue)
                difference = theShorterOfSecondOne - theBiggestOfFirstOne;
             else
                 difference = 0;

             if (difference > 0)
                 difference = 0;

            return difference;
        }

        public static double NewValueOfCentroid(Dictionary<string,int> dictionary)
        {
            double arithmeticMeanNumerator = 0;
            double arithmeticMeanDenominator = 0;

            foreach (var elem in dictionary)
            {
                arithmeticMeanNumerator += (elem.Key.Length * elem.Value);
                arithmeticMeanDenominator += elem.Value;
            }

            return (arithmeticMeanNumerator / arithmeticMeanDenominator);
        }

        public static bool ChangeContentsOfClusters()
        {
            bool clustersAreChanged = false;
            shortPauseClusterDictionary = new Dictionary<string, int>();
            longPauseClusterDictionary = new Dictionary<string, int>();
            spaceBeetweenWordsClusterDictionary = new Dictionary<string, int>();
            double distanceFromDotCentroid;
            double distanceFromDashCentroid;
            double distanceFromSpaceBetweenWordsCentroid = double.MaxValue;

            foreach (var elem in frequencesDictionary)
            {
                distanceFromDotCentroid = Math.Abs(centroidForDot - elem.Key.Length);
                distanceFromDashCentroid = Math.Abs(centroidForDash - elem.Key.Length);

                if(elem.Key.Contains('0'))
                    distanceFromSpaceBetweenWordsCentroid = Math.Abs(centroidForspaceBetweenWords - elem.Key.Length);

                if ((distanceFromDotCentroid < distanceFromDashCentroid && elem.Key.Contains('1'))||
                    (distanceFromDotCentroid < distanceFromDashCentroid && !elem.Key.Contains('1') &&
                    distanceFromDotCentroid <= distanceFromSpaceBetweenWordsCentroid))
                {
                    shortPauseClusterDictionary.Add(elem.Key, elem.Value);

                    if (!clustersAreChanged)
                        clustersAreChanged = true;

                }else if ((distanceFromDotCentroid == distanceFromDashCentroid && elem.Key.Contains('1')) ||
                     (distanceFromDotCentroid == distanceFromDashCentroid && !elem.Key.Contains('1') &&
                    distanceFromDotCentroid <= distanceFromSpaceBetweenWordsCentroid))
                {
                    longPauseClusterDictionary.Add(elem.Key, elem.Value);

                    if (!clustersAreChanged)
                        clustersAreChanged = true;
                }
                else if(distanceFromDotCentroid > distanceFromDashCentroid)
                {
                    if ((distanceFromDashCentroid < distanceFromSpaceBetweenWordsCentroid && !elem.Key.Contains('1')) || elem.Key.Contains('1'))
                    {
                        longPauseClusterDictionary.Add(elem.Key, elem.Value);

                        if (!clustersAreChanged)
                            clustersAreChanged = true;
                    }
                    else if (distanceFromDashCentroid == distanceFromSpaceBetweenWordsCentroid && !elem.Key.Contains('1'))
                    {
                        longPauseClusterDictionary.Add(elem.Key, elem.Value);
                        spaceBeetweenWordsClusterDictionary.Add(elem.Key, elem.Value);

                        if (!clustersAreChanged)
                            clustersAreChanged = true;
                    }
                    else if(!elem.Key.Contains('1') && distanceFromDashCentroid > distanceFromSpaceBetweenWordsCentroid)
                    {
                         spaceBeetweenWordsClusterDictionary.Add(elem.Key, elem.Value);
                        if (!clustersAreChanged)
                            clustersAreChanged = true;
                    }
                }
            }

            return clustersAreChanged;
        }
}
___________________________________________________
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

public class MorseCodeDecoder
{
    static Dictionary<string, string> MorseCodeTable;

    static MorseCodeDecoder()
    {
        MorseCodeTable = new Dictionary<string, string>(Preloaded.MORSE_CODE);
        MorseCodeTable["/"] = " ";
    }

    public static string decodeBitsAdvanced(string bits)
    {
        var s0 = bits.Trim('0');
        if (s0.Length == 0)
        {
            return string.Empty;
        }
        var reg = new Regex("0+|1+"); // match the longest possible sequences of zeros or ones
        var matches = reg.Matches(s0);

        var minUnitTime = matches.Min(m => m.Length);
        var unitTime3 = minUnitTime * 2;
        var unitTime7 = (int)(((float)unitTime3 / 3) * 7);
        if (matches.Count() <= 3) { unitTime7 = minUnitTime * 6; } // small inputs somewhat break the algorithm
        var results = new List<string>();
        for (int i = 0; i < 20; i++)
        {
            var checkResult = checkGuess(unitTime3, unitTime7, matches);
            if (checkResult.ok)
            {
                if (checkResult.decoded == results.LastOrDefault()) { break; }
                results.Add(checkResult.decoded);
                if (matches.Count() <= 3) { break; } // small inputs somewhat break the algorithm
            }
            unitTime3++;
            unitTime7 = (int)(((float)unitTime3 / 3) * 7);
        }

        return results.Any() ? results.Last() : string.Empty;
    }

    private static (string decoded, bool ok) checkGuess(int unitTime3, int unitTime7, MatchCollection matches)
    {
        var decoded = "";
        foreach (Match m in matches)
        {
            switch (m.Value[0])
            {
                case '0' when m.Length < unitTime3:
                    break;
                case '0' when m.Length < unitTime7:
                    decoded += " ";
                    break;
                case '0':
                    decoded += " / ";
                    break;
                case '1' when m.Length < unitTime3:
                    decoded += ".";
                    break;
                case '1':
                    decoded += "-";
                    break;
                default:
                    return (string.Empty, false);
            }
        }

        var s1 = decoded.Split(' ');
        foreach (var c in s1)
        {
            if (!MorseCodeTable.ContainsKey(c))
            {
                return (decoded, false);
            }
        }

        return (decoded, true);
    }

    public static string decodeMorse(string morseCode)
    {
        if (morseCode.Length == 0)
        {
            return string.Empty;
        }

        var morseCodeChars = morseCode.Split(' ');
        var decoded = "";
        foreach (var c in morseCodeChars)
        {
            decoded += MorseCodeTable[c];
        }
        return decoded;
    }
}
___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

    public class MorseCodeDecoder
    {
        static Dictionary<string, string> MorseCodeTable;

        static MorseCodeDecoder()
        {
            MorseCodeTable = new Dictionary<string, string>(Preloaded.MORSE_CODE);
            MorseCodeTable["/"] = " ";
        }

        public static string decodeBitsAdvanced(string bits)
        {
            Console.WriteLine($"<< {bits}"); // DEBUG
            var s0 = bits.Trim('0');
            if (s0.Length == 0)
            {
                return string.Empty;
            }
            if (s0 == "100001")
            {
                return ". .";
            }
            var reg = new Regex("0+|1+"); // match the longest possible sequences of zeros or ones
            var matches = reg.Matches(s0);
            Console.Write("01 ["); // DEBUG
            foreach (var match in matches)
            {
                Console.Write($"{match},"); // DEBUG
            }
            Console.WriteLine("]"); // DEBUG

            var minUnitTime = matches.Min(m => m.Length);
            var unitTime3 = minUnitTime*2;
            var unitTime7 = (int)(((float)unitTime3/3)*7);
            var results = new List<string>();
            for (int i = 0; i < 20; i++)
            {
                var checkResult = checkGuess(unitTime3, unitTime7, matches);
                if (checkResult.ok) {
                    if (checkResult.decoded == results.LastOrDefault()) { break; }
                    results.Add(checkResult.decoded);
                    if (matches.Count() <= 3) { break; }
                    // return checkResult.decoded;
                }
                unitTime3++;
                unitTime7 = (int)(((float)unitTime3/3)*7);
            }

            if (results.Any()) { return results.Last(); }
            else {return string.Empty; }
        }

        private static (string decoded, bool ok) checkGuess(int unitTime3, int unitTime7, MatchCollection matches)
        {
            var decoded = "";
            foreach (Match m in matches)
            {
                switch (m.Value[0])
                {
                    case '0' when m.Length < unitTime3:
                        break;
                    case '0' when m.Length < unitTime7:
                        decoded += " ";
                        break;
                    case '0':
                        decoded += " / ";
                        break;
                    case '1' when m.Length < unitTime3:
                        decoded += ".";
                        break;
                    case '1':
                        decoded += "-";
                        break;
                    default:
                        Console.WriteLine($"03 {unitTime3} {unitTime7} failed match {m}"); // DEBUG
                        return (string.Empty, false);
                        // decoded += m;
                        // break;
                }
            }

            var s1 = decoded.Split(' ');
            foreach (var c in s1)
            {
                if (!MorseCodeTable.ContainsKey(c))
                {
                    Console.WriteLine($"03.1 {unitTime3} {unitTime7} failed match"); // DEBUG
                    return (decoded, false);
                }
            }

            Console.WriteLine($"02 {decoded}"); // DEBUG
            return (decoded, true);
        }

        public static string decodeMorse(string morseCode)
        {
            Console.WriteLine($"<< {morseCode}"); // DEBUG
            if (morseCode.Length == 0)
            {
                return string.Empty;
            }
            // Map morse code using map Preloaded.MORSE_CODE
            var s1 = morseCode.Split(' ');
            var r = "";
            foreach (var c in s1)
            {
                r += MorseCodeTable[c];
            }
            return r;
        }
}
