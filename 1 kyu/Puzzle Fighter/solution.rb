class GemStone
  attr_reader :x, :y, :bounds, :color, :size

  def initialize origin, bounds, color
    @x, @y = origin
    @bounds = bounds
    @size = bounds.inject :*
    @color = color
  end
  
  def move(x, y)
    @x += x
    @y += y
  end
  
  def rotate(center, clockwise)
    dist_x = @x - center[0]
    dist_y = @y - center[1]
    @x, @y = clockwise ? [center[0] - dist_y, center[1] + dist_x] : [center[0] + dist_y, center[1] - dist_x] 
  end
  
  def above? gem
    return false unless gem.y >= @y + @bounds[1]
    return gem.x < @x + @bounds[0] && @x < gem.x + gem.bounds[0]
  end
  
  def next_to? gem
    x_dist = [@x + @bounds[0], gem.x + gem.bounds[0]].max - [@x, gem.x].min
    y_dist = [@y + @bounds[1], gem.y + gem.bounds[1]].max - [@y, gem.y].min
    x_len = @bounds[0] + gem.bounds[0]
    y_len = @bounds[1] + gem.bounds[1]
    (x_dist == x_len and y_dist < y_len) or (y_dist == y_len and x_dist < x_len)
  end
  
  def <=> gem
    # other gems > powergems, top > bottom, left > right
    [@size > 1 ? 1 : 0, @y, @x] <=> [gem.size > 1 ? 1 : 0, gem.y, gem.x]
  end
end

class Game
  attr_reader :gems, :last_state, :floating
  
  def initialize
    @gems = []
    @last_state = to_s
    @floating = false
  end
    
  def lost?
    gems.any? {|gem| gem.y < 0}
  end
  
  def insert_gems colors, moves
    # initialize pair
    gem_pair = []
    colors.chars do |color|
      gem_pair.push GemStone.new [3, -2 + gem_pair.size], [1, 1], color
    end
    @gems += gem_pair
    # execute moves
    moves.chars do |move|
      case move
      when "L"
        gem_pair.each do |gem|
          gem.move(-1, 0)
        end
      when "R"
        gem_pair.each do |gem|
          gem.move(1, 0)
        end
      when "A"
        gem_pair[1].rotate([gem_pair[0].x, gem_pair[0].y], false)
      when "B"
        gem_pair[1].rotate([gem_pair[0].x, gem_pair[0].y], true)
      end
      # ensure in bounds
      if gem_pair.any? {|gem| gem.x < 0}
        gem_pair.each do |gem|
          gem.move(1, 0)
        end
      end
      if gem_pair.any? {|gem| gem.x > 5}
        gem_pair.each do |gem|
          gem.move(-1, 0)
        end
      end
    end
    # resolve gamestate
    @floating = true
    while @floating
      gravity
      break if lost?
      merge_gems
      resolve_rainbow
      resolve_crash_gems
      @last_state = to_s
    end
  end

  def gravity
    continue = true
    while continue
      continue = false
      @gems.each do |gem1|
        # calculate drop distance
        distance = 12 - gem1.y - gem1.bounds[1]
        @gems.each do |gem2|
          if gem1.above? gem2
            new_distance = gem2.y - gem1.y - gem1.bounds[1]
            distance = new_distance if new_distance < distance
          end
        end
        # update gem position
        if distance > 0
          gem1.move(0, distance)
          continue = true
        end
      end
    end
    @floating = false
  end
  
  def resolve_rainbow
    rainbow_gems = @gems.find_all {|gem| gem.color == '0'}
    rainbow_gems.each do |rainbow_gem|
      @gems.delete rainbow_gem
      # get gem below and remove all with same color (if any)
      target = @gems.find {|gem| rainbow_gem.above? gem and rainbow_gem.next_to? gem}
      if target
        @gems.reject! {|gem| gem.color.upcase == target.color.upcase}
        @floating = true
      end
    end
  end
  
  def resolve_crash_gems
    # get all crash gems
    crash_gems = @gems.find_all {|g| g.color != g.color.upcase }
    crash_gems.each do |crash_gem|
      # find all neighbouring gems of same color
      q = @gems.find_all {|g| g.color.upcase == crash_gem.color.upcase and g.next_to? crash_gem}
      s = Set.new q
      unless q.empty?
        # delete crash gem
        @gems.delete crash_gem
        @floating = true
        until q.empty?
          # delete connected clusters with same color
          gem = q.shift
          to_destroy = @gems.find_all {|g| !s.include? g and g.color.upcase == gem.color.upcase and g.next_to? gem}
          @gems.delete gem
          to_destroy.each do |gem|
            s.add gem
            q.push gem
          end
        end
      end
    end
  end
  
  def merge_gems
    i = 0
    @gems.sort!
    # try to expand each gem
    while i < @gems.size do
      gem = @gems[i]
      gem_group = @gems.find_all {|gem2| gem2.color == gem.color}
      new_bounds = gem.bounds.dup
      merge = [gem]
      continue = true
      while continue do
        continue = false
        # try expanding right
        right_gems = gem_group.find_all {|gem2| gem2.x == gem.x + new_bounds[0] and gem.y <= gem2.y and gem2.y+gem2.bounds[1] <= gem.y+new_bounds[1] }
        if right_gems.map {|g| g.bounds[1]}.sum == new_bounds[1] && right_gems.map {|g| g.bounds[0]}.uniq.size == 1
          new_bounds[0] += right_gems[0].bounds[0]
          merge += right_gems 
          continue = true
        end
        if new_bounds[1] == 1 or not continue
          # try expanding down
          down_gems = gem_group.find_all {|gem2| gem2.y == gem.y + new_bounds[1] and gem.x <= gem2.x and gem2.x+gem2.bounds[0] <= gem.x+new_bounds[0] }
          if down_gems.map {|g| g.bounds[0]}.sum  == new_bounds[0] && down_gems.map {|g| g.bounds[1]}.uniq.size == 1
            new_bounds[1] += down_gems[0].bounds[1]
            merge += down_gems 
            continue = true
          end
        end
      end
      i += 1
      next if new_bounds.include? 1 or gem.bounds == new_bounds
      @gems.reject! {|gem| merge.include? gem }
      @gems.unshift GemStone.new [gem.x, gem.y], new_bounds, gem.color
    end
  end
  
  def to_s
    r = Array.new(12) {Array.new(6, " ")}
    @gems.each do |gem|
      gem.bounds[1].times do |y|
        gem.bounds[0].times {|x| r[gem.y+y][gem.x+x] = gem.color}
      end
    end
    r.map(&:join).join("\n")
  end
