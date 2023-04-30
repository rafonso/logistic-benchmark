
def calculate (x0, r, it)
  series = Array.new(it)
  
  t0 = Process.clock_gettime(Process::CLOCK_MONOTONIC, :millisecond)
  series[0] = x0 
  for i in (1..it) do 
    series[i] = r * series[i - 1] * (1.0 - series[i - 1])
  end
  deltaT = (Process.clock_gettime(Process::CLOCK_MONOTONIC, :millisecond) - t0)

  return series, deltaT
end

def simple_action(x0, r, it, show_output)
  series, deltaT = calculate(x0, r, it)

  if(show_output) 
      puts("-" * 40)
      for x in series do
        puts(x)        
      end
      puts("-" * 40)
  end
  
  puts("TIME: #{deltaT} ms")
end

def repeat_action(x0, r, it, repetitions)
  times = Array.new(repetitions)

  t0 = Process.clock_gettime(Process::CLOCK_MONOTONIC, :millisecond)
  for i in (0..repetitions - 1) do 
    printf("\r%4d / %4d", (i +1), repetitions)
    _, times[i] = calculate(x0, r, it)
  end
  deltaT = (Process.clock_gettime(Process::CLOCK_MONOTONIC, :millisecond) - t0)
  puts

  average = times.sum(0) / times.size

  puts "AVERAGE #{average} ms"
  puts "TOTAL_TIME #{deltaT}"
end

# MAIN

action = ARGV[0]
x0 = ARGV[1].to_f
r = ARGV[2].to_f
it = ARGV[3].to_i

if action == 's'
  show_output = (ARGV.length > 4) and (ARGV[4] == 's')
  simple_action(x0, r, it, show_output)
elsif  action == 'r'
  repetitions = ARGV[4].to_i
  repeat_action(x0, r, it, repetitions)
end
