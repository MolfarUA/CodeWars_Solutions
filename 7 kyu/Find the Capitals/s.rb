53573877d5493b4d6e00050c


def capital(capitals_hash_array)
  capitals_hash_array.map do |hsh|
    state = hsh[:state] || hsh["state"] || hsh[:country] || hsh["country"]
    capital = hsh[:capital] || hsh["capital"]
    "The capital of #{state} is #{capital}"
  end
end
_________________________
def capital(capitals_hash_array)
  capitals_hash_array.map {|cc| "The capital of #{cc[:state] || cc['state'] || cc[:country] || cc['country']} is #{cc[:capital] || cc['capital']}"}
end
_________________________
def capital(capitals_hash_array)
  capitals_hash_array.map do |data|
    "The capital of #{data.search(:state, :country)} is #{data.search(:capital)}"
  end
end

class Hash
  def search(*keys)
    keys.each do |key|
      value = self[key] || self[key.to_s]
      return value if value
    end
  end
end
