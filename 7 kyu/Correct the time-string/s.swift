57873ab5e55533a2890000c7


func correct(_ timeString: String?) -> String? {
    guard let time = timeString, time.isEmpty == false
        else { return timeString }
    
    let numbers = time.components(separatedBy: ":").flatMap({Int($0)})
    guard numbers.count == 3
        else { return nil }
    
    let timestamp = numbers[2] + numbers[1]*60 + numbers[0]*3600
    let hours = (timestamp/3600)%24
    let minutes = (timestamp/60)%60
    let seconds = timestamp % 60
    return "\(String(format: "%02d", hours)):\(String(format: "%02d",minutes)):\(String(format: "%02d",seconds))"
}
_________________________________
func correct(_ timeString: String?) -> String? {
     if timeString != nil { print(timeString!) }
    //check for nil test case 1
    if timeString == nil { return nil }
    if timeString!.isEmpty { return "" }
    //lenght test case 2
    if timeString!.count != 8 && timeString!.count != 9 { return nil }
    if timeString!.contains(" ") { return nil }
    var timeArray = timeString?.split(separator: ":")
    //test case 3 check for numbers
    var a : [Character] = ["0","1","2","3","4","5","6","7","8","9"]
    for test in timeArray! {
        for f in test {
            if f != a[0] && f != a[1] && f != a[2] && f != a[3] && f != a[4] && f != a[5] && f != a[6] && f != a[7] && f != a[8] && f != a[9] { return nil } } }
    var hour = Int(timeArray![0])
    var minute = Int(timeArray![1])
    var second = Int(timeArray![2])
    var answer = ""
    var totalSeconds = hour!*3600 + minute!*60 + second!
    if totalSeconds == 86400 || totalSeconds == 172800 {
        answer = "00:00:00" }
    func secondsConverter (_ seconds: Int) -> String {
        var stringHour = ""
        var stringMinute = ""
        var stringSecond = ""
        let newHour = seconds / 3600
        let hourRemain = seconds % 3600
        let newMinute = hourRemain / 60
        let minuteRemain = hourRemain % 60
        let newSecond = minuteRemain % 60
        print(newHour, newMinute, newSecond)
        if String(newHour).count == 1 {
            stringHour = "0" + "\(newHour)"
        } else {
            stringHour = String(newHour)
        }
        if String(newMinute).count == 1 {
            stringMinute = "0" + "\(newMinute)"
        } else {
            stringMinute = String(newMinute)
        }
        if String(newSecond).count == 1 {
            stringSecond = "0" + "\(newSecond)"

        } else {
            stringSecond = String(newSecond)
        }
        let finalTime = stringHour + ":" + stringMinute + ":" + stringSecond
        return finalTime
    }
    if totalSeconds > 172800 {
        let differenceOver24Hours = totalSeconds - 172800
        print(differenceOver24Hours)
        answer = secondsConverter(differenceOver24Hours)
    }
    if totalSeconds > 86400 && totalSeconds < 172799 {
        let differenceOver24Hours = totalSeconds - 86400
        answer = secondsConverter(differenceOver24Hours)
    }
    if totalSeconds < 86400 {
        let differenceUnder24Hours = totalSeconds
        answer = secondsConverter(differenceUnder24Hours)
    }
    return answer
}
_________________________________
import Foundation

func correct(_ timeString: String?) -> String? {
    if (timeString == "") {return ""}
    guard let split = timeString?.components(separatedBy: ":") else { return nil }
    if split.count != 3 { return nil }
    
    guard var hours = Int(split[0]), var mins = Int(split[1]), var secs = Int(split[2]) else { return nil }

    mins += Int(secs/60)
    hours += Int(mins/60)

    hours = hours%24
    mins = mins%60
    secs = secs%60

    return "\(makeTwoDigitString(from: hours)):\(makeTwoDigitString(from: mins)):\(makeTwoDigitString(from: secs))"
}

func makeTwoDigitString(from num: Int) -> String {
    return num >= 10 ? "\(num)" : "0\(num)"
}
