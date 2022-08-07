5861487fdb20cff3ab000030


func getPairData(_ s: [Int]) -> [(Int,Int)?]{
    func getPairWithIndex(_ index: Int) -> Int?{
        var needPair: Int = 0
        for i in index..<s.count{
            let c = Array(s)[i]
            if c == 5{
                needPair += 1
            }
            if c == 6{
                if needPair > 0{
                    needPair -= 1
                }else{
                    return i
                }
            }
            continue
        }
        return nil
    }
    var pairs: [(Int,Int)?] = Array(repeating: nil, count: s.count)
    for i in 0..<s.count{
        let c = Array(s)[i]
        if c == 5{
            if let pair = getPairWithIndex(i + 1){
                pairs[i] = (i,pair)
                pairs[pair] = (i,pair)
                continue
            }
        }
    }
    return pairs
}

func boolfuck(_ code: String, _ input: String = "") -> String {
    let inputDatas = input.map({String($0).data(using: .isoLatin1) ?? Data(String($0).utf8)})
    let inputBits = inputDatas.map({$0.reduce("") { (acc, byte) -> String in
        let byteStr = String(byte,radix: 2)
        return acc + String((byteStr.count < 8 ? Array(repeating: "0", count: 8 - byteStr.count).joined() + byteStr : byteStr).reversed())
        }}).joined().compactMap({Int("\($0)")})
    var inputIndex: Int = 0
    
    var pointers: [Bool] = [false]
    var pointerIndex: Int = 0
    
    var result: String = ""
    var bitBox: [Int] = []
    var current: Bool{
        set{
            pointers[pointerIndex] = newValue
        }
        get{
            return pointers[pointerIndex]
        }
    }
    var readIndex: Int = 0
    let codeArray = code.compactMap({[";","+",",","<",">","[","]"].firstIndex(of: $0)})
    let pairData = getPairData(codeArray)
    
    while readIndex < codeArray.count {
        let c = codeArray[readIndex]
        switch c {
        case 0:
            bitBox.append(current ? 1 : 0)
            readIndex += 1
        case 1:
            current.toggle()
            readIndex += 1
        case 2:
            if inputIndex == inputBits.count{
                pointers[pointerIndex] = false
            }else{
                pointers[pointerIndex] = (inputBits[inputIndex]) == 1
                inputIndex += 1
            }
            readIndex += 1
        case 3:
            if pointerIndex == 0{
                pointers.insert(false, at: 0)
            }else{
                pointerIndex -= 1
            }
            readIndex += 1
        case 4:
            pointerIndex += 1
            if pointerIndex == pointers.count{
                pointers.append(false)
            }
            readIndex += 1
        case 5:
            if !current,let forwardIndex = pairData[readIndex]?.1{
                readIndex = forwardIndex + 1
            }else{
                readIndex += 1
            }
        case 6:
            if current,let backIndex = pairData[readIndex]?.0{
                readIndex = backIndex + 1
            }else{
                readIndex += 1
            }
        default:
            readIndex += 1
            break
        }
        if bitBox.count == 8{
            let byte = UInt8(bitBox.reversed().reduce(0, {$0 << 1 + $1}))
            let c = Character(Unicode.Scalar.init(byte))
            result.append(c)
            bitBox = []
        }
    }
    
    if bitBox.count > 0{
        bitBox += Array(repeating: 0, count: 8 - bitBox.count)
        let byte =  UInt8(bitBox.reversed().reduce(0, {$0 << 1 + $1}))
        let c = Character(Unicode.Scalar.init(byte))
        result.append(c)
    }
    return result
}
_____________________________
extension UInt8 {
  
  private static let offsets: [UInt8] = [1, 2, 4, 8, 16, 32, 64, 128]
  
  init<Bits>(fromBits bits: Bits) where Bits: Sequence, Bits.Iterator.Element == Bool { // to allow array slices
    self = 0
    for (offset, bit) in zip(UInt8.offsets, bits) {
      if bit {
        self += offset
      }
    }
  }
  
  var bits: [Bool] {
    return UInt8.offsets.map { offset in
      self & offset == offset
    }
  }
}

extension Array where Element == Bool {
  
  func bytes() -> [UInt8] {
    var bytes: [UInt8] = []
    for i in 0 ..< (count + 7) / 8 {
      let bits = self[8 * i ..< Swift.min(8 * i + 8, count)]
      bytes.append(UInt8(fromBits: bits))
    }
    return bytes
  }
}

extension String {
  
  func asciiBits() -> [Bool] {
    return (self.data(using: .isoLatin1) ?? Data()).flatMap {
      $0.bits
    }
  }
}

class Tape {
  
  var position = 0
  var min = 0
  var max = 0
  var positive: [Bool] = [false]
  var negative: [Bool] = []
  
  func moveRight() {
    position += 1
    if position >= positive.count {
      positive.append(false)
    }
    if position > max {
      max = position
      print("max:\t", max)
    }
  }
  
  func moveLeft() {
    position -= 1
    if -1 - position >= negative.count {
      negative.append(false)
    }
    if position < min {
      min = position
      print("min:\t", min)
    }
  }
  
  func flip() {
    self[position] = !self[position]
  }
  
  subscript(index: Int) -> Bool {
    get {
      return index >= 0 ? positive[index] : negative[-1 - position]
    }
    set {
      if index >= 0 {
        positive[index] = newValue
      } else {
        negative[-1 - index] = newValue
      }
    }
  }
  
  var current: Bool {
    get {
      return self[position]
    }
    set {
      self[position] = newValue
    }
  }
}

enum Instruction: Character {
  
