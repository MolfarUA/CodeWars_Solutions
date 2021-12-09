def friend(friends)
  friends.select {|friend| friend.size == 4}
end
##########
def friend(friends)
  friends.select { |name| name.length == 4 }
end
#########
def friend(friends)
  friends.grep /^\w{4}$/
end
#######
def friend(friends)
  friends.reject{|f|f.length != 4}
end
#########
FRIEND_NAME_LENGTH = 4

def friend(friends)
  #your code here
  friends.select { |friend| friend.length == FRIEND_NAME_LENGTH }
end
##########
def friend(friends)
best_friends = friends.select do |friend|
    friend.length == 4
    end
return best_friends
end
#############
def friend(friends)
  friends.partition{|f| f.length == 4}.first
end
###########
def friend(friends)
  my_friends = [] 
  friends.each do |friend|
   friend.length == 4 && !(friend =~ /\d/) ? my_friends << friend : next
  end
  my_friends
end
##############
def friend(friends)
  my_friends = []
  friends.each { |name| my_friends << name if name.length == 4 }
  my_friends
end
###########
def friend(friends)
  friends.map { |name| name if name.length == 4 && name.start_with?(/[[:alpha:]]/) }.compact
end