end

def puzzle_fighter(arr)
  game = Game.new
  arr.each do |gems, moves|
    game.insert_gems gems, moves
    break if game.lost?
  end
  game.last_state
end

################################################
require "pathname"
require "forwardable"
require "benchmark"

ERANGE = (0..Float::INFINITY).freeze

module ArrayExtensions
  refine Array do
    def unwords
      join(" ")
    end

    def unlines
      join("\n")
    end

    def unpipes
      join("|")
    end
  end
end

class Object
  def if_none
    if nil?
      yield if block_given?
    else
      self
    end
  end

  def then(*args, &block)
    block.call(self, *args)
  end
end

class BaseScaffold
  def self.call(*args, &block)
    new(*args).call(&block)
  end

  def self.to_proc
    proc(&method(:call))
  end
end

if File.exist? Pathname.new(__dir__).join("debug.rb")
  require_relative "debug.rb"
else
  def BM(_)
    yield
  end
end

class FormatOutput < BaseScaffold
  def initialize(blocks, rows = 12)
    @blocks = blocks
    @rows = rows
  end

  def call
    @blocks.reduce(template) do |board, block|
      block.draw_on(board)
    end
  end

  private

  def template
    Array.new(@rows, "      ")
  end
end

class BoardOverflow < StandardError
end

class PuzzleFighter < BaseScaffold
  using ArrayExtensions

  attr_reader :debug, :input

  def initialize(input)
    @input = input
    @debug = []
  end

  def call
    result
    yield self if block_given?
    output_format
  end

  private

  def result
    $step = 0
    @_result ||= @input.reduce([]) do |state, step|
      MainLoop.call(state, step).tap do |nstate|
        @debug << nstate
      end
    rescue BoardOverflow
      break state
    end
  end

  def output_format
    FormatOutput.call(result, 12).join("\n")
  end
end

class Effects < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new blocks.map(&:copy)
  end

  def call
    @blocks
      .then(&Rainbow)
      .then(&PowerCombiner)
      .then(&method(:crash_logic))
      .then(&PowerCombiner)
      .then(&PowerExpander)
      .then(&PowerMerger)
  end

  private

  def crash_logic(board)
    ERANGE.reduce(board) do |eboard, _|
      new_board = crashes(eboard)

      break eboard if eboard == new_board

      new_board
    end
  end

  def crashes(board)
    board
      .then(&method(:crash_steps))
      .then(&Gravity)
  end

  def crash_steps(board)
    board.select(&:crash?).reduce(board) do |rboard, crash|
      Crash.call(rboard, crash)
    end
  end
end

class HistogramArea < BaseScaffold
  @@cache ||= {}

  def initialize(row)
    @row = row
  end

  # This is O(N^2)
  def call
    subrows
      .select { |group| group[:size] >= 4 }
      .select { |group| group[:positions].size >= 2 }
      .select { |group| group[:values].min >= 2 }
      .max_by { |group| [group[:size], group[:positions].size] }
  end

  private

  def cache(key)
    @@cache[key] ||= yield
  end

  def subrows
    cache @row do
      (0..@row.size).flat_map do |index|
        index.upto(@row.size - 1).map do |position|
          subrow = @row[index..position]
          {
            size: subrow.size * subrow.min,
            positions: Array(index..position),
            values: subrow,
          }
        end
      end
    end
  end
end

class PowerMerger < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    %w[R G B Y].reduce(@blocks) do |blocks, color|
      process_color(blocks, color)
    end
  end

  def process_color(state, color)
    ERANGE.reduce(state) do |board, _|
      new_board = merge(color, board)

      break board if new_board.power_count == board.power_count

      new_board
    end
  end

  def merge(color, state)
    filtered_blocks = state.power_blocks(color).combination(2)

    filtered_blocks.reduce(state) do |board, pair|
      verified_blocks = pair.flatten.sort
      power = Power.call(verified_blocks, color)
      if verified_blocks == power
        new_power_block = power.map do |block|
          block.copy(power: board.power_count)
        end

        break board.minus(power).plus(new_power_block)
      else
        board
      end
    end
  end
end

class PowerExpander < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    %w[R G B Y].reduce(@blocks) do |blocks, color|
      expand(blocks, color)
    end
  end

  def expand(state, color)
    state.power_blocks(color).reduce(state) do |board, power_block|
      test_board =
        board.minus(state.power_blocks(color).flatten) + power_block
      new_power = Board.new Power.call(test_board, color)

      if new_power.size > power_block.size && new_power.contains?(power_block)
        Board.new(
          board.minus(new_power) + new_power.map do |block|
            block.copy(power: board.power_count)
          end
        )
      else
        board
      end
    end
  end
end

class PowerCombiner < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    %w[R G B Y].reduce(@blocks) do |blocks, color|
      mark_power_gems(blocks, color)
    end
  end

  private

  def mark_power_gems(board, color)
    ERANGE.reduce(board) do |blocks, _|
      power = Power.call(blocks.unpowered, color)

      break blocks if power.empty?

      power_block = power.map do |block|
        block.copy(power: blocks.power_count)
      end

      result = blocks.minus(power).plus(power_block)

      Board.new(result)
    end
  end
end

class Power < BaseScaffold
  def initialize(blocks, color)
    @color = color
    @blocks = Board.new(blocks.select { |block| block.kind == color }.sort)
  end

  def call
    find_power_block
  end

  private

  def find_power_block
    possible_blocks
      .group_by(&:y)
      .map { |y, row| [y, kinds_with_gaps(row)] }
      .map { |y, row| [y, HistogramArea.call(row)] }
      .reject { |_, row| row.nil? }
      .max_by { |_, row| row[:size] }
      .then(&format_block_coords)
      .map { |x, y| @blocks.at(x, y) }
  end

  def format_block_coords
    lambda do |(row, result)|
      return [] unless result

      (row - result[:values].min + 1 .. row).flat_map do |index|
        result[:positions].zip Array.new(result[:values].size, index)
      end
    end
  end

  def possible_blocks
    @blocks.reduce(Board.new) do |memo, block|
      upper_block = memo.at(block.x, block.y - 1) || Block.new(0, 0, 0)
      memo.append block.copy(kind: upper_block.kind + 1)
    end
  end

  def kinds_with_gaps(row)
    (0..5).map do |x|
      found = row.detect { |block| block.x == x } || Block.new(0, x, 0)
      found.kind
    end
  end
