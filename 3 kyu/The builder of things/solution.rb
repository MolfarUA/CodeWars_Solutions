5571d9fc11526780a000011a


require 'active_support/core_ext/string'

class Is
    def initialize(thing)
        @thing = thing
    end

    def method_name(n, *args, &block)
        raise "method_name not implemented"
    end

    def method_body(n, *args, &block)
        raise "method_body not implemented"
    end

    def method_missing(m, *args, &block)
        name = method_name(m, *args, &block)
        body = method_body(m, *args, &block)

        @thing.define_singleton_method(name, body)
    end

    def respond_to?(m, include_private = false)
        @thing.respond_to?(m, include_private) || super
    end
end

class IsA < Is
    def initialize(thing)
        super(thing)
    end

    def method_name(m, *args, &block)
        "#{m}?"
    end

    def method_body(m, *args, &block)
        -> { true }
    end
end

class IsNotA < Is
    def initialize(thing)
        super(thing)
    end

    def method_name(m, *args, &block)
        "#{m}?"
    end

    def method_body(m, *args, &block)
        -> { false }
    end
end

class Has
    def initialize(thing, num)
        @thing = thing
        @num = num
    end

    def method_missing(m, *args, &block)
        name = m.to_s.singularize
        value = Thing.new(name)

        if @num != 1
            value = []
            @num.times { value << Thing.new(name) }
        end

        data = Each.new(value)

        var_name = "@#{m.to_s}"
        @thing.instance_variable_set(var_name, data)
        @thing.define_singleton_method(m) { instance_variable_get(var_name) }
        @thing.instance_variable_get(var_name)
    end

    def respond_to?(m, include_private = false)
        @thing.respond_to?(m, include_private) || super
    end
end

class Can
    def initialize(thing)
        @thing = thing
    end

    def method_missing(m, *args, &block)
        var_name = "@#{m.to_s}_data"

        @thing.define_singleton_method(m) do |*args|
            val = instance_variable_get(var_name) || []

            val << instance_exec(*args, &block)
            instance_variable_set(var_name, val)
            val.last
        end

        unless args.empty?
            @thing.define_singleton_method(args.first) { instance_variable_get(var_name) }
        end
    end

    def respond_to?(m, include_private = false)
        @data.respond_to?(m, include_private) || super
    end
end

class Each
    def initialize(data)
        @data = data
    end

    def is_a?(klass)
        @data.is_a?(klass)
    end

    def each(*args, &block)
        @data.each { |thing| thing.instance_exec(*args, &block) }
        self
    end

    def method_missing(m, *args, &block)
        @data.send(m, *args, &block)
    end

    def respond_to?(method_name, include_private = false)
        @data.respond_to?(method_name, include_private) || super
    end
end

class Property
    def initialize(thing)
        @thing = thing
        @variable_name = nil
    end

    def method_missing(m, *args, &block)
        if @variable_name.nil?
            @variable_name = m
            return self
        end

        # we got a value
        @thing.tap do |t|
            t.define_singleton_method(@variable_name) { m.to_s }
        end
    end

    def respond_to?(m, include_private = false)
        @thing.respond_to?(m, include_private) || super
    end
end

class Thing
    attr_reader :name, :is_a, :is_not_a, :can

    def initialize(name)
        @name = name
        @is_a = IsA.new(self)
        @is_not_a = IsNotA.new(self)
        @can = Can.new(self)
      
        is_a.send(name)
    end

    def has(num)
        Has.new(self, num)
    end

    def being_the
        Property.new(self)
    end

    alias_method :having, :has
    alias_method :and_the, :being_the
    alias_method :is_the, :being_the
end

___________________________________________________
require 'active_support/core_ext/string'

class BoolMethodDefiner
  def initialize(thing, bool)
    @thing = thing
    @bool = bool
  end

  def method_missing(m)
    bool = @bool
    @thing.define_singleton_method("#{m}?") { bool }
  end
end

class PropertyDefiner
  def initialize(thing, prop = nil)
    @thing = thing
    @prop = prop
  end

  def method_missing(m, *args, &block)
    prop = @prop
    
    if prop
      @thing.define_singleton_method(prop) { m.to_s }

      return @thing
    end

    @prop = m
    self
  end
end

class MethodDefiner
  def initialize(thing)
    @thing = thing
  end

  def method_missing(m, *args, &block)
    past_tense = args.first
    if past_tense.nil?
      @thing.instance_eval { define_singleton_method(m, &block) }

      return
    end
    
    @thing.instance_eval do
      cache = []

      define_singleton_method(m) do |*args|
        (cache << result = instance_exec(args.first, &block)) && result
      end

      define_singleton_method(past_tense) { cache }
    end
  end
