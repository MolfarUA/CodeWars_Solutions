from itertools import cycle

class VigenereCipher (object):
    def __init__(self, key, alphabet):
        self.key = key.decode('utf-8')
        self.alphabet = alphabet.decode('utf-8')
    
    def cipher(self, mode, str):
        return ''.join(self.alphabet[(self.alphabet.index(m) +
                  mode * self.alphabet.index(k)) % len(self.alphabet)]
                  if m in self.alphabet else m for m, k in zip(str.decode('utf-8'),
                  cycle(self.key))).encode('utf-8')
    
    def encode(self, str): return self.cipher(1, str)
    def decode(self, str): return self.cipher(-1, str)
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key: str, alphabet: str):
        self.alphabet = list(alphabet)
        self.key = [alphabet.index(i) for i in key]

    def encode(self, text):
        return "".join([self.alphabet[(self.alphabet.index(text[i]) + self.key[i % len(self.key)]) % len(self.alphabet)]
                        if text[i] in self.alphabet else text[i] for i in range(len(text))])

    def decode(self, text):
        return "".join([self.alphabet[(self.alphabet.index(text[i]) - self.key[i % len(self.key)]) % len(self.alphabet)]
                        if text[i] in self.alphabet else text[i] for i in range(len(text))])
_____________________________________________
class VigenereCipher(object):

    def __init__(self, key, alphabet):
        self.key = key * 10
        self.alphabet = alphabet * 2
        
    
    def encode(self, text):
        encrypted = ""
        a = 0
        for i in text:
            if i in self.alphabet:
                encrypted += self.alphabet[self.alphabet.index(i) + self.alphabet.index(self.key[a])]
                a += 1
            else:
                encrypted += i
                a += 1
        return encrypted
        
              
    def decode(self, text):
        decrypted = ""
        a = 0
        for i in text:
            if i in self.alphabet:
                decrypted += self.alphabet[self.alphabet.index(i) - self.alphabet.index(self.key[a])]
                a += 1
            else:
                decrypted += i
                a += 1
        return decrypted
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.alpha, self.key  = list(alphabet), key
    
    def encode(self, text):
        text, encoded = list(text), ""
        
        if len(text) > len(self.key):
            while len(self.key) < len(text): self.key *= 2
    
        for i in range(len(text)):
            if text[i] not in self.alpha: encoded += text[i]
            else: encoded += self.alpha[(self.alpha.index(text[i]) + self.alpha.index(self.key[i]))% len(self.alpha)]
                  
        return encoded
    
    def decode(self, text):
        text, decoded = list(text), ""
        
        if len(text) > len(self.key):
            while len(self.key) < len(text): self.key *= 2
        
        for i in range(len(text)):
            if text[i] not in self.alpha: decoded += text[i]
            else: decoded += self.alpha[(self.alpha.index(text[i]) - self.alpha.index(self.key[i]))]
        return decoded
_____________________________________________
class VigenereCipher (object):
    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet
        
    def cipher(self, shifter, text):
        return ''.join(
                  self.alphabet[(shifter * self.alphabet.find(self.key[i % len(self.key)]) + 
                  self.alphabet.find(ch)) % len(self.alphabet)]
                  if ch in self.alphabet else ch 
                  for i, ch in enumerate(text))
    
    def encode(self, text):
        return self.cipher(1, text)
    
    def decode(self, text):
        return self.cipher(-1, text)
_____________________________________________
class VigenereCipher (object):
    def __init__(self, key, alphabet):
        self.key = key.decode('utf-8')
        self.alphabet = alphabet.decode('utf-8')
        self.maps = {c:(self.alphabet[i:]+self.alphabet[:i]) for i, c in enumerate(self.alphabet) if c in self.key}   

    def code(self, f, s):
        return ''.join([f(self.maps[self.key[i % len(self.key)]], c) for i, c in enumerate(s.decode('utf-8'))]).encode('utf-8')
            
    def encode(self, s):    
        return self.code(lambda l, c: l[self.alphabet.index(c)] if c in self.alphabet else c, s)
        
    def decode(self, s):
        return self.code(lambda l, c: self.alphabet[l.index(c)] if c in self.alphabet else c, s)
_____________________________________________
from itertools import cycle

