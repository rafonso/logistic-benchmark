// To Compile: fpc -o"pascal-logistic-benchmark.exe" .\pascal-logistic-benchmark.pas
(*
# Pascal
WORKDIR /app/languages/pascal-logistic-benchmark
RUN sed -Ei "s/logistic_time_windows/logistic_time_linux/" pascal-logistic-benchmark.pas
RUN fpc -o"pascal-logistic-benchmark" pascal-logistic-benchmark.pas
RUN sed -Ei "s/(pascal-logistic-benchmark)\.exe/\1/" pascal.config.json
WORKDIR /app
*)

Uses logistic_time_windows,
SysUtils, Math;

Type 
  DoubleArray = array Of Double;

  Tuple = Record
    x: DoubleArray;
    time: Int64;
  End;

Function Calculate(x0, r: Double; size: Integer): Tuple;

Var 
  x: DoubleArray;
  i: Integer;
  t0, time: Int64;
Begin
  SetLength(x, size);

  t0 := GetUnixTimeMilliseconds;
  x[0] := x0;
  For i := 1 To size - 1 Do
    Begin
      x[i] := r * x[i - 1] * (1.0 - x[i - 1]);
    End;
  time := GetUnixTimeMilliseconds - t0;

  Calculate.x := x;
  Calculate.time := time;
End;

Function Sum(Const Values: Array Of Int64): Int64;

Var 
  i: Integer;
Begin
  Sum := 0;
  For i := Low(Values) To High(Values) Do
    Begin
      Sum := Sum + Values[i];
    End;
End;

Procedure SimpleAction(x0, r: Double; size: Integer; showSeries: Boolean);

Var 
  resultTuple: Tuple;
  x: DoubleArray;
  i: Integer;
Begin
  resultTuple := Calculate(x0, r, size);
  x := resultTuple.x;

  If showSeries Then
    Begin
      Writeln(StringOfChar('-', 40));
      For i := 0 To Length(x) - 1 Do
        Begin
          Writeln(FloatToStr(x[i]));
        End;
      Writeln(StringOfChar('-', 40));
    End;

  Writeln('TIME: ', resultTuple.time, ' ms');
End;

Procedure RepeatAction(x0, r: Double; size, repetitions: Integer);

Var 
  sumTimes: Int64;
  i: Integer;
  resultTuple: Tuple;
  t0, time: Int64;
Begin
  sumTimes := 0;

  t0 := GetUnixTimeMilliseconds;
  For i := 0 To repetitions - 1 Do
    Begin
      Write(#13, SysUtils.Format('%4d/%4d', [i + 1, repetitions]));
      resultTuple := Calculate(x0, r, size);
      sumTimes := sumTimes + resultTuple.time;
    End;
  time := GetUnixTimeMilliseconds - t0;
  Writeln;


  Writeln('AVERAGE ', (sumTimes.ToDouble / repetitions));
  Writeln('TOTAL_TIME ', time);
End;

Var 
  action: string;
  x0, r: Double;
  it, repetitions: Integer;
  showSeries: Boolean;
Begin
  DefaultFormatSettings.DecimalSeparator := '.';

  action := ParamStr(1);
  x0 := StrToFloat(ParamStr(2));
  r := StrToFloat(ParamStr(3));
  it := StrToInt(ParamStr(4));

  If CompareText('s', action) = 0 Then
    Begin
      showSeries := (ParamCount > 4) And (CompareText('s', ParamStr(5)) = 0);
      SimpleAction(x0, r, it, showSeries);
    End
  Else If CompareText('r', action) = 0 Then
         Begin
           repetitions := StrToInt(ParamStr(5));
           RepeatAction(x0, r, it, repetitions);
         End;
End.
