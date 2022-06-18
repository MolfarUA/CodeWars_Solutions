56d0a591c6c8b466ca00118b


unit Kata;

interface

function IsTriangular (t: Integer): Boolean;

implementation

function IsTriangular (t: Integer): Boolean;
var
  m : Integer;
begin
  m := Trunc(Sqrt(t * 2));
  Result := m * (m + 1) = t * 2;
end;

end.
__________________________
unit Kata;

interface

function IsTriangular (t: Integer): Boolean;

implementation

function IsTriangular (t: Integer): Boolean;
var d, x: real;
begin
  d := 1 + 8 * t;
  x := (-1 + sqrt(d))/2;
  Result := trunc(x) = x;
end;

end.
__________________________
unit Kata;

interface

function IsTriangular (t: Integer): Boolean;

implementation

function IsTriangular (t: Integer): Boolean;
 var a,d :real;
 begin
  d:=1-4*-2*t;
  a:=(-1+sqrt(d))/2;
  If a = trunc(a) then
  Result := true
  else Result:=false;
end;

end.
__________________________
unit Kata;

interface

function IsTriangular (t: Integer): Boolean;

implementation

function IsTriangular (t: Integer): Boolean;
begin
  Result := Frac((sqrt((8*t)+1)-1)/2)=0;
end;

end.
__________________________
unit Kata;

interface

function IsTriangular (t: Integer): Boolean;

implementation

function IsTriangular (t: Integer): Boolean;

var 
  n : Integer;

begin
  n := 1;
  while (n*(n+1)/2<t) do
  begin
    n := n + 1;
  end;
  Result := n*(n+1)/2 = t;
end;

end.
__________________________
unit Kata;

interface

function IsTriangular (t: Integer): Boolean;

implementation

uses math;

function IsTriangular (t: Integer): Boolean;
begin
  IsTriangular := Sqrt(8 * T + 1) mod 1 = 0;
end;

end.
