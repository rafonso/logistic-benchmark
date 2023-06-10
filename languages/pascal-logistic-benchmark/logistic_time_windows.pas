
Unit logistic_time_windows;

Interface
Function GetUnixTimeMilliseconds:   Int64;


Implementation

Uses 
Windows;

Function GetUnixTimeMilliseconds:   Int64;

Var 
  st:   TSystemTime;
  t:   TFileTime;
Begin
  GetSystemTime(st);
  SystemTimeToFileTime(st, t);
  GetUnixTimeMilliseconds := Int64(t.dwLowDateTime) Or Int64(t.dwHighDateTime
                             shl 32);
  GetUnixTimeMilliseconds := GetUnixTimeMilliseconds Div 10000;
  // Convert to milliseconds
End;

End.