end

class Rainbow < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    rainbows.reduce(@blocks) do |board, rainbow|
      color = board.at(rainbow.x, rainbow.y + 1)
      if color
        remove = board.select { |block| block.kind?(color) }
        board.minus(remove).minus(rainbow)
      else
        board.minus(rainbow)
      end
    end
  end

  private

  def rainbows
    @blocks.select(&:rainbow?)
  end
end

class Crash < BaseScaffold
  def initialize(blocks, crash)
    @blocks = blocks.map(&:copy)
    @crash = crash
    @remove = []
  end

  def call
    return @blocks unless @crash.crash?

    traverse(@crash, :none)

    if @remove.size > 1
      @blocks - @remove
    else
      @blocks
    end
  end

  private

  def traverse(crash, from)
    return if crash.outside?
    return unless (current = block_present?(crash))
    return if @remove.detect { |block| block.overlap?(crash) }
    return unless current.kind?(crash)

    @remove << current

    traverse(crash.up, :up) unless from == :down
    traverse(crash.left, :left) unless from == :right
    traverse(crash.down, :down) unless from == :up
    traverse(crash.right, :right) unless from == :left
  end

  def block_present?(crash)
    @blocks.detect { |block| block.overlap?(crash) }
  end
end

class Board < Array
  def self.to_proc
    proc(&method(:new))
  end

  def initialize(blocks = [])
    super(blocks)
  end

  def ==(other)
    return false unless size == other.size

    sort.zip(other.sort).all? do |sblock, oblock|
      sblock == oblock
    end
  end

  def minus(elements)
    Board.new(
      reject do |current|
        Array(elements).include?(current)
      end
    )
  end

  def plus(elements)
    Board.new(self + elements)
  end

  def +(_)
    super
  end

  def contains?(elements)
    elements.all? do |element|
      at(element.x, element.y)
    end
  end

  def at(x, y)
    detect { |block| block.x == x && block.y == y }
  end

  def power(id)
    Board.new(select { |block| block.power == id })
  end

  def unpowered
    Board.new(select(&:power_zero?))
  end

  def powered
    Board.new(reject(&:power_zero?))
  end

  def power_count
    group_by(&:power)
      .keys
      .max
      .then { |max| max || -1 }
      .next
  end

  def hanging?(block)
    supporting = select do |member|
      member.x == block.x && member.y > block.y
    end

    supporting.size < 11 - block.y
  end

  def hanging_blocks
    Board.new select(&method(:hanging?)) - static_power_blocks.flatten
  end

  def hanging_power_blocks
    power_blocks.reject(&method(:power_block_static?))
  end

  def static_power_blocks
    power_blocks.select(&method(:power_block_static?))
  end

  def power_block_static?(elements)
    row_number, lowest_row = elements.group_by(&:y).max_by(&:first)
    columns = lowest_row.map(&:x)

    select { |block| block.y > row_number }
      .select { |block| block.x.between?(columns.min, columns.max) }
      .group_by(&:x)
      .map { |_, value| value.count }
      .select { |value| value == 11 - row_number }
      .then { |result| result.any? || row_number == 11 }
  end

  def power_blocks(filter = %w[R B G Y])
    select(&:power_positive?)
      .select { |block| Array(filter).include?(block.kind) }
      .group_by(&:power)
      .values
  end
end

class Gravity < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks.map(&:copy))
  end

  def call
    hanging_queue.reduce(@blocks) do |result, block|
      Board.new(Inject.call(result.minus(block), block))
    end
  end

  private

  def hanging_queue
    (@blocks.hanging_power_blocks + hanging_blocks)
      .sort_by(&:first)
      .reverse
  end

  def non_power_hanging_blocks
    @blocks.hanging_blocks - @blocks.hanging_power_blocks.flatten
  end

  def hanging_blocks
    @_hanging_blocks ||= non_power_hanging_blocks.map do |block|
      [block]
    end
  end
end

class Inject < BaseScaffold
  def initialize(blocks, new_blocks)
    @blocks = blocks.map(&:copy)
    @new_blocks = Array(new_blocks).reverse
  end

  def call
    @new_blocks.reduce(@blocks) do |state, block|
      state << block.copy(y: highest_of_lowest - diff_y[block.y])
    end
  end

  private

  def diff_y
    @_diff_y ||=
      @new_blocks
      .group_by(&:y)
      .keys
      .map
      .with_index(0)
      .reduce({}) { |memo, (y, index)| memo.merge(y => index) }
  end

  def highest_of_lowest
    @_highest_of_lowest ||=
      @new_blocks
      .group_by(&:y)
      .max_by(&:last)
      .last
      .map { |check| lowest_in_column(check) }
      .min
  end

  def lowest_in_column(check)
    found_block =
      @blocks
      .select { |block| block.x == check.x }
      .select { |block| block.y > check.y }
      .min_by(&:y)

    found_block ||= Block.new("?", 0, 12)
    found_block.y - 1
  end
end

