515bb423de843ea99400000a


# TODO: complete this class

class PaginationHelper:

  # The constructor takes in an array of items and a integer indicating
  # how many items fit within a single page
  def __init__(self, collection, items_per_page):
    self.collection = collection
    self.items_per_page = items_per_page
      
  
  # returns the number of items within the entire collection
  def item_count(self):
    return len(self.collection)
  
  # returns the number of pages
  def page_count(self):
    if len(self.collection) % self.items_per_page == 0:
      return len(self.collection) / self.items_per_page
    else:
      return len(self.collection) / self.items_per_page + 1
    
      
	
  # returns the number of items on the current page. page_index is zero based
  # this method should return -1 for page_index values that are out of range
  def page_item_count(self,page_index):
    if page_index >= self.page_count():
      return -1
    elif page_index == self.page_count() - 1:
      return len(self.collection) % self.items_per_page or self.items_per_page
    else:
      return self.items_per_page
      	
      
  
  # determines what page an item is on. Zero based indexes.
  # this method should return -1 for item_index values that are out of range
  def page_index(self,item_index):
    if item_index >= len(self.collection) or item_index < 0:
      return -1
    else:
      return item_index / self.items_per_page
______________________________________
class PaginationHelper:

    def __init__(self, collection, items_per_page):
        """
        The constructor takes in an list of items and a integer indicating how many items fit within a single page
        """
        self._items_per_page = items_per_page
        self._pages = tuple(len(collection[i:i + items_per_page]) for i in range(0, len(collection), items_per_page))

    def item_count(self):
        """Returns the number of items within the entire collection"""
        return sum(self._pages)

    def page_count(self):
        """Returns the number of pages"""
        return len(self._pages)

    def page_item_count(self, page_index):
        """
        Returns the number of items on the current page. page_index is zero based
        This method should return -1 for page_index values that are out of range
        """
        try:
            return self._pages[page_index]
        except IndexError:
            return -1

    def page_index(self, item_index):
        """
        Determines what page an item is on. Zero based indexes.
        This method should return -1 for item_index values that are out of range
        """
        return item_index // self._items_per_page if 0 <= item_index < self.item_count() else -1
______________________________________
class PaginationHelper:

    # The constructor takes in an array of items and an integer indicating
    # how many items fit within a single page
    def __init__(self, collection: list, items_per_page: int):
        self.collection = collection
        self.items_per_page = items_per_page

    # returns the number of items within the entire collection
    def item_count(self):
        return len(self.collection)

    # returns the number of pages
    def page_count(self):
        return __import__('math').ceil(self.item_count() / self.items_per_page)

    # returns the number of items on the current page. page_index is zero based
    # this method should return -1 for page_index values that are out of range
    def page_item_count(self, page_index):
        if page_index * self.items_per_page > self.item_count():
            return -1
        else:
            page_start = self.items_per_page * page_index
            page_end = self.items_per_page * (page_index + 1)
            return len(self.collection[page_start:page_end])

    # determines what page an item is on. Zero based indexes.
    # this method should return -1 for item_index values that are out of range
    def page_index(self, item_index):
        if item_index < 0 or item_index >= self.item_count():
            return -1
        return item_index // self.items_per_page
______________________________________
class PaginationHelper:

    def __init__(self, collection, items_per_page):
        self.collection = collection
        self.items_per_page = items_per_page

    def item_count(self):
        c = 0
        for i in self.collection:
            c += 1
        return c

    def page_count(self):
        pages = 0
        items = self.item_count()
        while True:
            if items > self.items_per_page:
                pages += 1
                items = items - self.items_per_page
            else:
                pages += 1
                break
        return pages

    def page_item_count(self, page_index):
        items = self.item_count()
        on_page = 0

        if page_index >= self.page_count():
            return -1
        for i in range(page_index + 1):
            if items > self.items_per_page:
                on_page = self.items_per_page
                items -= self.items_per_page
            else:
                on_page = items
        return on_page

    def page_index(self, item_index):
        on_page = 0
        if item_index >= self.item_count() or item_index < 0:
            return -1

        for i in range(item_index + 1):
            if i % self.items_per_page == 0 and i != 0:
                on_page += 1
        return on_page
______________________________________
# TODO: complete this class

class PaginationHelper:

    # The constructor takes in an array of items and a integer indicating
    # how many items fit within a single page
    def __init__(self, collection, items_per_page):
        
        self.collection = collection
        self.items_per_page = items_per_page

    # returns the number of items within the entire collection
    def item_count(self):
        
        return len(self.collection)

    # returns the number of pages
    def page_count(self):
        
        return round((len(self.collection) / self.items_per_page) + .5)

    # returns the number of items on the current page. page_index is zero based
    # this method should return -1 for page_index values that are out of range
    def page_item_count(self, page_index):
        
        if page_index < 0 or page_index + 1 > self.page_count():
            return -1
        
        index_min = page_index * self.items_per_page
        index_max = (page_index + 1) * self.items_per_page
        
        return len(self.collection[index_min:index_max])
        
    # determines what page an item is on. Zero based indexes.
    # this method should return -1 for item_index values that are out of range
    def page_index(self, item_index):
        
        if item_index < 0 or item_index + 1 > self.item_count():
            return -1
        
        return round((item_index / self.items_per_page) - .5)
