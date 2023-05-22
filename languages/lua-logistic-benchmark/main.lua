require "io"

-- Code create by Chat GPT
local osname = os.getenv("OS")
local clock
if osname and osname:match("^Windows") then
  -- Usando a função 'os.clock()' no Windows
  clock = os.clock
else
  -- Usando a biblioteca 'socket' no Linux
  socket = require("socket")
  clock = socket.gettime
end

function calculate(x0, r, iter)
  local x = {}

  local t0 = clock()
  x[0] = x0
  for i = 1, iter - 1 do
    x[i] = r * x[i - 1] * (1.0 - x[i - 1])
  end
  local delta_t = (clock() - t0) * 1000

  return x, delta_t
end

function simple_action(x0, r, iter, show_series)
  local series, delta_t = calculate(x0, r, iter)

  if show_series then
    print(string.rep("-", 40))
    for i = 0, iter - 1 do
      print(string.format("%.17f", series[i]))
    end
    print(string.rep("-", 40))
  end

  print("TIME: " .. delta_t .. " ms")
end

function repeat_action(x0, r, iter, repetitions)
  local times = {}

  local total_time = 0
  local t0 = clock()
  for i = 0, (repetitions - 1) do
    io.write(string.format("\r%5d / %5d", (i + 1), repetitions))
    values, times[i] = calculate(x0, r, iter)
    total_time = total_time + times[i]
  end
  local delta_t = (clock() - t0) * 1000
  print()

  local average = math.floor(total_time / repetitions)

  print("AVERAGE " .. average .. " ms")
  print("TOTAL_TIME " .. delta_t)
end

function main()
  local action = arg[1]
  local x0 = tonumber(arg[2])
  local r = tonumber(arg[3])
  local iter = math.floor(tonumber(arg[4]))

  if action == "s" then
    local show_series = (#arg > 4) and arg[5] == "s"
    simple_action(x0, r, iter, show_series)
  elseif action == "r" then
    local repetitions = math.floor(tonumber(arg[5]))
    repeat_action(x0, r, iter, repetitions)
  end
end

main()