end

class SubThingGroup
  def initialize(thing, n)
    @thing = thing
    @n = n
  end
  
  def method_missing(m)
    n = @n
    
    sub_things = (1..n).map { Thing.new(m.to_s.singularize) }
    
    sub_things.instance_eval do
      def each(&block)
        (0..(self.size - 1)).each do |i|
          thing = self[i]
          thing.instance_eval(&block)
        end
      end
    end

    @thing.define_singleton_method(m) do
      return sub_things.first if n == 1
      
      sub_things
    end
    
    return sub_things.first if n == 1
    
    sub_things
  end  
end

class Thing
  attr_reader :name

  def initialize(name)
    @name = name

    define_singleton_method("#{@name}?") { true }
  end
  
  def is_a
    BoolMethodDefiner.new(self, true)
  end

  def is_not_a
    BoolMethodDefiner.new(self, false)
  end
  
  def has(n)
    SubThingGroup.new(self, n)
  end
  
  def having(n)
    SubThingGroup.new(self, n)
  end
  
  def is_the
    PropertyDefiner.new(self)
  end
  
  def being_the
    PropertyDefiner.new(self)
  end
  
  def and_the
    PropertyDefiner.new(self)
  end
  
  def can
    MethodDefiner.new(self)
  end
end

___________________________________________________
require 'active_support/core_ext/string'

class Caller
  def initialize(&block)
    @block = block
  end
  
  def method_missing(method, *args, &block)
    @block.(method, *args, &block)
  end  
end

def call_next(&block)
  Caller.new(&block)
end

class Array
  alias_method :old_each, :each
  
  def each(*args, &block)
    if block_given? && args.empty? && block.parameters.empty?
      self.old_each{|element| 
        if element.is_a?(Thing)
          element.instance_eval(&block)
        else
          block.()
        end  
      }
    else 
      old_each(*args, &block)
    end  
  end  
end  

class Thing
  attr_reader :name
  
  def initialize(name)
    @name = name
    @parts = {name+'?' => true}
  end
  
  def is_a
    call_next{|flag| @parts[flag.to_s+'?'] = true}
  end

  def is_not_a
    call_next{|flag| @parts[flag.to_s+'?'] = false}
  end
  
  def has(n)
    call_next{|part|
      if n == 1
        part_name = part.to_s
        @parts[part_name] = Thing.new(part_name) 
      else
        part_name = part.to_s.singularize
        part_key = part_name.pluralize
        @parts[part_key] = Array.new(n){Thing.new(part_name)} 
      end
    }
  end
  
  alias_method :having, :has
  
  def being_the
    call_next{|relation| call_next{|object| 
      @parts[relation.to_s] = object.to_s
      self #for chaining
    } }
  end
  
  alias_method :and_the, :being_the
  alias_method :is_the, :being_the
  
  def can
    call_next{|action, memo_name, &block|
      memo = []
      define_singleton_method(action){|*args|
        (memo << instance_exec(*args, &block)).last
      }
      define_singleton_method(memo_name){ memo } unless memo_name.nil?
    }
  end  
  
  def method_missing(method, *args)
    @parts[method.to_s]
  end  
end

___________________________________________________
require 'active_support/core_ext/string'

class Array
  alias_method :old_each, :each
  def each(*args, &b)
    if self[0].is_a?(Thing)
      0.upto(self.length-1) do |x|
        self[x].instance_eval(&b)
      end
    else
      send(:old_each, *args, &b)
    end
  end
end

