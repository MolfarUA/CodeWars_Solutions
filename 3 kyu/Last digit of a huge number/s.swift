func lastDigit<S>(_ numbers: S) -> Int where S: Sequence, S.Iterator.Element == Int {
	var iterator = numbers.makeIterator()
	let start = iterator.next()
	var zeroFixed = sequence(state: (iterator, start)) { (state: inout (iterator: S.Iterator, current: Int?)) -> Int? in
		guard let current = state.current else { return 1 }
		state.current = state.iterator.next()
		guard let next = state.current, next == 0 else { return current }
		var count = 1
		while state.iterator.next() == 0 {
			count += 1
		}
		state.current = nil
		if count % 2 == 0 {
			return current
		} else {
			return 1
		}
	}

	let first = zeroFixed.next()! % 10
	let second: Int

	switch zeroFixed.next()! % 4 {
	case 0: second = 4
	case 1: second = 1
	case 2: second = zeroFixed.next()! == 1 ? 2 : 4
	case 3: second = zeroFixed.next()! % 2 == 0 ? 1 : 3
	default: fatalError("Should be unreachable")
	}

	return Int(pow(Double(first), Double(second))) % 10
}
_____________________
func lastDigit<S>(_ numbers: S) -> Int where S: Sequence, S.Iterator.Element == Int {
    var iter = numbers.makeIterator()
    guard let first = iter.next() else{return 1}
    guard let second = iter.next() else{return first % 10}
    guard let fri1 = iter.next() else{if second != 0{return Int(pow(Double(first % 10), Double(second % 4 + 4))) % 10};return 1}
    
    var prosNumbers = [2,3,5,7,9,11,13,17,19,23]
    func prostN(_ a: Int) -> Array<Int>{
        if prosNumbers.last! < a{
            var z = prosNumbers.last!, c = prosNumbers.count
            repeat{
                z += 1
                var b: Bool = true
                for i in prosNumbers{if z % i != 0{b = false;break}}
                if b{prosNumbers.append(z);break}
            }while c == prosNumbers.count || a >= z
        }
        return prosNumbers
    }

    func elerF(_ m: Int) -> Int{
        if m == 1 || m == 2{return 1}
        var p: Array<Int> = Array(prostN(m))
        p = Array(p[...p.firstIndex(where: {return $0 >= m})!])
        if p.removeLast() == m{return m - 1}
        var k = 1
        for num in (2...(m - 1)){k += 1;for i in p[...(p.firstIndex(where: {z in return z > m}) ?? (p.count - 1))] {if m % i == 0 && num % i == 0{k -= 1;break}}}
        return k
    }
    
    func vzprost(_ a: Int, _ b: Int) -> Bool{
        let ma = max(a,b)
        let mi = min(a,b)
        if mi == 0 || mi == 2{return false}else if mi == 1{return true}
        for z in 2...Int(Double(sqrt(Double(mi)) + 1)){if ma % z == 0 && mi % z == 0{return false}}
        return true
    }
    
    func information(_ numberic: Int, _ maxST: Int, _ mod: Int) -> (Int, Array<Int>?){
        var array = [1], count = 0
        while maxST > count{
            let k = ( (array.last! * numberic) % mod)
            if let index = array.firstIndex(of: k){
                return (index, array)
            }
            count += 1;array.append(k)
        }
        return (array.last!, nil)
    }
    
    func rekursive(_ a: Int, _ mod: Int,_ next: Int,_ second1: Int) -> Int{
        let r = a % mod, next = next, second = second1, fri = iter.next() ?? 1
        var st: Int
        
        switch r{
            case 0: var k = 3; if next != 0{return 0}else if second != 0{return 1}else if fri != 0{return 0};while let ty = iter.next(), ty == 0{k += 1}; return k % 2
            case 1: return 1
            case let r where [5,6].contains(r): var k = 3; if next != 0{return r}else if second != 0{return 1}else if fri != 0{return r}; while let ty = iter.next(), ty == 0{k += 1}; return k % 2 == 0 ? r : 1
            default: break
        }
        
        if mod == Int.max{
            st = rekursive(next, mod, second, fri);return Int(pow(Double(r),Double(st)))
        }
        
        let info = information(r, Int.max, mod)
        
        if vzprost(r, mod){
            let y = elerF(mod)
            st = rekursive(next, y, second, fri) % y
            if st > info.0{return info.1![(st - info.0) % (info.1!.count - info.0) + info.0]}
            return info.1![st]
        }
        
        
        if (Double(second) * log2(Double(next)) > log2(Double(info.0)) && fri != 0 || next > info.0) && second != 0{
            let st1 = ( rekursive(next, info.1!.count - info.0, second, fri) - (info.0) % (info.1!.count - info.0) )
            if st1 > 0{st = st1 % (info.1!.count - info.0) + info.0}else{st = st1 + (info.1!.count - info.0) + info.0}
        }else{
            let st0 = rekursive(next, Int.max, second, fri)
            if st0 > info.0{
                let st1 = ( st0 - (info.0) % (info.1!.count - info.0) )
                if st1 > 0{st = st1 % (info.1!.count - info.0) + info.0}else{st = st1 + (info.1!.count - info.0) + info.0}
            }else{st = st0}
        }
        if st > info.0{return info.1![(st - info.0) % (info.1!.count - info.0) + info.0]}
        return info.1![st]
    }
    
    return rekursive(first, 10, second, fri1)
}
