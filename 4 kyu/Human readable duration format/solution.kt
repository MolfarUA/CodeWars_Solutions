52742f58faf5485cae000b9a


object TimeFormatter {
    fun formatDuration(sec: Int): String {
        if (sec == 0) return "now"
        val seconds = sec % 60
        val minutes = sec % 3600 / 60
        val hours = sec % 86400 / 3600
        val days = sec % 31536000 / 86400
        val years = sec / 31536000
    
        val list = listOf(years, days, hours, minutes, seconds)
            .zip(listOf("years", "days", "hours", "minutes", "seconds"))
            .filter { it.first > 0 }
            .map { "${it.first} ${if (it.first == 1) it.second.dropLast(1) else it.second}" }
    
        return list
            .chunked(if (list.size == 1) list.size else list.lastIndex)
            .joinToString(" and ") { it.joinToString() }
    }
}

__________________________________________________
object TimeFormatter {
    fun f(s: String, time: Int) = if(time==0) "" else time.toString()+" "+s+(if(time==1)"" else "s")
    fun formatDuration(s:Int)=if(s==0) "now" else listOf(
        f("year",s/31536000),
        f("day", (s/86400)%365),
        f("hour",(s/3600)%24),
        f("minute", (s/60)%60),
        f("second", (s%3600)%60)).filter { e-> e.isNotBlank() }.joinToString(", ").replace(Regex(", (?!.+,)"), " and ")
}

__________________________________________________
object TimeFormatter {
    fun formatDuration(seconds: Int): String {
        val second = seconds % 60
        var minute = seconds / 60
        var hour = minute / 60
        minute %= 60
        var day = hour / 24
        hour %= 24
        val year = day / 365
        day %= 365
        val timeText = arrayOf(year to "year", day to "day", hour to "hour",
            minute to "minute", second to "second"
        )
        val result = arrayListOf<String>()

        timeText.forEach { (time, text) ->
            if (time != 0) result.add("$time $text${if (time > 1) "s" else ""}") }
        if (result.size > 1){
            result[result.size - 2] += " and ${result[result.size - 1]}"
            result.remove(result[result.size - 1])
        }

        return if (result.isNotEmpty()) result.joinToString(separator = ", ") else "now"
    }
}

__________________________________________________
object TimeFormatter {

    private const val secondsInYear = 365 * 24 * 60 * 60
    private const val secondsInDay = 24 * 60 * 60
    private const val secondsInHour = 60 * 60
    private const val secondsInMinute = 60

    fun formatDuration(seconds: Int): String {
        var durationRepresentation = ""

        if (seconds > 0) {
            val stringBuilder = StringBuilder()
            var tempSeconds = seconds

            while (tempSeconds > 0) {
                when {
                    tempSeconds >= secondsInYear -> {
                        val yearCount = tempSeconds / secondsInYear
                        stringBuilder.append(yearCount)
                        stringBuilder.append(if (yearCount > 1) " years, " else " year, ")

                        tempSeconds %= (yearCount * secondsInYear)
                    }

                    tempSeconds >= secondsInDay -> {
                        val daysCount = tempSeconds / secondsInDay
                        stringBuilder.append(daysCount)
                        stringBuilder.append(if (daysCount > 1) " days, " else " day, ")

                        tempSeconds %= (daysCount * secondsInDay)
                    }

                    tempSeconds >= secondsInHour -> {
                        val hoursCount = tempSeconds / secondsInHour
                        stringBuilder.append(hoursCount)
                        stringBuilder.append(if (hoursCount > 1) " hours, " else " hour, ")

                        tempSeconds %= (hoursCount * secondsInHour)
                    }

                    tempSeconds >= secondsInMinute -> {
                        val minutesCount = tempSeconds / secondsInMinute
                        stringBuilder.append(minutesCount)
                        stringBuilder.append(if (minutesCount > 1) " minutes, " else " minute, ")

                        tempSeconds %= (minutesCount * secondsInMinute)
                    }

                    else -> {
                        stringBuilder.append(tempSeconds)
                        stringBuilder.append(if (tempSeconds > 1) " seconds, " else " second, ")

                        tempSeconds = 0
                    }
                }
            }

            // remove the last 2 characters from the string
            durationRepresentation = stringBuilder.removeSuffix(", ").toString().trim()

            // let's replace the last ", " to " and "
            val lastCommaIndex = durationRepresentation.lastIndexOf(", ")

            if (lastCommaIndex != -1) {
                val tempDurationRepresentation = durationRepresentation

                durationRepresentation = tempDurationRepresentation.substring(0, lastCommaIndex)
                durationRepresentation += " and "
                durationRepresentation += tempDurationRepresentation.substring(lastCommaIndex + 2)
            }
        } else {
            durationRepresentation = "now"
        }

        return durationRepresentation
    }

}

