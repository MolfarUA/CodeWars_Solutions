515bb423de843ea99400000a


class PaginationHelper(T)
  def initialize(@collection : Array(T), @items_per_page : Int32)
    
  end
  
  def collection
    
  end
  
  def items_per_page
    # TODO: Your implementation here !
  end
  
  def item_count
    @collection.size
  end
  
  def page_count
    (self.item_count / @items_per_page).ceil
  end
  
  def page_item_count(item_index : Int32)
    if item_index < 0
      -1
    elsif item_index >= self.page_count
      -1
    elsif (item_index + 1) * @items_per_page >= self.item_count
      self.item_count % @items_per_page
    else 
      @items_per_page
    end
  end
  
  def page_index(item_index : Int32)
    if item_index < 0
      -1
    elsif item_index >= self.item_count
      -1
    else
     (item_index / @items_per_page).floor
    end
  end
end
______________________________________
class PaginationHelper(T)
  def initialize(@collection : Array(T), @items_per_page : Int32)
  end
  
  def collection
    @collection
  end
  
  def items_per_page
    @items_per_page
  end
  
  def item_count
    @collection.size
  end
  
  def page_count
    (item_count / items_per_page).ceil
  end
  
  def page_item_count(item_index : Int32)
    return -1 if item_index < 0
    items_left = item_count - item_index * items_per_page
    return items_per_page if items_left > items_per_page
    return -1 if items_left <= 0
    items_left
  end
  
  def page_index(item_index : Int32)
    return -1 if item_index < 0
    items_left = item_count - item_index
    return -1 if items_left <= 0
    (item_index / items_per_page).floor
  end
end
______________________________________
class PaginationHelper(T)
  def initialize(@collection : Array(T), @items_per_page : Int32)
  end
  
  def collection
    @collection
  end
  
  def items_per_page
    @items_per_page
  end
  
  def item_count
    @collection.size
  end
  
  def page_count
    return 0 if item_count() == 0
    item_count() // @items_per_page + 1
  end
  
  def page_item_count(item_index : Int32)
    if item_index >= page_count || item_index < 0
      return -1
    elsif item_index == page_count - 1
      return item_count() - (page_count()-1) * @items_per_page
    else
      return @items_per_page
    end
  end
  
  def page_index(item_index : Int32)
    return -1 if item_index < 0 || item_index >= item_count
    item_index // @items_per_page
  end
end
______________________________________
class PaginationHelper(T)
  def initialize(@collection : Array(T), @items_per_page : Int32)
    
  end
  
  def collection
    @collection
  end
  
  def items_per_page
    @items_per_page
  end
  
  def item_count
    collection.size
  end
  
  def page_count
    (item_count / items_per_page).ceil
  end
  
  def page_item_count(item_index : Int32)
    (item_index < page_count) && (item_index >= 0) ? Math.min(items_per_page, item_count - item_index * items_per_page) : -1
  end
  
  def page_index(page_index : Int32)
    (page_index < item_count) && (page_index >= 0) ? (page_index / items_per_page).floor.to_i : -1
  end
end
