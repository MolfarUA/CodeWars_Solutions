function choose-best-sum($t, $k, $ls)
{
    function chooseBestSumAux($t, $k , $ls, $from) {
        if ($k -eq 0) {
            if ($t -ge 0) {
                return 0
            } else { 
                
                return $t
            }
        } else {
            if ($t -lt $k) {return -1}
        }
        $best = -1
        $tmpBest = -1
        $i = $from
        while ($i -lt $ls.Length) {
            $tmpBest = chooseBestSumAux ($t - $ls[$i]) ($k - 1) $ls ($i + 1)
            if ($tmpBest -ge 0) {
                $best = [math]::max($best, $ls[$i] + $tmpBest)
            }
            $i++
        }
        $best
    }
    chooseBestSumAux $t $k $ls 0
}
_______________________________________
function choose-best-sum($t, $k, $ls) {    
    if ($k -le 0 -or $ls.Length -eq 0 -or $ls.Length -lt $k) { return -1 }      
    $totals = Calculate-Combinations ($ls | Where-Object { $_ -le $t }) $k $t
    $result = ($totals | Measure-Object -Maximum).Maximum
    if ([string]::IsNullOrEmpty($result)) { return -1 }
    return $result
}

function Calculate-Combinations ($array, [int]$length, $maxTotal) {    
    $result = { }.Invoke()
    $combinations = { }.Invoke()
    Generate-Combinations $array.Length $length 0 $combinations
    
    foreach ($combination in $combinations) { 
        $sum = 0
        for ($bitPosition = 0; $bitPosition -lt $array.Length; $bitPosition++) {             
            if (($combination -bAND (1 -shl ($array.Length - $bitPosition - 1))) -ne 0) {               
                $sum += $array[$bitPosition]                            
            }
        }        
        if ($sum -le $maxTotal) {
            $result.Add($sum)
        }             
    }    
    
    $result 
}

function Generate-Combinations($index, $bits, $number, $list) {
    if ($index -eq 0) {
        if ($bits -eq 0) {            
            $list.Add($number)
        }
    }
    if (($index - 1) -ge $bits) {
        Generate-Combinations ($index - 1) $bits $number $list
    }
    if ($bits -gt 0) {
        $shiftValue = 1 -shl ($index - 1)
        $value = $number -bor $shiftValue
        Generate-Combinations ($index - 1) ($bits - 1) $value $list
    }
}
_______________________________________
function choose-best-sum($t, $k, $ls)
{
if($k -lt 1 -or $k -gt $ls.count){
    "-1"
}
elseif($k -eq $ls.count){
    $sum = ($ls | measure-object -sum).sum
    if($sum -le $t){
        $sum
    }
    else{
        "-1"
    }
  }
elseif($k -eq 1){
    $sum = -1
    $ls | foreach-object {
        $partsum = $_
        if($partsum -le $t){
            if($partsum -gt $sum){
                $sum = $partsum
            }
        }
    }
    $sum
}
if($k -gt 1){
    $start = 0 
    $ls = $ls | Sort-Object -Descending
    $runs = [math]::Floor($ls.Count / 2 ) + 1 
    $partSumRuns = $k - 2
    $sum = -1 
    0..$runs | ForEach-Object {
        if($partSumRuns -eq 0){
            $partsum = $ls[$start]
        }
        else{
            $start..($partSumRuns + $start) | foreach{
                $partsum = 0 
                $start..$partsumruns | foreach {
                $partsum += $ls[$_]
                }
            }   
        }
        if($partSum -ge $t){
            $start++
            $partsum = 0
        }
        else{
            ($partSumRuns + 1)..($ls.Count -1) | foreach { 
               if($partsum + $ls[$_] -eq $t){
                    $t
                    break
               }
               else{
               #$partsum + $ls[$_]
                    if($partsum + $ls[$_] -lt $t){
                        if($partsum + $ls[$_] -gt $sum){
                            $sum = $partsum + $ls[$_]                             
                        }
                    }
               }
            }
        }
        $start++
    }
    $sum 
}
}
_______________________________________
function choose-best-sum($t, $k, $ls)
{
    function chooseBestSumAux($t, $k , $ls, $from) {
        if ($k -eq 0) {
            if ($t -ge 0) {
                return 0
            } else { 
                
                return $t
            }
        } else {
            if ($t -lt $k) {return -1}
        }
        $best = -1
        $tmpBest = -1
        $i = $from
        while ($i -lt $ls.Length) {
            $tmpBest = chooseBestSumAux ($t - $ls[$i]) ($k - 1) $ls ($i + 1)
            if ($tmpBest -ge 0) {
                $best = [math]::max($best, $ls[$i] + $tmpBest)
            }
            $i++
        }
        $best
    }
    chooseBestSumAux $t $k $ls 0
}