__________________________________________________
object TimeFormatter {

    private val units = listOf(
        60 * 60 * 24 * 365 to "year",
        60 * 60 * 24 to "day",
        60 * 60 to "hour",
        60 to "minute",
        1 to "second"            
    )

    fun formatDuration(seconds: Int): String {
        var result = mutableListOf<Pair<Int, String>>()
        var currentUnitIndex = 0
        var currentSeconds = seconds
        
        while (currentUnitIndex < units.size && currentSeconds > 0) {
            val currentUnit = units[currentUnitIndex]
            val unitCount = currentSeconds / currentUnit.first
            
            if (unitCount > 0) {
                result.add(unitCount to currentUnit.second)
                currentSeconds %= currentUnit.first
            }
            
            currentUnitIndex++
        }
        
        return result.format()
    }
    
    private fun List<Pair<Int, String>>.format(): String {
        if (size == 0) return "now"
        if (size == 1) return get(0).format()
        
        var result = ""
        var currentUnitIndex = 0
        
        while (currentUnitIndex < size - 1) {
            result += "${get(currentUnitIndex).format()}"
            result += if (currentUnitIndex != size - 2) ", " else " "
                
            currentUnitIndex++
        }
        
        result += "and ${get(size - 1).format()}"
        
        return result
    }
    
    private fun Pair<Int, String>.format(): String {
        val ending = if (first == 1) "" else "s"
        return "$first $second$ending"
    }
    
}

__________________________________________________
object TimeFormatter {