  case flip = "+"
  case left = "<"
  case right = ">"
  case read = ","
  case write = ";"
  case enter = "["
  case exit = "]"
}

func boolfuck(code: String, input: String = "") -> String {
  let instructions = code.characters.flatMap { Instruction(rawValue: $0) }
  var inputProvider = input.asciiBits().makeIterator()
  
  let tape = Tape()
  var counter = 0
  var jumpbackPoints: [Int] = []
  var matchingBraces: [Int: Int] = [:]
  
  var output: [Bool] = []
  
  while counter < instructions.count {
    switch instructions[counter] {
    case .flip:
      tape.flip()
    case .read:
      tape.current = inputProvider.next() ?? false
    case .write:
      output.append(tape.current)
    case .left:
      tape.moveLeft()
    case .right:
      tape.moveRight()
    case .enter:
      if !tape.current {
        if let match = matchingBraces[counter] {
          counter = match
        } else {
          let start = counter
          var level = 0
          search: repeat {
            switch instructions[counter] {
            case .exit:
              if level == 1 {
                break search
              } else {
                level -= 1
              }
            case .enter:
              level += 1
            default:
              break
            }
            counter += 1
          } while counter < instructions.count
          matchingBraces[start] = counter
        }
      } else {
        jumpbackPoints.append(counter)
      }
    case .exit:
      matchingBraces[jumpbackPoints.last!] = counter
      counter = jumpbackPoints.popLast()! - 1 // cheeky - 1
    }
    counter += 1
  }
  //print(output)
  return String(bytes: output.bytes(), encoding: .isoLatin1)!
}

func boolfuck(_ code: String, _ input: String = "") -> String {
  return boolfuck(code: code, input: input)
}
_____________________________

func boolfuck(_ code: String, _ input: String = "") -> String {
  let fucker = BoolFucker(code: code, input: input)
  return String(data: Data(fucker.stream), encoding: .isoLatin1) ?? ""
}

class TapeNode {
  var bit: Bool
  var next: TapeNode?
  var prev: TapeNode?
  
  init(bit: Bool? = nil, next: TapeNode? = nil, prev: TapeNode? = nil) {
    self.bit = bit ?? false
    self.next = next
    self.prev = prev
  }
}

class Tape {
    var root: TapeNode?
  
    init() {
      //root = TapeNode(bit: false)  
    }
  
  func write(bit: Bool) {
    if nil == root {
      root = TapeNode()
    }
    
    root!.bit = bit
  }
  
  func toggle() {
    if nil == root {
      root = TapeNode(bit: false)
    }
    root!.bit.toggle()
  }
    
    func next() {
        if nil == root {
            root = TapeNode(bit: false)
            return
        }
      let c = root
        root = root?.next ?? TapeNode(bit: nil, prev: root)
      c?.next = root
    }
    
    func prev() {
        if nil == root {
            root = TapeNode(bit: false)
            return
        }
        let c = root
        root = root?.prev ?? TapeNode(bit: nil, next: root)
        c?.prev = root
    }
    
    func debug() {
        guard var start = root else { return }
        
        while nil != start.prev && nil != start.prev?.bit {
            start = start.prev!
        }
        var output = ""
        repeat {
          output += (start.bit ?? false) ? "1" : "0"
          if output.count > 0, output.count % 8 == 0 {
            output += " "
          }
            if let n = start.next {
              start = n              
            }
        } while nil != start.next && start.bit != nil
    }
}

class BoolFucker {
  // 00101010 = *
  var tape = Tape()
  
  var stream = [UInt8]()
  private var code: String
  private var input: Data
  private var pointer = 0
  private var streamPointer = 0
  private var current = false
  
  init(code: String, input: String) {
    self.code = code
    self.input = input.data(using: .isoLatin1) ?? Data()
    fuck()
  }
  
  private func fuck() {
    var codePointer = code.startIndex
    while codePointer < code.endIndex {
      let instruction = code[codePointer]
      switch instruction {
        case "+":
              tape.toggle()
              current = tape.root?.bit ?? false
        case ",":
              current = read()
          
              tape.write(bit: current)
        case ";":
              writeStream(bit: tape.root?.bit ?? false)
        case "<":
              tape.prev()
              current = tape.root?.bit ?? false
        case ">":
              tape.next()
              current = tape.root?.bit ?? false
        case "[":
          if !current {
            var needed = 1
            while needed != 0 {
              codePointer = code.index(after: codePointer)
              if code[codePointer] == "[" {
                needed += 1
              }
              if code[codePointer] == "]" {
                needed -= 1
              }
            }
          }
        case "]":
          if current {
            var needed = 1
            while needed != 0 {
              codePointer = code.index(before: codePointer)
              if code[codePointer] == "]" {
                needed += 1
              }
              if code[codePointer] == "[" {
                needed -= 1
              }
            }

          }
        default: break
      }
        codePointer = code.index(after: codePointer)        
    }
      tape.debug()
  }
  
  func writeStream(bit: Bool) {
    let bytePosition = streamPointer / 8
    if bytePosition >= stream.count {
      stream.append(0)
    }
    let bitPosition = streamPointer % 8
    let mask: UInt8 = (bit ? 1 : 0) << bitPosition
    let currentByte = stream[bytePosition]
    stream[bytePosition] = currentByte | mask
    
    streamPointer += 1
  }
  
  func read() -> Bool {
    guard pointer >= 0, pointer < input.count * 8 else {
      return false
    }
    
    let bytePosition = pointer / 8
    let bitPosition = pointer % 8
    let mask: UInt8 = 1 << UInt8(bitPosition)
    
    pointer += 1
    return (input[bytePosition] & mask) != 0
  }
}