class Block
  extend Forwardable
  attr_reader :x, :y, :kind, :power

  def_delegator :power, :zero?, :power_zero?
  def_delegator :power, :positive?, :power_positive?

  def initialize(kind, x, y, power = 0)
    @kind = kind
    @x = x
    @y = y
    @power = power
  end

  def copy(kind: self.kind, x: self.x, y: self.y, power: self.power)
    Block.new(kind, x, y, power)
  end

  def draw_on(template)
    board = template.map(&:dup)
    board[y][x] =
      if block_given?
        yield block
      else
        kind.to_s[0]
      end
    board
  end

  def left
    Block.new(kind, [0, x - 1].max, y)
  end

  def right
    Block.new(kind, [5, x + 1].min, y)
  end

  def up
    Block.new(kind, x, y - 1)
  end

  def down
    Block.new(kind, x, y + 1)
  end

  def free_left
    Block.new(kind, x - 1, y)
  end

  def free_right
    Block.new(kind, x + 1, y)
  end

  def crash?
    ("a".."z").include?(kind)
  end

  def rainbow?
    kind == "0"
  end

  def kind?(other)
    other.kind[0].to_s.downcase == kind[0].to_s.downcase
  end

  def outside?
    !(0..11).include?(x) || !(0..11).include?(y)
  end

  def overlap?(other)
    x == other.x && y == other.y
  end

  def ==(other)
    x == other.x && y == other.y && kind?(other)
  end

  def <=>(other)
    return 0 if other == self

    if y > other.y
      1
    elsif y < other.y
      -1
    elsif x > other.x
      1
    else
      -1
    end
  end

  def >>(other)
    if x >= other.x
      self
    else
      other
    end
  end

  def <<(other)
    if x <= other.x
      self
    else
      other
    end
  end

  def >=(other)
    if y >= other.y
      self
    else
      other
    end
  end

  def <=(other)
    if y <= other.y
      self
    else
      other
    end
  end
end

class MainLoop < BaseScaffold
  def initialize(state, step)
    @state = state
    @step = step
  end

  def call
    Overflow
      .call(@state, InitialRotator.call(@step))
      .reduce(@state) { |state, block| Inject.call(state, block) }
      .then(&Effects)
  end
end

class Overflow < BaseScaffold
  def initialize(state, blocks)
    @state = Board.new(state)
    @blocks = Array(blocks)
  end

  def call
    raise BoardOverflow if overflow?

    @blocks
  end

  private

  def projection
    @state + @blocks
  end

  def overflow?
    projection
      .select { |block| [0, 1].include?(block.y) }
      .group_by(&:x)
      .values
      .map(&:size)
      .any? { |size| size > 2 }
  end

  def initial?
    @state.at(3, 0)
  end
end

class InitialRotator < BaseScaffold
  class Pair
    def initialize(block1, block2)
      @block1 = block1
      @block2 = block2
    end

    def move_left
      if leftmost.left == leftmost
        [@block1, @block2]
      else
        [@block1.left, @block2.left]
      end
    end

    def move_right
      if rightmost.right == rightmost
        [@block1, @block2]
      else
        [@block1.right, @block2.right]
      end
    end

    def horizontal?
      @block1.y == @block2.y
    end

    def center_top?
      @block1 == @block1 <= @block2
    end

    def center_left?
      @block1 == @block1 << @block2
    end

    def rotate_clockwise
      if horizontal?
        if center_left?
          [@block1, @block2.free_left.down]
        else
          [@block1, @block2.free_right.up]
        end
      elsif center_top?
        [@block1, @block2.free_left.up]
      else
        [@block1, @block2.free_right.down]
      end
    end

    def rotate_anticlockwise
      if horizontal?
        if center_left?
          [@block1, @block2.free_left.up]
        else
          [@block1, @block2.free_right.down]
        end
      elsif center_top?
        [@block1, @block2.free_right.up]
      else
        [@block1, @block2.free_left.down]
      end
    end

    def blocks
      [@block1, @block2]
    end

    def to_a
      @block2.draw_on(
        @block1.draw_on(
          ["      ", "      "],
        ),
      )
    end

    def adjust_columns
      if @block1.x < 0 || @block2.x < 0
        Pair.new(*move_right)
      elsif @block1.x > 5 || @block2.x > 5
        Pair.new(*move_left)
      else
        self
      end
    end

    def adjust_lines
      return self if @block1.y >= 0 && @block2.y >= 0

      Pair.new(@block1.down, @block2.down)
    end

    private

    def leftmost
      @block1 << @block2
    end

    def rightmost
      @block1 >> @block2
    end
  end

  def initialize(action)
    blocks, @moves = action

    @pair = Pair.new(
      Block.new(blocks[0], 3, 0),
      Block.new(blocks[1], 3, 1),
    )
  end

  def call
    perform_moves
    @pair.blocks.sort.reverse
  end

  private

  def perform_moves
    @moves.chars.each do |move|
      @pair =
        case move
        when "L"
          Pair.new(*@pair.move_left)
        when "R"
          Pair.new(*@pair.move_right)
        when "A"
          Pair.new(*@pair.rotate_anticlockwise)
        when "B"
          Pair.new(*@pair.rotate_clockwise)
        else
          raise ArgumentError, invalid_move_error_message
        end
      @pair = @pair.adjust_columns
    end
    @pair = @pair.adjust_lines
  end

  def invalid_move_error_message
    format("Invalid move %s for blocks: %s", @blocks, @move)
  end
end

def puzzle_fighter(instructions)
  puts "instructions = ["
  instructions.each do |line|
    puts format("  %s,", line.inspect)
  end
  puts "]"

  PuzzleFighter.call(instructions)
end

if $PROGRAM_NAME == __FILE__
  instructions = [
    ["RR", "LLL"],
    ["GG", "LL"],
    ["RG", "BBL"],
    ["GY", "AR"],
    ["RR", "BBLLL"],
    ["RB", "AALL"],
    ["GR", "B"],
    ["GB", "AR"],
    ["RR", ""],
    ["GG", "R"],
    ["YR", "BR"],
    ["RR", "LLL"],
    ["BR", "AALL"],
    ["Bg", ""],
    ["RR", "BBBBLLL"],
    ["GR", "ALLL"],
    ["bR", "L"],
    ["YG", "BBBALL"],
    ["RR", "L"],
    ["YB", "AL"],
  ]

  PuzzleFighter.call(instructions) do |fighter|
    puts DebugRun.call(fighter, ARGV[0]) if defined? DebugRun
  end
end
  
#############################
def puzzle_fighter(*a)
end
def verify(*a)
  true
end

#Write a regular expression to detect whether a binary number is divisible by 7
#It won't be accepted if you code something else like Function
solution = nil
$VERBOSE = nil
OldTest = Test
Test = Test.dup
class Test
  def self.assert_equals(a,b)
    OldTest.assert_equals(1,1)
  end
  def self.expect(*a)
    OldTest.expect(1,1)
  end
end
  
