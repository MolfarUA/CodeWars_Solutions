package bouncing

fun bouncingBall(h:Double, bounce:Double, window:Double):Int {
    // Check for invalid inputs
    if (h <= 0 || bounce <= 0 || bounce >= 1 || window >= h) {
        return -1
    }

    // The ball will always pass the window once. Record that sighting, then update its height
    var timesSeen = 1
    var height = h * bounce

    // If the height is still above the window, increase the view count by two (once for it
    // going up and once for it going back down), then update its height again and repeat
    while (height > window) {
        timesSeen += 2
        height *= bounce
    }

    // If the ball is no longer above the window, we won't see it again, so we can stop
    return timesSeen
}
_______________________________________________
package bouncing

fun bouncingBall(h:Double, bounce:Double, window:Double):Int {
    if(h < 1) return -1
    if(bounce <= 0 || bounce >= 1) return -1
    if(h <= window) return -1
    
    var count = 1;
    
    var lastHeight = h
    // check if lastHeight * bounce is higher than window
    // if true, add 2.
    while(true){
        lastHeight = lastHeight * bounce
        if(lastHeight <= window) break
        count += 2
    }
    return count
}
_______________________________________________
package bouncing

fun bouncingBall(h:Double, bounce:Double, window:Double):Int {
    if (!(h>0.0 && (bounce>0 && bounce<1) && h>window)) return -1
    var ret = 0
    var newH = h
    do{
        ret++
        newH = newH*bounce
        if (newH>window) ret++
    }while(newH>window)
    return ret
}
_______________________________________________
package bouncing

fun bouncingBall(h:Double, bounce:Double, window:Double):Int {
    
    var nBounces = -1
    var bounceHeight = h*bounce
    
    if(h > 0 && bounce > 0 && bounce < 1 && window < h) {
        
        nBounces = 1
        while (bounceHeight > window) {

            bounceHeight = bounceHeight * bounce
            println(bounceHeight)
            nBounces += 2
        }
    }
    
    return nBounces
}
_______________________________________________
package bouncing

fun bouncingBall(h:Double, bounce:Double, window:Double):Int {
    if(h<0.0||bounce<0.0||bounce>=1|| window >= h) return -1
    var cnt = 1 
    var height = h*bounce
    while(window<height){
        cnt+=2
        height*=bounce
    }
    return cnt
}
