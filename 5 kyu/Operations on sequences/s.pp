unit Kata;
interface

type
  TArr = array of Int64;
type
  T2Arr = array[0..1] of Int64;  
function Solve(arr: TArr): T2Arr; 

implementation
  
function Solve(arr: TArr): T2Arr;
var a, b, x, y, z, t: Int64; i: Integer;
begin
  a := arr[0];
  b := arr[1];
  i := 1;
  while (i < Length(arr) Div 2) do
  begin
    x := a; y := b; z := arr[2 * i]; t := arr[2 * i + 1];
    a := Abs(x * z - y * t);
    b := Abs(x * t + y * z);
    Inc(i);
  end;
  Result[0] := a;
  Result[1] := b;
end;

end.
