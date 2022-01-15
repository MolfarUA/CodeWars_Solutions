class User
  RANKS = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]

  def initialize
    @points = 0
  end
  
  def rank
    RANKS[@points / 100] || 8
  end
  
  def progress
    rank == 8 ? 0 : @points % 100
  end
  
  def inc_progress(completed_rank)
    raise "Invalid rank" unless index = RANKS.index(completed_rank)

    @points += case delta = index - @points / 100
    when -1    then 1
    when 0     then 3
    when 1..16 then 10 * delta * delta
    else            0
    end    
  end
end
_____________________________________
class User
  def initialize
    @progress_max = 1500
    @progress = 0
    @ranks = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]
  end
  
  def rank
    @ranks[@progress / 100]
  end
  
  def progress
    @progress % 100
  end
  
  def inc_progress(kata_rank)
    raise ArgumentError unless @ranks.include? kata_rank
    d = (kata_rank > 0 ? kata_rank-1 : kata_rank) - (rank > 0 ? rank-1 : rank)
    @progress += d < -1 ? 0 : d == -1 ? 1 : d == 0 ? 3 : 10*d*d 
    @progress = @progress_max if @progress > @progress_max
  end
end
_____________________________________
class User
  RANKS = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]
  PROGRESS_THRESHOLD = 100
  attr_accessor :global_progress

  def initialize
    @global_progress = 0 
  end
  
  def rank
    RANKS[global_progress / PROGRESS_THRESHOLD]
  end
  
  def progress
    global_progress > ((RANKS.size - 1) * PROGRESS_THRESHOLD) ? 0 : global_progress % 100
  end

  #Completing an activity that is ranked the same as that of the user's will be worth 3 points
  #Completing an activity that is ranked one ranking lower than the user's will be worth 1 point
  #Any activities completed that are ranking 2 levels or more lower than the user's ranking will be ignored
  #The formula is 10 * d * d where d equals the difference in ranking between the activity and the user.
  
  def inc_progress(kata_rank)
    gap = RANKS.index(kata_rank) - RANKS.index(rank) 
    increase = gap < -1 ? 0 : gap < 0 ? 1 : gap == 0 ? 3 : 10 * gap * gap
    self.global_progress += increase #Store all progress anyway in case we need it later ;)
  end
end
_____________________________________
class User
  RANGE_OF_RANK = (-8..8).reject(&:zero?).freeze
  DEFAULT_VALUE = 0

  attr_reader :index, :progress

  def initialize
    @index = DEFAULT_VALUE
    @progress = DEFAULT_VALUE
  end

  def rank
    return max_rank if index > RANGE_OF_RANK.size-1
    RANGE_OF_RANK[index]
  end

  def inc_progress(activity_rank)
    raise if !RANGE_OF_RANK.include?(activity_rank)

    @progress += new_progress(activity_rank)
    @index += progress / 100
    @progress = rank == max_rank ? 0 : progress % 100
  end

  private
  
  def max_rank
    RANGE_OF_RANK.last
  end

  def new_progress(activity_rank)
    rank_difference = (RANGE_OF_RANK.index(activity_rank) - index).abs

    case
    when activity_rank < rank && rank_difference == 1 then 1
    when activity_rank == rank then 3
    when activity_rank > rank && activity_rank then 10*rank_difference**2
    else DEFAULT_VALUE
    end
  end
end
_____________________________________
class User
  attr_reader :rank, :progress
  RANKS = ((-8..-1).to_a + (1..8).to_a).sort
  
  
  def initialize
    @rank = RANKS.first
    @progress = 0
  end
  
  def inc_progress(rank)
    @progress += 
      case rank_index(rank) - rank_index(@rank)
      #Completing an activity that is ranked the same as that of the user's will be worth 3 points
      when 0
        3
      #Completing an activity that is ranked one ranking lower than the user's will be worth 1 point
      when -1
        1
      #Completing an activity ranked higher than the current user's rank will accelerate the rank progression. 
      when 1..100
        10*(rank_index(rank) - rank_index(@rank))**2
      #Any activities completed that are ranking 2 levels or more lower than the user's ranking will be ignored
      else
        0
      end
    inc_rank 
  end
  
  private
  def inc_rank
    return @progress = 0 if @rank == RANKS.last
    if @progress >= 100
      @progress -= 100
      @rank = RANKS[rank_index(@rank)+1]
      inc_rank
    end
  end
  
  def rank_index(rank)
    RANKS.index(rank)
  end
end
_____________________________________
class User
  attr_reader :rank, :progress

  RANKS = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]

  def initialize
    @rank = -8
    @progress = 0
  end
  
  def inc_progress(act_rank)
    diff = RANKS.find_index(act_rank) - RANKS.find_index(@rank)
    
    case
      when diff < 0
        exp = 1
      when diff == 0
        exp = 3
      when diff > 0
        exp = 10 * diff * diff
    end
    
    @rank = RANKS[RANKS.find_index(@rank) + ((@progress + exp) / 100)] || 8
    @progress = @rank != 8 ? (@progress + exp) % 100 : 0
  end
end
_____________________________________
class User

  def rank
    @rank = -8 + (overall_progress / 100.0).floor
    @rank += 1 if @rank >= 0
    @rank
  end
  
  def progress
    overall_progress.modulo(100)
  end
  
  def inc_progress(r)
    raise 'Oh No!' unless (-8..8).include?(r) && r != 0
    r -= 1 if r > 0 && rank < 0
    if rank < r
      @progress += 10 * (r - rank)**2
    elsif rank == r
      @progress += 3
    else
      @progress += 1
    end
  end
  
  private
  
  def overall_progress
    [@progress ||= 0,1500].min
  end

end
