55466989aeecab5aac00003e


export class G964 {
    public static sqInRect(l: number, w: number): number[] {
        if(l == w) return null;
        var sqs = [], tmp;
        while(l) {
            tmp = Math.min(w, l);
            l = Math.max(w, l); 
            w = tmp;
            sqs.push(w);
            l -= w
        }
        return sqs;
    }
}
______________________________
export class G964 {
    static sqInRect(l: number, w: number): number[] | null {
        if (l === w) return null;
        if (w > l) [l, w] = [w, l];
        return [w].concat(G964.sqInRect(l - w, w) || w)
    }
}
______________________________
export class G964 {
    public static sqInRect(l: number, w: number): number[] {
        let remainingSize: number = l * w;
        let shorterSide: number;        
        const insideSqSides: Array<number> = [];
        
        if (l == w) {
          return null;
        }
              
        while (remainingSize > 0) {        
          shorterSide = Math.min(l, w);
          remainingSize -= Math.pow(shorterSide, 2);
          
          l = shorterSide;
          w = remainingSize / l;          
          
          insideSqSides.push(shorterSide);
        }
        
        return insideSqSides;
    }
}
