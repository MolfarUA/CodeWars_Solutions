53f40dff5f9d31b813000774

require 'tsort'

def recover_secret triplets
  graph = Hash.new([])
  
  triplets.each do |t|
  	1.upto(t.size) do |n|
  		graph[t[n-1]] += t.drop(n)
  	end
  end
  
  TSort.tsort(
  	lambda { |&b| graph.each_key(&b) },
  	lambda { |n, &b| graph[n].each(&b) }
  ).reverse.join
end
##########################
def recover_secret triplets
  # Assumptions.
  # Letters are in correct order of what they appear in the secret string
  # It is possible to deduce the secret string from the given triples
  # Thus all letters are given at least once, and more likely all are given multiple times
  # All letters are unique, and all letters in the triplets exist in the string
  # Extract an order from triplets, essentially
  
  
  # Happens_before modeling.
  # 1.First flatten the triplets, so we get a data structure containing each letter only once.
  # 1.1 Create a hash of it, with the key being the letter, value 0.
  # 3. iterate over triples. increment value in hash for first letter by 2, and for second letter by 1. 
  # We now know the order.
  # String construction:
  # 1. Sort hash-keys by their values in descending order, assemble character-keys as string
  letter_score = Hash[triplets.flatten.uniq.collect { |k| [k, []]}]
  triplets.each do |triplet|
    letter_score[triplet[0]] << triplet[1] 
    letter_score[triplet[0]] << triplet[2]
    letter_score[triplet[1]] << triplet[2]
  end
  letter_score.values.each{|list| list.uniq!}
  secret_string = []
  until letter_score.values.empty?
    next_letter = letter_score.min_by{|k,v| v.count}[0]
    # Get first letter from current secret_string
    secret_string << next_letter
    # Remove letter from lists
    letter_score.values.each{|list| list.delete(next_letter)}
    # Remove key from hash
    letter_score.delete(next_letter)
  end
  secret_string.reverse.join
  
  
end
###########################
require 'matrix'
def recover_secret triplets
  word = ''
  begin
    first,second,third = Matrix.columns(triplets).row_vectors.map(&:to_a)
    letter = (first - second - third).first
    if letter
      word << letter 
      triplets.each do |triplet|
        if triplet.include? letter
          triplet.shift
          triplet << nil
        end
      end
    end
  end while letter
  word
end