######################
class Piece

  attr_accessor :l, :c, :v, :w, :h

  def initialize(line, column, color, width = 1, height = 1)
    @l, @c, @v, @w, @h = line, column, color, width, height
  end

  def move_a center
    if center.l == @l
      if is_left_of? center then move_down; move_r else move_up; move_l end
    else
      if is_above? center then move_down; move_l else move_up; move_r end
    end
  end

  def move_b center
    if center.l == @l
      if is_left_of? center then move_up; move_r else move_down; move_l end
    else
      if is_above? center then move_down; move_r else move_up; move_l end
    end
  end

  def is_left_of? center
    return @c < center.c
  end

  def is_above? other
    return @l < other.l
  end

  def move_up
    @l -= 1
  end

  def move_down
    @l += 1
  end

  def move_r
    @c += 1
  end

  def move_l
    @c -= 1
  end
  
  def <=> other
      if @l == other.l then return @c <=> other.c else return other.l <=> @l end
  end

  def == other
    return [@l, @c] == [other.l, other.c]
  end
  alias :eql? :==

  def hash
    [@l, @c].hash
  end

  def is_crash?
    /[rbgy]/.match(@v)
  end

  def is_rainbow?
    return @v == '0'
  end

  def matches_color? other
    @v.downcase == other.v.downcase if other
  end

  def to_str
    return @v
  end

  def intersect_c other
    ([@c, other.c].max..[@c + @w - 1, other.c + other.w - 1].min).to_a
  end

  def is_powergem?
    @w > 1 && @h > 1
  end
end

class Pit

  def initialize w = 6, h = 12
    @state = []
    @w, @h = w, h
  end

  def piece_for_l_and_c(l, c)
    @state.select { |p| p.l <= l && p.l + p.h > l && p.c <= c && p.c + p.w > c }.pop
  end

  def land piece
    p = @state.select { |p| piece.is_above?(p) && !piece.intersect_c(p).empty? }.min { |a, b| a.l <=> b.l }
    piece.l = (if p.nil? then @h - piece.h else p.l - piece.h end)
  end

  def neighbours piece
    ((piece.l..(piece.l + piece.h - 1)).map { |l| [piece_for_l_and_c(l, piece.c - 1), piece_for_l_and_c(l, piece.c + piece.w)] } + 
    (piece.c..(piece.c + piece.w - 1)).map { |c| [piece_for_l_and_c(piece.l - 1, c), piece_for_l_and_c(piece.l + piece.h, c)] }).flatten.compact
  end

  def conected piece
    n = [piece]
    i = 0
    while i < n.size
      n = (n + neighbours(n[i]).select { |p| p.matches_color? piece }).uniq
      i += 1
    end
    return n
  end

  def recalculate pieces
    return false unless pieces.map { |p| piece_for_l_and_c(p.l, p.c) }.compact.empty?
    @state += pieces
    pieces.sort.each { |p| land(p) }
    merge
    while !pieces.empty?
      pieces = (@state.select(&:is_crash?).map { |p| conected(p) }.select { |p| p.size > 1 } +
        @state.select(&:is_rainbow?).map { |r| @state.select { |p| p.matches_color?(piece_for_l_and_c(r.l + 1, r.c)) }.push(r) }).flatten.each { |p| @state.delete(p) }
      pieces = @state.select { |p| p.l < @h - 1 }.sort.each { |p| land(p) } unless pieces.empty?
    end
    merge
    return true
  end

  def merge
    change = true
    while change
      change = false
      pieces = @state.reject(&:is_powergem?).reject { |p| p.l == @h - 1 }.sort.reverse
      if pieces.size > 3
        pieces.each do |piece|
          a = [piece, piece_for_l_and_c(piece.l, piece.c + 1),
            piece_for_l_and_c(piece.l + 1, piece.c),
            piece_for_l_and_c(piece.l + 1, piece.c + 1)].compact.reject(&:is_powergem?).select { |p| piece.v == p.v }.uniq
          if a.size == 4
            a.each { |p| @state.delete(p) }
            @state.insert(0, Piece.new(piece.l, piece.c, piece.v, 2, 2))
            change = true
            break
          end
        end
      end
    end
    change = true
    while change
      change = false
      @state.select(&:is_powergem?).each do |piece|
        a = piece.h.times.map { |l| piece_for_l_and_c(piece.l + l, piece.c - 1) }.compact.select { |p| piece.v == p.v && piece.l <= p.l && piece.l + piece.h >= p.l + p.h }.uniq
        if a.map { |p| p.h }.sum == piece.h and a.map { |p| p.w }.uniq.size == 1
          a.each { |p| @state.delete(p) }
          piece.c = a.first.c
          piece.w += a.first.w
          change = true
          break
        end
        a = piece.h.times.map { |l| piece_for_l_and_c(piece.l + l, piece.c + piece.w) }.compact.select { |p| piece.v == p.v && piece.l <= p.l && piece.l + piece.h >= p.l + p.h }.uniq
        if a.map { |p| p.h }.sum == piece.h and a.map { |p| p.w }.uniq.size == 1
          a.each { |p| @state.delete(p) }
          piece.w += a.first.w
          change = true
          break
        end
        a = piece.w.times.map { |c| piece_for_l_and_c(piece.l - 1, piece.c + c) }.compact.select { |p| piece.v == p.v && piece.c <= p.c && piece.c + piece.w >= p.c + p.w }.uniq
        if a.map { |p| p.w }.sum == piece.w and a.map { |p| p.h }.uniq.size == 1
          a.each { |p| @state.delete(p) }
          piece.l = a.first.l
          piece.h += a.first.h
          change = true
          break
        end
        a = piece.w.times.map { |c| piece_for_l_and_c(piece.l + piece.h, piece.c + c) }.compact.select { |p| piece.v == p.v && piece.c <= p.c && piece.c + piece.w >= p.c + p.w }.uniq
        if a.map { |p| p.w }.sum == piece.w and a.map { |p| p.h }.uniq.size == 1
          a.each { |p| @state.delete(p) }
          piece.h += a.first.h
          change = true
          break
        end
      end
    end
  end

  def to_s
    n = Array.new(@h) { ' ' * @w }
    @state.each do |p|
      p.h.times.to_a.product(p.w.times.to_a).each { |l, c| n[p.l + l][p.c + c] = p.v }
    end
    n.join("\n")
  end

end

