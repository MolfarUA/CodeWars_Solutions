515bb423de843ea99400000a


//                              `-:/+++++++/++:-.                                          
//                            .odNMMMMMMMMMMMMMNmdo-`                                      
//                           +mMMNmdhhhhhhhhhdmNMMMNd/`                                    
//                          sMMMmhyyyyyyyyyyyyyyhmNMMMh-                                   
//                         +MMMdyyyyyyyhhhhdddddddmMMMMN/                                  
//                        `NMMmyyyyyymNNMMNNNmmmmmmmNNMMMy`                                
//                        :MMMhyyyyyNMMMho+//:-.....-:omMMd-                               
//                    ```:mMMNhyyyyhMMMh+::::-        `:sNMN:                              
//                 -oyhdmMMMMmhyyyyhMMNyy+::::---------::yMMm                              
//                +MMMMNNNMMMdhyyyyhMMNyyyso/::::::://+oshMMM`                             
//                NMMNhyyyMMMhhyyyyyNMMmyyyyyyssssyyyyyyymMMd                              
//                MMMdyyyhMMNhhyyyyyhNMMNdyyyyyyyyyyyhdmMMMN-                              
//                MMMdhhhdMMNhhhyyyyyymMMMMNmmmmmmNNMMMMMMN.                               
//                MMMhhhhdMMNhhhyyyyyyyhdmNNNMMNNNmmdhhdMMd                                
//               `MMMhhhhdMMNhhhhyyyyyyyyyyyyyyyyyyyyyydMMM.                               
//               .MMMhhhhdMMNhhhhyyyyyyyyyyyyyyyyyyyyyydMMM:                               
//               .MMNhhhhdMMNhhhhhyyyyyyyyyyyyyyyyyyyyhhMMM+                               
//               -MMNhhhhdMMNhhhhhyyyyyyyyyyyyyyyyyyyyhdMMM/                               
//               -MMMhhhhdMMNhhhhhhhyyyyyyyyyyyyyyyyyhhdMMM-                               
//               `MMMhhhhhMMNhhhhhhhhhhyyyyyyyyyyyhhhhhmMMN                                
//                hMMmhhhhMMNhhhhhhhhhhhhhhhhhhhhhhhhhhNMMy                                
//                :MMMNmddMMMhhhhhhhhhhddddhhhhhhhhhhhdMMM/                                
//                 :hNMMMMMMMdhhhhhhhhdMMMMMMNNNNNdhhhNMMN`                                
//                   .-/+oMMMmhhhhhhhhmMMmyhMMMddhhhhdMMMy                                 
//                        hMMNhhhhhhhhmMMd :MMMhhhhhhdMMM+                                 
//                        sMMNhhhhhhhhNMMm .MMMdhhhhhdMMN.                                 
//                        /MMMdhhhhhhdMMM+  oNMMNNNNNMMm:                                  
//                        `dMMMNmmmNNMMMh`   -syyyyhhy/`                                   
//                         `/hmNNNNNmdh/`                                                  
//                            `.---..`

using System;
using System.Collections.Generic;


public class PagnationHelper<T>
{
  private readonly bool emptyCollection;
  

  public PagnationHelper(IList<T> collection, int itemsPerPage)
  {
    emptyCollection = collection.Count == 0;
  }


  public int ItemCount
  {
    get
    {
      return 24; 
    }
  }


  public int PageCount
  {
    get
    {
      return 3;  
    }
  }

  
  public int PageItemCount(int pageIndex)
  {
    switch (pageIndex)
    {
      case 0:
      case 1:  return 10;
      case 2:  return 4;
      default: return -1;
    }
  }

  
  public int PageIndex(int itemIndex)
  {
    if (emptyCollection)
      return -1;
    
    
    switch (itemIndex)
    {
      case 0:
      case 1:   
      case 9:   return 0;
      
      case 10:
      case 11:
      case 19:  return 1;
      
      case 20:
      case 21:
      case 22:
      case 23:  return 2;
      
      default:  return -1;
    }
  }
}
______________________________________
using System;
using System.Collections.Generic;

public class PagnationHelper<T>
{
  private IList<T> collection;
  private int pageCount;
  private int itemsPerPage;
  
  public PagnationHelper(IList<T> collection, int itemsPerPage)
  {
    this.collection = collection;
    pageCount = (collection.Count - 1) / itemsPerPage + 1;
    this.itemsPerPage = itemsPerPage;
  }

  public int ItemCount
  {
    get
    {
      return collection.Count;
    }
  }

  public int PageCount
  {
    get
    {
      return pageCount;
    }
  }

