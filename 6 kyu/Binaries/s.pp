unit Kata;

interface

function Code(s: String): String;
function Decode(str: String): String;

implementation

uses SysUtils, StrUtils;
  
function Code(s: String): String;
var m: TStringArray; i, u: Int64; v: String;
begin
    m := ['10','11','0110','0111','001100','001101','001110','001111','00011000','00011001'];
    Result := '';
    For i := 1 To Length(s) do begin
      u := StrToInt(s[i]);
      v := m[u];
      Result += v;
    end;
end;

function Decode(str: String): String;
var i, lg, n, zero_i, ll: Int64; ErrorCode: Integer; ss: String;
begin
    Result := ''; i := 1; lg := Length(str);
    while (i < lg) do begin
      zero_i := i;
      while ((zero_i <= lg) And (str[zero_i] <> '1')) do begin
        Inc(zero_i);
      end;
      ll := zero_i - i + 1;
      ss := str.Substring(zero_i, ll);
      val('%' + ss, n, ErrorCode);
      Result += IntToStr(n);
      i := zero_i + ll + 1;
    end;
end;

end.
