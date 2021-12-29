function mix($s1, $s2) {
    $alphabase="abcdefghijklmnopqrstuvwxyz"
    $result = @()
    for ($i = 0; $i -lt $alphabase.Length; $i++) {
        $c = $alphabase[$i]
        $nb_s1 = [Regex]::Replace($s1, "[^$c]+", "")
        $nb_s2 = [Regex]::Replace($s2, "[^$c]+", "")
        $lg_s1 = $nb_s1.Length
        $lg_s2 = $nb_s2.Length
        if (($lg_s1 -gt 1) -or ($lg_s2 -gt 1)) {
            if ($lg_s1 -eq $lg_s2) { 
                $result += @("E:" + $nb_s1)
            }
            if ($lg_s1 -gt $lg_s2) {
                $result += @("1:" + $nb_s1)
            }
            if ($lg_s1 -lt $lg_s2) { 
                $result += @("2:" + $nb_s2)
            }
        }
    }
    $res = $result | Sort-Object -Property {-$_.Length}, {$_}
    $res -join "/"
}

_____________________________________________________
function mix($s1, $s2) {
  $s1CharArr = $s1.ToCharArray() | Where-Object { $_ -cmatch '[a-z]' }
  $s2CharArr = $s2.ToCharArray() | Where-Object { $_ -cmatch '[a-z]' }
  $s1Group = $s1CharArr | Group-Object | Where-Object { $_.count -gt 1 }
  $s2Group = $s2CharArr | Group-Object | Where-Object { $_.count -gt 1 }
  
  $tempArr = New-Object System.Collections.ArrayList
  
  foreach ($item in $s1Group)
  {
    if ($s2Group.Name -contains $item.Name)
    {
      $s2Comparison = $s2Group | Where-Object { $_.Name -eq $item.Name }
      if ($s2Comparison.Count -gt $item.count)
      {
        $tempArr.Add("2:$($item.Name * $s2Comparison.Count)") | Out-Null
      }
      elseif ($s2Comparison.Count -lt $item.count)
      {
        $tempArr.Add("1:$($item.Name * $item.Count)") | Out-Null
      }
      elseif ($s2Comparison.Count -eq $item.count)
      {
        $tempArr.Add("E:$($item.Name * $item.Count)") | Out-Null
      }
    }
    else
    {
      $tempArr.Add("1:$($item.Name * $item.Count)") | Out-Null
    }
  }
  foreach ($item in $s2Group)
  {
    if ($s1Group.Name -notcontains $item.Name)
    {
      $tempArr.Add("2:$($item.Name * $item.Count)") | Out-Null
    }
  }
  
  $output = New-Object System.Collections.ArrayList
  $tempArr = $tempArr | Sort-Object -Property Length -Descending
  
  foreach ($group in ($tempArr | Group-Object -Property Length))
  {
    foreach ($item in ($group.Group | Sort-Object))
    {
      $output.Add($item) | Out-Null
    }
  }
  $output -join '/'
}

_____________________________________________________
function mix($s1, $s2) {
    $d1 = [regex]::Matches($s1, "[a-z]").value | group | where count -gt 1 | select name,count,@{ n = "label"; e = { 1 } } 
    $d2 = [regex]::Matches($s2, "[a-z]").value | group | where count -gt 1 | select name,count,@{ n = "label"; e = { 2 } } 
    
    $result = @($d1; $d2) | Sort-Object count -des | group name |
    select name,
           @{ n = "label"; e = { if($_.group[0].count -eq $_.group[1].count) { "E" } else { $_.group[0].label } } },
           @{ n = "count"; e = { $_.group[0].count } } |
    Sort-Object @{ e = "count"; d = 1 },label,name |
    foreach { "{0}:{1}" -f $_.label, ($_.name * $_.count) }
    
    $result -join "/"
}

_____________________________________________________
function mix($s1, $s2) {
    $g1 = $s1 -split "" | Group-Object -CaseSensitive | Where-Object {$_.Name -cin ('a'..'z') -and $_.Count -gt 1}
    $g2 = $s2 -split "" | Group-Object -CaseSensitive | Where-Object {$_.Name -cin ('a'..'z') -and $_.Count -gt 1}
    $out = @()
    $out += $g1 | Where-Object { $_.Count -eq ( ($g2 | Where-Object Name -eq $_.Name).Count )} | Foreach-Object { "E:$($_.Name*$_.Count)" }
    $out += $g1 | Where-Object { $_.Count -gt ( ($g2 | Where-Object Name -eq $_.Name).Count )} | Foreach-Object { "1:$($_.Name*$_.Count)" }
    $out += $g2 | Where-Object { $_.Count -gt ( ($g1 | Where-Object Name -eq $_.Name).Count )} | Foreach-Object { "2:$($_.Name*$_.Count)" }
    ($out | Sort-Object Length, @{ Expression = { $_ }; Descending = $false } -Descending) -join '/'
}