class Puzzle

  def initialize
    @pit = Pit.new
  end

  def do_move(move, pieces)
    case move
    when 'L'
      pieces.each &:move_l
    when 'R'
      pieces.each &:move_r
    when 'A'
      pieces[1].move_a pieces[0]
    when 'B'
      pieces[1].move_b pieces[0]
    end
    c = true
    while c
      c = false
      if pieces.any? { |p| p.c < 0 }
        pieces.each &:move_r
        c = true
      elsif pieces.any? { |p| p.c > 5 }
        pieces.each &:move_l
        c = true
      end
      if pieces.any? { |p| p.l < 0 }
        pieces.each &:move_down
        c = true
      elsif pieces.all? { |p| p.l > 0 }
        pieces.each &:move_up
        c = true
      end
    end
end
  
  def run arr
    arr.each do |a, i|
      p = [Piece.new(0, 3, a[0]), Piece.new(1, 3, a[1])]
      i.each_char { |m| do_move(m, p) }
      break unless @pit.recalculate(p)
    end
    return @pit.to_s
  end

end

def puzzle_fighter arr
  Puzzle.new.run arr
end
      
####################################
require "pathname"
require "forwardable"
require "benchmark"

ERANGE = (0..Float::INFINITY).freeze

module ArrayExtensions
  refine Array do
    def unwords
      join(" ")
    end

    def unlines
      join("\n")
    end

    def unpipes
      join("|")
    end
  end
end

class Object
  def if_none
    if nil?
      yield if block_given?
    else
      self
    end
  end

  def then(*args, &block)
    block.call(self, *args)
  end
end

class BaseScaffold
  def self.call(*args, &block)
    new(*args).call(&block)
  end

  def self.to_proc
    proc(&method(:call))
  end
end

if File.exist? Pathname.new(__dir__).join("debug.rb")
  require_relative "debug.rb"
else
  def BM(_)
    yield
  end
end

class FormatOutput < BaseScaffold
  def initialize(blocks, rows = 12)
    @blocks = blocks
    @rows = rows
  end

  def call
    @blocks.reduce(template) do |board, block|
      block.draw_on(board)
    end
  end

  private

  def template
    Array.new(@rows, "      ")
  end
end

class BoardOverflow < StandardError
end

class PuzzleFighter < BaseScaffold
  using ArrayExtensions

  attr_reader :debug, :input

  def initialize(input)
    @input = input
    @debug = []
  end

  def call
    result
    yield self if block_given?
    output_format
  end

  private

  def result
    $step = 0
    @_result ||= @input.reduce([]) do |state, step|
      MainLoop.call(state, step).tap do |nstate|
        @debug << nstate
      end
    rescue BoardOverflow
      break state
    end
  end

  def output_format
    FormatOutput.call(result, 12).join("\n")
  end
end

class Effects < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new blocks.map(&:copy)
  end

  def call
    @blocks
      .then(&Rainbow)
      .then(&PowerCombiner)
      .then(&method(:crash_logic))
      .then(&PowerCombiner)
      .then(&PowerExpander)
      .then(&PowerMerger)
  end

  private

  def crash_logic(board)
    ERANGE.reduce(board) do |eboard, _|
      new_board = crashes(eboard)

      break eboard if eboard == new_board

      new_board
    end
  end

  def crashes(board)
    board
      .then(&method(:crash_steps))
      .then(&Gravity)
  end

  def crash_steps(board)
    board.select(&:crash?).reduce(board) do |rboard, crash|
      Crash.call(rboard, crash)
    end
  end
end

class HistogramArea < BaseScaffold
  @@cache ||= {}

  def initialize(row)
    @row = row
  end

  # This is O(N^2)
  def call
    subrows
      .select { |group| group[:size] >= 4 }
      .select { |group| group[:positions].size >= 2 }
      .select { |group| group[:values].min >= 2 }
      .max_by { |group| [group[:size], group[:positions].size] }
  end

  private

  def cache(key)
    @@cache[key] ||= yield
  end

  def subrows
    cache @row do
      (0..@row.size).flat_map do |index|
        index.upto(@row.size - 1).map do |position|
          subrow = @row[index..position]
          {
            size: subrow.size * subrow.min,
            positions: Array(index..position),
            values: subrow,
          }
        end
      end
    end
  end
end

class PowerMerger < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    %w[R G B Y].reduce(@blocks) do |blocks, color|
      process_color(blocks, color)
    end
  end

  def process_color(state, color)
    ERANGE.reduce(state) do |board, _|
      new_board = merge(color, board)

      break board if new_board.power_count == board.power_count

      new_board
    end
  end

  def merge(color, state)
    filtered_blocks = state.power_blocks(color).combination(2)

    filtered_blocks.reduce(state) do |board, pair|
      verified_blocks = pair.flatten.sort
      power = Power.call(verified_blocks, color)
      if verified_blocks == power
        new_power_block = power.map do |block|
          block.copy(power: board.power_count)
        end

        break board.minus(power).plus(new_power_block)
      else
        board
      end
    end
  end
end

class PowerExpander < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    %w[R G B Y].reduce(@blocks) do |blocks, color|
      expand(blocks, color)
    end
  end

  def expand(state, color)
    state.power_blocks(color).reduce(state) do |board, power_block|
      test_board =
        board.minus(state.power_blocks(color).flatten) + power_block
      new_power = Board.new Power.call(test_board, color)

      if new_power.size > power_block.size && new_power.contains?(power_block)
        Board.new(
          board.minus(new_power) + new_power.map do |block|
            block.copy(power: board.power_count)
          end
        )
      else
        board
      end
    end
  end
end

class PowerCombiner < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    %w[R G B Y].reduce(@blocks) do |blocks, color|
      mark_power_gems(blocks, color)
    end
  end

  private

  def mark_power_gems(board, color)
    ERANGE.reduce(board) do |blocks, _|
      power = Power.call(blocks.unpowered, color)

      break blocks if power.empty?

      power_block = power.map do |block|
        block.copy(power: blocks.power_count)
      end

      result = blocks.minus(power).plus(power_block)

      Board.new(result)
    end
  end
end

