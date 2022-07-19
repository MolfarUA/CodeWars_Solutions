561e9c843a2ef5a40c0000a4
  
  
#include <vector>
class GapInPrimes
{
public:
    static std::pair <long long, long long> gap(int g, long long m, long long n) 
    {
        std::vector<bool> sieve(n,false);
        sieve[0] = sieve[1] = true;
        long long lastprime = 1;
        for(long long i = 2; i<n; i++) {
            if(!sieve[i]) {
                if (lastprime > m && i < n && i - lastprime == g) { 
                    return {lastprime, i};
                } else {
                    lastprime = i;
                    for (int temp = 2*i; temp<n; temp += i)
                        sieve[temp] = true;
                }
            }
        }
        return {0,0};
    };
};
__________________________________
class GapInPrimes
{
private:
    static bool isPrime(long long n);
public:
    static std::pair <long long, long long> gap(int g, long long m, long long n);
};

bool GapInPrimes::isPrime(long long n)
{
  if (n % 2 == 0) return false;
  for (int i = 3; i * i <= n ; i += 2)
    if (n % i == 0) return false;
  return true;
}

std::pair <long long, long long> GapInPrimes::gap(int g, long long m, long long n)
{
    std::pair <long, long> res = {0, 0};
    long long i = m;
    while (i < n + 1)
    {
        if (isPrime(i))
        {
            res.first = i;
            break;
        }
        i++;
    }
    bool cont = true;
    while (cont)
    {
        long long j = i + 1;
        while (j < n + 1)
        {
            if (isPrime(j))
            {
                if (j - i == g)
                {
                    res.second = j;
                    return res;
                }
                else
                {
                    res.first = j;
                    i = j;
                }
            }
            j++;
        }
        cont = false;
    }
    return {0, 0};
}
__________________________________
#include <vector>
#include <unordered_map>
#include <iostream>
#include <utility>
#include <ctime>
#include <cstdlib>
using ll = long long;
std::vector<ll> primes;
std::unordered_map<ll, bool> flags;
ll cnt = 15;
class GapInPrimes
{
  public:
    static ll qpow(ll a, ll b, const ll &mod)
    {
        ll ans = 1;
        while (b)
        {
            if (b & 1)
                ans = (ans * a) % mod;
            a = (a * a) % mod;
            b >>= 1;
        }
        return ans;
    }
    static bool miller_rabin(const long long &n)
    {
        srand(time(NULL));
        if (n == 2)
            return true;
        for (ll i = 0; i < cnt; ++i)
        {
            ll a = rand() % (n - 2) + 2;
            if (qpow(a, n, n) != (a % n))
                return false;
        }
        return true;
    }

    static std::pair<ll, ll> gap(int g, ll m, ll n)
    {
        for (ll i = m; i + g <= n; i++)
        {
            if (miller_rabin(i) && miller_rabin(i + g))
            {
                for (ll j = i + 1; j < i + g; ++j)
                {
                    if (miller_rabin(j))
                    {
                        i = j;
                        goto next;
                    }
                    
                }
                return std::make_pair(i, i + g);
            }
            next: continue;
        }
        return std::make_pair(0, 0);
    }
};
