namespace Converter {
  public class Converter
  {
    public string dnaToRna(string dna)
    {
      return dna.Replace('T', 'U');
    }
  }
}

_____________________________
namespace Converter {
  public class Converter
  {
    public string dnaToRna(string dna) => dna.Replace('T','U');
  }
}

_____________________________
namespace Converter {
  public class Converter
  {
    public string dnaToRna(string dna)
    {
      char[] ch = dna.ToCharArray();
      for (int i = 0; i < ch.Length; i++){
        if (ch[i] == 'T'){
          ch[i] = 'U';
        }
      }
      string rna = new string (ch);
      return rna;
    }
  }
}

_____________________________
namespace Converter {
  public class Converter
  {
    public string dnaToRna(string dna)
    {
       return dna.Length > 0? dna.Replace('T', 'U'):dna;
    }
  }
}