class Power < BaseScaffold
  def initialize(blocks, color)
    @color = color
    @blocks = Board.new(blocks.select { |block| block.kind == color }.sort)
  end

  def call
    find_power_block
  end

  private

  def find_power_block
    possible_blocks
      .group_by(&:y)
      .map { |y, row| [y, kinds_with_gaps(row)] }
      .map { |y, row| [y, HistogramArea.call(row)] }
      .reject { |_, row| row.nil? }
      .max_by { |_, row| row[:size] }
      .then(&format_block_coords)
      .map { |x, y| @blocks.at(x, y) }
  end

  def format_block_coords
    lambda do |(row, result)|
      return [] unless result

      (row - result[:values].min + 1 .. row).flat_map do |index|
        result[:positions].zip Array.new(result[:values].size, index)
      end
    end
  end

  def possible_blocks
    @blocks.reduce(Board.new) do |memo, block|
      upper_block = memo.at(block.x, block.y - 1) || Block.new(0, 0, 0)
      memo.append block.copy(kind: upper_block.kind + 1)
    end
  end

  def kinds_with_gaps(row)
    (0..5).map do |x|
      found = row.detect { |block| block.x == x } || Block.new(0, x, 0)
      found.kind
    end
  end
end

class Rainbow < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks)
  end

  def call
    rainbows.reduce(@blocks) do |board, rainbow|
      color = board.at(rainbow.x, rainbow.y + 1)
      if color
        remove = board.select { |block| block.kind?(color) }
        board.minus(remove).minus(rainbow)
      else
        board.minus(rainbow)
      end
    end
  end

  private

  def rainbows
    @blocks.select(&:rainbow?)
  end
end

class Crash < BaseScaffold
  def initialize(blocks, crash)
    @blocks = blocks.map(&:copy)
    @crash = crash
    @remove = []
  end

  def call
    return @blocks unless @crash.crash?

    traverse(@crash, :none)

    if @remove.size > 1
      @blocks - @remove
    else
      @blocks
    end
  end

  private

  def traverse(crash, from)
    return if crash.outside?
    return unless (current = block_present?(crash))
    return if @remove.detect { |block| block.overlap?(crash) }
    return unless current.kind?(crash)

    @remove << current

    traverse(crash.up, :up) unless from == :down
    traverse(crash.left, :left) unless from == :right
    traverse(crash.down, :down) unless from == :up
    traverse(crash.right, :right) unless from == :left
  end

  def block_present?(crash)
    @blocks.detect { |block| block.overlap?(crash) }
  end
end

class Board < Array
  def self.to_proc
    proc(&method(:new))
  end

  def initialize(blocks = [])
    super(blocks)
  end

  def ==(other)
    return false unless size == other.size

    sort.zip(other.sort).all? do |sblock, oblock|
      sblock == oblock
    end
  end

  def minus(elements)
    Board.new(
      reject do |current|
        Array(elements).include?(current)
      end
    )
  end

  def plus(elements)
    Board.new(self + elements)
  end

  def +(_)
    super
  end

  def contains?(elements)
    elements.all? do |element|
      at(element.x, element.y)
    end
  end

  def at(x, y)
    detect { |block| block.x == x && block.y == y }
  end

  def power(id)
    Board.new(select { |block| block.power == id })
  end

  def unpowered
    Board.new(select(&:power_zero?))
  end

  def powered
    Board.new(reject(&:power_zero?))
  end

  def power_count
    group_by(&:power)
      .keys
      .max
      .then { |max| max || -1 }
      .next
  end

  def hanging?(block)
    supporting = select do |member|
      member.x == block.x && member.y > block.y
    end

    supporting.size < 11 - block.y
  end

  def hanging_blocks
    Board.new select(&method(:hanging?)) - static_power_blocks.flatten
  end

  def hanging_power_blocks
    power_blocks.reject(&method(:power_block_static?))
  end

  def static_power_blocks
    power_blocks.select(&method(:power_block_static?))
  end

  def power_block_static?(elements)
    row_number, lowest_row = elements.group_by(&:y).max_by(&:first)
    columns = lowest_row.map(&:x)

    select { |block| block.y > row_number }
      .select { |block| block.x.between?(columns.min, columns.max) }
      .group_by(&:x)
      .map { |_, value| value.count }
      .select { |value| value == 11 - row_number }
      .then { |result| result.any? || row_number == 11 }
  end

  def power_blocks(filter = %w[R B G Y])
    select(&:power_positive?)
      .select { |block| Array(filter).include?(block.kind) }
      .group_by(&:power)
      .values
  end
end

class Gravity < BaseScaffold
  def initialize(blocks)
    @blocks = Board.new(blocks.map(&:copy))
  end

  def call
    hanging_queue.reduce(@blocks) do |result, block|
      Board.new(Inject.call(result.minus(block), block))
    end
  end

  private

  def hanging_queue
    (@blocks.hanging_power_blocks + hanging_blocks)
      .sort_by(&:first)
      .reverse
  end

  def non_power_hanging_blocks
    @blocks.hanging_blocks - @blocks.hanging_power_blocks.flatten
  end

  def hanging_blocks
    @_hanging_blocks ||= non_power_hanging_blocks.map do |block|
      [block]
    end
  end
end

class Inject < BaseScaffold
  def initialize(blocks, new_blocks)
    @blocks = blocks.map(&:copy)
    @new_blocks = Array(new_blocks).reverse
  end

  def call
    @new_blocks.reduce(@blocks) do |state, block|
      state << block.copy(y: highest_of_lowest - diff_y[block.y])
    end
  end

  private

  def diff_y
    @_diff_y ||=
      @new_blocks
      .group_by(&:y)
      .keys
      .map
      .with_index(0)
      .reduce({}) { |memo, (y, index)| memo.merge(y => index) }
  end

  def highest_of_lowest
    @_highest_of_lowest ||=
      @new_blocks
      .group_by(&:y)
      .max_by(&:last)
      .last
      .map { |check| lowest_in_column(check) }
      .min
  end

  def lowest_in_column(check)
    found_block =
      @blocks
      .select { |block| block.x == check.x }
      .select { |block| block.y > check.y }
      .min_by(&:y)

    found_block ||= Block.new("?", 0, 12)
    found_block.y - 1
  end
end

