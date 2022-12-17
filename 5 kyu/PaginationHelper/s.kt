515bb423de843ea99400000a


class PaginationHelper<T>(val collection: List<T>, val itemsPerPage: Int) {
    val itemCount = collection.count()
    val pageCount = (itemCount / itemsPerPage).inc()
    fun pageItemCount(index: Int) = collection.chunked(itemsPerPage).getOrNull(index)?.count() ?: -1
    fun pageIndex(index: Int) = if (itemCount == 0) -1 else (index / itemsPerPage).takeIf { index in 0..itemCount && it in 0..pageCount } ?: -1
}
______________________________________
class PaginationHelper<T>(private val collection: List<T>, private val itemsPerPage: Int) {

    private val pages = collection.chunked(itemsPerPage)

    /** Returns the number of items within the entire collection. */
    val itemCount get() = collection.size

    /** Returns the number of pages. */
    val pageCount get() = pages.size

    /**
     * Returns the number of items on the page with index [pageIndex] (zero based).
     * Returns -1 if the provided page index is out of range.
     */
    fun pageItemCount(pageIndex: Int) = if (pageIndex in pages.indices) pages[pageIndex].size else -1

    /**
     * Returns the number of the page the item with index [itemIndex] is on (zero based).
     * Returns -1 if the provided item index is out of range.
     */
    fun pageIndex(itemIndex: Int) = if (itemIndex in collection.indices) itemIndex / itemsPerPage else -1
}
______________________________________
class PaginationHelper<T>(val collection: List<T>, val itemsPerPage: Int) {
    
    val itemCount: Int
    get() = collection.size

    val pageCount: Int
    get() = Math.ceil(itemCount.toDouble()/itemsPerPage).toInt()

    fun pageItemCount(pageIndex: Int): Int {
        if(pageIndex !in (0..pageCount-1)) return -1
        val diff = Math.abs(itemCount - pageIndex * itemsPerPage)
        return if(diff>itemsPerPage) itemsPerPage else diff
    }

    fun pageIndex(itemIndex: Int): Int {
        if(itemIndex !in (0..itemCount-1)) return -1
        return (itemIndex+1)/itemsPerPage 
    }
}
