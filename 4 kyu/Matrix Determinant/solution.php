function minor(array $matrix, int $x): array
{
    array_shift($matrix);
    foreach ($matrix as $key => $row) {
        $matrix[$key] = array_merge(
            array_slice($row, 0, $x),
            array_slice($row, $x + 1)
        );
    }
    return $matrix;
}

function determinant(array $matrix): int
{
    $size = count($matrix);
    if ($size === 1) {
        return $matrix[0][0];
    }
    
    $result = 0;
    for ($i = 0, $k = 1; $i < $size; $i++, $k = -$k) {
        $result += $k * $matrix[0][$i] * determinant(minor($matrix, $i));
    }
    return $result;
}
_____________________________________________
function determinant(array $matrix): int {
  if (count($matrix) == 1) return $matrix[0][0];
  $d = 0;
  for ($i = 0; $i < count($matrix); $i++) {
    $nm = [];
    for ($j = 1; $j < count($matrix); $j++) {
      $temp = $matrix[$j];
      array_splice($temp, $i, 1);
      array_push($nm, $temp);
    }
    $d += pow(-1, $i) * ($matrix[0][$i]) * determinant($nm);
  }
  return $d;
}
_____________________________________________
//Вычисление det(2x2)
function det(array $matrix): int{ 
  $tmp1=$matrix[0][0]*$matrix[1][1];
  $tmp2=$matrix[0][1]*$matrix[1][0];
  return $tmp1-$tmp2; 
}
//Разложение матрицы до уровня det(2x2)
function decomp_matrix(array $matrix){
  $sum=0;
  $n=count($matrix);    
  for($k=0;$k<$n;$k++){       
          $coef=$matrix[0][$k]; // Коэффициенты
          $mat_tmp=$matrix;            
          for($l=0;$l<$n;$l++){
            unset($mat_tmp[$l][$k]);
            }
          unset($mat_tmp[0]);
          $n_tmp=count($mat_tmp);
          array_splice($mat_tmp,1,0);
          for($t=0;$t<$n_tmp;$t++){
            array_splice($mat_tmp[$t],1,0);
          }          
      // Вычисляем сумму
       if ($n>3){
          $sum_tmp= $coef*decomp_matrix($mat_tmp);  
       }else{
         $sum_tmp=$coef*(det($mat_tmp));    
       }
      //
      if (($k % 2)==0){
        $sum+=$sum_tmp;
      }else {
        $sum-=$sum_tmp;
      }
  } 
  return $sum;
}

function determinant(array $matrix): int {
  $n=count($matrix);
  $sum=0;
  echo "Размер матрицы:".$n."<br>";
  var_export($matrix);
 
 switch ($n){
    case 0:
        $sum=0;
        break;
    case 1:
        $sum=$matrix[0][0];
        break;
    case 2:
        $sum = det($matrix);      
        break;
    default:
        $sum = decomp_matrix($matrix);
        break;
    }  
  return $sum;
}