class Thing
  attr_accessor :sente
  attr_accessor :name

  def initialize(val)
    self.name = val
  end

  def set_variable_and_method(meth, value)
    self.instance_variable_set("@#{meth}", value)
    self.define_singleton_method meth do
      self.instance_variable_get("@#{meth}")
    end
  end

  def method_missing(meth, *args, &block)
    if meth =~ /is_a|is_not_a|is_the|has|having|being_the|and_the|can/
      self.sente = meth.to_s + (args.empty? ? "" : "_#{args[0]}")
      return self
    end
    unless self.sente.nil?
      if self.sente =~ /can/
        unless args.empty?
          self.instance_variable_set("@#{args[0]}", [])
          self.define_singleton_method args[0].to_s do
            self.instance_variable_get("@#{args[0]}")
          end
        end
        self.define_singleton_method meth do |value|
          unless args.empty?
            self.instance_variable_get("@#{args[0]}").push(self.instance_exec(value, &block))
            self.instance_variable_get("@#{args[0]}")[-1]
          else
            self.instance_exec(value, &block)
          end
        end
        self.sente = nil
      elsif self.sente =~ /being_the$|and_the$/
        self.sente += "_#{meth}"
      elsif matched = self.sente.match(/being_the_(.*)|and_the_(.*)/)
        value = matched.captures[0] ? matched.captures[0] : matched.captures[1]
        # self.instance_variable_set("@#{value}", meth.to_s)
        # self.define_singleton_method "#{value}" do
        #   self.instance_variable_get("@#{value}")
        # end
        set_variable_and_method(value, meth.to_s)
        self.sente = nil
      elsif self.sente =~ /is_a|is_not_a/
        type = self.sente
        self.define_singleton_method "#{meth}?" do
          type.match(/is_a/) ? true : false
        end
        self.sente = nil
      elsif self.sente =~ /^is_the$/ and meth =~ /(\w+)_of$/
        self.sente += "_" + meth.to_s
      elsif matched = self.sente.match(/is_the_(\w+)/)
        self.define_singleton_method "#{matched.captures[0]}" do
          meth.to_s
        end
        self.sente = nil
      elsif matched = self.sente.match(/has_(.*)|having_(.*)/)
        times_value = matched.captures[0] ? matched.captures[0] : matched.captures[1]
        values = []
        times_value.to_i.times do
          values << Thing.new(meth.to_s.singularize)
        end
        if values.length <= 1
          values = values[0]
        end
        # self.instance_variable_set("@#{meth}", values)
        # self.define_singleton_method "#{meth}" do
        #   self.instance_variable_get("@#{meth}")
        # end
        set_variable_and_method(meth, values)
        self.sente = nil
        return values
      end
      return self
    end
    if (self.name + "?") =~ /#{meth}/
      return true
    end
    super
  end
end

___________________________________________________
require 'active_support/core_ext/string'

def build_thing(methods = {})
  result = Class.new(Thing)
  methods.each { |m, v| result.define_method(m) { v } }
  result
end

class MagicArray < Array
  def each(&block)
    super do |e|
      e.instance_exec(e, &block)
    end
  end
end

class Builder
  def initialize(thing, type, params = nil)
    @thing = thing
    @type = type
    @params = params
  end
  
  def method_missing(name, *args, &block)
    case @type
    when :is_a
      @thing.define_runtime_method("#{name}?") { true }
    when :is_not_a
      @thing.define_runtime_method("#{name}?") { false }
#      @thing.class.define_method("#{name}?") { false }
    when :has
      klass = build_thing({ "#{name[0...-1]}?" => true })
      result = klass.new(name.to_s)
      if @params == 1
        @thing.define_runtime_method("#{name}") { result }
        result

        # @thing.class.define_method("#{name}") { klass.new(name.to_s) }
      else
        result = MagicArray.new(@params) { klass.new(name[0...-1]) }
        @thing.define_runtime_method("#{name}") { result }
        result
        # @thing.class.define_method("#{name}") { result }
      end
    when :is_the
      Builder.new(@thing, name)
    when :can
      @thing.define_runtime_method(:speak) do |param|
        # block.call(param)
        @latest_spoken ||= []
        result = instance_exec(param, &block)
        @latest_spoken << result
        result
      end
      @thing.define_runtime_method(:spoke) do
        @latest_spoken
      end
    else
      @thing.define_runtime_method(@type) { name.to_s }
      @thing
    end
  end
end

class Thing
  attr_reader :name
  
  def initialize(name)
    @name = name
  end
  
  def is_a
    Builder.new(self, :is_a)
  end
  
  def is_not_a
    Builder.new(self, :is_not_a)
  end
  
  def has(number)
    Builder.new(self, :has, number)
  end

  def having(number)
    Builder.new(self, :has, number)
  end
  
  def is_the
    Builder.new(self, :is_the)
  end
  
  def being_the
    Builder.new(self, :is_the)
  end
  
  def and_the
    Builder.new(self, :is_the)
  end
  
  def can
    Builder.new(self, :can)
  end

  def define_runtime_method(name, &block)
    (class << self; self; end).class_eval do
      define_method name, &block
    end
  end

  #def can()
  #  Builder.new(self, :has, number)
  #end

  # TODO: make the magic happen
end