    fun formatDuration(seconds: Int): String {
        val minuteUnit = 60
        val hourUnit = 3600
        val dayUnit = 86400
        val yearUnit = 31536000
        var result = ""

        if (seconds == 0) {
            return "now"
        }

        if (seconds >= yearUnit) {
            result += if (seconds/yearUnit > 1) ""+seconds/yearUnit+" years" else "1 year"
            if (seconds%yearUnit != 0) {
                val y = seconds%yearUnit
                if (y >= dayUnit) {
                    if (y%dayUnit != 0) {
                        result += if (y/dayUnit > 1) ", "+y/dayUnit+" days" else ", 1 day"
                        val d = y%dayUnit
                        if (d >= hourUnit) {
                            if (d%hourUnit != 0) {
                                result += if (d/hourUnit > 1) ", "+d/hourUnit+" hours" else ", 1 hour"
                                val h = d%hourUnit
                                if (h >= minuteUnit) {
                                    if (h%minuteUnit != 0) {
                                        result += if (h/minuteUnit > 1) ", "+h/minuteUnit+" minutes" else ", 1 minute"
                                        val m = h%minuteUnit
                                        result += if (m>1) " and $m seconds" else " and 1 second"
                                    } else {
                                        result += if (h/minuteUnit > 1) " and "+h/minuteUnit+" minutes" else " and 1 minute"
                                    }
                                } else {
                                    result += if (h>1) " and $h minutes" else " and 1 minute"
                                }
                            } else {
                                result += if (d/hourUnit > 1) " and "+d/hourUnit+" hours" else " and 1 hour"
                            }
                        } else {
                            if (d >= minuteUnit) {
                                if (d%minuteUnit != 0) {
                                    result += if (d/minuteUnit > 1) ", "+d/minuteUnit+" minutes" else ", 1 minute"
                                    val m = d%minuteUnit
                                    result += if (m>1) " and $m seconds" else " and 1 second"
                                } else {
                                    result += if (d/minuteUnit > 1) " and "+d/minuteUnit+" minutes" else " and 1 minute"
                                }
                            } else {
                                result += if (d>1) " and $d minutes" else " and 1 minute"
                            }
                        }
                    } else {
                        result += if (y/dayUnit > 1) " and "+y/dayUnit+" days" else " and 1 day"
                    }
                } else {
                    if (y >= hourUnit) {
                        if (y%hourUnit != 0) {
                            result += if (y/hourUnit > 1) ", "+y/hourUnit+" hours" else ", 1 hour"
                            val h = y%hourUnit
                            if (h >= minuteUnit) {
                                if (h%minuteUnit != 0) {
                                    result += if (h/minuteUnit > 1) ", "+h/minuteUnit+" minutes" else ", 1 minute"
                                    val m = h%minuteUnit
                                    result += if (m>1) " and $m seconds" else " and 1 second"
                                } else {
                                    result += if (h/minuteUnit > 1) " and "+h/minuteUnit+" minutes" else " and 1 minute"
                                }
                            } else {
                                result += if (h>1) " and $h minutes" else " and 1 minute"
                            }
                        } else {
                            result += if (y/hourUnit > 1) " and "+y/hourUnit+" hours" else " and 1 hour"
                        }
                    } else {
                        if (y >= minuteUnit) {
                            if (y%minuteUnit != 0) {
                                result += if (y/minuteUnit > 1) ", "+y/minuteUnit+" minutes" else ", 1 minute"
                                val m = y%minuteUnit
                                result += if (m>1) " and $m seconds" else " and 1 second"
                            } else {
                                result += if (y/minuteUnit > 1) " and "+y/minuteUnit+" minutes" else " and 1 minute"
                            }
                        } else {
                            result += if (y>1) " and $y minutes" else " and 1 minute"
                        }
                    }
                }
            }
        } else {
            if (seconds >= dayUnit) {
                if (seconds%dayUnit != 0) {
                    result += if (seconds/dayUnit > 1) ""+seconds/dayUnit+" days" else "1 day"
                    val d = seconds%dayUnit
                    if (d >= hourUnit) {
                        if (d%hourUnit != 0) {
                            result += if (d/hourUnit > 1) ", "+d/hourUnit+" hours" else ", 1 hour"
                            val h = d%hourUnit
                            if (h >= minuteUnit) {
                                if (h%minuteUnit != 0) {
                                    result += if (h/minuteUnit > 1) ", "+h/minuteUnit+" minutes" else ", 1 minute"
                                    val m = h%minuteUnit
                                    result += if (m>1) " and $m seconds" else " and 1 second"
                                } else {
                                    result += if (h/minuteUnit > 1) " and "+h/minuteUnit+" minutes" else " and 1 minute"
                                }
                            } else {
                                result += if (h>1) " and $h minutes" else " and 1 minute"
                            }
                        } else {
                            result += if (d/hourUnit > 1) " and "+d/hourUnit+" hours" else " and 1 hour"
                        }
                    } else {
                        if (d >= minuteUnit) {
                            if (d%minuteUnit != 0) {
                                result += if (d/minuteUnit > 1) ", "+d/minuteUnit+" minutes" else ", 1 minute"
                                val m = d%minuteUnit
                                result += if (m>1) " and $m seconds" else " and 1 second"
                            } else {
                                result += if (d/minuteUnit > 1) " and "+d/minuteUnit+" minutes" else " and 1 minute"
                            }
                        } else {
                            result += if (d>1) " and $d minutes" else " and 1 minute"
                        }
                    }
                } else {
                    result += if (seconds/dayUnit > 1) ""+seconds/dayUnit+" days" else "1 day"
                }
            } else {
                if (seconds >= hourUnit) {
                    if (seconds%hourUnit != 0) {
                        result += if (seconds/hourUnit > 1) ""+seconds/hourUnit+" hours" else "1 hour"
                        val h = seconds%hourUnit
                        if (h >= minuteUnit) {
                            if (h%minuteUnit != 0) {
                                result += if (h/minuteUnit > 1) ", "+h/minuteUnit+" minutes" else ", 1 minute"
                                val m = h%minuteUnit
                                result += if (m>1) " and $m seconds" else " and 1 second"
                            } else {
                                result += if (h/minuteUnit > 1) " and "+h/minuteUnit+" minutes" else " and 1 minute"
                            }
                        } else {
                            result += if (h>1) " and $h minutes" else " and 1 minute"
                        }
                    } else {
                        result += if (seconds/hourUnit > 1) ""+seconds/hourUnit+" hours" else "1 hour"
                    }
                } else {
                    if (seconds >= minuteUnit) {
                        if (seconds%minuteUnit != 0) {
                            result += if (seconds/minuteUnit > 1) ""+seconds/minuteUnit+" minutes" else "1 minute"
                            val m = seconds%minuteUnit
                            result += if (m>1) " and $m seconds" else " and 1 second"
                        } else {
                            result += if (seconds/minuteUnit > 1) ""+seconds/minuteUnit+" minutes" else "1 minute"
                        }
                    } else {
                        result += if (seconds>1) "$seconds seconds" else "1 second"
                    }
                }
            }
        }

        return result
    }
}
