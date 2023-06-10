
Unit logistic_time_linux;

Interface
Function GetUnixTimeMilliseconds: Int64;


Implementation

Uses 
Unix;

Function GetUnixTimeMilliseconds: Int64;

Var 
  tv: TTimeval;
Begin
  fpgettimeofday(@tv, Nil);
  GetUnixTimeMilliseconds := Int64(tv.tv_sec) * 1000 + Int64(tv.tv_usec) Div 1000;
End;

End.
