using System;
using System.Collections.Generic;
using System.Linq;
public class Primes
{
        public static IEnumerable<int> Stream()
        {
            return Enumerable.Range(2, int.MaxValue - 1).Where(number =>
            {
                if (number == 2 || number == 3)
                    return true;
                if (number % 2 == 0 || number % 3 == 0)
                    return false;
                for (var i = 5; i * i <= number; i = i + 6)
                    if (number % i == 0 || number % (i + 2) == 0)
                        return false;
                return true;
            });
        }
      
}
___________________________________________________________
using System.Collections;
using System.Collections.Generic;
public class Primes
{
    public static IEnumerable<int> Stream()
    {
        var sieve = new BitArray(1<<24);
        for (var p = 2; p < sieve.Length; p++)
        {
            if (sieve[p]) continue;
            yield return p;
            for (int i = p * 2; i < sieve.Length; i += p)
                sieve.Set(i, true);
        }
    }
}
___________________________________________________________
using System.Collections;
using System.Collections.Generic;
public class Primes
{
    static int n = 0;
    static bool[] s;

    public static IEnumerable<int> Stream()
    {
        //  筛选出所有合数i，并使 s[i]=true
        if (n == 0)
        {
            n = 20000000;
            s = new bool[n];
            for (long i = 3; i < n; i += 2)
                if (!s[i])
                    for (long j = i * i; j < n; j += 2 * i)
                        s[j] = true;
        }
        yield return 2;
        for (int i = 3; i < n; i += 2)
            if (!s[i]) yield return i;
    }
}
___________________________________________________________
using System.Collections;
using System.Collections.Generic;
public class Primes
    {
        public static IEnumerable<int> Stream()
        {
            return new PrimesStream();
        }
    }

    public class PrimesStream : IEnumerable<int>
    {
        public IEnumerator<int> GetEnumerator()
        {
            return new PrimesEnum();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }

    public class PrimesEnum : IEnumerator<int>
    {
        private int _current = 1;
        public int Current
        {
            get
            {
                return _current;
            }
        }

        object IEnumerator.Current => Current;

        public bool MoveNext()
        {
            _current = nextPrime(_current);
            return true;
        }

        public void Reset()
        {
            _current = 1;
        }
        public void Dispose()
        {
        }

        private int nextPrime(int position)
        {
            while (!IsPrime(++position))
            { }
            return position;
        }
        private bool IsPrime(int number)
        {

            if (number == 2 || number == 3)
                return true;

            if (number % 2 == 0 || number % 3 == 0)
                return false;

            int divisor = 6;
            while (divisor * divisor - 2 * divisor + 1 <= number)
            {

                if (number % (divisor - 1) == 0)
                    return false;

                if (number % (divisor + 1) == 0)
                    return false;

                divisor += 6;
            }

            return true;
        }
    }
___________________________________________________________
using System;
using System.Collections.Generic;

public class Primes
{
   public static IEnumerable<int> Stream()
   {
      yield return 2;
      for (var i = 3;; i += 2)
        if (isPrime(i))
          yield return i;
      bool isPrime(int n) {
        if (n <= 1) return false;
        if (n % 2 == 0 || n % 3 == 0) return n < 4;
        for (var m = 5; m <= (int) Math.Sqrt(n); m += 6) {
          if (n % m == 0 || n % (m + 2) == 0)
            return false;
        }
        return true;
      }
   }
}
___________________________________________________________
using System.Collections;
using System.Collections.Generic;
using System.Linq;
public class Primes
{
   public static IEnumerable<int> Stream()
   {
       return new Prime();
   }
}

public class Prime : IEnumerable<int>
{
  IEnumerator<int> IEnumerable<int>.GetEnumerator() => new PrimeEnumerator();
  IEnumerator IEnumerable.GetEnumerator() => new PrimeEnumerator();  
}

public class PrimeEnumerator : IEnumerator<int>
{
    int prime = 1;
    
    public int Current => prime;
    object IEnumerator.Current => prime;
    
    bool IEnumerator.MoveNext()
    {
      NextPrime();
      return true;
    }
    
    void IEnumerator.Reset()
    {
      prime = 1;
    }
    
    void NextPrime()
    {
      do
      {
        if(prime==2 || prime == 1)
          prime++;
        else prime+=2;
      }
      while(!IsPrime(prime));
    }
    
    bool IsPrime(int n)
    {
      if (n <= 3) return true;
      if (n%2 == 0 || n % 3 == 0) return false;
      
      for(int i = 5; i*i <= n; i+=6)
        if(n % i == 0 || n % (i+2) == 0) return false;
      
      return true;
    }
    
    public void Dispose()
    {
    
    }
    
    
}
___________________________________________________________
using System.Linq;
using System;
using System.Collections;
using System.Collections.Generic;
public class Primes
{
        public static IEnumerable<int> Stream()
        {
            yield return 2; 
            int top_number = 20000000;
            var bitArrayLimit = (top_number - 3) / 2;
            var SQRTLMT = ((uint)(Math.Sqrt((double)top_number)) - 3) / 2;
            var buf = new BitArray((int)bitArrayLimit + 1,true);
            for (var i = 0; i <= bitArrayLimit; ++i){ 
                if (buf[(int)i]) {
                    var p = 3 + i + i; 
                        if (i <= SQRTLMT) {
                            for (var j = (p * p - 3) / 2; j <= bitArrayLimit; j += p)
                                buf[(int)j] = false; 
                        } 
                    yield return p; 
                } 
            }
        }
}
