func formatDuration(_ seconds: Int) -> String {
    guard seconds > 0 else { return "now" }
    
    var unit = ["year", "day", "hour", "minute", "second"],
        unitDuration = [Int.max, 365, 24, 60, 60],
        duration = seconds,
        result = [String](),
        divisor: Int

    while duration > 0 {
        divisor = unitDuration.removeLast()
        
        let r = duration % divisor,
            suffix = r > 1 ? "s" : "",
            str = "\(r) \(unit.removeLast())\(suffix)"
        if r > 0 { result.insert(str, at: 0) }

        duration /= divisor
    }

    return result.count > 1 ?
        result.dropLast().joined(separator: ", ") + " and " + result.last! :
        result.last!
}

__________________________________________________
func formatDuration(_ seconds: Int) -> String {
    guard seconds > 0 else { return "now" }
    
    let result = [
        (seconds / 31536000, "year"),
        ((seconds % 31536000)/86400, "day"),
        (((seconds % 31536000) % 86400)/3600, "hour"),
        ((seconds % 3600) / 60, "minute"),
        ((seconds % 3600) % 60, "second")
        ]
        .filter({$0.0 > 0})
        .map({$0.0 > 1 ? "\($0.0) \($0.1)s" : "\($0.0) \($0.1)"})
        .joined(separator: ", ")
    
    if let range = result.range(of: ", ", options: String.CompareOptions.backwards) {
        return result.replacingCharacters(in: range, with: " and ")
    } else {
        return result
    }
    
}

__________________________________________________
func formatDuration(_ seconds: Int) -> String {
    guard seconds > 0 else { return "now" }
    let durations = [ "\(seconds/(60*60*24*365)) year\(seconds/(60*60*24*365) > 1 ? "s" : "")",
                      "\(seconds/(60*60*24) % 365) day\(seconds/(60*60*24) % 365 > 1 ? "s" : "")",
                      "\(seconds/(60*60) % 24) hour\(seconds/(60*60) % 24 > 1 ? "s" : "")",
                      "\(seconds/60 % 60) minute\(seconds/60 % 60 > 1 ? "s" : "")",
                      "\(seconds % 60) second\(seconds % 60 > 1 ? "s" : "")"].filter({$0.first != "0"})
    return durations.dropLast().joined(separator: ", ") + (durations.count > 1 ? " and " : "") + durations.last!
}


__________________________________________________
func formatDuration(_ seconds: Int) -> String {
    if seconds > 0 {
        let y = ((seconds / 3600) / 24) / 365
        let d = ((seconds / 3600) / 24) % 365
        let h = ((seconds / 3600) % 24) % 60
        let m = (seconds % 3600) / 60
        let s = (seconds % 3600) % 60
        
        let array = [("year", y), ("day", d), ("hour", h), ("minute", m), ("second", s)]
        let filtered = array.filter { $0.1 != 0 }.map { String($0.1) + " \($0.0)" + ($0.1 > 1 ? "s" : "") }
        let result = filtered.enumerated().filter { $0.offset != (filtered.count - 1)}.map { $0.element}.joined(separator: ", ") + ((filtered.count == 1) ? "\(filtered.last!)" : " and \(filtered.last!)")
        return result
    } else {
        return "now"
    }
}