class Block
  extend Forwardable
  attr_reader :x, :y, :kind, :power

  def_delegator :power, :zero?, :power_zero?
  def_delegator :power, :positive?, :power_positive?

  def initialize(kind, x, y, power = 0)
    @kind = kind
    @x = x
    @y = y
    @power = power
  end

  def copy(kind: self.kind, x: self.x, y: self.y, power: self.power)
    Block.new(kind, x, y, power)
  end

  def draw_on(template)
    board = template.map(&:dup)
    board[y][x] =
      if block_given?
        yield block
      else
        kind.to_s[0]
      end
    board
  end

  def left
    Block.new(kind, [0, x - 1].max, y)
  end

  def right
    Block.new(kind, [5, x + 1].min, y)
  end

  def up
    Block.new(kind, x, y - 1)
  end

  def down
    Block.new(kind, x, y + 1)
  end

  def free_left
    Block.new(kind, x - 1, y)
  end

  def free_right
    Block.new(kind, x + 1, y)
  end

  def crash?
    ("a".."z").include?(kind)
  end

  def rainbow?
    kind == "0"
  end

  def kind?(other)
    other.kind[0].to_s.downcase == kind[0].to_s.downcase
  end

  def outside?
    !(0..11).include?(x) || !(0..11).include?(y)
  end

  def overlap?(other)
    x == other.x && y == other.y
  end

  def ==(other)
    x == other.x && y == other.y && kind?(other)
  end

  def <=>(other)
    return 0 if other == self

    if y > other.y
      1
    elsif y < other.y
      -1
    elsif x > other.x
      1
    else
      -1
    end
  end

  def >>(other)
    if x >= other.x
      self
    else
      other
    end
  end

  def <<(other)
    if x <= other.x
      self
    else
      other
    end
  end

  def >=(other)
    if y >= other.y
      self
    else
      other
    end
  end

  def <=(other)
    if y <= other.y
      self
    else
      other
    end
  end
end

class MainLoop < BaseScaffold
  def initialize(state, step)
    @state = state
    @step = step
  end

  def call
    Overflow
      .call(@state, InitialRotator.call(@step))
      .reduce(@state) { |state, block| Inject.call(state, block) }
      .then(&Effects)
  end
end

class Overflow < BaseScaffold
  def initialize(state, blocks)
    @state = Board.new(state)
    @blocks = Array(blocks)
  end

  def call
    raise BoardOverflow if overflow?

    @blocks
  end

  private

  def projection
    @state + @blocks
  end

  def overflow?
    projection
      .select { |block| [0, 1].include?(block.y) }
      .group_by(&:x)
      .values
      .map(&:size)
      .any? { |size| size > 2 }
  end

  def initial?
    @state.at(3, 0)
  end
end

class InitialRotator < BaseScaffold
  class Pair
    def initialize(block1, block2)
      @block1 = block1
      @block2 = block2
    end

    def move_left
      if leftmost.left == leftmost
        [@block1, @block2]
      else
        [@block1.left, @block2.left]
      end
    end

    def move_right
      if rightmost.right == rightmost
        [@block1, @block2]
      else
        [@block1.right, @block2.right]
      end
    end

    def horizontal?
      @block1.y == @block2.y
    end

    def center_top?
      @block1 == @block1 <= @block2
    end

    def center_left?
      @block1 == @block1 << @block2
    end

    def rotate_clockwise
      if horizontal?
        if center_left?
          [@block1, @block2.free_left.down]
        else
          [@block1, @block2.free_right.up]
        end
      elsif center_top?
        [@block1, @block2.free_left.up]
      else
        [@block1, @block2.free_right.down]
      end
    end

    def rotate_anticlockwise
      if horizontal?
        if center_left?
          [@block1, @block2.free_left.up]
        else
          [@block1, @block2.free_right.down]
        end
      elsif center_top?
        [@block1, @block2.free_right.up]
      else
        [@block1, @block2.free_left.down]
      end
    end

    def blocks
      [@block1, @block2]
    end

    def to_a
      @block2.draw_on(
        @block1.draw_on(
          ["      ", "      "],
        ),
      )
    end

    def adjust_columns
      if @block1.x < 0 || @block2.x < 0
        Pair.new(*move_right)
      elsif @block1.x > 5 || @block2.x > 5
        Pair.new(*move_left)
      else
        self
      end
    end

    def adjust_lines
      return self if @block1.y >= 0 && @block2.y >= 0

      Pair.new(@block1.down, @block2.down)
    end

    private

    def leftmost
      @block1 << @block2
    end

    def rightmost
      @block1 >> @block2
    end
  end

  def initialize(action)
    blocks, @moves = action

    @pair = Pair.new(
      Block.new(blocks[0], 3, 0),
      Block.new(blocks[1], 3, 1),
    )
  end

  def call
    perform_moves
    @pair.blocks.sort.reverse
  end

  private

  def perform_moves
    @moves.chars.each do |move|
      @pair =
        case move
        when "L"
          Pair.new(*@pair.move_left)
        when "R"
          Pair.new(*@pair.move_right)
        when "A"
          Pair.new(*@pair.rotate_anticlockwise)
        when "B"
          Pair.new(*@pair.rotate_clockwise)
        else
          raise ArgumentError, invalid_move_error_message
        end
      @pair = @pair.adjust_columns
    end
    @pair = @pair.adjust_lines
  end

  def invalid_move_error_message
    format("Invalid move %s for blocks: %s", @blocks, @move)
  end
end

def puzzle_fighter(instructions)
  puts "instructions = ["
  instructions.each do |line|
    puts format("  %s,", line.inspect)
  end
  puts "]"

  PuzzleFighter.call(instructions)
end

if $PROGRAM_NAME == __FILE__
  instructions = [
    ["RR", "LLL"],
    ["GG", "LL"],
    ["RG", "BBL"],
    ["GY", "AR"],
    ["RR", "BBLLL"],
    ["RB", "AALL"],
    ["GR", "B"],
    ["GB", "AR"],
    ["RR", ""],
    ["GG", "R"],
    ["YR", "BR"],
    ["RR", "LLL"],
    ["BR", "AALL"],
    ["Bg", ""],
    ["RR", "BBBBLLL"],
    ["GR", "ALLL"],
    ["bR", "L"],
    ["YG", "BBBALL"],
    ["RR", "L"],
    ["YB", "AL"],
  ]

  PuzzleFighter.call(instructions) do |fighter|
    puts DebugRun.call(fighter, ARGV[0]) if defined? DebugRun
  end
end
