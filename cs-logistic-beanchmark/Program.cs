
using System.Globalization;

Tuple<double[], long> calculate(double x0, double r, int size)
{
    double[] x = new double[size];

    long t0 = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
    x[0] = x0;
    for (int i = 1; i < size; i++)
    {
        x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
    }
    long time = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - t0;

    return Tuple.Create(x, time);
}

void simpleAction(double x0, double r, int size, bool showSeries)
{
    var result = calculate(x0, r, size);

    if (showSeries)
    {
        foreach (var x in result.Item1)
        {
            Console.WriteLine(x);
        }
    }

    Console.WriteLine(new string('-', 20));
    Console.WriteLine("TIME {0} ms", result.Item2);
}


void repeatAction(double x0, double r, int size, int repetitions)
{
    long[] times = new long[repetitions];

    long t0 = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
    for (int i = 0; i < repetitions; i++)
    {
        Console.Write("\r{0,4}/{1,4}", (i + 1), repetitions);
        times[i] = calculate(x0, r, size).Item2;
    }
    long time = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - t0;
    Console.WriteLine();

    Console.WriteLine("AVERAGE {0}", times.Average());
    Console.WriteLine("TOTAL_TIME {0}", time);

}

#region main

string action = args[0];
double x0 = Convert.ToDouble(args[1], CultureInfo.InvariantCulture);
double r = Convert.ToDouble(args[2], CultureInfo.InvariantCulture);
int it = Convert.ToInt32(args[3], CultureInfo.InvariantCulture);

if ("s".Equals(action))
{
    bool showSeries = args.Length > 4 && args[4].Equals("s");
    simpleAction(x0, r, it, showSeries);
}
else if ("r".Equals(action))
{
    int repetitions = Convert.ToInt32(args[4], CultureInfo.InvariantCulture);
    repeatAction(x0, r, it, repetitions);
}

#endregion