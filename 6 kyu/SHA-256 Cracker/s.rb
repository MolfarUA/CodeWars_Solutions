587f0abdd8730aafd4000035


require 'digest'

def sha256Crack(hash, characters)
  characters.chars.permutation
            .find{|x| Digest::SHA256.hexdigest(x.join('')) == hash}
            .join('') rescue nil
end
_________________________
require 'digest'

def sha256Crack(hash, characters)
  all = characters.chars.permutation.map &:join
  all.find{ |a| Digest::SHA256.hexdigest(a) == hash }
end
_________________________
require 'digest'
def sha256Crack(hash, characters)
  arr = (characters.chars.to_a.permutation.map &:join).collect{|p| [p, Digest::SHA256.hexdigest(p)]}.flatten
  index = arr.index(hash)
  return index ? arr[index-1] : nil
end
