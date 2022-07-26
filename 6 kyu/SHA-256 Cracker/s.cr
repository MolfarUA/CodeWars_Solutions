587f0abdd8730aafd4000035


require "openssl"

def sha256Crack(hash, characters)
  characters.
    chars.
    permutations.
    map(&.join).
    find{|s| OpenSSL::Digest.new("sha256").update(s).hexdigest == hash}
end
_________________________
require "openssl"

def sha256Crack(hash, characters)
  characters.chars.permutations(characters.size).map(&.join).each { |i| return i if OpenSSL::Digest.new("SHA256").update(i).hexdigest == hash }
end
_________________________
require "openssl"

def sha256Crack(hash, characters)
  result = nil
  h = OpenSSL::Digest.new("sha256")
  characters.chars.permutations.each do |perm|
    word = perm.join
    h.reset
    h.update(word)
    if h.hexdigest == hash
      result = word
      break
    end
  end
  result
end