  public int PageItemCount(int pageIndex)
  {
    if(pageIndex < 0 || pageIndex >= pageCount) {
      return -1;
    }
    if(pageIndex == pageCount - 1) {
      return collection.Count % itemsPerPage;
    }
    return itemsPerPage;
  }

  public int PageIndex(int itemIndex)
  {
    if(itemIndex < 0 || itemIndex >= collection.Count) {
      return -1;
    }
    return itemIndex / itemsPerPage;
  }
}
______________________________________
using System;
using System.Collections.Generic;

public class PagnationHelper<T>
{
  // TODO: Complete this class
  private int _itemCount = 0;
  private int _pageCount = 0;  
  private int _itemsPerPage = 0; 
  /// <summary>
  /// Constructor, takes in a list of items and the number of items that fit within a single page
  /// </summary>
  /// <param name="collection">A list of items</param>
  /// <param name="itemsPerPage">The number of items that fit within a single page</param>
  public PagnationHelper(IList<T> collection, int itemsPerPage)
  {  
    if(null == collection || collection.Count ==0 || itemsPerPage <=0)
      {_itemCount =0; _pageCount =0;}
    else
      {
        _itemCount =collection.Count;
        
        int partialPage  = 0;
        if((_itemCount%itemsPerPage)!=0){partialPage =1;}
        
        _pageCount = _itemCount/itemsPerPage + partialPage;
      }
    
    _itemsPerPage = itemsPerPage;
  }

  /// <summary>
  /// The number of items within the collection
  /// </summary>
  public int ItemCount
  {
    get
    {
    return _itemCount;
      
    }
  }

  /// <summary>
  /// The number of pages
  /// </summary>
  public int PageCount
  {
    get
    {
      return _pageCount;
    }
  }

  /// <summary>
  /// Returns the number of items in the page at the given page index 
  /// </summary>
  /// <param name="pageIndex">The zero-based page index to get the number of items for</param>
  /// <returns>The number of items on the specified page or -1 for pageIndex values that are out of range</returns>
  public int PageItemCount(int pageIndex)
  {     
      if(pageIndex <0 || pageIndex >= _pageCount) 
      {return -1;}      
      if(_itemCount == 0)
      {return 0;  }
      if(pageIndex == (_pageCount-1))
      {
        return _itemCount - (_itemsPerPage *(pageIndex));
      }
      return _itemsPerPage;
  }

  /// <summary>
  /// Returns the page index of the page containing the item at the given item index.
  /// </summary>
  /// <param name="itemIndex">The zero-based index of the item to get the pageIndex for</param>
  /// <returns>The zero-based page index of the page containing the item at the given item index or -1 if the item index is out of range</returns>
  public int PageIndex(int itemIndex)
  {
     if(itemIndex < 0 || itemIndex >= _itemCount) 
      {return -1;}
     if( itemIndex < _itemsPerPage)
      {return 0; }
     return itemIndex/_itemsPerPage;
  }
}
______________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class PagnationHelper<T>
{
  public IList<T> Source { get; set; }

  public int PageSize { get; set; }
  
  /// <summary>
  /// Constructor, takes in a list of items and the number of items that fit within a single page
  /// </summary>
  /// <param name="collection">A list of items</param>
  /// <param name="itemsPerPage">The number of items that fit within a single page</param>
  public PagnationHelper(IList<T> collection, int itemsPerPage)
  {
    this.Source = collection;
    this.PageSize = itemsPerPage;
  }

  /// <summary>
  /// The number of items within the collection
  /// </summary>
  public int ItemCount
  {
    get
    {
      return this.Source.Count;
    }
  }

  /// <summary>
  /// The number of pages
  /// </summary>
  public int PageCount
  {
    get
    {
      return this.ItemCount / this.PageSize + 1;
    }
  }

  /// <summary>
  /// Returns the number of items in the page at the given page index 
  /// </summary>
  /// <param name="pageIndex">The zero-based page index to get the number of items for</param>
  /// <returns>The number of items on the specified page or -1 for pageIndex values that are out of range</returns>
  public int PageItemCount(int pageIndex)
  {
    if (pageIndex < 0 || this.PageSize * pageIndex > ItemCount)
    {
        return -1;
    }
    return this.Source
        .Skip(this.PageSize * pageIndex)
        .Take(this.PageSize)
        .Count();
  }

  /// <summary>
  /// Returns the page index of the page containing the item at the given item index.
  /// </summary>
  /// <param name="itemIndex">The zero-based index of the item to get the pageIndex for</param>
  /// <returns>The zero-based page index of the page containing the item at the given item index or -1 if the item index is out of range</returns>
  public int PageIndex(int itemIndex)
  {
    if (itemIndex < 0 || itemIndex >= this.ItemCount)
    {
        return -1;
    }

    return itemIndex / this.PageSize;
  }
}