class VigenereCipher(object):
    def __init__(self, key, alphabet):
        k, a, l, i = key, alphabet, len(alphabet), alphabet.index
        self.code = lambda t, o=1: "".join(a[(i(c) + o*i(d)) % l] if c in a else c for c, d in zip(t, cycle(k)))
    
    def encode(self, text):
        return self.code(text)
    
    def decode(self, text):
        return self.code(text, -1)
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key=key
        self.alphabet=alphabet
    
    def encode(self, text):
        a1=list(self.alphabet)
        a2=list(self.key)
        a3=list(text)
        for i in range(len(a2)):
            a2[i]=a1.index(a2[i])
        for i in range(len(a3)):
            aa=i%len(a2)
            if a3[i] in a1:
                bb=(a1.index(a3[i])+a2[aa])%len(a1)
                a3[i]=a1[bb]
            else:
                pass
        return("".join(a3))
                
    def decode(self, text):
        a1=list(self.alphabet)
        a2=list(self.key)
        a3=list(text)
        for i in range(len(a2)):
            a2[i]=a1.index(a2[i])
        for i in range(len(a3)):
            aa=i%len(a2)
            if a3[i] in a1:
                bb=(a1.index(a3[i])-a2[aa])%len(a1)
                a3[i]=a1[bb]
            else:
                pass
        return("".join(a3))
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        
        self.alphabet = alphabet
        self.key = key
    
    def encode(self, text):

        self.key = self.key* (int(len(text)/len(self.key))+1)
        return''.join(list(map(lambda x: self.alphabet[(self.alphabet.index(x[0])+self.alphabet.index(x[1]))%len(self.alphabet)] if (x[0] in self.alphabet) else x[0] ,list(zip(text, self.key)))))
        
    
    def decode(self, text):
        self.key = self.key* (int(len(text)/len(self.key))+1)
        return''.join(list(map(lambda x: self.alphabet[(self.alphabet.index(x[0])-self.alphabet.index(x[1]))%len(self.alphabet)] if (x[0] in self.alphabet) else x[0] ,list(zip(text, self.key)))))
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet
        
    def encode(self, text):
        letters = list(text)
        
        while len(text) > len(self.key):
            self.key += self.key
            
        for i in range(0, len(letters)):
            
            if letters[i] not in list(self.alphabet):
                continue
                
            aIndex = self.alphabet.index(letters[i])
            kIndex = self.alphabet.index(self.key[i])
            
            newIndex = aIndex + kIndex
            
            if newIndex >= len(self.alphabet):
                newIndex = newIndex - len(self.alphabet)
                
            letters[i] = self.alphabet[newIndex]
        
        return ''.join(letters)
    
    def decode(self, text):
        letters = list(text)
        while len(text) > len(self.key):
            self.key += self.key
            
        for i in range(0, len(letters)):
            if letters[i] not in list(self.alphabet):
                continue
                
            aIndex = self.alphabet.index(letters[i])
            kIndex = self.alphabet.index(self.key[i])
                                                  
            newIndex = aIndex - kIndex
                                                  
            if newIndex < 0:
                newIndex = newIndex + len(self.alphabet)
                                                  
            letters[i] = self.alphabet[newIndex]
            
        return ''.join(letters)
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet * 999
    
    def encode(self, text):
        key_counter = 0
        encoded = ""
        if len(text) > len(self.key):
            self.key = self.key*len(text)
        else:
            pass
        
        for letter in text:
            if letter in self.alphabet:
                encoded += self.alphabet[self.alphabet.index(letter)+self.alphabet.index(self.key[key_counter])]
                key_counter += 1
            else:
                encoded += letter
                key_counter += 1
        return encoded
    
    def decode(self, text):
        key_counter = 0
        decoded = ""
        if len(text) > len(self.key):
            self.key = self.key*len(text)
        else:
            pass
        
        for letter in text:
            if letter in self.alphabet:
                decoded += self.alphabet[self.alphabet.index(letter)-self.alphabet.index(self.key[key_counter])]
                key_counter += 1
            else:
                decoded += letter
                key_counter += 1
        return decoded
_____________________________________________
class VigenereCipher():
    
    def __init__(self, key, abc):
        self.key = key
        self.alphabet = abc
        
    def encode(self, text):
        ciphertext = ""
        key_len = len(text)//len(self.key) + 1
        new_key = key_len*self.key
        for count, char in enumerate(text):
            if char in self.alphabet:
                key_index = self.alphabet.index(new_key[count])
                new_index = (self.alphabet.index(char) + key_index)%len(self.alphabet)   
                new_char = self.alphabet[new_index]
                ciphertext = ciphertext + new_char
            else:
                ciphertext = ciphertext + char
        return ciphertext
        
    def decode(self, text):
        phrase = ""
        key_len = len(text)//len(self.key) + 1
        new_key = key_len*self.key
        for count, char in enumerate(text):
            if char in self.alphabet:
                key_index = self.alphabet.index(new_key[count])
                new_index = (self.alphabet.index(char) - key_index)%len(self.alphabet)             
                new_char = self.alphabet[new_index]
                phrase = phrase + new_char
            else:
                phrase = phrase + char
        return phrase
_____________________________________________
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key = key
        self.keylen = len(key)
        self.alphalen = len(alphabet)
        self.dic1 = dict(zip(alphabet, list(range(self.alphalen))))
        self.dic2 = dict(zip(list(range(self.alphalen)), alphabet))
    
    def encode(self, text):
        if self.keylen == 0 or self.alphalen == 0:
            return text
        else:
            res = ''
            text = text
            for i in range(len(text)):
                if text[i] in self.dic1:
                    shift = self.dic1[self.key[i%self.keylen]]
                    res += self.dic2[(self.dic1[text[i]] + shift) % self.alphalen]
                else:
                    res += text[i]
            return res
    
    def decode(self, text):
        if self.keylen == 0 or self.alphalen == 0:
            return text
        else:
            res = ''
            text = text
            for i in range(len(text)):
                if text[i] in self.dic1:
                    shift = self.dic1[self.key[i%self.keylen]]
                    res += self.dic2[(self.dic1[text[i]] - shift + self.alphalen) % self.alphalen]
                else:
                    res += text[i]
            return res
