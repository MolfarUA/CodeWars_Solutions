unit Kata;

interface

uses
  SysUtils, Math;
  
function Mix(s1, s2: String): String;

implementation

type
  TStringArray = array of String;
type
  TArray = array of Int64;

function Mix(s1, s2: String): String;
  procedure Sort(a: TStringArray);
    function Compare(const a, b: String): integer;
    var w1, w2: Int64;
    begin
      w1 := Length(a); w2 := Length(b);
      if (w1 = w2) then
        Result := CompareText(a, b)
      else
        Result := w2 - w1;
    end;
  var i, nr: Int64; tmp: String;
  begin
    i:=0; nr := Length(a);
    repeat
      if (Compare(a[i], a[i+1]) > 0) then
      begin
          tmp := a[i];
          a[i] := a[i+1];
          a[i+1] := tmp;
          i := -1;
      end;
      Inc(i);
    until i = nr -1;
  end;

  function ConcatArrayOfStringToString(A: TStringArray): String;
  var i: Int64; res: String;
  begin
    if (Length(A) = 0) then
      Exit('');
    res := '';
    for i := 0 to High(A) do
    begin
      res += A[i];
    end;
    Result := Copy(res, 1, Length(res) - 1);
  end;

var alpha1, alpha2: TArray; i, c, sm, cnt: Int64; r1: String; res: TStringArray;
begin
  SetLength(alpha1, 26);
  SetLength(alpha2, 26);
  for i := 0 to Length(s1) do
  begin
    c := Ord(s1[i]);
    if ((c >= 97) And (c <= 122)) then
        Inc(alpha1[c - 97]);
  end;
  for i := 0 to Length(s2) do
  begin
    c := Ord(s2[i]);
    if ((c >= 97) And (c <= 122)) then
        Inc(alpha2[c - 97]);
  end;
  r1 := '';
  cnt := 0;
  SetLength(res, 0);
  for i := 0 to 25 do
  begin
    sm := Max(alpha1[i], alpha2[i]);
    if (sm > 1) then
    begin
      Inc(cnt);
      if (sm > alpha1[i]) then
        r1 := '2:' + StringOfChar(Chr(i + 97), sm) + '/'
      else
        if (sm > alpha2[i]) then
          r1 := '1:' + StringOfChar(Chr(i + 97), sm) + '/'
        else r1 := '=:' + StringOfChar(Chr(i + 97), sm) + '/';
      SetLength(res, cnt);
      res[cnt - 1] := r1;
    end;
  end;
  if (Length(res) <> 0) then
    Sort(res);
  Result := ConcatArrayOfStringToString(res);
end;

end.
